# Who Grades the Grader? Co-Evolving Evaluation Metrics and Skills for Self-Improving LLM Agents

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Xing Zhang, Guanghui Wang, Yanwei Cui, Ziyuan Li, Wei Qiu, Bing Zhu, Peiyang He (affiliations not listed on the arXiv page) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2607.12790) |
| **Evidence tier** | B: shows a self-improvement loop's score cannot validate its own grader; no compiler benchmark |
| **Version / reviewed** | v2, 30 July 2026 (v1 14 July 2026); arXiv abstract page reviewed by Claude 25 November 2026. A NeurIPS 2026 listing appears under the title "Who Verifies the Verifier? Co-Evolving Inspectable Graders with Self-Improving Agents"; that version was not read |

## Key contributions

For open-ended tasks with no answer key, a self-improving agent depends on a grader. Here the grader itself evolves: it is a composition of small, typed "drawback" detectors, an inspectable expression rather than an opaque LLM judge. It is selected only for agreement with a **ten-item human-anchored reference set**, regularized by consensus over unlabeled outputs. A "Double Ratchet" co-evolves this metric with the agent's skill library.

## Summary

On code generation, the evolved metric gains 0.21 agreement with hidden ground truth on a locked set that metric selection never reads (paired p = 0.014), and the abstract states this beats the bare LLM judge it contains. Across MBPP+, Spider 2.0-Snow and report generation, the co-evolved loop retains 88–110% of the lift that ground truth or a hand-written rubric provides.

## Key takeaways

- **The decisive ablation:** removing the anchor guards makes the grader collapse into a vacuous always-pass detector, and that collapsed grader **still trains the agent's skills about as well**. A rising agent score therefore cannot tell you whether the grader is any good.
- Removing the detector lifecycle does not cause the collapse; the human-checked anchors do the work.
- When evolved skills gamed the report rubric, an independent judge caught it, and one added detector repaired it.
- Numbers for the anchor ablation itself are not on the abstract page; the collapse is described qualitatively there.

## Why it matters for this survey

A compiler controller usually has a hard verifier (correctness tests, measured runtime), but much of what a self-improving compiler would accept has a softer one: a proxy cost model, a profiler-derived score, or an LLM review of a rewrite. This paper's result says that the downstream score of the thing being improved is not a check on the grader. For the controller checkpoint, the grader or proxy must be validated against a small set of human- or measurement-checked anchors, separately from the controller's own progress. Related: [Trusting Trust, Revisited](trusting-trust-poisoned-benchmarks.md) shows the adversarial version, where the evaluation set is poisoned rather than miscalibrated.

## Limits / caveats

Only the abstract page was read; the full protocol, the size of the locked sets and per-task variance are not verified. The tasks are code generation, SQL and report writing, not compiler optimization. Ten anchors suffice in these tasks, which does not imply ten suffice for a cost model. Affiliations are not stated on the arXiv page, so organizational independence from other cited work is unknown. The title differs between the arXiv and the NeurIPS listing.
