# FlowCompile: An Optimizing Compiler for Structured LLM Workflows

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | UMass Amherst · MIT · MIT-IBM Watson AI Lab |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2605.13647](https://arxiv.org/abs/2605.13647) |
| **Evidence tier** | **A** — compile-time optimization of sub-agent workflow graphs (accuracy–latency) |

## Key contributions

- Treats structured LLM workflows (specialized sub-agents on a predefined graph) as a **compilation** problem, not only runtime routing.
- Before deployment, globally explores model choices, reasoning budgets, and workflow structures; builds a reusable set of workflow-level configurations across accuracy–latency trade-offs.
- Explicitly draws inspiration from **ML compilers** for compile-time search vs inference-time routing alone.

## Summary

Formalizes what ACCLAIM/GEAK/KernelEvolve do operationally: multi-agent graphs have a combinatorial config space that should be *compiled* (explored offline, frozen configs) rather than rediscovered per query. Bridges Compiler.next-style FMware compile and classical compiler thinking.

## Key takeaways

- Sub-agent topology is a first-class compile object (P3, P10, P18).
- Compile-time Pareto fronts of workflows mirror ACF/heuristic freezing in AI compilers.
- Supports §5.7 lean: batch/CI specialize → freeze, not always-on frontier routing only.

## Why it matters for this survey

★ Control-plane substrate for agentic compilers that *are* multi-agent (ACCLAIM levels, GEAK loops, KernelEvolve synthesizer/search/eval). Cite with Compiler.next and P23 amortization.

## Limits / caveats

- Targets general LLM workflows; not LLVM/Triton-specific — use as architecture evidence, not kernel speedups.
