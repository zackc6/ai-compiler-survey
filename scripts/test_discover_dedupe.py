"""Network-free tests for canonical-repository alias resolution and event URL dedupe.

Fixtures follow the 2026-11-15 ledger: the index listed both ``amd-agi/geak`` and
``amd-agi/geak-agent``, GitHub resolves both names to repository id 1028816796
(``AMD-AGI/GEAK``), and the ledger carried the same eight commit URLs twice and two
truncation lines for one repository. The acceptance checks agreed in the Review
thread on 2026-11-15 (ChatGPT 04:47 UTC, Claude 04:51 UTC) are numbered below.
"""
import datetime as dt
import unittest
import urllib.error

from scripts import discover as d

GEAK_ID = 1028816796
GEAK_SHAS = ["9b5c740e7a23daf0ba0f8d2796ffc796abc02628", "04646d32f676dab455d35ed287e203339e7bb268",
             "86f6771b735d3367446d13fad7cff396d712c568", "28d180b7b62637c71fe19cd72fa3fca1a2ec4432",
             "6d387b9411095e5c27c10e381807e9b6fb6cc9b3", "0dd7b3a845829da5d6886cf02483cf990d9e8666",
             "c3c10e6f380fd92456f8eaa4e40a4e65f1306bd0", "db735399bdd7a33c8322ca8b79d48487dd64c2ce"]


def commit(sha, repo="AMD-AGI/GEAK", date="2026-11-14T12:32:46Z", msg="refactor(mega)"):
    return {"sha": sha, "commit": {"message": msg, "committer": {"date": date}},
            "html_url": f"https://github.com/{repo}/commit/{sha}"}


class Router:
    """Answer metadata, commits and releases per repository, recording every URL."""

    def __init__(self, metadata, commits, releases=None, redirect_names=()):
        self.metadata, self.commits, self.releases = metadata, commits, releases or {}
        self.redirect_names = set(redirect_names)
        self.urls = []

    def __call__(self, url):
        self.urls.append(url)
        if url.startswith("https://api.github.com/repositories/"):
            rid = int(url.rsplit("/", 1)[1])
            return next(m for m in self.metadata.values() if m["id"] == rid)
        path = url[len("https://api.github.com/repos/"):]
        if "/commits?" in path:
            return self.commits.get(path.split("/commits?")[0].lower(), [])
        if "/releases?" in path:
            return self.releases.get(path.split("/releases?")[0].lower(), [])
        name = path.lower()
        if name in self.redirect_names:  # GitHub REST: 301 to /repositories/<id>
            raise urllib.error.HTTPError(url, 301, "Moved Permanently",
                                         {"Location": f"https://api.github.com/repositories/{self.metadata[name]['id']}"}, None)
        if name not in self.metadata:
            raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)
        return self.metadata[name]


GEAK_META = {"amd-agi/geak": {"id": GEAK_ID, "full_name": "AMD-AGI/GEAK"},
             "amd-agi/geak-agent": {"id": GEAK_ID, "full_name": "AMD-AGI/GEAK"}}


