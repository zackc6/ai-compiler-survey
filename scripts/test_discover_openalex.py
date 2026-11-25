"""Network-free tests for the OpenAlex budget handling in scripts/discover.py.

Background (Review thread, 24 November 2026): run r30 logged 172 OpenAlex 429s, and both
`cites` and `refs` returned nothing. Keyless OpenAlex clients get about $0.10 a day (derived; budget unit undocumented).
A search costs $0.001 and a list request $0.0001, and the venue listings had spent the budget
on ~136 `title.search` OR-groups. These tests check the mechanics agreed with ChatGPT (11:40 UTC)
and the Action (11:44 UTC):
  1. a `daily_budget` 429 trips a breaker, and every later OpenAlex call is skipped and counted
     against the channel that was running;
  2. a per-second 429 honours Retry-After and then succeeds;
  3. venue listings page with plain list requests (no `title.search`) and filter titles locally;
  4. an API key is sent when configured and is never written to the log;
  5. digest titles that start with a UTF-8 BOM are cleaned.
ChatGPT's 12:36 review added: 6. a venue page that fails after page one keeps page one's rows
and marks the listing incomplete (DEGRADED); 7. refs falls back to a title search only on a DOI
miss, not on a DOI hit with an empty reference list, and audits both; 8. referenced works below
the resolution cap are reported; 9. the announcement reads the saved ledger from a main checkout
and refuses to publish a test notice without it.
A fixture test validates mechanics only. It does not replace a live discovery run.
"""
import io
import json
import unittest
import urllib.error
from unittest import mock

from scripts import discover as d


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http429(reason, retry_after=None):
    hdrs = {"Retry-After": str(retry_after)} if retry_after is not None else {}
    return urllib.error.HTTPError("https://api.openalex.org/x", 429, "Too Many", hdrs,
                                  io.BytesIO(json.dumps({"reason": reason}).encode()))


def reset():
    d.OA.update({"lists": 0, "searches": 0, "skipped": 0, "breaker": "", "per_second_429": 0, "capped": False,
                 "channel": "", "skipped_in": {}, "sleep_429": 0.0})
    d.DIAG.clear()


