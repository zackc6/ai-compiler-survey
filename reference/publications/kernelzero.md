# KernelZero: Co-Evolving Proposer and Coder for GPU Kernel Generation

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Research authors |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2609.33074) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Jointly trains a workload Proposer and a CUDA/Triton kernel Coder, progressing to performance objectives after correctness criteria. Reports KernelBench Level 1/2 pass@1 of 75.8%/69.6% for CUDA and 77.2%/72.5% for Triton under its study protocol.

## Summary

Improving the kernel-generation model offline is a separate choice from longer online search or reusable compiler pass generation.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Compare total training resources and held-out performance against fixed-model inference-time search and conventional tuning.

## Limits / caveats

Kernel pass rates do not imply application speedups or recursive compiler-controller self-modification.
