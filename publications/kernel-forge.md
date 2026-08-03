# Kernel Forge: An Agent Harness for LLM-based Generation and Optimization of CUDA Kernels

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Michigan |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2607.24762](https://arxiv.org/abs/2607.24762) |
| **Evidence tier** | **A** — MCTS harness that rewrites live PyTorch models |

## Key contributions

- Open agent harness: accept any PyTorch model + example inputs; validate vs eager; **auto-integrate** optimized CUDA/Triton-style kernels back into execution.
- Uses **MCTS** over linear refine/beam; GUI+CLI observability.
- Reports speedups on vision/diffusion/LLM kernels (e.g. up to ~2.8× softmax) with 50 iterations/kernel on GB10.

## Summary

Product-shaped harness for the online agentic compiler job: not a standalone KernelBench solver, but a drop-in optimizer for real models. Complements AutoKernel (Amdahl loop) with search-tree exploration and UX.

## Key takeaways

- Integration-back-into-PyTorch is a stack-reshape requirement (artifacts must be loadable, not gist dumps).
- MCTS revisit helps when greedy refine local-opts into slow correct kernels (**C2**).

## Why it matters for this survey

Tier A UX/integration signal for ROADMAP “agentic compile as a tool in the ML engineer loop.”

## Limits / caveats

- CUDA/NVIDIA path; less codesign breadth than KForge/KernelEvolve.
- Name collision with KForge — keep digests distinct.
