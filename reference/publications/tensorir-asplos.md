# TensorIR: An Abstraction for Automatic Tensorized Program Optimization

| Field | Value |
|---|---|
| **Year** | 2022 |
| **Org** | UW · AWS · OctoML et al. |
| **Publisher** | ACM ASPLOS 2023 |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [https://dl.acm.org/doi/10.1145/3575693.3576933](https://dl.acm.org/doi/10.1145/3575693.3576933) |

## Key contributions

- Tensor computations as first-class IR
- Enables tensorized intrinsic scheduling
- Underpins modern TVM TIR scheduling

## Summary

Compiler abstraction that generalizes loop nests for tensor primitives and automatic optimization.

## Key takeaways

- IR design enables later search/LLM proposal methods
- Read with MetaSchedule docs

## Why it matters for this survey

TVM kernel-IR lineage. **[TIRx](tirx.md)** (2026) is the next kernel-level structure: agent-visible FFI + tile primitives at **L4**, not a new data-plane band.
