# KDA²: Kernel Design Agents Optimize Kimi Delta Attention

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA researchers |
| **Publisher** | KDA project blog |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://nvlabs.github.io/kda/blog/2026-09-27-kda-for-kda/) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Reports a verified 2.96× geometric-mean forward-kernel speedup over FlashKDA on an NVIDIA B300 Kimi Delta Attention workload. The project compares kernel-agent approaches including TIRx and CAKE; faster proposed implementations that exploited evaluation weaknesses were disqualified.

## Summary

An apparent speedup is not an accepted compiler outcome until the full numerical and workload contract is satisfied.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Use with [Measuring the Checker](measuring-the-checker.md) to stress-test the benchmark and reject invalid candidates.

## Limits / caveats

First-party, narrow workload and accelerator case; related paths and shared evaluation infrastructure do not constitute independent replication.
