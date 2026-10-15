# KernelOPT: Dispatch-Aware Agentic Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Research authors |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2609.30059) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Preserves cuBLAS/cuDNN vendor-library dispatch while optimizing selected Triton kernels remaining in compiled PyTorch model graphs. Includes static, numerical and model-level acceptance checks and preserves a fallback. Authors report 1.40×/1.15×/1.07× geometric-mean improvements over torch.compile across KernelBench Levels 1–3 with fallback cases included.

## Summary

Performance improvement can come from selecting the addressable generated kernels rather than replacing high-performance library components.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Compare profiler-guided restricted optimization against [AI as a Compiler](ai-as-compiler.md) under shared workloads, budgets and integration tests.

## Limits / caveats

These are benchmark integration results, not serving-production A/B; hardware and baseline dispatch policy affect the gain.
