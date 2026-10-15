# MetaKernelBench: Measuring GPU Kernel Knowledge Transfer Beyond Code

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Westlake University · Shanghai Jiao Tong University · Zhejiang University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2610.05014](https://arxiv.org/abs/2610.05014) |
| **Evidence tier** | **A** — controlled test of whether distilled optimization knowledge transfers across kernel languages; negative transfer measured |
| **Version / reviewed** | v1, 4 October 2026; reviewed 15 October 2026 |

## Key contributions

74 fused-subgraph problems in six families, each posed as a CuTe DSL variant and a [TIRx](tirx.md) variant. During a solo attempt the agent maintains a natural-language skill file (evidence-backed findings, work partitioning, failure reasons, applicability conditions, open questions; no code or commands). That file is passed verbatim to a fresh attempt in the other language, whether or not the source attempt passed. Each attempt has a 40-minute wall-clock limit and at most 10 feedback submissions; development sandboxes are CPU-only, and grading runs on one NVIDIA B200.

## Summary

Across six models (DeepSeek-V4-Pro, GLM-5.3, GLM-5.3-Flash, Gemini 3.7 Flash, GPT-5.6 Sol, Qwen3.8-Flash) and both directions, paired lift over solo attempts ranges from **−19% to +29%**. Four models improve in both directions, but **regressions occur on 16.2–44.6% of problems in every model and direction**.

## Key takeaways

- Transferred knowledge helps on average for most models and hurts on a large minority of problems for all of them; a transfer mechanism needs a rejection path, not just an inclusion path.
- Matched per-attempt budgets do not equalize total computation: producing the skill costs a full source attempt.
- Monetary and token costs are not reported.

## Why it matters for this survey

The closest public experiment to the memory-only arm of the controller checkpoint: knowledge, not procedure, changes, and the effect is measured on paired fresh attempts. It separates retained examples, memory adaptation, skill instructions, learned policies, and procedure changes—none is automatically beneficial. Read with [D2K-Bench](d2k-bench.md), where supplied expert design guidance raises results much more consistently, and with the TIRx Harness finding that concrete reference kernels beat agent-written summaries. Lineage: built on TIRx and evaluated with the same community's tooling; the authors are a separate group.

## Limits / caveats

- Same-problem transfer between two languages on one GPU; cross-problem and cross-hardware transfer are not tested.
- Agent framework and prompts are fixed; results may differ with other skill formats.
- Six models at one point in time; the regression rate may change with model capability.
