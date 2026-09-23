# Mirage: A Multi-Level Superoptimizer for Tensor Programs

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Carnegie Mellon University · Peking University · Pennsylvania State University · Purdue University · Weizmann Institute of Science |
| **Publisher** | USENIX OSDI 2025 |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [Primary source](https://arxiv.org/abs/2405.05751v3) |
| **Evidence tier** | **A** — relevance to the design decisions, not a quality score |
| **Reviewed** | 2026-09-23 |

## Key contributions

Unified graphs expose transformations across kernel, thread-block, and thread levels. Search combines algebraic and scheduling changes with equivalence checks.

## Summary

Mirage demonstrates a structured route to tensor-program optimization without requiring a language-model agent.

## Key takeaways

Compare agent search against strong symbolic search, not just a fixed compiler configuration.

## Why it matters for this survey

Its multi-level search is an alternative implementation for the guide’s optimization loop, and could also be a tool used by an agent.

## Limits / caveats

The equivalence method has a defined language and semantic scope; do not generalize it to arbitrary floating-point programs. Results are author evaluations. Prism shares a research lineage and is not an independent replication.
