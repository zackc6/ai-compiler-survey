# KCoral: Lightweight Benchmark Server for Agentic GPU Programming

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | MLC Community |
| **Publisher** | MLC blog |
| **Type** | company |
| **Group** | Agent control-plane substrate |
| **Link** | [Primary source](https://blog.mlc.ai/2026/10/05/kcoral-lightweight-benchmark-server-for-agentic-gpu-programming) |
| **Evidence tier** | **B** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Separates agent host and GPU worker, provides remote profiling and benchmark adapters and isolates GPU timing. On one B200, reported throughput rises from 4.98 to 12.86 completed evaluations/minute (2.58×) for 256 fixed-kernel evaluations at high concurrency.

## Summary

The result is evaluation throughput, not a 2.58× speedup of generated kernels; it isolates GPU benchmarking from CPU and agent-side activities.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Measure queueing, device time, timing fidelity and failure recovery; compare with [TIRx Harness](tirx-harness.md).

## Limits / caveats

Single-hardware setting; model generation time excluded. Remote execution of generated code requires isolation and careful contract ownership.
