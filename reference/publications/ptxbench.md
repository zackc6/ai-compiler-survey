# PTXBench: Architecture-Specific PTX Kernel Evaluation

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Research authors |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2608.17379) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Evaluates model-written architecture-specific PTX on NVIDIA H100/B200 in GEMM and attention workloads, including correctness, execution of requested hardware instructions and runtime versus expert libraries. Reports no tested model consistently matching expert libraries across the suite.

## Summary

PTX syntax, correct execution, and competitive performance are different achievements; direct code generation can underperform.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Read beside [AI as a Compiler](ai-as-compiler.md) as contrary evidence with a different benchmark protocol.

## Limits / caveats

Different task sets, reference libraries and models prevent a direct headline-speed comparison. A study snapshot is not a permanent upper bound.