class CanonicalRepoTests(unittest.TestCase):
    def setUp(self):
        d.DIAG.clear()
        self.start = dt.date(2026, 10, 25)

    # (1) renamed repository: full_name body, and a 301 redirect that urllib would follow
    def test_renamed_alias_resolves_by_body_and_by_redirect(self):
        for redirect in ((), ("amd-agi/geak-agent",)):
            d.DIAG.clear()
            router = Router(GEAK_META, {}, redirect_names=redirect)
            records = d.resolve_canonical_repos(["amd-agi/geak-agent", "amd-agi/geak"], router)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["repo"], "amd-agi/geak")
            self.assertEqual(records[0]["identity"], f"id:{GEAK_ID}")
            self.assertEqual(records[0]["aliases"], ["amd-agi/geak", "amd-agi/geak-agent"])
            self.assertTrue(any(x.startswith("repoevent alias: amd-agi/geak-agent -> amd-agi/geak") for x in d.DIAG))
            self.assertIn("repoevent coverage: 2 indexed names -> 1 resolved canonical repositories + 0 unresolved indexed names", d.DIAG)
            if redirect:
                self.assertTrue(any("/repositories/1028816796" in u for u in router.urls))

    # (5) the eight GEAK duplicates become eight rows, fetched once, with both aliases as provenance
    def test_eight_geak_duplicates_collapse_to_one_fetch(self):
        router = Router(GEAK_META, {"amd-agi/geak": [commit(s) for s in GEAK_SHAS]})
        rows = d.indexed_repo_event_candidates({"github": {"amd-agi/geak", "amd-agi/geak-agent"}},
                                               self.start, fetch_json=router)
        self.assertEqual(len(rows), 8)
        self.assertEqual(sum("/commits?" in u for u in router.urls), 1)
        self.assertEqual({r["id"].split("@")[0] for r in rows}, {"amd-agi/geak"})
        self.assertIn("family amd-agi/geak (indexed as amd-agi/geak, amd-agi/geak-agent)", rows[0]["why"])
        self.assertEqual(len({r["url"] for r in rows}), 8)

    # (5) truncation under aliases: one line per canonical repository, naming the aliases
    def test_truncation_reported_once_per_canonical_repository(self):
        router = Router(GEAK_META, {"amd-agi/geak": [commit(s) for s in GEAK_SHAS] + [commit("f" * 40)]})
        rows = d.indexed_repo_event_candidates({"github": {"amd-agi/geak", "amd-agi/geak-agent"}},
                                               self.start, fetch_json=router)
        self.assertEqual(len(rows), 8)
        truncated = [x for x in d.DIAG if x.startswith("repoevent truncated:")]
        self.assertEqual(truncated, ["repoevent truncated: amd-agi/geak (indexed as amd-agi/geak, "
                                     "amd-agi/geak-agent): first 8 of >8 commits; older updates require review"])

    # (4) a genuine fork has its own id and is never merged with the upstream repository
    def test_fork_with_identical_commits_stays_distinct(self):
        meta = dict(GEAK_META)
        meta["someone/geak"] = {"id": 999, "full_name": "someone/GEAK"}
        shared = commit(GEAK_SHAS[0])
        fork_commit = commit(GEAK_SHAS[0], repo="someone/GEAK")
        router = Router(meta, {"amd-agi/geak": [shared], "someone/geak": [fork_commit]})
        rows = d.indexed_repo_event_candidates({"github": {"amd-agi/geak", "someone/geak"}},
                                               self.start, fetch_json=router)
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(d.dedupe_repo_events(rows)), 2)  # different canonical URLs
        self.assertIn("repoevent coverage: 2 indexed names -> 2 resolved canonical repositories + 0 unresolved indexed names", d.DIAG)

    # (4) a commit and a release of the same repository are different events
    def test_commit_and_release_are_distinct_events(self):
        router = Router(GEAK_META, {"amd-agi/geak": [commit(GEAK_SHAS[0])]},
                        {"amd-agi/geak": [{"tag_name": "v1.0", "published_at": "2026-11-14T00:00:00Z",
                                           "html_url": "https://github.com/AMD-AGI/GEAK/releases/tag/v1.0"}]})
        rows = d.indexed_repo_event_candidates({"github": {"amd-agi/geak"}}, self.start, fetch_json=router)
        self.assertEqual(len(rows), 2)
        self.assertEqual(len(d.dedupe_repo_events(rows)), 2)
        self.assertNotEqual(d.canonical_event_url("https://github.com/AMD-AGI/GEAK/commit/v1.0"),
                            d.canonical_event_url("https://github.com/AMD-AGI/GEAK/releases/tag/v1.0"))

    # (2) metadata failures are visible and the repository is still fetched under its indexed name
    def test_metadata_failure_is_visible_and_repo_not_dropped(self):
        router = Router({}, {"aetherheart-ai/aeloon": [commit("a" * 40, repo="aetherheart-ai/aeloon")]})
        rows = d.indexed_repo_event_candidates({"github": {"aetherheart-ai/aeloon"}}, self.start, fetch_json=router)
        self.assertEqual(len(rows), 1)
        self.assertTrue(any(x.startswith("repoevent metadata failed: aetherheart-ai/aeloon: HTTP Error 404")
                            and "attempted under its indexed name" in x for x in d.DIAG))
        self.assertIn("repoevent coverage: 1 indexed names -> 0 resolved canonical repositories + "
                      "1 unresolved indexed names (aetherheart-ai/aeloon); unresolved names may still alias each other",
                      d.DIAG)

    # (2)/(5) mixed success and failure: unresolved names are counted apart from resolved identities
    def test_mixed_resolution_counts_unresolved_separately(self):
        router = Router(GEAK_META, {"amd-agi/geak": [commit(GEAK_SHAS[0])],
                                    "org/gone": [], "org/gone-mirror": []})
        idx = {"github": {"amd-agi/geak", "amd-agi/geak-agent", "org/gone", "org/gone-mirror"}}
        rows = d.indexed_repo_event_candidates(idx, self.start, fetch_json=router)
        self.assertEqual(len(rows), 1)
        self.assertIn("repoevent coverage: 4 indexed names -> 1 resolved canonical repositories + "
                      "2 unresolved indexed names (org/gone, org/gone-mirror); unresolved names may still alias each other",
                      d.DIAG)
        self.assertEqual(sum(x.startswith("repoevent metadata failed:") for x in d.DIAG), 2)
        # Unresolved names are still attempted, once each, never dropped.
        self.assertEqual(sum("/commits?" in u for u in router.urls), 3)

    # (5) cap-boundary coverage: the slot freed by an alias reaches a repository the alias displaced
    def test_alias_slot_reaches_boundary_repository(self):
        meta = dict(GEAK_META)
        meta["zzz/last"] = {"id": 7, "full_name": "zzz/last"}
        router = Router(meta, {"amd-agi/geak": [commit(GEAK_SHAS[0])],
                               "zzz/last": [commit("b" * 40, repo="zzz/last")]})
        idx = {"github": {"amd-agi/geak", "amd-agi/geak-agent", "zzz/last"}}
        rows = d.indexed_repo_event_candidates(idx, self.start, max_repos=2, fetch_json=router)
        self.assertEqual({r["id"].split("@")[0] for r in rows}, {"amd-agi/geak", "zzz/last"})
        self.assertFalse(any(x.startswith("repoevent truncated: only") for x in d.DIAG))
        # Three names but only two distinct repositories: the old code would have reported
        # "only 2/3 indexed repos checked" and left zzz/last unvisited.

    # (5) cap still binds on distinct repositories and names the unvisited ones
    def test_cap_on_distinct_repositories_is_reported(self):
        meta = {f"org/r{i}": {"id": i, "full_name": f"org/r{i}"} for i in range(4)}
        router = Router(meta, {})
        d.indexed_repo_event_candidates({"github": set(meta)}, self.start, max_repos=2, fetch_json=router)
        line = next(x for x in d.DIAG if x.startswith("repoevent truncated: only"))
        self.assertIn("only 2/4 distinct indexed repos checked (4 indexed names)", line)
        self.assertIn("unvisited include org/r2, org/r3", line)

    # (3) URL dedupe keeps the first row, records the other family, reports counts; deterministic
    def test_url_dedupe_keeps_provenance_and_counts(self):
        rows = [{"channel": "repoevent", "id": f"amd-agi/geak@{s}", "title": "t", "date": "2026-11-14",
                 "url": f"https://github.com/AMD-AGI/GEAK/commit/{s}", "why": "COMMIT; family amd-agi/geak; x"}
                for s in GEAK_SHAS]
        rows += [{"channel": "repoevent", "id": f"amd-agi/geak-agent@{s}", "title": "t", "date": "2026-11-14",
                  "url": f"https://github.com/amd-agi/geak/commit/{s}/?utm=1#diff",
                  "why": "COMMIT; family amd-agi/geak-agent; x"} for s in GEAK_SHAS]
        rows.append({"channel": "repoevent", "id": "amd-agi/geak@" + "c" * 40, "title": "t", "date": "2026-11-13",
                     "url": "https://github.com/AMD-AGI/GEAK/commit/" + "c" * 40, "why": "COMMIT; family amd-agi/geak; x"})
        out = d.dedupe_repo_events(rows)
        self.assertEqual(len(out), 9)
        self.assertEqual([r["id"] for r in out], [r["id"] for r in rows[:8]] + [rows[-1]["id"]])
        self.assertTrue(all("also listed under amd-agi/geak-agent" in r["why"] for r in out[:8]))
        self.assertNotIn("also listed", out[8]["why"])
        self.assertIn("repoevent dedupe: 17 event rows before URL dedupe, 9 after", d.DIAG)
        self.assertEqual(d.dedupe_repo_events(rows), out)

    def test_url_normalization_never_touches_tag_case(self):
        a = d.canonical_event_url("https://GitHub.com/AMD-AGI/GEAK/releases/tag/V1.0/")
        b = d.canonical_event_url("https://github.com/amd-agi/geak/releases/tag/v1.0")
        self.assertEqual(a, "https://github.com/amd-agi/geak/releases/tag/V1.0")
        self.assertNotEqual(a, b)


if __name__ == "__main__":
    unittest.main()
