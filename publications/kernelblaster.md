# KernelBlaster: Continual Cross-Task CUDA Optimization via Memory-Augmented In-Context RL

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA · UC Berkeley |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2602.14293](https://arxiv.org/abs/2602.14293) |
| **Evidence tier** | **A** — persistent memory / in-context RL for CUDA agents |

## Key contributions

- **MAIC-RL**: memory-augmented in-context RL so CUDA agents accumulate a persistent knowledge base across tasks/GPU generations.
- Profile-guided textual-gradient agentic flow; open-source harness.
- Reports KernelBench Level 1/2/3 geomean speedups vs PyTorch baseline (1.43× / 2.50× / 1.50× in abstract).

## Summary

NVIDIA/UCB line attacking the “agents forget prior exploration” failure mode. Memory becomes a first-class compiler artifact beside ACFs and evolved heuristics.

## Key takeaways

- Future agentic compilers need **versioned optimization memory** across HW gens — codesign with ISA changelogs.
- Complements Magellan offline synthesis with continual online memory (**C5**).

## Why it matters for this survey

Tier A for ROADMAP claim that traces/memory, not only one-shot kernels, reshape the stack.

## Limits / caveats

- CUDA-centric; compare ceilings with KernelBench-X.
