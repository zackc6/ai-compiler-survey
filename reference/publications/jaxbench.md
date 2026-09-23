# JAXBench: Benchmarking Autonomous TPU Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google · Google DeepMind · Harvard University · UC Berkeley |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2607.20466](https://arxiv.org/abs/2607.20466) |
| **Evidence tier** | **A** — TPU-native kernel ladder with hand-tuned Pallas references and a public harness |

## Key contributions

- **50** JAX/TPU workloads: **17** production operators from MaxText (Llama-3.1, DeepSeek-V3, Mixtral, Mamba-2, AlphaFold2, …) and **33** fused sequences adapted from KernelBench. Eight of the 17 ship grid-searched **Pallas** kernels from Tokamax as an expert bound.
- Harness: JIT compile → `np.allclose` → Perfetto/`jax.profiler` timing vs XLA and, when present, the Pallas reference. Code lives next to MaxKernel in [accelerator-agents/JAXBench](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/JAXBench).
- Gemini 3 Flash, full suite: best-of-N **13/50** at **1.01×** geomean; iterative refine **32/50** at **1.18×**. Injecting curated TPU docs lifts iterative refine to **48/50** at **1.28×** and per-sample correctness from **5.8%** to **37.3%**.
- Autocomp (beam search + the same docs) solves **45/50** at **1.36×** geomean, with **76%** of benchmarks beating XLA. On the eight hand-tuned kernels: **1.60×** vs XLA against a **2.08×** Tokamax geomean, trailing paged and ragged attention. A Gemini 3.1 Pro ablation: **49.1%** per-sample correctness and **3.13×** geomean (author).

## Summary

The TPU analogue of KernelBench, released with the same Google kernel-agent effort as [MaxKernel](maxkernel.md). The result that matters for the prediction is not the headline speedup: on a sparsely documented DSL (**Pallas**), **target-specific context** moves correctness more than model scale, and search structure only pays after kernels compile. High-quality TPU kernels remain open — agents recover much of the Tokamax gap and still lose specialized attention.

## Key takeaways

- New **T8** rung: single-kernel / fused-op hillclimb on TPU, with an expert Pallas ceiling. Not a serving-graph ladder and not cost-to-compile as a first-class column (tokens are discussed; the shared protocol is correct × speed).
- Reinforces **C3-B**: the agent should see docs, block specs, and compiler feedback, not a raw XLA dump.
- **C9** unchanged. This is a peak ladder on a mature compiler (XLA), not a coverage-first ASIC backend.
- **C4**: Pallas/Mosaic is now a named agent sink with a public bench. Digest the language, not only the agent.

## Why it matters for this survey

★ for **T8** and the Pallas face of **T1**. Read with MaxKernel (later search on the same 50 tasks) and [KernelGenBench](kernelgenbench.md) (cross-chip Triton, where NVIDIA skill does not transfer).

## Limits / caveats

- One vendor’s accelerator and docs pack. “Docs help” may not copy to a DSL that is already in the pretraining mix (Triton).
- Author baselines; Tokamax block sizes were grid-searched by the benchmark authors.
- Posted before the 2026-08-31 survey fold and missed until MaxKernel cited it (2026-09).
