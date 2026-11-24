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

    def test_bom_title(self):
        self.assertEqual(d._digest_title("﻿# Ansor: Generating High-Performance Tensor Programs (OSDI 2020)\n"),
                         "Ansor: Generating High-Performance Tensor Programs")


if __name__ == "__main__":
    unittest.main()
