# Triton-distributed: Programming Overlapping Kernels on Distributed AI Systems with the Triton Compiler

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | ByteDance Seed · Tsinghua University · Peking University · Shanghai Jiao Tong University · Zhejiang University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [Primary source](https://arxiv.org/abs/2504.19442v3) |
| **Evidence tier** | **A** — relevance to the design decisions, not a quality score |
| **Reviewed** | 2026-09-23 |

## Key contributions

Adds communication operations to the Triton programming model, allowing computation, memory movement, and communication to be scheduled together.

## Summary

The compiler supports overlap within and across nodes. The authors evaluate systems with up to 64 devices.

## Key takeaways

An optimizer needs access to communication and execution choices when they limit application performance.

## Why it matters for this survey

It supplies both a conventional baseline and a possible interface for wider automated search. It challenges a survey focused only on isolated kernels.

## Limits / caveats

This is evidence for distributed compilation, not agent superiority. Measured gains depend on communication patterns, hardware, and baselines; source-level reuse alone does not establish performance portability.
