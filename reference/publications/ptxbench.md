# PTXBench: Benchmarking and Adapting LLMs for GPU Kernel Optimization with Architecture-specific PTX

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Stanford University · Carnegie Mellon University · RadixArk · independent researchers |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2608.17379](https://arxiv.org/abs/2608.17379) |
| **Evidence tier** | **A** — the contrary case to direct PTX synthesis: model-written architecture-specific PTX does not consistently match expert libraries |
| **Version / reviewed** | v1 18 August 2026, v3 28 September 2026; reviewed 15 October 2026 |

## Key contributions

A benchmark for GEMM and attention (forward and backward, causal and non-causal) on NVIDIA H100 and B200 that scores three things: functional correctness, whether the requested target PTX instructions actually execute at runtime, and speed against frontier libraries (cuBLAS, cuDNN). Includes supervised fine-tuning of Qwen3.6-27B with repair-conditioned training data.

## Summary

No evaluated model consistently matches the libraries. Best target-instruction-qualified results: GEMM 0.976× of cuBLAS on H100 and **1.012× on B200** (Claude Opus 4.8, the only case above the library); attention forward 0.872× (H100) and 0.536× (B200) of cuDNN; attention backward 0.746× causal on H100 and **0.339–0.372× on B200** (GPT-5.6). Attention backward is the hardest family.

## Key takeaways

- Executing the right instructions does not produce competitive performance; the benchmark measures both and finds them separable.
- Fine-tuning Qwen3.6-27B moved it from no correct GEMM or attention kernels to 0.34× (GEMM) and 0.20–0.57× (attention) on H100, with uneven generalization (no correct kernels on either d96 backward task). Data coverage, balance, and teacher quality mattered alongside size.
- Transfer of the fine-tuned model to Triton raised best speedups on some tasks while lowering turn-level correctness on every workload.

## Why it matters for this survey

The direct counterweight to [AI as a Compiler](ai-as-compiler.md): on a different suite with library baselines rather than Triton, direct PTX generation trails the expert libraries, and most on Blackwell attention. Together they bound the replace-lowering question: synthesis wins where the fixed pipeline hides a feature and the workload is small; it loses against mature libraries on the kernels that dominate transformer runtime. Lineage note: shares a Stanford affiliation with AI as a Compiler and KernelBench, and a Carnegie Mellon author with the TIRx community.

## Limits / caveats

- Two kernel families; the library baselines are the strongest available, which makes the comparison harder than Triton-based ones.
- Results depend on the harness and turn budget (eight turns in the fine-tuning experiments).
- Version 3 is recent; numbers may move with model updates.
