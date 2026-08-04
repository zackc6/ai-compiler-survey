# LLVM Developers' Meeting slides: Magellan

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Google DeepMind / Google |
| **Publisher** | LLVM Developers' Meeting 2025 |
| **Type** | talk |
| **Group** | Agentic & RL compilers |
| **Link** | [https://llvm.org/devmtg/2025-10/slides/technical_talks/chen.pdf](https://llvm.org/devmtg/2025-10/slides/technical_talks/chen.pdf) |
| **Evidence tier** | **A** — Magellan production + **future signals** for §5 |

## Key contributions

- Operational Magellan / AlphaEvolve loop on LLVM: propose C++ in `EVOLVE-BLOCK` → local evaluate (`llvm-size` / perf) → reward feedback.
- **Inlining for size** in production context (Chrome mobile, Fuchsia, Android Search App lineage shared with MLGO): reported ~4–5%+ vs upstream/human heuristics in short search windows; ~8.8% avg size reduction across 10+ apps (on par with NN MLGO).
- Preliminary **XLA** results: graph rewrite / e-graph extraction (~7% vs manual); auto-sharding contest (4th/20 on Transformer/Gemma/diffusion) — *not* yet full end-to-end XLA pipeline.
- Explicit **next steps** (prediction-relevant): push performance ceiling; tackle **green-field** domains with little prior expertise; **open-source implementation based on OpenEvolve and OSS models**.

## Summary

LLVM Dev Meeting 2025 slides (Chen / Novikov / Vũ / Trofin / Yazdanbakhsh) that add production numbers and a forward roadmap beyond the Magellan paper abstract. Framing: LLM+evolution as a force multiplier for heuristic discovery vs slow manual deep-dive; trade-off that convergence/ceiling vs NNs remains open research.

## Key takeaways (future signals)

1. **OSS path named:** OpenEvolve + OSS models is the stated Magellan open-source vector → watch [`openevolve`](https://github.com/algorithmicsuperintelligence/openevolve) ([digest](openevolve.md)).
2. **XLA / AI-compiler green-field:** auto-sharding and graph rewrite are early ports beyond LLVM size/perf — tests whether offline agents invent heuristics where human expertise is thin (**C1**, §5.4).
3. **Ship as C++:** evolved heuristics stay reviewable and deployable (parallel bet to neural MLGO advisors).
4. Ceiling vs NN policies is unresolved — do not treat Magellan as having “won” MLGO (**C1**).

## Why it matters for this survey

Fold these next-steps into [`docs/SURVEY.md`](../../docs/SURVEY.md) **§5.4**, not only related work. Prefer this PDF for production/ops claims; prefer the [Magellan paper](magellan.md) for system design.
