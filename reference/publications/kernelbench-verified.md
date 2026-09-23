# KernelBench-Verified: Do LLM-Generated Kernels Actually Beat PyTorch?

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Meta · Stanford University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2607.16241v1) |
| **Evidence tier** | **A** — relevance to the guide’s design choices, not a quality rating |
| **Version / reviewed** | Version 1 (26 June 2026); reviewed 2026-09-23 |

## Key contributions

Extends the [KernelBench](kernelbench.md) protocol without regenerating kernels: a PyTorch baseline with TF32 Tensor Core matrix multiplication enabled, a hidden correctness gate over four input transformations (original, ×3, ×0.01, negated), and peak-memory measurement. Excludes three Level 2 problems whose reference output is always zero.

## Summary

Seven frontier models generated single-turn CUDA kernels (best of five) for 247 KernelBench problems on one H200, evaluated in FP32 with tolerance 10⁻³. Under the full protocol the best model’s geometric-mean speedup over correct problems is 0.88, against 1.43 under the standard protocol; no model reaches 1.0 at any difficulty level. Correctness stays high (up to 99%), and the best model is faster than the baseline on 32–65% of problems, depending on level. Among the best model’s correct kernels, 28% raise peak memory.

## Key takeaways

The baseline correction explains most of the drop on fused and full-model problems (Level 2: 1.67 to 0.88 for the best model); hidden tests matter more on single operators (Level 1: 1.37 to 1.17), where negated inputs expose shortcuts that assume positive values. In BF16, where the baseline already uses Tensor Cores, the best model reaches 1.63 at Level 2, so the FP32 result is largely a baseline effect rather than a general inability to beat PyTorch. Correctness and speed are largely decoupled.

## Why it matters for this survey

Shows how much a kernel speedup depends on the baseline’s precision mode and on correctness tests the generator cannot anticipate. Complements [KernelBench-X](kernelbench-x.md) and the [kernel-headroom study](kernel-headroom.md): all three narrow what a benchmark speedup establishes. Shares authorship with the original KernelBench, so it is a refinement within that evidence family, not independent corroboration. [Code](https://github.com/facebookresearch/kernel_bench_verified) supports further checking.

## Limits / caveats

- Single-turn generation without compiler or profiler feedback; agentic and multi-turn methods are not evaluated.
- One H200, inference only. The TF32 baseline also changes baseline numerics, and it penalizes kernels that delegate to cuBLAS, which the authors acknowledge.
- The four hidden transformations are fixed and could be anticipated. The reward-hacking audit uses two language models as judges, with manual review of only the six kernels both flagged.
- Speedups are geometric means over each model’s correctly solved problems, so the denominator differs between models. Kernel speed only; no application measurement.
