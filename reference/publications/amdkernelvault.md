# AMDKernelVault: Large-Scale Datasets and Agentic Training for AMD GPU Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2609.12471](https://arxiv.org/abs/2609.12471) |
| **Evidence tier** | **A** — execution-verified HIP + Triton corpus for CDNA; correctness lead is not a speed lead |

## Key contributions

- Open corpus for recent AMD CDNA GPUs: **62,153** execution-verified HIP samples, **39,893** Triton kernels, and **2,377** production-grounded ROCm Libraries QA entries.
- **HIPKernelGen** and **TritonKernelGen**: agent pipelines that turn PyTorch references into HIP or Triton, compile and validate under ROCm, and latency-profile on AMD hardware.
- Demonstration train: Qwen3-8B with supervised fine-tuning plus execution-aware RL. Under fixed budgets it posts the **highest correctness** among compared models — PyTorch-to-HIP **34.0%** Pass@1, TritonBench-G **33.2%** Corr@3, ROCmBench **41.94%** Corr@3 — and **does not uniformly lead compilation or speed**.
- Posted 2026-09-11. Addresses CUDA-centric kernel agents that depend on repeated frontier-LLM calls.

## Summary

AMD’s answer to KernelBook/TritonRL for its own ISA: generate a large *executed* kernel pile with agents, then distill a small model. The survey-relevant result is the split score. Execution-aware training can win Pass@1 and still lose the race on compile success and latency. That is the same lesson as KernelBench-X (correct ≠ fast), now on HIP and Triton for CDNA, with the generator and the student both in the paper.

## Key takeaways

- **T7** exists-cell grows: open HIP + Triton positives with hardware labels, not only NVIDIA Triton pairs. Versioned negatives (failed compiles, miscompiles, slow-but-correct) are still not the product.
- Does **not** make an 8B model a replacement for GEAK/Hyperloom search. The paper’s own speed column refuses that reading.
- **C4** pressure: two sinks (HIP and Triton) in one corpus. Multi-DSL agents stay necessary on AMD.
- Not job (d) and not C9 settlement. No ASIC coverage playbook.

## Why it matters for this survey

★ for **T7** (AMD multi-language kernel data). Pair with [KernelBook](kernelbook.md) / [TritonRL](tritonrl.md) and with [Hyperloom](hyperloom.md), which still *searches* at serving time rather than trusting a distilled generator.

## Limits / caveats

- “Highest correctness among compared models” is a leaderboard claim inside this paper’s budget. Do not generalize to frontier agents with larger search.
- Corpus construction uses the same agent pipelines that the bench evaluates; contamination and selection bias need the full data card before treating it as ImageNet-for-compilers.
- Primary link is the preprint. Confirm the data URL from the paper before citing a mirror.
