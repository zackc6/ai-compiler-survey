# KernelGenBench: Can LLMs and Agents Write Efficient Kernels Across Operator Sources and Hardware Platforms?

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | BAAI · Beijing Normal University · Beijing Jiaotong University · Institute of Automation, CAS · Peking University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2607.27231](https://arxiv.org/abs/2607.27231) |
| **Evidence tier** | **A** — multi-source × multi-chip Triton ladder with token cost; NVIDIA skill does not transfer |

## Key contributions

- One Triton target, two views. **MS:** 210 operators from PyTorch ATen, production vLLM CUDA ops, and cuBLAS. **MC:** a stable 110-operator ATen subset across **six** hardware stacks (NVIDIA, Moore Threads, Hygon, Iluvatar CoreX, and two anonymous platforms).
- Protocol reports correctness, speedup, and **agentic cost**, with a distributed sandbox and layered anti-hack checks. Evaluation spent **>15 billion** tokens. Code: [flagos-ai/KernelGenBench](https://github.com/flagos-ai/KernelGenBench).
- No method dominates. ATen is the easiest source, vLLM the hardest to get right, cuBLAS the highest performance ceiling. **AutoKernel** accuracy falls from **87%** on NVIDIA to **25%** on Iluvatar CoreX.
- Specialized agents average **4.99 million** tokens per successful operator (**6.25 million** for a CUDA Optimized Skill).

## Summary

A portability and cost bench, not another single-GPU KernelBench clone. Holding the kernel language fixed (Triton) still does not make correctness or speed portable: operator *source* and hardware *stack* are separate axes, and the tokens required to cross them are large enough to matter in a product budget. The paper argues explicitly that a win on a familiar NVIDIA/PyTorch pair is not deployment readiness.

## Key takeaways

- **T8** rung the survey was missing: correctness × speed × **cost-to-compile**, across sources and chips. Still not the full IR → fused region → serving-graph ladder.
- **P23:** multi-million tokens per kept operator falsifies “LLM in the loop on every op” as a default SKU. Freeze the artifact; do not rerun the agent per request.
- **C9** pressure without settlement. Cross-chip *drop* (87% → 25%) is evidence that a second vendor is not a prompt change. It is not a TritorX-class coverage playbook on a new ASIC.
- **C2:** do not average a NVIDIA KernelBench number with a non-NVIDIA number from this suite.

## Why it matters for this survey

★ for **T8** and **P23**. Read next to [JAXBench](jaxbench.md) (TPU, different language) and [AMDKernelVault](amdkernelvault.md) (AMD data, not this six-chip protocol). Posted mid-2026 and missed until the September fold.

## Limits / caveats

- MC uses ATen only; vLLM and cuBLAS were not crossed with all six chips, by design (reference stacks differ).
- Two platforms are anonymous. Reproducibility of the worst-transfer claim depends on the public adapters.
- Triton as the common language *is* the experimental control. It does not show what a native DSL (Pallas, HIP, Tile) would do on the same chips.
