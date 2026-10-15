# D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Alibaba Group · Hong Kong University of Science and Technology · University of Science and Technology of China |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2610.03226](https://arxiv.org/abs/2610.03226) |
| **Evidence tier** | **A** — separates design discovery from implementation as the source of the remaining agent gap |
| **Version / reviewed** | v1, 2 October 2026; reviewed 15 October 2026 |

## Key contributions

A diagnostic benchmark of 26 tasks and 85 workloads on NVIDIA B200 (eight GPUs, NVLink). Expert guidance is organized in three levels—algorithmic insight, dataflow design, low-level tricks—with dependencies. Paired runs with and without guidance share task descriptions, workloads, tools, hardware, and a 350-turn budget. Two assessments by an LLM judge examine independently proposed designs and whether the design properties actually appear in the generated code. Five agents: GPT-6 Astra, Claude Opus 4.8, GPT-5.6 Sol, GLM-5.3, Kimi K3.

## Summary

With guidance, correctness rises from 93.1% to 98.5% across 130 model-task pairs; the performance score across all 26 tasks rises from 1.46 to 1.95; for the three frontier models correct on every task in both runs, geometric-mean speedup rises from **1.69× to 2.49×**; the mean implementation score rises from 57 to 70 of 100. Even with guidance, agents "still leave assessed design properties unimplemented."

## Key takeaways

- A large share of the remaining gap is design discovery, not implementation skill. Supplying the design closes much of it; the rest is implementation.
- Guidance raised estimated API cost for Claude Opus 4.8 by about 29.9%, mostly cached input tokens.
- The judge scores describe design quality and completeness, not speedup; alignment with measured performance is approximate and shown only in aggregate.

## Why it matters for this survey

This bears on the controller checkpoint. Knowledge supplied to the controller (here, expert designs) changes outcomes far more consistently than the knowledge the agent distills itself ([MetaKernelBench](metakernelbench.md), −19% to +29% with frequent regressions). The checkpoint should therefore separate a design-knowledge arm from a procedure-change arm, or a reference-library win could be mis-scored as controller improvement. It also supports the TIRx Harness choice of a concrete kernel zoo over agent-written summaries.

## Limits / caveats

- One hardware platform; the speedup comparison covers only the three models that succeeded on every task.
- An LLM judge (Qwen3.8-Max) scores design and implementation; the SOL score is withheld because algorithmic changes can exceed the analytical bound.
- Expert guidance is hand-written for each task; the cost of producing it is outside the budget.
