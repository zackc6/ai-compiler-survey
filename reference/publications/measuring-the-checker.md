# Measuring the Checker: Mutation Analysis for GPU Kernel Benchmark Oracles

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Research authors |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Validation and approximate hardware |
| **Link** | [Primary source](https://arxiv.org/abs/2609.22220) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

The authors inject 10,303 compilable faulty mutants on 188 KernelBench tasks and establish independent witnesses for 7,384. The official KernelBench checker misses 16.9% of independently witnessed faults, especially precision-related ones.

## Summary

Checking an optimization candidate and testing the adequacy of its checker are distinct activities. A passing kernel remains bound by the sampled or formally modeled domain.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Add witnessed-mutation detection, false-rejection rates, and hidden-input robustness to the validation ladder. Pair with [KDA²](kda2.md).

## Limits / caveats

Constructed fault distributions are not representative production miscompilation probabilities and cannot prove a checker complete.
