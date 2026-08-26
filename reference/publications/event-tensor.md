# Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Carnegie Mellon University · NVIDIA et al. |
| **Publisher** | MLSys 2026 · arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2604.13327](https://arxiv.org/abs/2604.13327) |
| **Evidence tier** | **B** — megakernel *compiler IR* (events-as-tensors) above L4; not an LLM-oriented IR and not a new L-band |

## Key contributions

- **Event Tensor:** first-class tensor of SM-granularity completion events (`notify` / `wait`) with **symbolic shapes** and data-dependent index maps (MoE routing via `topk` / `exp_indptr`).
- **Event Tensor Compiler (ETC):** static scheduling (pre-assigned SM queues) vs dynamic on-GPU ready queues; lowers events to integer tensors + atomics; AOT for dynamic shapes (no CUDA Graph recapture).
- Language: device functions (tile tasks) + graph functions (`call_device` + in/out event edges). Authors: incorporated into a major open-source system.
- Author-reported vs vLLM/SGLang-class baselines (already CUDA Graphs / PDL / `torch.compile`): up to **1.40×** fused GEMM+Reduce-Scatter; **1.23×** on MoE vs specialized libs; **~3.5×** lower engine warmup in dynamic-shape low-batch; matches or exceeds those engines on reported decode shapes.
- [TIRx](tirx.md) positions Event Tensor as a megakernel compiler **above** TIRx, not TIRx itself.

## Summary

Sense-B adjacent (IR for compiling LLM *inference*), not sense-A LLM-oriented IR. The miss was still real: a 2026 MLSys compiler IR that TIRx’s own launch cited, with no digest. Slot it as **L6 fusion / persistent-kernel** machinery sitting *on* L4 tile tasks — dynamism and inter-kernel overlap, not a typed agent mutation surface.

## Key takeaways

- **Not** a new survey L-band and **not** T1 Cake/Argus/TIRx. Events-as-tensors are a *runtime/serving* IR for megakernels.
- Strengthens L6 (CUDA Graphs vs persistent fusion) without moving the hybrid lean: ETC still compiles classically.
- Warmup/AOT vs Graph recapture is a serving-ops point (P18/P23), not an agent-loop settlement (**C2**).

## Why it matters for this survey

Tier B for **L6** / Trend D serving kernels. Cite with [TIRx](tirx.md) (below), vLLM/SGLang as baselines in the paper, not as this survey’s own SKUs.

## Limits / caveats

- Speedups are author-reported vs strong but selected serving configs — **C2**, do not average into “agents beat libraries.”
- “Major open-source system” is unnamed in the abstract; do not invent the product name.
- Device functions may use warp specialization / tensor cores — that is L4 *inside* the megakernel, not Event Tensor replacing Triton.
