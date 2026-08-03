# Meta Engineering: KernelEvolve / Ranking Engineer Agent

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Type** | company |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/) |
| **Evidence tier** | **A** — public industrial narrative for ★ [KernelEvolve paper](kernelevolve.md) (ISCA 2026) |

## Key contributions

- Positions KernelEvolve as the **infra half** of Meta’s Ranking Engineer Agent (companion to ML-experimentation agents).
- States production impact in plain numbers: **>60%** Andromeda ads inference throughput on NVIDIA; **>25%** ads training throughput on MTIA.
- Clarifies multi-DSL surface: Triton / TLX / CuTe / FlyDSL plus CUDA, HIP, MTIA C++ — not Triton-only.
- Describes the six-component loop: LLM synthesizer, tree search (MCTS/evolution + selective memory), RAG knowledge base, automated eval/profiling, shared data foundation, agentic RL post-training.

## Summary

Engineering blog (2026-04-02) for the same system as arXiv:2512.23236 / ISCA 2026. Emphasizes search-over-candidates vs one-shot coding assistants, knowledge injection for proprietary MTIA, and federated profiling. Useful for productized claims and Ranking Engineer Agent framing; prefer the paper for methods and KernelBench/ATen eval tables.

## Key takeaways

- Public confirmation that hetero kernel agents are **in production** for ads ranking at Meta scale.
- Multi-DSL + proprietary-ISA RAG is the stated answer to O(models × ops × HW gens).
- Self-improving skill library + RL on trajectories is an industrial path for cheaper specialist models (**job a** + memory artifacts **A3**).

## Why it matters for this survey

Companion Tier A narrative for [kernelevolve.md](kernelevolve.md). Cite blog for product/throughput headlines; cite paper for system design and public-bench numbers. Reinforces **C9** coverage→perf ladder with TritorX and **S5** profilers-as-agent-APIs.

## Limits / caveats

- Vendor blog; speedups are selected production cases, not KernelBench-X averages (**C2**).
- Code remains internal; reproducibility limited.
