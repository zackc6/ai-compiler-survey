# TIRx Harness: An Open Compiler Harness for Agentic GPU Programming

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | MLC Community · TVM ecosystem |
| **Publisher** | MLC blog · GitHub |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://blog.mlc.ai/2026/09/29/tirx-harness-an-open-compiler-harness-for-agentic-gpu-programming) |
| **Evidence tier** | **A** — relevance to compiler design, not independent replication |
| **Version / reviewed** | Source reviewed 15 October 2026 |

## Key contributions

Combines TIRx-lite kernel construction, compiler analyses for synchronization, races and numerical behavior, reference kernels, agent skills, profiling, and GPU evaluation through KCoral. Authors report 1.33–6.84× geometric-mean kernel speedup across selected Blackwell attention families using differing family baselines.

## Summary

The harness is distinct from the older [TIRx language/compiler substrate](tirx.md). A usable agent-facing compiler system includes diagnostics, knowledge and stable evaluation contracts as well as an intermediate representation.

## Key takeaways

Report the baseline, hardware, evaluated object, and checker scope alongside any numeric result. Do not equate kernel speed with application throughput or optimization cost.

## Why it matters for this survey

Ablate representation, reference knowledge, analysis and evaluation services at matched agent budgets; compare with [KCoral](kcoral.md) and [CAKE](cake.md).

## Limits / caveats

The benefit of individual harness elements is not isolated. Checker verdicts are scoped to their model and invocation. Reported results are kernel-level rather than application-level.
