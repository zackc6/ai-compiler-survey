"""Regressions for the controller-improvement miss (maintainer, 25 November 2026): a 2026
recursive-self-improvement reading list (Harness-Delta Attribution, The Winner's Curse in LLM
Self-Improvement Loops, Who Grades the Grader?, Exo, Harness Evolution Hits a Ceiling, Trusting
Trust Revisited) was missed. Ledger check (25 November 2026, main and the ten unmerged discovery
branches): The Last AI Built by Humans reached ledgers but was excluded (a triage-policy error);
Singularity-Bench was listed but never triaged; Exo, Winner's Curse and Spotify appear only in
the discovery-2026-11-24-test-34 test ledger via GEPA cited-by; the other five never surfaced.
These tests cover the retrieval causes only, one test each; a mocked seed test is not live recovery:
1. cites seeded only Tier A digests, and every Controller-improvement digest is Tier B;
2. arXiv admitted a paper only with a compiler (CORE) term, and listed no cs.AI;
3. venue titles needed a CORE term."""
import datetime
import json
import pathlib
import tempfile
import unittest
from unittest import mock

import discover as d


def _digest(tmp, stem, tier, group, aid):
    (tmp / f"{stem}.md").write_text(
        f"# {stem} title\n\n| Field | Value |\n|---|---|\n| **Type** | paper |\n| **Group** | {group} |\n"
        f"| **Link** | [Primary source](https://arxiv.org/abs/{aid}) |\n| **Evidence tier** | {tier} |\n",
        encoding="utf-8")


class CitesSeedRoles(unittest.TestCase):
    def _run(self, max_seeds=100, extra=()):
        tmp = pathlib.Path(tempfile.mkdtemp())
        _digest(tmp, "kernel-a", "A: kernel evidence", "Kernel generation", "2601.00001")
        for args in extra:
            _digest(tmp, *args)
        _digest(tmp, "meta-harness", "B: controller-code search", "Controller improvement", "2603.28052")
        _digest(tmp, "other-b", "B: infrastructure", "Languages & interfaces", "2601.00003")
        asked = []

        def fake_get(url, timeout=0, retries=0):
            if "filter=doi:" in url:
                asked.append(url)
                ids = [x.split("arxiv.")[1] for x in url.split("filter=doi:")[1].split("&")[0].split("|")]
                return json.dumps({"results": [{"id": f"https://openalex.org/W{a}", "title": a,
                                                "doi": f"https://doi.org/10.48550/arxiv.{a}"} for a in ids]}).encode()
            if "cites:W2603.28052" in url:
                return json.dumps({"meta": {"count": 1}, "results": [
                    {"id": "W9", "title": "Harness-Delta Attribution: Dissecting Gains from Harness Evolution",
                     "publication_date": "2026-10-15"}]}).encode()
            return json.dumps({"meta": {"count": 0}, "results": []}).encode()

        d.CITES_INCOMPLETE.clear()
        with mock.patch.object(d, "PUBS", tmp), mock.patch.object(d, "get", fake_get), \
                mock.patch.object(d.time, "sleep", lambda s: None), mock.patch.dict(d.OA, {"breaker": ""}):
            out = d.cited_by_candidates({}, datetime.date.today(), max_seeds=max_seeds)
        return out, asked

    def test_controller_group_tier_b_digest_seeds_cites(self):
        out, asked = self._run()
        self.assertIn("2603.28052", asked[0], "a Tier B Controller-improvement digest must be a cites seed")
        self.assertNotIn("2601.00003", asked[0], "a Tier B digest outside SEED_GROUPS stays out")
        self.assertTrue(any("Harness-Delta" in c["title"] for c in out))

    def test_seed_cap_keeps_tier_a_first_and_reports_the_cut(self):
        _, asked = self._run(max_seeds=1)
        self.assertIn("2601.00001", asked[0])
        self.assertNotIn("2603.28052", asked[0])
        self.assertEqual(d.CITES_INCOMPLETE, ["seed cap 1 dropped 1 seeds"])

    def test_shared_id_takes_tier_a_priority_when_group_digest_sorts_first(self):
        # ChatGPT/Codex round 2: "n-group" sorts before "zzz-tier-a" and carries the same arXiv ID; it
        # also sorts after "meta-harness", so filename-order claiming would rank it behind that group seed
        # and the cap of 2 would drop it. The ID must be a Tier A seed: the cap keeps it and drops meta-harness.
        extra = [("n-group", "B: controller", "Controller improvement", "2605.00005"),
                 ("zzz-tier-a", "A: decision evidence", "Kernel generation", "2605.00005")]
        _, asked = self._run(max_seeds=2, extra=extra)
        self.assertIn("2601.00001", asked[0])
        self.assertIn("2605.00005", asked[0])
        self.assertNotIn("2603.28052", asked[0])
        self.assertEqual(d.CITES_INCOMPLETE, ["seed cap 2 dropped 1 seeds"])


