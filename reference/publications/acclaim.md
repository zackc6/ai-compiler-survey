# Agentic Code Optimization via Compiler-LLM Cooperation (ACCLAIM)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AWS AI · Georgia Tech |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [https://arxiv.org/abs/2604.04238](https://arxiv.org/abs/2604.04238) |
| **Evidence tier** | **A** — multi-level compiler↔LLM cooperation (Q2/Q3) |

## Key contributions

- Framework for **compiler–LLM cooperation**: interleave deterministic compiler passes with LLM rewrites across **source / IR / assembly** levels, not a single-level rewrite loop.
- Multi-agent realization (**ACCLAIM**): guiding orchestrator + level-specific optimization agents + compiler constituents as tools + LLM **test** agent (correctness + performance feedback).
- Method for **distributing compute budget** across abstraction levels; works without large SFT/RL corpora (compatible with them, not dependent).
- Mean speedups up to **1.25×** vs `clang -O3` on a standard C suite; beats level-specific and naive multi-level baselines at equal budget.

## Summary

AWS AI / Georgia Tech paper arguing that LLMs miss when they replace compilers, and compilers miss purpose-level opts. ACCLAIM keeps compilers as correctness anchors while letting LLMs propose creative rewrites where they help. The guiding agent chooses when to call frontend/middle-end/backend tools vs level agents, and backtracks when tests fail — a concrete hybrid control-plane design for Q2/Q3.

## Key takeaways

- **Cooperation > replacement:** best results come from interleaving compiler tools with LLM agents, not unconstrained codegen.
- **Multi-level matters:** single-level LLM opt (source-only or asm-only) underperforms orchestrated multi-level search.
- **Test agent is the admit gate:** correctness/performance probing is first-class; open models still stumble on tool-calling before code quality (cited in survey §3.2).
- Strong evidence for survey jobs **(a) online** propose–measure–admit across levels; complements Magellan-style **(b) offline** heuristic synthesis.

## Why it matters for this survey

Primary **Tier A** citation for Q2 (how agents help) and Q3 (control-plane reshape without replacing `opt`). Anchors the §5 claim that agents own search/orchestration while compilers own legality and fallback. Prefer the arXiv link above when citing; OSS code: [amazon-science/acclaim](https://github.com/amazon-science/acclaim) ([digest](acclaim-github.md)).
