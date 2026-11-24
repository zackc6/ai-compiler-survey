# Zep: A Temporal Knowledge Graph Architecture for Agent Memory

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Zep AI |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2501.13956](https://arxiv.org/abs/2501.13956) · [Graphiti](https://github.com/getzep/graphiti) |
| **Evidence tier** | **C** — a mechanism for invalidating outdated memory; conversational and business data only |
| **Version / reviewed** | v1, 20 January 2025; HTML full text reviewed 24 November 2026 |

## Key contributions

Graphiti, Zep's engine, stores memory as a knowledge graph with two timelines: when a fact held in the world (valid from, valid until) and when the system recorded or retired it. When a new fact contradicts an existing one whose validity overlaps, a language model detects the contradiction and closes the old fact's validity at the new fact's start, keeping the history instead of overwriting it.

## Summary

Deep Memory Retrieval: 94.8% against 93.4% for MemGPT. LongMemEval: up to 18.5% higher accuracy and about 90% lower response latency than full-context baselines, with gpt-4o-mini and gpt-4o. Gains depend on the model: on single-session-assistant questions accuracy falls (17.7% for gpt-4o, 9.06% for gpt-4o-mini). Latency was measured over a network from a residential laptop.

## Key takeaways

- The authors call Deep Memory Retrieval a weak benchmark and note that no benchmark tests conversation history combined with structured data.
- Incremental community maintenance drifts from full recomputation and needs periodic refreshes.

## Why it matters for this survey

It names a problem compiler memory has that the agent evidence has not tested: **experience goes stale**. A hardware note, a tuned schedule or a "this rewrite is faster" lesson is valid only for a compiler version, driver, kernel library and chip. Bi-temporal validity is one candidate mechanism: record the toolchain state under which each lesson was measured, and retire it when a later measurement contradicts it. The [Storage-to-Experience survey](agent-memory-storage-to-experience.md) lists the same staleness problem as open.

## Limits / caveats

- First-party benchmarks by the product vendor; the MemGPT comparison could not be run on LongMemEval.
- Contradiction detection is itself a model judgment; for compiler facts a re-measurement would be the stronger invalidation signal.
