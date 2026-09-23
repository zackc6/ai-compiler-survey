# Ave: Guiding Agentic GPU Optimization Using Data-Flow Invariants

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | CausalFlow · HKUST · Tsinghua University · Stanford · UCAS · UC Riverside |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Version 2](https://arxiv.org/abs/2604.18616v2) |
| **Evidence tier** | **A** — targeted compiler feedback for agent optimization |
| **Version** | Ave, 14 September 2026; originally Argus. Filename retained for existing links. |

## Key contributions

Data-flow annotations express relationships that the compiler checks before execution. Failed checks provide counterexamples to guide optimization without adding runtime checks.

## Summary

Ave combines planning and code generation with a language and compiler designed to provide more useful feedback than compilation success or numerical tests alone.

## Key takeaways

The revised paper reports 89–99% of expert-library effective throughput on selected MI300X kernel families. KernelBench validity is 100% at Level 1 and 88% at Level 2 within three attempts. Validity and throughput measure different outcomes.

## Why it matters for this survey

The system supports testing representations and diagnostic feedback together. It does not establish a permanent boundary between an agent and compiler components.

## Limits / caveats

Results are author evaluations on a specific target. Assertion checking is not a complete proof of arbitrary program correctness. Path-insensitive analysis limits precision; it should not automatically be described as unsound. Version 1’s title and metrics should not be reused for current claims.
