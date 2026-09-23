# ForgeMegakernel: A General Framework for Efficient Auto-Regressive Model Decode Megakernels

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Tsinghua University · University of Chinese Academy of Sciences · ModelBest |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2609.12379](https://arxiv.org/abs/2609.12379) |
| **Evidence tier** | **A** — coding agents forge decode megakernels under an independent mid-state oracle |

## Key contributions

- Per-model **decode megakernel** built by coding agents. A knowledge base of **ten** milestones fixes structure: a fine-grained instruction stream per SM, dependency counters instead of a global sync, and a shared-memory buffer pool.
- An **independent mid-state test oracle** derives intermediate states and checks performance, error, and precision **during** generation, not only on the final token stream.
- Eval: **14** decode ops, eight model families, 0.6B–13B. Author figures: **50.5–85.9%** memory-bandwidth utilization; geomean **1.21×** vs SGLang 0.5.18 and **1.54×** vs a megakernel compiler under the same config. Inside SGLang on GSM8K with ragged prompts, all 14 decode faster at comparable answer accuracy. Posted 2026-09-11.

## Summary

Event Tensor compiles a megakernel from a structured IR. ForgeMegakernel **generates** a decode megakernel with agents, and uses a mid-state oracle so a wrong fusion cannot hide behind an end-to-end score. The milestones are a typed skeleton (what must be true of the kernel) rather than a free CUDA dump. Classical launch and the serving engine still run the frozen kernel.

## Key takeaways

- **T2 / T6** color: localized correctness during synthesis, then a serving check (GSM8K). Not a multi-month default-path A/B.
- **Names:** ForgeMegakernel ≠ AMD **KernelForge** (a Hyperloom backend) ≠ Michigan **Kernel Forge**. Do not merge the digests.
- Not an L-band. The megakernel sits at L6 (fusion above the tile DSL), same slot as [Event Tensor](event-tensor.md), with an agent on the control plane.
- Hybrid holds. The oracle, not the model, decides whether a milestone is kept.

## Why it matters for this survey

★ for the mid-state admit pattern (**T2**) on memory-bound decode. Pair with Event Tensor (compiler-owned megakernel IR, no LLM loop) so the two mechanisms stay distinct.

## Limits / caveats

- Author speedups on 14 ops through 13B. Not a fleet p50 (**C2**).
- “Guaranteeing” correctness means the oracle’s checks, which are only as strong as the derived mid-states.
- Hardware target is an NVIDIA-class GPU in the SGLang comparison; portability is not the claim.
