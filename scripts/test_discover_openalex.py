"""Network-free tests for the OpenAlex budget handling in scripts/discover.py.

Background (Review thread, 24 November 2026): run r30 logged 172 OpenAlex 429s, and both
`cites` and `refs` returned nothing. Keyless OpenAlex clients get about $0.10 a day per IP.
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
                 "channel": "", "skipped_in": {}})
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

    def test_venue_listing_pages_without_search_and_filters_locally(self):
        works = [{"title": f"Paper {i}", "doi": "", "publication_date": "2026-05-01"} for i in range(399)]
        works[250]["title"] = "AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization"
        urls = []

        def fake_get(url, timeout=0, retries=0):
            urls.append(url)
            page = int(url.split("&page=")[1].split("&")[0])
            chunk = works[(page - 1) * 200: page * 200]
            return json.dumps({"meta": {"count": len(works)}, "results": chunk}).encode()

        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            kept = d._openalex_venue("MLSys", "Machine Learning and Systems", 2026)
        self.assertEqual(len(urls), 2)
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
        page1 = [{"title": f"Paper {i}", "doi": ""} for i in range(200)]
        page1[3]["title"] = "AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization"

        def fake_get(url, timeout=0, retries=0):
            if "&page=1&" in url:
                return json.dumps({"meta": {"count": 450}, "results": page1}).encode()
            return None

        d.VENUE_INCOMPLETE.clear()
        with mock.patch.object(d, "get", fake_get), mock.patch.object(d, "_openalex_sources", lambda t: ["S1"]):
            kept = d._openalex_venue("ICLR", "International Conference on Learning Representations", 2026)
        self.assertEqual([w["title"][:8] for w in kept], ["AccelOpt"])
        self.assertEqual(d.VENUE_INCOMPLETE, ["ICLR 2026 page 2 failed after 200 of 450 works"])

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

    def test_bom_title(self):
        self.assertEqual(d._digest_title("﻿# Ansor: Generating High-Performance Tensor Programs (OSDI 2020)\n"),
                         "Ansor: Generating High-Performance Tensor Programs")


if __name__ == "__main__":
    unittest.main()
