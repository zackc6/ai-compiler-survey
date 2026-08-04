# Ansor: Generating High-Performance Tensor Programs for Deep Learning

| Field | Value |
|---|---|
| **Year** | 2020 |
| **Org** | UW · AWS · OctoML et al. |
| **Publisher** | USENIX OSDI 2020 |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [https://www.usenix.org/conference/osdi20/presentation/zheng](https://www.usenix.org/conference/osdi20/presentation/zheng) |

## Key contributions

- Template-free evolutionary auto-scheduling
- Automatic search space construction
- Strong empirical wins vs manual templates

## Summary

Shows that evolutionary search over automatically derived tensor program spaces can outperform template-based AutoTVM-style tuning.

## Key takeaways

- Predecessor to MetaSchedule-era search
- LLM+MCTS papers often compare against this lineage
- Search cost remains a key pain point agents try to cut

## Why it matters for this survey

This source informs the living survey in `docs/SURVEY.md` (trends, agent roles, process reshape, and/or gaps). Prefer the primary link above when citing.
