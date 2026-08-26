# TIRx: An Open Compiler Stack for Evolving Frontier ML Kernels

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Apache TVM · MLC (CMU course) |
| **Publisher** | Apache TVM blog |
| **Type** | company |
| **Group** | Classic DL compilers |
| **Link** | [https://tvm.apache.org/2026/06/22/tirx](https://tvm.apache.org/2026/06/22/tirx) |
| **Evidence tier** | **B** — TVM kernel IR designed as an agent-visible mutation surface; library-class B200 numbers are expert-authored, not a public agent loop |

## Key contributions

- **TIRx** (“tier-ex”, Tensor IR next): hardware-native kernel DSL + compiler on Apache TVM. Orchestration (pipeline, sync, roles, intrinsics) stays in source; **execution scope**, **tensor layout** (storage contract, not CuTe-style work partitioning), and **tile primitive dispatch** expose recurring tile ops to the compiler.
- **Agent-visible infrastructure:** IR + utilities over **TVM FFI** (Python / C++ / Rust) so agents can construct, inspect, visit, mutate, and analyze without a compiler rebuild.
- **Dense pre-benchmark feedback:** well-formedness, synchronization validity, race-freedom, value simulation — compiler-mediated search, not compile-then-bench as the only reward.
- **Agent-search rungs** (TIRx docs say L1–L4; **not** this survey’s data-plane L1–L7): local tune of expert kernels → sample a human search space → agents edit the space from meta-rules → (goal) bootstrap spaces from docs + compiler feedback. TIRx targets the **middle** of that spectrum.
- New hardware enters as **intrinsics first**, then promoted tile primitives. Positions itself *below* TileLang (layout inference / thread binding stay out of core); Event Tensor (MLSys 2026) is a megakernel compiler *above* TIRx, not TIRx itself.
- Expert kernels on NVIDIA B200 (54 configs): dense/block-scaled GEMM and FA4 typically **~0.95–1.00×** the best of cuBLAS / DeepGEMM / FlashInfer / CuTeDSL FA4 on reported shapes.

## Summary

June 2026 TVM launch of the next kernel-level structure after TensorIR/MetaSchedule: a lower, more explicit boundary than Triton, with a typed tile surface the compiler can check before hardware time. The agent story is **toolability + structured search**, not a published generate–eval product loop. Peak numbers are expert TIRx vs libraries — **C2**-class, family-selected, not serving A/B.

## Key takeaways

- Fits **typed agent-facing IR** (T1) at **L4 kernel DSL**, sibling of Triton / Tile / CuTe / Cake / Argus — **not** a new data-plane band and **not** an L-llm.
- Pre-benchmark static/sim checks are T2-color admit *signals*; they do not replace serving oracles (T6).
- Another L4 surface (**C4**): TVM-side Cake analog (FFI + primitives) without Cake’s matched agent-vs-CUDA/PTX study.
- Do not read TIRx’s search rungs as this survey’s L1–L7 inventory.

## Why it matters for this survey

Tier B substrate for **T1/T2** and **C3-B/C4**. Completes the LLM-oriented IR fold on the TVM kernel path (TensorIR → TIRx). Hybrid lean holds: agents mutate a typed surface; `tir_pipeline="tirx"` still lowers classically to CUDA C++/PTX. Cite with [Cake](cake.md), [Argus](argus.md), [LLM4IR](llm4ir.md) (dump ≠ face), [Helion](helion-blog.md) (higher Triton surface).

## Limits / caveats

- Launch blog + docs + [`mlc-ai/tirx-kernels`](https://github.com/mlc-ai/tirx-kernels); no public agent-loop p50/p90.
- Blackwell-centric reported kernels; megakernel/Event Tensor integration is follow-up.
- Layout algebra vs Cake: TIRx layout is a **storage** contract consumed by dispatch; Cake IR has **no** layout algebra — competing L4 designs, not one LLM IR.
