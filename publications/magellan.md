# Magellan: Autonomous Discovery of Novel Compiler Optimization Heuristics with AlphaEvolve

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google DeepMind / Google |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [https://arxiv.org/abs/2601.21096](https://arxiv.org/abs/2601.21096) |
| **Evidence tier** | **A** — offline heuristic synthesis (agent job b) |

## Key contributions

- Evolves executable **C++ heuristics** via LLM coding agent + evolutionary search + autotune (AlphaEvolve lineage).
- LLVM function inlining (size + performance) and register-allocation priority rules; preliminary **XLA** ports.
- Produces human-readable, deployable pass logic — unlike opaque neural-in-the-compiler policies.

## Summary

Google/DeepMind/Cornell agentic framework that synthesizes compiler pass decision logic and evaluates it on macro-benchmarks / end-to-end apps, matching or beating expert heuristics. Canonical evidence for the **offline** agent job in SURVEY §5: ship reviewable heuristics into the classical data plane rather than replacing `opt` at runtime.

## Key takeaways

- Offline compiler-engineering agent archetype (complements ACCLAIM-style **online** multi-level loops).
- Production inlining narrative strengthened in [LLVM Dev Meeting slides](magellan-llvm-slides.md) (prefer slides for ops numbers).
- Parallel bet to MLGO neural advisors — do not collapse into one winner (**C1**).

## Future signals (fold into §5.4)

From companion [slides digest](magellan-llvm-slides.md) — not only related work:

1. **OSS path:** open-source Magellan via **OpenEvolve + OSS models** ([openevolve](openevolve.md)).
2. **XLA green-field:** auto-sharding / graph-rewrite where human heuristic expertise is thin.
3. **Ship as C++:** evolved heuristics stay reviewable (HITL / ownership still open — gap 4.8).

## Why it matters for this survey

Primary **Tier A** citation for offline heuristic synthesis and §5 prediction (defaults stay classical; agents synthesize artifacts that land in the data plane). Prefer this paper for system design; prefer the slides digest for production/next-step claims.
