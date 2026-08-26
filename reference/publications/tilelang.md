# TileLang: A Composable Tiled Programming Model for AI Systems

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | Peking University · Microsoft Research · Imperial College London |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [https://arxiv.org/abs/2504.17577](https://arxiv.org/abs/2504.17577) |
| **Evidence tier** | **B** — TVM-based tile DSL + layout inference; LSP is T1-adjacent; peak numbers are expert kernels, not a public agent loop |

## Key contributions

- Pythonic **tile DSL** on TVM: dataflow operators (`T.copy`, `T.gemm`, `T.reduce`, …) decoupled from schedule knobs (thread binding, layout, tensorize, pipeline).
- **Layout inference** auto-completes thread–data mapping; experts can still override. Compiler lowers to CUDA / HIP / Metal / LLVM.
- **[TileLang LSP](https://github.com/tile-ai/tilelang-lsp)** (2026-08-04): inlay hints for buffer shapes, dtypes, scopes, and **inferred layouts**, plus hover and diagnostics — agent- and IDE-visible face of the same IR.
- Sits **above [TIRx](tirx.md)** in the TVM stack (TileLang does layout inference / thread binding; TIRx is the storage-layout + tile-primitive layer). GEAK MLA replaced a TileLang SGLang baseline with Triton ([digest](geak-mla-rocm-blog.md)).
- Author-reported: GEMM tracks vendor libs (~0.97–1.10× on A100/H100/MI300X/RTX 4090); MHA 1.36× vs FlashAttention-3 on reported H100 shapes; MLA ~98% of FlashMLA / ~95% of AITER with ~70 Python LoC.

## Summary

TileLang is the production-facing TVM tile language: users write dataflow; the compiler infers layouts and pipelines unless overridden. That is the same *class* of miss as TIRx — a kernel IR launched as docs/code, not an arXiv paper titled “LLM + IR.” The 2026 LSP makes inferred layouts a typed, inspectable surface (T1 color) without claiming a generate–eval product loop.

## Key takeaways

- **L4** TVM-family face, sibling of Triton / Helion / CuTe / Cake — **not** a new data-plane band and **not** an L-llm.
- Layout inference vs TIRx storage layout vs Cake (no layout algebra) vs Argus (layout algebra + SMT) = competing **C4** designs.
- LSP inlay hints are T1-adjacent *tooling*, not Cake-class co-designed agent IR.

## Why it matters for this survey

Tier B substrate for **T1/C4**. Completes the TVM kernel path the TensorIR-2022 freeze missed (TensorIR → TileLang → TIRx). Cite with [TIRx](tirx.md), [Helion](helion-blog.md), [Argus](argus.md), [GEAK MLA](geak-mla-rocm-blog.md).

## Limits / caveats

- Paper + [`tile-ai/tilelang`](https://github.com/tile-ai/tilelang); no public agent-loop p50/p90.
- Headline vs-Torch MLA speedups are vs eager, not vs serving defaults — **C2**-class, family-selected.
- Code has migrated IR usage toward TVM TIRX; treat TileLang and TIRx as stacked, not aliases.
