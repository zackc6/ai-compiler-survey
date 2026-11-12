"""Network-free regression tests for known-repository event discovery."""
import datetime as dt
import unittest

from scripts import discover as d


class IndexedRepoEventTests(unittest.TestCase):
    def setUp(self):
        d.DIAG.clear()
        self.start = dt.date(2026, 11, 9)

    def test_indexed_identity_not_suppressed_by_title_or_stars(self):
        def fake(url):
            self.assertIn("apache/tvm-tirx", url)
            return [{"sha": "abc1234", "commit": {
                "message": "docs(spec): clarify IR ownership",
                "committer": {"date": "2026-11-11T00:00:00Z"}}}]
        rows = d.indexed_repo_event_candidates(
            {"github": {"apache/tvm-tirx"}}, self.start, fetch_json=fake)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel"], "repoevent")
        self.assertIn("abc1234", rows[0]["id"])
        self.assertIn("docs(spec)", rows[0]["title"])

    def test_priority_history_keeps_more_than_eight_events(self):
        commits = [{"sha": f"commit-{i}", "commit": {
            "message": "fix", "committer": {"date": "2026-11-10"}}}
            for i in range(12)]
        requested = []
        def fake(url):
            requested.append(url)
            return [] if "/releases?" in url else commits
        rows = d.indexed_repo_event_candidates(
            {"github": {"apache/tvm-tirx", "other/compiler"}}, self.start,
            fetch_json=fake)
        priority_rows = [r for r in rows if "apache/tvm-tirx@" in r["id"]]
        ordinary_rows = [r for r in rows if "other/compiler@" in r["id"]]
        self.assertEqual(len(priority_rows), 12)
        self.assertEqual(len(ordinary_rows), 8)
        self.assertTrue(any("per_page=51" in u for u in requested))
        self.assertTrue(any("repoevent truncated: other/compiler:" in x for x in d.DIAG))
        self.assertFalse(any("repoevent truncated: apache/tvm-tirx:" in x for x in d.DIAG))

    def test_truncated_commit_history_is_visible(self):
        commits = [{"sha": c, "commit": {
            "message": "fix", "committer": {"date": "2026-11-10"}}}
            for c in ("a", "b")]
        rows = d.indexed_repo_event_candidates(
            {"github": {"other/compiler"}}, self.start, max_events=1,
            fetch_json=lambda _: commits)
        self.assertEqual(len(rows), 1)
        self.assertTrue(any("repoevent truncated:" in x for x in d.DIAG))

    def test_failure_is_not_reported_as_no_updates(self):
        def fail(_url):
            raise ConnectionError("inaccessible")
        rows = d.indexed_repo_event_candidates(
            {"github": {"tile-ai/tilelang"}}, self.start, fetch_json=fail)
        self.assertEqual(rows, [])
        self.assertTrue(any("repoevent failed:" in x for x in d.DIAG))

    def test_priority_and_skipped_repositories_recorded(self):
        called = []
        d.indexed_repo_event_candidates(
            {"github": {"other/old", "tile-ai/tilelang", "apache/tvm-tirx"}},
            self.start, max_repos=2, fetch_json=lambda url: called.append(url) or [])
        commit_urls = [u for u in called if "/commits?" in u]
        self.assertIn("apache/tvm-tirx", commit_urls[0])
        self.assertIn("tile-ai/tilelang", commit_urls[1])
        self.assertTrue(any("unvisited include" in x for x in d.DIAG))

    def test_release_is_found_without_new_commit(self):
        def fake(url):
            if "/commits?" in url:
                return []
            self.assertIn("/releases?", url)
            return [{"tag_name": "v0.1.0", "published_at": "2026-11-11T12:00:00Z",
                     "html_url": "https://github.com/apache/tvm-tirx/releases/tag/v0.1.0"}]
        rows = d.indexed_repo_event_candidates(
            {"github": {"apache/tvm-tirx"}}, self.start, fetch_json=fake)
        self.assertEqual(len(rows), 1)
        self.assertIn("release:v0.1.0", rows[0]["id"])

    def test_non_release_objects_not_mislabeled_as_source(self):
        def fake(url):
            if "/releases?" in url:
                return []
            return [{"sha": "abc", "commit": {
                "message": "feat: add dynamic IR op", "committer": {"date": "2026-11-11"}}}]
        rows = d.indexed_repo_event_candidates(
            {"github": {"apache/tvm-tirx"}}, self.start, fetch_json=fake)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["channel"], "repoevent")


if __name__ == "__main__":
    unittest.main()
