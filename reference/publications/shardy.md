# Shardy: A Tensor Partitioning System

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | OpenXLA (GSPMD and PartIR teams) |
| **Publisher** | OpenXLA documentation |
| **Type** | code |
| **Group** | Structured and distributed compilation |
| **Link** | [Primary source](https://openxla.org/shardy/overview) |
| **Evidence tier** | **B** — relevance to the design decisions, not a quality score |
| **Reviewed** | 2026-09-23 |

## Key contributions

Provides a tensor partitioning system built on MLIR, with axis-based sharding, user constraints, propagation, and partitioning.

## Summary

Shardy represents how tensors are distributed over a device mesh and carries those choices into executable distributed programs.

## Key takeaways

Distribution decisions belong in a compiler design when communication and placement affect performance.

## Why it matters for this survey

Use its documented interfaces as concrete alternatives to inventing a new distribution layer. An agent could propose or revise sharding choices without replacing every downstream component.

## Limits / caveats

Documentation establishes interfaces and intended behavior, not a general performance advantage or agentic optimization result. This digest records the documentation reviewed in September 2026.
