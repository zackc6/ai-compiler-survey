# DITRON: Distributed Multi-level Tiling Compiler for Parallel Tensor Programs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | ByteDance Seed · Peking University · Tsinghua University · Zhejiang University · Shanghai Jiao Tong University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [Primary source](https://arxiv.org/abs/2605.02953v1) |
| **Evidence tier** | **A** — relevance to the guide’s design choices, not a quality rating |
| **Version / reviewed** | Linked version; reviewed 2026-09-23 |

## Key contributions

Hierarchical tiling and reordered execution coordinate computation with communication across devices and nodes.

## Summary

DITRON broadens compilation without requiring a language-model controller. Its selected vLLM experiments report 5–30% gains at batch sizes above 128; smaller batches favor the baseline.

## Key takeaways

Communication overlap can improve application performance even when the constituent matrix multiplication is slower.

## Why it matters for this survey

A strong non-agent comparison for wider optimization. The project shares the [Triton-distributed](triton-distributed.md) lineage and repository.

## Limits / caveats

Author evaluation and industry report, not independent replication. The abstract’s greater-than-10% model floating-point utilization claim must not be relabeled as percentage points or ranked against another system’s throughput. Gains depend on shape and scale.
