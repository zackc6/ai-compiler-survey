#!/usr/bin/env python3
"""Network-free regression for low-popularity HN direction posts.

Run: python3 -m unittest test_discover_hn_recall (from scripts/) or
python3 scripts/test_discover_hn_recall.py (from repository root).
"""
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discover  # noqa: E402


class HNRecallTests(unittest.TestCase):
    def test_date_filter_does_not_require_points(self):
        self.assertIsNone(discover.HN_MIN_POINTS)
        self.assertEqual(discover.hn_numeric_filters(123), "created_at_i>123")
        self.assertEqual(discover.hn_numeric_filters(123, 5),
                         "created_at_i>123,points>5")

    def test_single_vote_architecture_story_is_kept(self):
        # An otherwise relevant primary-source direction link must not be
        # suppressed merely because its HN submission has one point.
        story = {
            "title": "Building a Rust-Native, Cross-Language Foundation for Agentic ML Compilers",
            "url": "https://tvm.apache.org/2026/11/16/rust-native-cross-language-ml-compiler-foundation",
            "objectID": "50528233",
            "created_at": "2026-11-19T00:00:00Z",
            "num_comments": 0,
            "points": 1,
        }
        seen = []

        def fake_get(url, *args, **kwargs):
            seen.append(url)
            self.assertIn("created_at_i>", url)
            self.assertNotIn("points>", url)
            return json.dumps({"nbPages": 1, "hits": [story]}).encode()

        with mock.patch.object(discover, "load_feeds", return_value=[]), \
             mock.patch.object(discover, "get", side_effect=fake_get), \
             mock.patch.object(discover, "HN_QUERIES", ["compiler"]), \
             mock.patch.object(discover, "HN_MAX_PAGES", 1), \
             mock.patch.object(discover.time, "sleep"):
            leads = discover.blog_candidates(__import__("datetime").date(2026, 11, 17))
        self.assertEqual(len(seen), 1)
        self.assertEqual(len(leads), 1)
        self.assertIn("50528233", leads[0]["why"])
        self.assertEqual(leads[0]["channel"], "blog")
        self.assertEqual(leads[0]["date"], "2026-11-19")


if __name__ == "__main__":
    unittest.main()