class OpenAlexBudget(unittest.TestCase):
    def setUp(self):
        reset()
        self.sleep = mock.patch.object(d.time, "sleep", lambda s: None)
        self.sleep.start()

    def tearDown(self):
        self.sleep.stop()

    def test_daily_budget_trips_breaker_and_skips_later_calls(self):
        calls = []

        def urlopen(req, timeout=0):
            calls.append(req.full_url)
            raise http429("daily_budget")

        d.OA["channel"] = "refs"
        with mock.patch.object(d.urllib.request, "urlopen", urlopen):
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:x"))
            d.OA["channel"] = "cites"
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=cites:W1"))
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=cites:W2"))
        self.assertEqual(len(calls), 1, "no retry after daily_budget, and nothing sent after the breaker")
        self.assertIn("daily_budget in refs", d.OA["breaker"])
        self.assertEqual(d.OA["skipped_in"], {"refs": 1, "cites": 2})

    def test_per_second_429_honours_retry_after(self):
        waits, seq = [], [http429("requests_per_second", 1), Resp(b'{"results": []}')]

        def urlopen(req, timeout=0):
            r = seq.pop(0)
            if isinstance(r, Exception):
                raise r
            return r

        with mock.patch.object(d.urllib.request, "urlopen", urlopen), \
                mock.patch.object(d.time, "sleep", waits.append):
            self.assertEqual(d.get("https://api.openalex.org/works?filter=doi:x"), b'{"results": []}')
        self.assertEqual(waits, [1.0])
        self.assertEqual(d.OA["per_second_429"], 1)
        self.assertEqual(d.OA["lists"], 1)
        self.assertFalse(d.OA["breaker"])

    def test_long_retry_after_without_reason_trips_breaker(self):
        # Run 45437945681 (69cc338): keyless daily-budget 429s with no parseable reason and
        # Retry-After ~26,900 s retried 3 x 30 s per call until the job's 2 h timeout.
        calls = []

        def urlopen(req, timeout=0):
            calls.append(req.full_url)
            raise urllib.error.HTTPError("https://api.openalex.org/x", 429, "Too Many",
                                         {"Retry-After": "26905"}, io.BytesIO(b"Too Many Requests"))

        d.OA["channel"] = "cites"
        with mock.patch.object(d.urllib.request, "urlopen", urlopen):
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:x"))
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:y"))
        self.assertEqual(len(calls), 1, "no retry on a long Retry-After, nothing sent after the breaker")
        self.assertIn("daily budget inferred (Retry-After 26905s", d.OA["breaker"])
        self.assertEqual(d.OA["per_second_429"], 0)

    def test_429_reason_and_body_never_echo_server_text(self):
        # ChatGPT 18:58: the key is masked in the URL, but a 429 that echoes it in `reason` or the
        # body must not reach stderr, the breaker line or the ledger's fetch log.
        key = "SENTINELKEY123"
        cases = [  # (reason, body message, Retry-After): long-wait breaker; per-second 429 then sleep-cap breaker
            (f"leak-{key}", f"Insufficient budget. This request has no API key {key} mailto", 26905),
            (key, f"echo api_key={key}", 30),
        ]
        for reason, extra, ra in cases:
            reset()
            d.OA["channel"] = "refs"
            body = json.dumps({"reason": reason, "message": extra}).encode()

            def urlopen(req, timeout=0, body=body, ra=ra):
                raise urllib.error.HTTPError(req.full_url, 429, "Too Many", {"Retry-After": str(ra)},
                                             io.BytesIO(body))

            err = io.StringIO()
            with mock.patch.object(d, "OPENALEX_KEY", key), mock.patch.object(d, "OA_429_SLEEP_CAP", 60.0), \
                    mock.patch.object(d.urllib.request, "urlopen", urlopen), mock.patch.object(d.sys, "stderr", err):
                self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:x"))
                ledger = "\n".join(d.render_fetch_log(True))
            self.assertTrue(d.OA["breaker"])
            for text in (err.getvalue(), ledger, d.OA["breaker"], "\n".join(d.DIAG)):
                self.assertNotIn(key, text)
            self.assertIn("api_key=***", err.getvalue())
            self.assertIn("retry-after=", d.DIAG[-1])
            if ra > d.OA_LONG_WAIT:
                self.assertIn("reason other", d.OA["breaker"])
                self.assertIn("429 body markers: insufficient-budget,keyless,mailto-mentioned", d.DIAG[-1])
            else:
                self.assertIn("persistent 429s", d.OA["breaker"])
                self.assertIn("HTTP 429 reason=other", err.getvalue())
                self.assertIn("429 body markers: none", d.DIAG[-1])

    def test_persistent_short_429s_trip_breaker_after_sleep_cap(self):
        def urlopen(req, timeout=0):
            raise http429("", 30)

        slept = []
        with mock.patch.object(d.urllib.request, "urlopen", urlopen), \
                mock.patch.object(d.time, "sleep", slept.append):
            for i in range(40):
                d.get(f"https://api.openalex.org/works?filter=doi:{i}")
        self.assertIn("persistent 429s", d.OA["breaker"])
        self.assertLessEqual(sum(slept), d.OA_429_SLEEP_CAP)

    def test_sleep_cap_check_includes_attempt_increment(self):
        # ChatGPT/Codex 18:33: with 870 s already spent, a 30 s header on attempt 1 passed the
        # check (870 + 30 = 900) but slept 31 s, so total waiting reached 901 s > cap.
        seq = [http429("", 0), http429("", 30)]

        def urlopen(req, timeout=0):
            raise seq.pop(0)

        slept = []
        d.OA["sleep_429"] = d.OA_429_SLEEP_CAP - 30
        with mock.patch.object(d.urllib.request, "urlopen", urlopen), \
                mock.patch.object(d.time, "sleep", slept.append):
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:x"))
        self.assertEqual(slept, [0.0], "attempt 0 waits 0 s; attempt 1 (30 + 1 s) would pass the cap")
        self.assertIn("persistent 429s", d.OA["breaker"])
        self.assertLessEqual(d.OA["sleep_429"], d.OA_429_SLEEP_CAP)

    def test_malformed_retry_after_never_reaches_sleep(self):
        for header in ("-5", "nan", "inf", "-inf", "soon", " ", "Wed, 99 Foo 2026 00:00:00 GMT"):
            with self.subTest(header=header):
                reset()
                seq = [http429("", header), Resp(b"{}")]

                def urlopen(req, timeout=0):
                    r = seq.pop(0)
                    if isinstance(r, Exception):
                        raise r
                    return r

                slept = []
                with mock.patch.object(d.urllib.request, "urlopen", urlopen), \
                        mock.patch.object(d.time, "sleep", slept.append):
                    self.assertEqual(d.get("https://api.openalex.org/works?filter=doi:x"), b"{}")
                self.assertEqual(slept, [1.0])
                self.assertFalse(d.OA["breaker"])

    def test_retry_after_http_date(self):
        now = d.dt.datetime(2026, 11, 24, 18, 0, 0, tzinfo=d.dt.timezone.utc)
        self.assertEqual(d._retry_after("Tue, 24 Nov 2026 18:00:20 GMT", now), 20.0)
        self.assertEqual(d._retry_after("Tue, 24 Nov 2026 17:59:00 GMT", now), 0.0, "past date → no wait")
        self.assertEqual(d._retry_after("Wed, 25 Nov 2026 00:00:00 GMT", now), 21600.0)
        self.assertEqual(d._retry_after("26905", now), 26905.0)
        self.assertEqual(d._retry_after("0", now), 0.0)
        self.assertEqual(d._retry_after(None, now), 1.0)

    def test_http_date_until_midnight_trips_breaker(self):
        # A daily-budget 429 that gives Retry-After as an HTTP-date (midnight UTC) is a long wait too.
        calls = []
        midnight = (d.dt.datetime.now(d.dt.timezone.utc) + d.dt.timedelta(hours=2)).strftime(
            "%a, %d %b %Y %H:%M:%S GMT")

        def urlopen(req, timeout=0):
            calls.append(req.full_url)
            raise http429("", midnight)

        with mock.patch.object(d.urllib.request, "urlopen", urlopen):
            self.assertIsNone(d.get("https://api.openalex.org/works?filter=doi:x"))
        self.assertEqual(len(calls), 1)
        self.assertIn("daily budget inferred", d.OA["breaker"])

    def test_venue_listing_pages_without_search_and_filters_locally(self):
        works = [{"title": f"Paper {i}", "doi": "", "publication_date": "2026-05-01"} for i in range(399)]
        works[250]["title"] = "AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization"
        urls = []

        def fake_get(url, timeout=0, retries=0):
            urls.append(url)
            page = int(url.split("&page=")[1].split("&")[0])
            n = d.OA_PAGE_SIZE
            chunk = works[(page - 1) * n: page * n]
            return json.dumps({"meta": {"count": len(works)}, "results": chunk}).encode()

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            kept = d._openalex_venue("MLSys", "Machine Learning and Systems", 2026)
        self.assertEqual(len(urls), 4)  # 100/100/100/99 at the supported page size
        self.assertTrue(all("per-page=100&" in u for u in urls), "per-page=200 is deprecated (ChatGPT 19:24)")
        self.assertTrue(all("search" not in u for u in urls), "venue listing must not spend searches")
        self.assertEqual([w["title"][:8] for w in kept], ["AccelOpt"])
        self.assertTrue(any("399 works listed of 399, 1 title-matched" in m for m in d.DIAG))

    def test_api_key_sent_but_never_logged(self):
        seen = []

        def urlopen(req, timeout=0):
            seen.append(req.full_url)
            raise urllib.error.HTTPError(req.full_url, 500, "x", {}, io.BytesIO(b""))

        with mock.patch.object(d, "OPENALEX_KEY", "sekrit"), \
                mock.patch.object(d.urllib.request, "urlopen", urlopen):
            d.get("https://api.openalex.org/works?filter=doi:x", retries=0)
        self.assertIn("api_key=sekrit", seen[0])
        self.assertFalse(any("sekrit" in m for m in d.DIAG))
        self.assertTrue(any("api_key=***" in m for m in d.DIAG))

    def test_venue_page_two_failure_is_degraded_but_keeps_page_one(self):
        # ChatGPT 12:36: page one returns matches, page two fails -> rows kept, listing marked incomplete.
        page1 = [{"title": f"Paper {i}", "doi": ""} for i in range(d.OA_PAGE_SIZE)]
        page1[3]["title"] = "AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization"

        def fake_get(url, timeout=0, retries=0):
            if "&page=1&" in url:
                return json.dumps({"meta": {"count": 450}, "results": page1}).encode()
            return None

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            kept = d._openalex_venue("ICLR", "International Conference on Learning Representations", 2026)
        self.assertEqual([w["title"][:8] for w in kept], ["AccelOpt"])
        self.assertEqual(d.VENUE_INCOMPLETE, ["ICLR 2026 page 2 failed after 100 of 450 works"])

    def _refs(self, responses):
        """Run references_candidates against two fake DOI digests with scripted OpenAlex answers."""
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        for stem, doi, title in (("hit-empty", "10.1/a", "Empty Reference List Paper Title"),
                                 ("miss", "10.1/b", "Paper Missing From OpenAlex By DOI")):
            (tmp / f"{stem}.md").write_text(f"# {title}\n\n| **Type** | paper |\n| **DOI** | {doi} |\n",
                                            encoding="utf-8")
        urls = []

        def fake_get(url, timeout=0, retries=0):
            urls.append(url)
            if callable(responses):
                return responses(url)
            for k, v in responses.items():
                if k in url:
                    return json.dumps({"results": v}).encode()
            return json.dumps({"results": []}).encode()

        d.REFS_AUDIT.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get), \
                mock.patch.object(d, "_digest_keys",
                                  lambda t: (("10.1/a" if "Empty" in t else "10.1/b"), d._digest_title(t))):
            d.references_candidates({}, min_digests=2)
        return urls

    def test_refs_doi_hit_with_empty_list_does_not_fall_back(self):
        urls = self._refs({"filter=doi:": [{"id": "W1", "doi": "https://doi.org/10.1/a", "referenced_works": []}],
                           "title.search": [{"id": "W2", "title": "Paper Missing From OpenAlex By DOI",
                                             "referenced_works": ["https://openalex.org/W9"]}]})
        searches = [u for u in urls if "title.search" in u]
        self.assertEqual(len(searches), 1, "only the DOI miss is searched by title")
        self.assertIn("Missing", d.urllib.parse.unquote(searches[0]))
        self.assertEqual({k: d.REFS_AUDIT[k] for k in ("doi_seeds", "doi_hit", "doi_hit_refs", "doi_miss", "title_hit")},
                         {"doi_seeds": 2, "doi_hit": 1, "doi_hit_refs": 0, "doi_miss": 1, "title_hit": 1})
        self.assertTrue(any("1 matched (0 with a reference list, 1 empty), 1 missed" in m for m in d.DIAG))

    def test_refs_precut_is_reported(self):
        refs = [f"https://openalex.org/W{i}" for i in range(12)]
        with mock.patch.object(d, "REFS_RESOLVE_CAP", 10):
            self._refs({"filter=doi:": [{"id": "W1", "doi": "https://doi.org/10.1/a", "referenced_works": refs}]})
        self.assertEqual(d.REFS_AUDIT["precut"], 2)
        self.assertTrue(any("refs truncated: 2 referenced works" in m for m in d.DIAG))

    def test_announce_reads_saved_ledger_from_main_checkout(self):
        import pathlib
        import subprocess
        import sys
        import tempfile
        helper = pathlib.Path(__file__).with_name("announce_discovery.py").resolve()
        work, keep = pathlib.Path(tempfile.mkdtemp()), pathlib.Path(tempfile.mkdtemp())
        (work / "STATUS.md").write_text("# S\n\n## Review thread\n\nold\n", encoding="utf-8")
        (keep / "ledger.md").write_text("# L\n\n**Status: DEGRADED** — venue: 1 incomplete.\n\n"
                                        "Known-positive regression (x): AccelOpt: recovered by venue.\n", encoding="utf-8")
        env = dict(__import__("os").environ, LEDGER_FILE=str(keep / "ledger.md"))
        args = [sys.executable, "-I", str(helper), "reference/discovery/2026-11-24.md", "5", "0",
                "claude/discovery-2026-11-24-test-9", "2026-11-24", "claude/discovery-fix-2026-11-24@abc"]
        subprocess.run(args, cwd=work, env=env, check=True)
        s = (work / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("LIVE TEST of claude/discovery-fix-2026-11-24@abc", s)
        self.assertIn("**Status: DEGRADED**", s)
        self.assertIn("Known-positive regression", s)
        env["LEDGER_FILE"] = str(keep / "absent.md")
        self.assertNotEqual(subprocess.run(args, cwd=work, env=env).returncode, 0,
                            "a test notice without its ledger must fail, not publish unlabelled")

    def test_announce_reads_ledger_from_discovery_branch_without_workflow_help(self):
        # The current workflow checks out main (ledger absent) and passes no LEDGER_FILE.
        import os
        import pathlib
        import subprocess
        import sys
        import tempfile
        helper = pathlib.Path(__file__).with_name("announce_discovery.py").resolve()
        repo = pathlib.Path(tempfile.mkdtemp())
        git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],  # noqa: E731
                                        cwd=repo, check=True, capture_output=True)
        git("init", "-q", "-b", "main")
        (repo / "STATUS.md").write_text("# S\n\n## Review thread\n\nold\n", encoding="utf-8")
        git("add", "."); git("commit", "-qm", "base")
        br, f = "claude/discovery-2026-11-24-test-9", "reference/discovery/2026-11-24.md"
        git("checkout", "-qb", br)
        (repo / "reference/discovery").mkdir(parents=True)
        (repo / f).write_text("**Status: all enumerated channels returned candidates.**\n", encoding="utf-8")
        git("add", "."); git("commit", "-qm", "ledger"); git("checkout", "-q", "main")
        env = {k: v for k, v in os.environ.items() if k != "LEDGER_FILE"}
        subprocess.run([sys.executable, "-I", str(helper), f, "5", "0", br, "2026-11-24",
                        "claude/discovery-fix-2026-11-24@abc"], cwd=repo, env=env, check=True)
        s = (repo / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("LIVE TEST", s)
        self.assertIn("**Status: all enumerated channels returned candidates.**", s)

    def test_venue_unresolved_source_is_recorded(self):
        # ChatGPT 12:50: an unresolved venue source must not vanish silently.
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_openalex_sources", lambda t: []), mock.patch.dict(d.OA, {"breaker": ""}):
            self.assertEqual(d._openalex_venue("CC", "Compiler Construction", 2026), [])
        self.assertEqual(d.VENUE_INCOMPLETE, ["CC 2026 source unresolved"])

    def test_venue_page_size_is_supported_maximum_and_cap_is_derived(self):
        # ChatGPT 19:24: help.openalex.org/api/paging documents 100 as the supported maximum and
        # page * per_page <= 10,000 for basic paging.
        self.assertEqual(d.OA_PAGE_SIZE, 100)
        self.assertEqual(d.VENUE_MAX_PAGES * d.OA_PAGE_SIZE, 10_000)

    def test_venue_full_full_partial_pages_complete(self):
        sizes = {1: 100, 2: 100, 3: 37}

        def fake_get(url, timeout=0, retries=0):
            page = int(url.split("&page=")[1].split("&")[0])
            rows = [{"title": f"P{page}-{i}", "doi": ""} for i in range(sizes.get(page, 0))]
            return json.dumps({"meta": {"count": 237}, "results": rows}).encode()

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            d._openalex_venue("ICML", "International Conference on Machine Learning", 2026)
        self.assertEqual(d.VENUE_INCOMPLETE, [])
        self.assertTrue(any("237 works listed of 237" in m for m in d.DIAG))

    def test_venue_denominator_above_basic_paging_limit_is_truncated(self):
        calls = []

        def fake_get(url, timeout=0, retries=0):
            calls.append(url)
            rows = [{"title": "x", "doi": ""}] * d.OA_PAGE_SIZE
            return json.dumps({"meta": {"count": 12_345}, "results": rows}).encode()

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]), \
                mock.patch.object(d.time, "sleep", lambda s: None):
            d._openalex_venue("NeurIPS", "Neural Information Processing Systems", 2025)
        self.assertEqual(len(calls), d.VENUE_MAX_PAGES)
        self.assertTrue(all(int(u.split("&page=")[1].split("&")[0]) * d.OA_PAGE_SIZE <= 10_000 for u in calls))
        self.assertEqual(d.VENUE_INCOMPLETE, ["NeurIPS 2025 truncated at 10000 of 12345 works"])

    def test_venue_clamped_page_size_is_degraded_not_silent(self):
        # If OpenAlex ever clamps a request to fewer rows than asked while meta.count says more
        # remain, the listing is recorded incomplete rather than treated as finished.
        def fake_get(url, timeout=0, retries=0):
            return json.dumps({"meta": {"count": 450}, "results": [{"title": "x", "doi": ""}] * 50}).encode()

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            d._openalex_venue("ICLR", "International Conference on Learning Representations", 2026)
        self.assertEqual(d.VENUE_INCOMPLETE, ["ICLR 2026 short page 1 at 50 of 450 works"])

    def test_venue_short_page_below_count_is_incomplete(self):
        # ChatGPT 12:50: a short page while meta.count says records remain is a premature stop.
        page1 = [{"title": f"Paper {i}", "doi": ""} for i in range(60)]  # short at page size 100

        def fake_get(url, timeout=0, retries=0):
            return json.dumps({"meta": {"count": 450}, "results": page1}).encode()

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            d._openalex_venue("ICLR", "International Conference on Learning Representations", 2026)
        self.assertEqual(d.VENUE_INCOMPLETE, ["ICLR 2026 short page 1 at 60 of 450 works"])

    def test_proceedings_zero_titles_past_year_is_incomplete(self):
        # Codex 16:35: a 200 response that parses to zero titles (changed template, interstitial)
        # must not pass as a complete listing for a published year. Codex 16:39: "published" is
        # per venue-year, not the calendar year. The date is pinned so the test does not drift.
        interstitial = b"<html><body><h1>Just a moment...</h1><p>Checking your browser.</p></body></html>"
        good = (b'<ul><li><a title="paper title" href="/paper_files/paper/2025/hash/abc-Abstract-Conference.html">'
                b'Compiling Tensor Programs at Scale</a></li></ul>')
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)):
            for name in ("MLSys", "NeurIPS"):
                d.VENUE_INCOMPLETE.clear()
                with mock.patch.object(d, "get", lambda url, timeout=0, retries=0: interstitial):
                    self.assertEqual(d._proceedings_titles(name, 2025), [])
                    self.assertEqual(d._proceedings_titles(name, 2026), [])
                n = len(interstitial)
                want = [f"{name} 2025 proceedings volume root parsed 0 paper links ({n} bytes)",
                        f"{name} 2025 proceedings page parsed 0 titles ({n} bytes)"]
                if name == "MLSys":  # MLSys 2026 is published by November; NeurIPS 2026 is not
                    want += [f"MLSys 2026 proceedings volume root parsed 0 paper links ({n} bytes)",
                             f"MLSys 2026 proceedings page parsed 0 titles ({n} bytes)"]
                self.assertEqual(d.VENUE_INCOMPLETE, want)
                d.VENUE_INCOMPLETE.clear()
                with mock.patch.object(d, "get", lambda url, timeout=0, retries=0: good):
                    self.assertEqual(len(d._proceedings_titles(name, 2025)), 1)
                self.assertEqual(d.VENUE_INCOMPLETE, [])

    def test_proceedings_current_year_follows_publication_date(self):
        # Codex 16:39: MLSys 2026 (135 papers) was published by mid-2026; before its date an empty
        # page is log-only, after it a failed or empty listing degrades coverage.
        for today, expect in ((d.dt.date(2026, 3, 1), []),
                              (d.dt.date(2026, 11, 24), ["MLSys 2026 proceedings site unavailable"])):
            d.VENUE_INCOMPLETE.clear()
            with mock.patch.object(d, "_today", lambda t=today: t), \
                    mock.patch.object(d, "get", lambda url, timeout=0, retries=0: None):
                self.assertEqual(d._proceedings_titles("MLSys", 2026), [])
            self.assertEqual(d.VENUE_INCOMPLETE, expect)

    def test_proceedings_without_main_track_is_incomplete(self):
        # 24 Nov 2026: papers.nips.cc/paper_files/paper/2025 listed only the 64-paper Creative AI
        # track; test 35 logged "NeurIPS 2025: 64 titles" as a complete listing.
        page = "".join(f'<a href="/paper_files/paper/2025/hash/{i:032x}-Abstract-Creative_AI_Track.html">'
                       f'Creative paper number {i}</a>' for i in range(64)).encode()
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: page):
            self.assertEqual(len(d._proceedings_titles("NeurIPS", 2025)), 64)
        self.assertEqual(d.VENUE_INCOMPLETE,
                         ["NeurIPS 2025 proceedings page has no main-track papers (64 titles from other tracks only)"])

    def test_proceedings_follow_sibling_volumes(self):
        # ChatGPT 18:18: papers.nips.cc/paper_files/paper/2025 (64 Creative AI papers) links to
        # /paper_files/paper/2025/vol38-main-conference (5,823 papers), which links back.
        root_url = "https://papers.nips.cc/paper_files/paper/2025"
        main_url = root_url + "/vol38-main-conference"

        def vol(n, suffix, adv, sib, listed=None):
            rows = "".join(f'<li><a href="/paper_files/paper/2025/hash/{suffix[:2]}{i:030x}-Abstract-{suffix}.html">'
                           f'{suffix} paper number {i}</a></li>' for i in range(listed if listed is not None else n))
            return (f'<h4>Advances 38</h4><p>{adv} papers</p><p>See also <a href="{sib}">other volume</a> '
                    f'<a href="/paper_files/paper/2024">2024</a></p><ul>{rows}</ul>').encode()

        root = vol(64, "Creative_AI_Track", 64, "/paper_files/paper/2025/vol38-main-conference")
        main = vol(5, "Conference", 5, "/paper_files/paper/2025/")
        calls = []

        def fake(pages):
            def get(url, timeout=0, retries=0):
                calls.append(url)
                return pages.get(url)
            return get

        today = mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24))
        # Healthy: both volumes read once each (reciprocal link deduplicated), no other year, no degrade.
        d.VENUE_INCOMPLETE.clear()
        with today, mock.patch.object(d, "get", fake({root_url: root, main_url: main})):
            got = d._proceedings_titles("NeurIPS", 2025)
        self.assertEqual(len(got), 69)
        self.assertEqual(sorted(calls), sorted([root_url, main_url]))
        self.assertEqual(sum(u.endswith("-Abstract-Conference.html") for _, u in got), 5)
        self.assertEqual(d.VENUE_INCOMPLETE, [])
        # Failed sibling fetch: the Creative AI volume is kept, the missing volume is named.
        d.VENUE_INCOMPLETE.clear()
        with today, mock.patch.object(d, "get", fake({root_url: root})):
            self.assertEqual(len(d._proceedings_titles("NeurIPS", 2025)), 64)
        self.assertEqual(d.VENUE_INCOMPLETE, [
            "NeurIPS 2025 proceedings volume vol38-main-conference unavailable",
            "NeurIPS 2025 proceedings page has no main-track papers (64 titles from other tracks only)"])
        # Short non-zero listing: main track present but below the publisher's count.
        d.VENUE_INCOMPLETE.clear()
        short = vol(5, "Conference", 5823, "/paper_files/paper/2025", listed=3)
        with today, mock.patch.object(d, "get", fake({root_url: root, main_url: short})):
            self.assertEqual(len(d._proceedings_titles("NeurIPS", 2025)), 67)
        self.assertEqual(d.VENUE_INCOMPLETE,
                         ["NeurIPS 2025 proceedings volume vol38-main-conference lists 3 of 5823 advertised papers"])
        # Links whose titles do not parse (inline markup) are a template change, not a complete list.
        d.VENUE_INCOMPLETE.clear()
        marked = b"".join(f'<a href="/paper_files/paper/2025/hash/{i:032x}-Abstract-Conference.html"><i>T</i> {i}</a>'
                          .encode() for i in range(10)) + b"<p>10 papers</p>"
        with today, mock.patch.object(d, "get", fake({"https://proceedings.mlsys.org/paper_files/paper/2025": marked})):
            self.assertEqual(d._proceedings_titles("MLSys", 2025), [])
        self.assertEqual(d.VENUE_INCOMPLETE, [
            "MLSys 2025 proceedings volume root: 10 of 10 paper links have no parseable title",
            f"MLSys 2025 proceedings page parsed 0 titles ({len(marked)} bytes)"])

    def test_proceedings_zero_link_volume_is_incomplete_per_volume(self):
        # ChatGPT 18:42: the per-volume audit ran only when a page had paper links. A sibling that
        # returns 200, advertises 100 papers and parses zero links passed silently because the root
        # supplied main-track titles; so did a zero-link root beside a healthy main-track sibling.
        root_url = "https://papers.nips.cc/paper_files/paper/2025"
        sib_url = root_url + "/vol38-main-conference"
        rows = "".join(f'<li><a href="/paper_files/paper/2025/hash/{i:032x}-Abstract-Conference.html">'
                       f'Main track paper number {i}</a></li>' for i in range(5))
        healthy_root = (f'<p>5 papers</p><a href="/paper_files/paper/2025/vol38-main-conference">See also</a>'
                        f'<ul>{rows}</ul>').encode()
        empty_sib = b'<p>100 papers</p><div class="new-template">papers load here</div>'
        empty_root = b'<p>See also <a href="/paper_files/paper/2025/vol38-main-conference">main</a></p>'
        healthy_sib = f'<p>5 papers</p><ul>{rows}</ul>'.encode()
        today = mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24))
        for pages, want_n, want in (
                ({root_url: healthy_root, sib_url: empty_sib}, 5,
                 [f"NeurIPS 2025 proceedings volume vol38-main-conference parsed 0 paper links of 100 advertised "
                  f"({len(empty_sib)} bytes)"]),
                ({root_url: empty_root, sib_url: healthy_sib}, 5,
                 [f"NeurIPS 2025 proceedings volume root parsed 0 paper links ({len(empty_root)} bytes)"])):
            d.VENUE_INCOMPLETE.clear()
            d.PROCEEDINGS_AUDIT.clear()
            with today, mock.patch.object(d, "get", lambda url, timeout=0, retries=0, p=pages: p.get(url)):
                got = d._proceedings_titles("NeurIPS", 2025)
            self.assertEqual(len(got), want_n)  # the healthy volume's titles are kept
            self.assertEqual(d.VENUE_INCOMPLETE, want)  # and coverage is DEGRADED, naming the empty volume
            self.assertEqual(len(d.PROCEEDINGS_AUDIT), 2)  # every visited volume has a denominator line
        self.assertIn("NeurIPS 2025 vol38-main-conference: 5 links, 5 titled, 0 untitled, advertised 5",
                      d.PROCEEDINGS_AUDIT)
        self.assertIn("NeurIPS 2025 root: 0 links, 0 titled, 0 untitled, advertised none", d.PROCEEDINGS_AUDIT)

    def test_proceedings_volume_bound_is_incomplete(self):
        page = ("".join(f'<a href="/paper_files/paper/2025/vol{i}">v</a>' for i in range(10))
                + '<a href="/paper_files/paper/2025/hash/aa-Abstract-Conference.html">A main track paper</a>').encode()
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: page):
            self.assertEqual(len(d._proceedings_titles("NeurIPS", 2025)), 1)
        self.assertEqual(d.VENUE_INCOMPLETE,
                         [f"NeurIPS 2025 more than {d.PROCEEDINGS_MAX_VOLUMES} proceedings volumes; not all read"])

    def test_usenix_zero_titles_or_unavailable_past_year_is_incomplete(self):
        # Same class as the proceedings sites: the USENIX program parser was silent on both a failed
        # fetch and a page with zero parsed titles. Codex 16:39: OSDI 2026 (437 titles) is published
        # by November, so its current-year failure degrades too; before June it stays log-only.
        page = b"<html><body>Program coming soon</body></html>"
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)):
            with mock.patch.object(d, "get", lambda url, timeout=0, retries=0: page):
                self.assertEqual(d._usenix_program("OSDI", 2025), [])
                self.assertEqual(d._usenix_program("OSDI", 2026), [])
            with mock.patch.object(d, "get", lambda url, timeout=0, retries=0: None):
                self.assertEqual(d._usenix_program("ATC", 2025), [])
        self.assertEqual(d.VENUE_INCOMPLETE, [f"OSDI 2025 USENIX program parsed 0 titles ({len(page)} bytes)",
                                              f"OSDI 2026 USENIX program parsed 0 titles ({len(page)} bytes)",
                                              "ATC 2025 USENIX program unavailable"])
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 3, 1)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: page):
            self.assertEqual(d._usenix_program("OSDI", 2026), [])
        self.assertEqual(d.VENUE_INCOMPLETE, [])
        slug = d.USENIX["OSDI"].format(yy="25")
        ok = f'<a href="/conference/{slug}/presentation/x">A Tensor Compiler</a>'.encode()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: ok):
            self.assertEqual(d._usenix_program("OSDI", 2025), ["A Tensor Compiler"])
        self.assertEqual(d.VENUE_INCOMPLETE, [])

    def test_usenix_venue_after_last_edition_is_not_fetched_or_degraded(self):
        # USENIX sunset ATC after ATC '25; atc26 is HTTP 404. The venue-year gate must not turn a
        # venue that no longer exists into a permanent DEGRADED, and must not spend a fetch on it.
        calls = []
        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: calls.append(url)):
            self.assertEqual(d._usenix_program("ATC", 2026), [])
            self.assertEqual(d._usenix_program("ATC", 2027), [])
        self.assertEqual(calls, [])
        self.assertEqual(d.VENUE_INCOMPLETE, [])
        # The last edition and OSDI are unaffected: a failed fetch still degrades.
        with mock.patch.object(d, "_today", lambda: d.dt.date(2026, 11, 24)), \
                mock.patch.object(d, "get", lambda url, timeout=0, retries=0: None):
            self.assertEqual(d._usenix_program("ATC", 2025), [])
            self.assertEqual(d._usenix_program("OSDI", 2026), [])
        self.assertEqual(d.VENUE_INCOMPLETE, ["ATC 2025 USENIX program unavailable",
                                              "OSDI 2026 USENIX program unavailable"])
        d.VENUE_INCOMPLETE.clear()

    def test_refs_second_metadata_batch_failure_is_counted(self):
        # ChatGPT 12:50: one successful metadata batch, then a failed one -> returned < requested, DEGRADED input.
        refs = [f"https://openalex.org/W{i}" for i in range(60)]
        calls = {"n": 0}

        def responses_get(url, timeout=0, retries=0):
            if "filter=doi:" in url:
                return json.dumps({"results": [{"id": "W1", "doi": "https://doi.org/10.1/a",
                                                "referenced_works": refs}]}).encode()
            if "filter=openalex:" in url:
                calls["n"] += 1
                if calls["n"] == 1:
                    ids = url.split("filter=openalex:")[1].split("&")[0].split("|")
                    return json.dumps({"results": [{"id": f"https://openalex.org/{w}", "title": f"Work {w}"}
                                                   for w in ids]}).encode()
                return None
            return json.dumps({"results": []}).encode()

        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "hit.md").write_text("# Some Paper Title Here\n\n| **Type** | paper |\n| **DOI** | 10.1/a |\n",
                                    encoding="utf-8")
        d.REFS_AUDIT.clear()
        d.REFS_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", responses_get), \
                mock.patch.object(d, "_digest_keys", lambda t: ("10.1/a", d._digest_title(t))):
            d.references_candidates({"arxiv": set(), "doi": set(), "github": set(), "titles": set()}, min_digests=2)
        self.assertEqual((d.REFS_AUDIT["requested"], d.REFS_AUDIT["returned"], d.REFS_AUDIT["failed_batches"]),
                         (60, 50, 1))
        self.assertEqual(d.REFS_INCOMPLETE, ["batch 2 (10 works) failed"])
        self.assertTrue(any("refs incomplete: 50 of 60 requested works returned" in m for m in d.DIAG))

    def _cites_run(self, cites_get):
        import datetime
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        for n, aid in (("a", "2601.00001"), ("b", "2601.00002")):
            (tmp / f"{n}.md").write_text(f"# Seed {n} paper title\n\n| **Evidence tier** | A |\n"
                                         f"| **Link** | https://arxiv.org/abs/{aid} |\n", encoding="utf-8")

        def fake_get(url, timeout=0, retries=0):
            if "filter=doi:" in url:
                return json.dumps({"results": [
                    {"id": "https://openalex.org/WA", "doi": "https://doi.org/10.48550/arxiv.2601.00001", "title": "Seed a"},
                    {"id": "https://openalex.org/WB", "doi": "https://doi.org/10.48550/arxiv.2601.00002", "title": "Seed b"},
                ]}).encode()
            return cites_get(url)

        d.CITES_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get), \
                mock.patch.object(d.time, "sleep", lambda s: None), mock.patch.dict(d.OA, {"breaker": ""}):
            return d.cited_by_candidates({}, datetime.date.today())

    def test_cites_one_seed_ok_one_failed_is_incomplete(self):
        # ChatGPT 12:56: a failed seed must mark cites incomplete even when another seed returned rows.
        def cites_get(url):
            if "cites:WA" in url:
                return json.dumps({"meta": {"count": 2}, "results": [
                    {"id": "W1", "title": "Citer 1"}, {"id": "W2", "title": "Citer 2"}]}).encode()
            return None

        out = self._cites_run(cites_get)
        self.assertEqual(len(out), 2)
        self.assertEqual(d.CITES_INCOMPLETE, ["2601.00002 page 1 failed after 0 citing works"])

    def test_cites_count_above_page_cap_is_truncated(self):
        # ChatGPT 12:56: more in-window citing works than the pages read must be reported, not silently cut.
        def cites_get(url):
            if "cites:WA" in url:
                page = int(url.split("&page=")[1].split("&")[0])
                return json.dumps({"meta": {"count": 750}, "results": [
                    {"id": f"W{page}-{i}", "title": f"Citer {page}-{i}"} for i in range(d.CITES_PER_PAGE)]}).encode()
            return json.dumps({"meta": {"count": 1}, "results": [{"id": "WX", "title": "Only citer"}]}).encode()

        out = self._cites_run(cites_get)
        self.assertEqual(len(out), d.CITES_PER_PAGE * d.CITES_MAX_PAGES + 1)
        self.assertEqual(d.CITES_INCOMPLETE, [f"2601.00001 truncated at {d.CITES_PER_PAGE * d.CITES_MAX_PAGES} of 750 citing works"])

    def test_cites_failed_doi_batch_is_recorded(self):
        import datetime
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        d.CITES_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", lambda u, timeout=0, retries=0: None), \
                mock.patch.dict(d.OA, {"breaker": ""}):
            (tmp / "a.md").write_text("# Seed\n\n| **Evidence tier** | A |\n| **Link** | https://arxiv.org/abs/2601.00001 |\n",
                                      encoding="utf-8")
            d.cited_by_candidates({}, datetime.date.today())
        self.assertEqual(d.CITES_INCOMPLETE[0], "DOI batch 1 (1 seeds) failed")

    def _cites_title_fallback(self, hits):
        # Seed b misses by DOI, so it falls back to a title search that returns `hits`.
        import datetime
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "b.md").write_text("# Seed b paper title (ICLR 2026)\n\n| **Evidence tier** | A |\n"
                                  "| **Link** | https://arxiv.org/abs/2601.00002 |\n", encoding="utf-8")
        asked = []

        def fake_get(url, timeout=0, retries=0):
            if "filter=doi:" in url:
                return json.dumps({"results": []}).encode()
            if "title.search:" in url:
                return json.dumps({"results": hits}).encode()
            asked.append(url.split("filter=cites:")[1].split(",")[0])
            return json.dumps({"meta": {"count": 1}, "results": [{"id": "WC", "title": "Citer"}]}).encode()

        d.CITES_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get), \
                mock.patch.object(d.time, "sleep", lambda s: None), mock.patch.dict(d.OA, {"breaker": ""}):
            d.cited_by_candidates({}, datetime.date.today())
        return asked

    def test_cites_title_fallback_skips_unrelated_first_hit(self):
        # ChatGPT 13:01: an unrelated first hit must not be taken as the seed.
        asked = self._cites_title_fallback([
            {"id": "https://openalex.org/WWRONG", "title": "Seed b paper title revisited: a survey"},
            {"id": "https://openalex.org/WRIGHT", "title": "Seed B: paper title"}])
        self.assertEqual(asked, ["WRIGHT"])
        self.assertEqual(d.CITES_INCOMPLETE, [])

    def test_cites_title_fallback_prefers_arxiv_id(self):
        asked = self._cites_title_fallback([
            {"id": "https://openalex.org/WDUP1", "title": "Seed b paper title"},
            {"id": "https://openalex.org/WARX", "title": "Seed b paper title",
             "ids": {"openalex": "https://openalex.org/WARX", "arxiv": "https://arxiv.org/abs/2601.00002"}}])
        self.assertEqual(asked, ["WARX"])

    def test_cites_title_fallback_unconfirmed_is_incomplete(self):
        # Only near-misses, or two distinct exact-title records: unresolved, no citers read.
        for hits in ([{"id": "https://openalex.org/WWRONG", "title": "Seed b paper title revisited"}],
                     [{"id": "https://openalex.org/W1", "title": "Seed b paper title"},
                      {"id": "https://openalex.org/W2", "title": "Seed b paper title"}]):
            asked = self._cites_title_fallback(hits)
            self.assertEqual(asked, [])
            self.assertEqual(len(d.CITES_INCOMPLETE), 1)
            self.assertIn("2601.00002 title match unconfirmed", d.CITES_INCOMPLETE[0])

    def test_cites_fallback_uses_owning_digest_title_not_citing_digest(self):
        # ChatGPT 13:06: an earlier digest (a.md) cites the seed's arXiv ID; the fallback must search
        # the owning digest's title (b.md), so the citing paper's exact title cannot validate itself.
        import datetime
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        (tmp / "a.md").write_text("# Citing paper title here\n\n| **Evidence tier** | B |\n"
                                  "| **Link** | https://arxiv.org/abs/2601.00009 |\n"
                                  "Builds on https://arxiv.org/abs/2601.00002.\n", encoding="utf-8")
        (tmp / "b.md").write_text("# Seed b paper title\n\n| **Evidence tier** | A |\n"
                                  "| **Link** | https://arxiv.org/abs/2601.00002 |\n", encoding="utf-8")
        searched, asked = [], []

        def fake_get(url, timeout=0, retries=0):
            if "filter=doi:" in url:
                return json.dumps({"results": []}).encode()
            if "title.search:" in url:
                q = d.urllib.parse.unquote(url.split("title.search:")[1].split("&")[0])
                searched.append(q)
                title = "Citing paper title here" if "Citing" in q else "Seed b paper title"
                return json.dumps({"results": [{"id": "https://openalex.org/W" + title.split()[0].upper(),
                                                "title": title}]}).encode()
            asked.append(url.split("filter=cites:")[1].split(",")[0])
            return json.dumps({"meta": {"count": 0}, "results": []}).encode()

        d.CITES_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get), \
                mock.patch.object(d.time, "sleep", lambda s: None), mock.patch.dict(d.OA, {"breaker": ""}):
            d.cited_by_candidates({}, datetime.date.today())
        self.assertEqual(searched, ["Seed b paper title"])
        self.assertEqual(asked, ["WSEED"])

    def test_refs_title_fallback_rejects_shared_prefix(self):
        # ChatGPT 13:06: a different paper sharing the first 30 normalized characters must not
        # supply the reference list; a unique exact title does.
        wrong = {"id": "W2", "title": "Paper Missing From OpenAlex By DOI: Extended Journal Version",
                 "referenced_works": ["https://openalex.org/W9"]}
        self._refs({"filter=doi:": [{"id": "W1", "doi": "https://doi.org/10.1/a", "referenced_works": []}],
                    "title.search": [wrong]})
        self.assertEqual((d.REFS_AUDIT["title_hit"], d.REFS_AUDIT["title_unconfirmed"]), (0, 1))
        self._refs({"filter=doi:": [{"id": "W1", "doi": "https://doi.org/10.1/a", "referenced_works": []}],
                    "title.search": [wrong, {"id": "W3", "title": "Paper Missing From OpenAlex By DOI",
                                             "referenced_works": ["https://openalex.org/W9"]}]})
        self.assertEqual((d.REFS_AUDIT["title_hit"], d.REFS_AUDIT["title_unconfirmed"]), (1, 0))

    def test_refs_failed_doi_batch_with_incomplete_fallback_is_degraded(self):
        # ChatGPT 13:11: the DOI batch fails; one seed is recovered by title, the other's title
        # search also fails. The DOI failure and the unrecovered seed are both named.
        def responses(url):
            if "title.search" in url and "Empty" in d.urllib.parse.unquote(url):
                return json.dumps({"results": [{"id": "W1", "title": "Empty Reference List Paper Title",
                                                "referenced_works": ["https://openalex.org/W9"]}]}).encode()
            return None

        d.REFS_INCOMPLETE.clear()
        self._refs(responses)
        self.assertEqual((d.REFS_AUDIT["title_hit"], d.REFS_AUDIT["title_failed"]), (1, 1))
        self.assertIn("DOI batch 1 (2 seeds) failed -> title fallback", d.REFS_INCOMPLETE)
        self.assertIn("miss title search failed", d.REFS_INCOMPLETE)
        self.assertTrue(any(m.startswith("refs seeds unresolved: 2") for m in d.DIAG))

    def test_refs_zero_hit_title_search_is_named_not_failed(self):
        d.REFS_INCOMPLETE.clear()
        self._refs({"filter=doi:": [{"id": "W1", "doi": "https://doi.org/10.1/a", "referenced_works": []}]})
        self.assertEqual((d.REFS_AUDIT["title_zero"], d.REFS_AUDIT["title_failed"]), (1, 0))
        self.assertEqual(d.REFS_INCOMPLETE, ["miss unresolved (title search: 0 hits)"])

    def test_refs_seed_audit_renders_every_gap_uncapped(self):
        # ChatGPT (review of 6d41a41): with only 0-hit / unconfirmed gaps, the `refs seeds
        # unresolved` line matched no fetch-log filter and the status line showed six. Eight 0-hit
        # seeds, one unconfirmed, one matched-but-empty and one duplicate title must all be in the
        # rendered ledger, with matched-empty and duplicates kept apart from unresolved identity.
        import pathlib
        import tempfile
        tmp = pathlib.Path(tempfile.mkdtemp())
        for n in range(8):
            (tmp / f"zero{n}.md").write_text(f"# Zero hit seed paper number {n}\n\n| **Type** | paper |\n",
                                            encoding="utf-8")
        (tmp / "amb.md").write_text("# Ambiguous seed paper title\n\n| **Type** | paper |\n", encoding="utf-8")
        (tmp / "dupa.md").write_text("# Ambiguous seed paper title\n\n| **Type** | paper |\n", encoding="utf-8")
        (tmp / "empty.md").write_text("# Empty list seed paper title\n\n| **Type** | paper |\n"
                                      "| **Link** | https://doi.org/10.1000/e |\n", encoding="utf-8")

        def fake_get(url, timeout=0, retries=0):
            q = d.urllib.parse.unquote(url)
            if "filter=doi:" in url:
                return json.dumps({"results": [{"id": "WE", "doi": "https://doi.org/10.1000/e",
                                                "referenced_works": []}]}).encode()
            if "title.search" in url and "Ambiguous" in q:
                return json.dumps({"results": [{"id": "WX", "title": "Something else"}]}).encode()
            return json.dumps({"results": []}).encode()

        d.REFS_AUDIT.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get):
            d.references_candidates({}, min_digests=2)
        self.assertEqual((d.REFS_AUDIT["title_zero"], d.REFS_AUDIT["title_unconfirmed"]), (8, 1))
        ledger = "\n".join(d.render_fetch_log(True))
        for n in range(8):
            self.assertIn(f"- zero{n} unresolved (title search: 0 hits)", ledger)
        self.assertIn("- amb title match unconfirmed", ledger)
        empty_part = ledger.split("identity resolved, not DEGRADED", 1)[1]
        self.assertIn("- empty\n", empty_part + "\n")
        self.assertIn("- dupa (duplicate key of amb", empty_part)
        self.assertNotIn("empty unresolved", ledger)
        self.assertEqual(len(d.REFS_INCOMPLETE), 9)

    def test_bom_title(self):
        self.assertEqual(d._digest_title("﻿# Ansor: Generating High-Performance Tensor Programs (OSDI 2020)\n"),
                         "Ansor: Generating High-Performance Tensor Programs")


