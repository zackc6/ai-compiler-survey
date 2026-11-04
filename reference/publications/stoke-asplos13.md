# Stochastic Superoptimization (STOKE)

| Field | Value |
|---|---|
| **Year** | 2013 |
| **Org** | Stanford University |
| **Publisher** | ACM ASPLOS 2013 |
| **Type** | paper |
| **Group** | Correctness lineage |
| **Link** | https://theory.stanford.edu/~aiken/publications/papers/asplos13.pdf |
| **Evidence tier** | A: non-agent broad synthesis comparator |
| **Version / reviewed** | ASPLOS 2013, full author paper read 22 October 2026 |

## Key contributions

STOKE uses stochastic search over loop-free x86-64 machine-code sequences with test-guided selection and symbolic validation, without a language-model agent.

## Summary

On an OpenSSL Montgomery multiplication kernel the authors report 1.6 times faster runtime than gcc -O3, slightly faster than expert assembly. This is kernel latency, not end-to-end application throughput.

## Key takeaways

The starting binary is LLVM -O0; strong comparisons are gcc -O3 and icc -O3. The study used 40 dual-core 1.8 GHz AMD Opterons, with synthesis and optimization each allocated 30 minutes in parallel. The verifier uses fixed-offset stack assumptions and uninterpreted 64-bit multiplication and division, limiting the formal contract. Workloads are selected loop-free x86 fragments.

## Why it matters for this survey

This historical non-agent optimizer can synthesize algorithmically different verified code. Compare an agent under the same instruction actions, solver, workload and total budget; report failures, search cost and verified runtime.

## Limits / caveats

The 1.6-times result is one kernel, not a suite average. No evidence for GPUs, loops, modern numerical semantics, compiler-component persistence or deployment payback. Historical CPU costs cannot be compared directly with current GPU-hours or tokens.
