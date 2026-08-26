# ThunderKittens 2.0: Even Faster Kernels for Your GPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Stanford Hazy Research |
| **Publisher** | Hazy Research blog |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://hazyresearch.stanford.edu/blog/2026-02-19-tk-2](https://hazyresearch.stanford.edu/blog/2026-02-19-tk-2) |
| **Evidence tier** | **B** — CUDA-embedded tile DSL; “you (or your agent)” is a packaging claim, not a public agent loop |

## Key contributions

- **ThunderKittens (TK):** CUDA-embedded tile primitives (layouts, TMA, tensor-core wrappers) so kernels stay close to the machine and can drop to raw CUDA/PTX. Original 2024; **2.0** (2026-02) = Blackwell, MXFP8/NVFP4, CLC, tensor memory, simpler per-kernel builds.
- Blog: “much simpler build structure … so **you (or your agent)** can easily adapt” example kernels. Industry forks contributed back; authors cite Cursor Composer training kernels and Together AI inference.
- [TIRx](tirx.md) cites TK in the explicit-tile lineage. Concurrent: **[HipKittens](https://arxiv.org/html/2511.08083v1)** (arXiv:2511.08083) — AMD-side tile primitives (not a separate digest this wave).
- Author-reported B200 GEMM tracks cuBLAS on BF16/MXFP8/NVFP4 in the 2.0 post.

## Summary

TK is a *lower* CUDA DSL, not an LLM-oriented IR. It belongs in the same vendor-DSL search that found TIRx: blogs and GitHub, not arXiv “LLM + compiler.” The agent sentence is an invitation to mutate examples, not Cake-class typed admit.

## Key takeaways

- **L4** CUDA-embedded face (**C4**), sibling of CuTe DSL / TileLang / Gluon — different embedding (C++ in CUDA vs Python DSLs).
- Library-class GEMM is expert TK vs cuBLAS — **C2**, not serving A/B.
- HipKittens = AMD analog; still undigested as its own file (watchlist).

## Why it matters for this survey

Tier B C4 substrate; TIRx/TLX related-work. Cite with [CuTe DSL](cute-dsl.md), [TileLang](tilelang.md), [TIRx](tirx.md).

## Limits / caveats

- 2.0 drops active Ampere support; Hopper/Blackwell-centric.
- No public TK agent-loop p50. “Or your agent” ≠ KernelEvolve-class evidence.
- Do not confuse with Triton, TileLang, or TIRx.