class ArxivPartialCoverage(unittest.TestCase):
    """test-34: arXiv 429s cost three categories but the channel still returned rows."""

    def test_failed_category_page_is_recorded(self):
        d.ARXIV_INCOMPLETE.clear()
        feed = (b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><published>2026-11-20T00:00:00Z</published>'
                b'<title>A Tensor Compiler for Kernels</title><summary>compiler kernel</summary>'
                b'<id>http://arxiv.org/abs/2611.00001v1</id></entry>'
                b'<entry><published>2026-10-01T00:00:00Z</published><title>Old</title><summary>x</summary>'
                b'<id>http://arxiv.org/abs/2610.00001v1</id></entry></feed>')
        calls = []

        def fake_get(url, timeout=0, retries=0):
            calls.append(url)
            return None if "cs.LG" in url else feed

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "ARXIV_CATS", ["cs.PL", "cs.LG"]), \
                mock.patch.object(d.time, "sleep", lambda s: None):
            rows = d.arxiv_candidates(d.dt.date(2026, 11, 3), max_per_cat=100)
        self.assertEqual(len(rows), 1)
        self.assertEqual(d.ARXIV_INCOMPLETE, ["cs.LG from offset 0 failed"])

    @staticmethod
    def _page(n, offset, date="2026-11-20"):
        body = "".join(f'<entry><published>{date}T00:00:00Z</published><title>Paper {offset + i}</title>'
                       f'<summary>x</summary><id>http://arxiv.org/abs/2611.{offset + i:05d}v1</id></entry>'
                       for i in range(n))
        return ('<feed xmlns="http://www.w3.org/2005/Atom">' + body + '</feed>').encode()

    def test_cap_with_full_in_window_pages_degrades(self):
        """Codex 13:25: four full in-window pages ending at the cap must not pass silently."""
        d.ARXIV_INCOMPLETE.clear()
        offsets = []

        def fake_get(url, timeout=0, retries=0):
            off = int(url.split("start=")[1].split("&")[0])
            offsets.append(off)
            return self._page(100, off)

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "ARXIV_CATS", ["cs.LG"]), \
                mock.patch.object(d.time, "sleep", lambda s: None):
            d.arxiv_candidates(d.dt.date(2026, 11, 3), max_per_cat=400, page=100)
        self.assertEqual(offsets, [0, 100, 200, 300])
        self.assertEqual(d.ARXIV_INCOMPLETE, ["cs.LG cap 400 reached at offset 400, window not exhausted"])

    def test_pages_to_window_boundary_without_degrading(self):
        d.ARXIV_INCOMPLETE.clear()
        offsets = []

        def fake_get(url, timeout=0, retries=0):
            off = int(url.split("start=")[1].split("&")[0])
            offsets.append(off)
            return self._page(100, off, "2026-11-20" if off < 500 else "2026-10-01")

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "ARXIV_CATS", ["cs.LG"]), \
                mock.patch.object(d.time, "sleep", lambda s: None):
            d.arxiv_candidates(d.dt.date(2026, 11, 3), page=100)
        self.assertEqual(offsets, [0, 100, 200, 300, 400, 500])  # read past the old 400 cap
        self.assertEqual(d.ARXIV_INCOMPLETE, [])

    def test_empty_page_mid_listing_degrades(self):
        d.ARXIV_INCOMPLETE.clear()

        def fake_get(url, timeout=0, retries=0):
            off = int(url.split("start=")[1].split("&")[0])
            if off == 0:
                return self._page(100, 0)
            return (b'<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">'
                    b'<opensearch:totalResults>90000</opensearch:totalResults></feed>')

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "ARXIV_CATS", ["cs.LG"]), \
                mock.patch.object(d.time, "sleep", lambda s: None):
            d.arxiv_candidates(d.dt.date(2026, 11, 3), page=100)
        self.assertEqual(d.ARXIV_INCOMPLETE, ["cs.LG empty page at offset 100 before window boundary"])