class ControllerLaneAdmission(unittest.TestCase):
    FEED = ('<feed xmlns="http://www.w3.org/2005/Atom">'
            '<entry><published>2026-11-20T00:00:00Z</published>'
            '<title>Harness-Delta Attribution: Dissecting Gains from Harness Evolution</title>'
            '<summary>Harness evolution improves agent systems around a fixed-weight model.</summary>'
            '<id>http://arxiv.org/abs/2610.22466v1</id></entry>'
            '<entry><published>2026-11-20T00:00:00Z</published>'
            '<title>A Survey of Protein Folding</title><summary>proteins and benchmarks</summary>'
            '<id>http://arxiv.org/abs/2611.99999v1</id></entry>'
            '<entry><published>2026-10-01T00:00:00Z</published><title>Old</title><summary>x</summary>'
            '<id>http://arxiv.org/abs/2610.00001v1</id></entry></feed>').encode()

    def test_arxiv_admits_controller_title_without_compiler_term(self):
        d.ARXIV_INCOMPLETE.clear()
        with mock.patch.object(d, "get", lambda u, timeout=0, retries=0: self.FEED), \
                mock.patch.object(d, "ARXIV_CATS", ["cs.AI"]), mock.patch.object(d.time, "sleep", lambda s: None):
            rows = d.arxiv_candidates(d.dt.date(2026, 11, 3), max_per_cat=100)
        self.assertEqual([r["id"] for r in rows], ["2610.22466v1"])
        self.assertTrue(rows[0]["why"].startswith("controller lane: "))

    def test_cs_ai_is_listed(self):
        self.assertIn("cs.AI", d.ARXIV_CATS)

    def test_controller_terms_cover_the_missed_titles(self):
        for t in ("Harness-Delta Attribution: Dissecting Gains from Harness Evolution",
                  "The Winner's Curse in LLM Self-Improvement Loops",
                  "Who Grades the Grader? Co-Evolving Evaluation Metrics and Skills for Self-Improving LLM Agents",
                  "Exo: An Architecture for Self-Improving Systems at Runtime",
                  "Harness Evolution Hits a Ceiling: When Weight Training Should Begin",
                  "Reflections on Trusting Trust, Revisited: Contaminating Self-Modifying AI Coding Agents",
                  "SEAGym: An Evaluation Environment for Self-Evolving LLM Agents"):
            self.assertTrue(d.controller_hit(t), t)
        self.assertFalse(d.controller_hit("A Survey of Protein Folding"))

    def test_known_positives_include_the_rsi_regression(self):
        titles = [t for t, _ in d.KNOWN_POSITIVES]
        self.assertTrue(any(t.startswith("Harness-Delta Attribution") for t in titles))
        self.assertTrue(any(t.startswith("The Winner's Curse") for t in titles))


if __name__ == "__main__":
    unittest.main()
