# KernelOPT: Dispatch-Aware Agentic Search for GPU Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Red Hat (PyTorch team; four authors as interns) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2609.30059](https://arxiv.org/abs/2609.30059) |
| **Evidence tier** | **A** — integration-aware optimization of compiled models with fallbacks counted in the headline |
| **Version / reviewed** | v1 24 September 2026, v2 6 October 2026; reviewed 15 October 2026 |

## Key contributions

Treats a `torch.compile` output as a structured artifact: vendor-library calls (cuBLAS, cuDNN) are kept, and only the generated Triton sub-kernels are rewritten. Acceptance is a four-gate cascade—static validation, multi-seed numerical correctness, model-level verification against a float64 fallback on the re-stitched model, and a performance gate at 1.03×. Candidates that fail keep the `torch.compile` baseline. Search: five iterations, four plans per iteration, up to four executor retries, beam width four, about 20 LLM-driven candidates per problem, with Claude Sonnet 4.6.

## Summary

On 250 KernelBench problems on one NVIDIA H200, geometric-mean speedup over `torch.compile` **including fallbacks**: 1.40× (Level 1, 100 problems), 1.15× (Level 2, 100), 1.07× (Level 3, 50). Over optimized problems only: 2.54× (36 of 100), 1.84× (23 of 100), 1.37× (11 of 50). Against eager: 1.72×, 1.79×, 1.56×. Of 250 problems, 70 were optimized, 95 matched the baseline, and 85 fell back.

## Key takeaways

- Reporting the fallback-inclusive geometric mean is the honest denominator for an integrated optimizer; the optimized-only figures are what most kernel papers report.
- Total compute about 1,100 GPU-hours (Level 1 about 145 h on one GPU; Level 2 about 210 h on two; Level 3 about 730 h on up to eight). Monetary cost not reported.
- The largest single end-to-end gain is 88.63× on one Level 1 problem; such outliers dominate arithmetic means, which is why the geometric mean matters.

## Why it matters for this survey

A measured example of the recommended integration pattern: preserve what the compiler and libraries already do well, optimize the residual, and count the whole workload. The coverage result (70 of 250 improved) is as informative as the speedup. Compare with [KernelBench-Verified](kernelbench-verified.md) on baseline strength and with [KernelEvolve](kernelevolve.md) on production integration.

## Limits / caveats

- KernelBench problems, not production serving; no application A/B.
- One GPU, one model; the 1.03× gate and the float64 fallback define what "correct" and "better" mean here.
- Search cost per accepted kernel is high relative to the per-kernel gains at Levels 2–3; reuse must justify it.