class FrozenCorpusRecall(unittest.TestCase):
    """ChatGPT 13:49 / Action 13:52: held-out set = later digests absent from the frozen corpus."""

    def _run(self, digests: dict, cands: list, since=(2026, 9, 24)) -> str:
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as tmp:
            old, new = Path(tmp, "old"), Path(tmp, "new")
            for root in (old, new):
                (root / "reference" / "publications").mkdir(parents=True)
                (root / "reference" / "publications" / "kept.md").write_text("# Kept paper\n", encoding="utf-8")
            for stem, body in digests.items():
                (new / "reference" / "publications" / f"{stem}.md").write_text(body, encoding="utf-8")
            with mock.patch.object(d, "PUBS", old / "reference" / "publications"):
                return "\n".join(d.recall_section(new, cands, d.dt.date(*since)))

    def test_recall_section_counts_per_channel(self):
        text = self._run({
            "accelopt": "# AccelOpt: A Self-Improving LLM Agentic System (MLSys 2026)\n| **Year** | 2025 |\n"
                        "| **Type** | paper |\n| **Link** | [arXiv](https://arxiv.org/abs/2511.15915) |\n",
            "lost": "# A Paper Nobody Surfaces At All\n| **Year** | 2026 |\n| **Type** | paper |\n"
                    "| **Link** | [x](https://example.org) |\n"},
            [{"channel": "venue", "id": "", "title": "AccelOpt: A Self-Improving LLM Agentic System",
              "url": "https://proceedings.mlsys.org/x"},
             {"channel": "arxiv", "id": "2511.15915v2", "title": "AccelOpt", "url": ""}])
        self.assertIn("**1 of 2**", text)
        self.assertIn('{"arxiv": 1, "venue": 1}', text)
        self.assertIn("| lost | paper | 2026 | indeterminate | **not recovered** | — |", text)
        self.assertIn("| accelopt | paper | 2025-11 | before window | arxiv, venue | identifier |", text)
        self.assertIn("before window: 1 of 1 recovered", text)

    def test_cited_paper_in_body_does_not_credit_the_digest(self):
        # Codex 14:13: a digest lacking its own arXiv id must not borrow one from a related-work link.
        text = self._run({
            "blogpost": "# Vendor Kernel Blog Post About Something\n| **Year** | 2026 |\n| **Type** | company |\n"
                        "| **Link** | [blog](https://vendor.example/blog) |\n\nBuilds on https://arxiv.org/abs/2502.00001.\n"},
            [{"channel": "arxiv", "id": "2502.00001", "title": "The Cited Paper", "url": ""}])
        self.assertIn("**0 of 1**", text)
        self.assertIn("**not recovered**", text)

    def test_shared_title_prefix_is_not_a_match(self):
        # Codex 14:13: two works sharing a 50-character prefix are different works.
        title = "Learning to Optimize Tensor Programs with Graph Neural Networks"
        text = self._run({
            "tp": f"# {title}\n| **Year** | 2026 |\n| **Type** | paper |\n| **Link** | [x](https://example.org) |\n"},
            [{"channel": "venue", "id": "", "title": title + " and Reinforcement Learning at Scale", "url": ""}])
        self.assertIn("**0 of 1**", text)

    def test_same_title_different_identifier_is_ignored_and_short_title_needs_adjudication(self):
        text = self._run({
            "x": "# Same Title Different Work Here\n| **Year** | 2026 |\n| **Type** | paper |\n"
                 "| **Link** | [arXiv](https://arxiv.org/abs/2610.11111) |\n",
            "short": "# Ansor\n| **Year** | 2020 |\n| **Type** | paper |\n| **Link** | [x](https://example.org) |\n"},
            [{"channel": "arxiv", "id": "2611.22222", "title": "Same Title Different Work Here", "url": ""},
             {"channel": "refs", "id": "10.1/abc", "title": "Ansor", "url": ""}])
        self.assertIn("**0 of 2** (1 more need adjudication", text)
        self.assertIn("| short | paper | 2020 | before window | **adjudicate:** refs | ambiguous title |", text)
        self.assertIn("| x | paper | 2026-10 | in window | **not recovered** | — |", text)

    def test_cutoff_month_and_year_are_indeterminate(self):
        # Codex 14:19: an arXiv id carries year and month only, a Year row the year only.
        digests = {
            "sep": "# A September Paper On Compilers\n| **Year** | 2026 |\n| **Type** | paper |\n"
                   "| **Link** | [arXiv](https://arxiv.org/abs/2609.00001) |\n",
            "oct": "# An October Paper On Compilers\n| **Year** | 2026 |\n| **Type** | paper |\n"
                   "| **Link** | [arXiv](https://arxiv.org/abs/2610.00001) |\n",
            "aug": "# An August Paper On Compilers\n| **Year** | 2026 |\n| **Type** | paper |\n"
                   "| **Link** | [arXiv](https://arxiv.org/abs/2608.00001) |\n",
            "yr": "# A Year Only Paper On Compilers\n| **Year** | 2026 |\n| **Type** | paper |\n"
                  "| **Link** | [x](https://example.org) |\n",
            "nodate": "# An Undated Paper On Compilers\n| **Type** | paper |\n| **Link** | [x](https://example.org) |\n"}
        text = self._run(digests, [])
        self.assertIn("| sep | paper | 2026-09 | indeterminate |", text)
        self.assertIn("| oct | paper | 2026-10 | in window |", text)
        self.assertIn("| aug | paper | 2026-08 | before window |", text)
        self.assertIn("| yr | paper | 2026 | indeterminate |", text)
        self.assertIn("| nodate | paper | ? | undated |", text)
        self.assertIn("indeterminate: 0 of 2 recovered", text)
        # A window opening on the first of the month (or year) puts the whole cutoff month (or year) in window.
        text = self._run(digests, [], since=(2026, 9, 1))
        self.assertIn("| sep | paper | 2026-09 | in window |", text)
        self.assertIn("| yr | paper | 2026 | indeterminate |", text)
        text = self._run(digests, [], since=(2026, 1, 1))
        self.assertIn("| yr | paper | 2026 | in window |", text)

    def test_pre_cutoff_venue_hit_is_credited_and_wording_names_channel_windows(self):
        # Codex 14:23: venues lists the current and preceding years without `since`, so a source dated
        # before the window start can be recovered by venues alone; the report must not say refs/cites only.
        text = self._run({
            "old": "# A Venue Paper From Last Year On Kernels\n| **Year** | 2025 |\n| **Type** | paper |\n"
                   "| **Link** | [x](https://example.org) |\n"},
            [{"channel": "venue", "id": "", "title": "A Venue Paper From Last Year On Kernels", "url": ""}])
        self.assertIn("| old | paper | 2025 | before window | venue | title only |", text)
        self.assertIn("before window: 1 of 1 recovered", text)
        self.assertIn('{"venue": 1}', text)
        self.assertNotIn("can only be recovered by refs or cites", text)
        self.assertIn("venues: listings for the current and preceding calendar years, with no window filter", text)
        self.assertIn("| Date class |", text)


    def test_frozen_cutoff_follows_corpus_commit(self):
        # Codex 14:58: an alternate frozen SHA must not inherit the default commit's cutoff.
        import pathlib
        import subprocess
        import sys
        import tempfile
        root = pathlib.Path(tempfile.mkdtemp())
        corpus, out = root / "corpus", root / "out"
        (corpus / "reference" / "publications").mkdir(parents=True)
        out.mkdir()
        (corpus / "reference" / "publications" / "INDEX.md").write_text("# Index\n", encoding="utf-8")
        env = dict(__import__("os").environ, GIT_COMMITTER_DATE="2026-08-10T12:00:00Z",
                   GIT_AUTHOR_DATE="2026-08-10T12:00:00Z")
        git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a],  # noqa: E731
                                        cwd=corpus, env=env, check=True, capture_output=True)
        git("init", "-q"); git("add", "."); git("commit", "-qm", "corpus")
        sha, when = d.corpus_commit(corpus)
        self.assertEqual(when.isoformat(), "2026-08-10")
        script = pathlib.Path(d.__file__).resolve()
        run = lambda *extra: subprocess.run([sys.executable, "-I", str(script), "--channels", "none",  # noqa: E731
                                             "--corpus-root", str(corpus), *extra], check=True, capture_output=True)
        run("--out", str(out / "derived.md"))
        derived = (out / "derived.md").read_text(encoding="utf-8")
        self.assertIn(f"Frozen corpus: `{sha[:12]}` committed 2026-08-10 UTC; cutoff 2026-08-11 (derived", derived)
        self.assertIn("Window: since 2026-08-11.", derived)
        self.assertNotIn("cutoff: --since", derived)
        self.assertIn("**Status: NOT RUN** — fixture mode", derived)  # ChatGPT 15:05: zero channels is not a pass
        run("--since", "2026-09-24", "--out", str(out / "stale.md"))
        stale = (out / "stale.md").read_text(encoding="utf-8")
        self.assertIn("**Status: DEGRADED** — cutoff: --since 2026-09-24 does not follow frozen corpus", stale)
        self.assertIn("expected 2026-08-11", stale)

    def test_frozen_corpus_without_feeds_does_not_use_current_watchlist(self):
        # ChatGPT 15:05: 4336d72 has no feeds.txt; the frozen run must not fall back to today's feeds.
        import pathlib
        import subprocess
        import sys
        import tempfile
        root = pathlib.Path(tempfile.mkdtemp())
        corpus, out = root / "corpus", root / "out"
        (corpus / "reference" / "publications").mkdir(parents=True)
        out.mkdir()
        (corpus / "reference" / "publications" / "INDEX.md").write_text("# Index\n", encoding="utf-8")
        self.assertTrue(d.FEEDS.exists(), "fixture needs a current feeds.txt to show the leak")
        script = pathlib.Path(d.__file__).resolve()
        run = lambda name: subprocess.run([sys.executable, "-I", str(script), "--channels", "none",  # noqa: E731
                                           "--since", "2026-09-24", "--corpus-root", str(corpus),
                                           "--out", str(out / name)], check=True, capture_output=True)
        run("l.md")
        text = (out / "l.md").read_text(encoding="utf-8")
        self.assertIn("Frozen feeds: none (the snapshot has no reference/discovery/feeds.txt", text)
        self.assertNotIn("all enumerated channels returned candidates", text)
        (corpus / "reference" / "discovery").mkdir(parents=True)
        (corpus / "reference" / "discovery" / "feeds.txt").write_text("# empty\n", encoding="utf-8")
        run("m.md")
        self.assertIn("Frozen feeds: 0 from the snapshot's feeds.txt.", (out / "m.md").read_text(encoding="utf-8"))

    def test_unknown_channel_is_rejected(self):
        import pathlib
        import subprocess
        import sys
        import tempfile
        script = pathlib.Path(d.__file__).resolve()
        r = subprocess.run([sys.executable, "-I", str(script), "--channels", "arxiv,bogus",
                            "--out", str(pathlib.Path(tempfile.mkdtemp()) / "x.md")], capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unknown channel(s): bogus", r.stderr)

    def test_main_dedupes_ordinary_candidates_offline(self):
        # ChatGPT 16:08: a local `known` set in main() shadowed the known() dedupe and crashed on the first
        # non-repoevent candidate. Drive main() end to end with one indexed and one unindexed arXiv candidate.
        import pathlib
        import sys
        import tempfile
        root = pathlib.Path(tempfile.mkdtemp())
        corpus, out = root / "corpus", root / "l.md"
        (corpus / "reference" / "publications").mkdir(parents=True)
        (corpus / "reference" / "publications" / "INDEX.md").write_text(
            "# Index\n\n- [Indexed Compiler Paper](indexed.md) arXiv 2401.00001\n", encoding="utf-8")
        mk = lambda aid, t: {"channel": "arxiv", "id": aid, "title": t, "date": "2026-11-01",  # noqa: E731
                             "url": f"https://arxiv.org/abs/{aid}", "why": "compiler", "cat": "cs.PL"}
        cands = [mk("2401.00001v2", "Indexed Compiler Paper"), mk("2611.99999", "An Unindexed Agentic Compiler")]
        # Without a key the run reaches the dedupe loop directly; with a key it must still not probe
        # OpenAlex, because no OpenAlex channel was selected.
        for key in ("", "k"):
            with self.subTest(openalex_key=bool(key)):
                saved = (d.INDEX, d.REPOS, d.PUBS, d.FEEDS)
                try:
                    with mock.patch.object(sys, "argv", ["discover.py", "--channels", "arxiv", "--since", "2026-10-01",
                                                         "--corpus-root", str(corpus), "--out", str(out)]), \
                         mock.patch.object(d, "arxiv_candidates", return_value=cands), \
                         mock.patch.object(d, "get", side_effect=AssertionError("network call in offline test")), \
                         mock.patch.object(d, "OPENALEX_KEY", key):
                        d.main()
                finally:
                    d.INDEX, d.REPOS, d.PUBS, d.FEEDS = saved
                text = out.read_text(encoding="utf-8")
                self.assertIn("An Unindexed Agentic Compiler", text)
                self.assertNotIn("2401.00001", text)
                self.assertNotIn("Indexed Compiler Paper", text)

    def test_ledger_notices_carry_degraded_reasons_and_seed_audit(self):
        # Codex 14:58: annotations must let a reviewer tell coverage gaps from rate limits and unresolved seeds.
        import pathlib
        import subprocess
        import sys
        import tempfile
        helper = pathlib.Path(__file__).with_name("ledger_notices.py").resolve()
        f = pathlib.Path(tempfile.mkdtemp()) / "l.md"
        recovery = "## Frozen-corpus recovery estimate\n\n" + "| row |\n" * 6000 + "\n"
        f.write_text("# Discovery ledger\n\nProvenance: x\n\nWindow: since 2026-09-24.\n\n"
                     "**Status: DEGRADED** — refs: 3 seeds or metadata batches incomplete (a; b; c).\n\n"
                     + recovery + "## Channel diagnostics\n\nRaw candidates per channel: {\"refs\": 0}\n\n"
                     "### refs seed audit (complete)\n\n- seed-one: HTTP 429 (Retry-After 3600)\n\n"
                     "Fetch log (failures and venue page sizes):\n\n- openalex breaker: tripped\n", encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(helper), str(f), "frozen", "ledger-frozen-abc"],
                             check=True, capture_output=True, text=True).stdout
        notes = [l for l in out.splitlines() if l.startswith("::notice")]
        self.assertLessEqual(len(notes), 9)
        self.assertIn("refs: 3 seeds or metadata batches incomplete", notes[0])
        self.assertIn("Raw candidates per channel", notes[0])
        self.assertTrue(any("seed-one: HTTP 429" in n for n in notes), "seed audit must survive a long recovery table")
        self.assertTrue(any("openalex breaker: tripped" in n for n in notes))
        self.assertTrue(any("truncated for the annotation budget; full text in ledger-frozen-abc" in n for n in notes))
        self.assertIn("ledger-frozen-abc", notes[-1])

    def test_ledger_notices_budget_counts_escaped_utf8_bytes(self):
        # Codex 16:31: a character budget let a non-ASCII, %-bearing table exceed 4 KB once escaped.
        import pathlib
        import subprocess
        import sys
        import tempfile
        helper = pathlib.Path(__file__).with_name("ledger_notices.py").resolve()
        f = pathlib.Path(tempfile.mkdtemp()) / "l.md"
        rows = "".join(f"| d-{i} | Ünïcödé 混合精度 50% “quoted” {i} | not recovered |\n" for i in range(400))
        longline = "混%" * 3000 + "\n"
        f.write_text("# Discovery ledger\n\n**Status: DEGRADED** — x\n\n## Frozen-corpus recovery estimate\n\n"
                     + longline + rows + "\n## Channel diagnostics\n\nFetch log\n\n- ok\n", encoding="utf-8")
        out = subprocess.run([sys.executable, "-I", str(helper), str(f), "frozen", "ledger-frozen-abc"],
                             check=True, capture_output=True, text=True, encoding="utf-8").stdout
        notes = [l for l in out.splitlines() if l.startswith("::notice")]
        self.assertLessEqual(len(notes), 9)
        for n in notes:
            self.assertLessEqual(len(n.split("::", 2)[2].encode("utf-8")), 3500, n[:80])
            self.assertLess(len(n.encode("utf-8")), 4000)
        self.assertTrue(any("truncated for the annotation budget; full text in ledger-frozen-abc" in n for n in notes))

if __name__ == "__main__":
    unittest.main()
