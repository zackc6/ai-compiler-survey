# GEAK Agent-Driven Optimization of the DeepSeekV4 MLA Kernel

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | AMD ROCm blog |
| **Type** | company |
| **Group** | Commercial products & proposals |
| **Link** | [https://rocm.blogs.amd.com/software-tools-optimization/geak-mla-optimization/README.html](https://rocm.blogs.amd.com/software-tools-optimization/geak-mla-optimization/README.html) |
| **Evidence tier** | **B** — vendor case study (one MLA / one MI355 shape); use with GEAK v4, do not average into C2 |

## Key contributions

- Walks GEAK through PyTorch→Triton migration, profile-localize-optimize, and **SGLang e2e** validation for DeepSeekV4 MLA on AMD Instinct.
- Replaces a TileLang SGLang baseline with an optimized Triton sparse MLA kernel (integration cited as sglang#26208).
- Author-reported on MI355, ISL/OSL=8k/1k, TP=8, concurrency=32: **2.10×** e2e throughput, **3.71×** TTFT vs that baseline.

## Summary

July 2026 ROCm blog that shows the v4-class loop on a flagship serving kernel: not a KernelBench task, but a real MLA path with prefill/decode and an engine integration PR. Mechanism matches [GEAK v4](geak-v4-github.md) (profile → iterate → e2e gate). Numbers are a selected production-like shape, not a distribution.

## Key takeaways

- Confirms GEAK is being pointed at **serving graphs**, not only kernels (**T6** / §5.1.3).
- TileLang → Triton replacement is a **C4** data point (multi-DSL in one product).
- Treat 2.10× / 3.71× as **Claim A** color for C2, not a settlement — no p50/p90, no pinned public trace bundle.

## Why it matters for this survey

Companion to the v4 release. Cite when the narrative needs a concrete e2e figure; keep C2 unresolved. Do not promote to ★.

## Limits / caveats

- Single model / kernel family / HW point; vendor blog.
- Baseline is TileLang-in-SGLang, not a library-peak NVIDIA stack — not a cross-vendor TCO claim.
