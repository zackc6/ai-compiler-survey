# Automated Design of Agentic Systems

| Field | Value |
|---|---|
| **Year** | 2024/25 |
| **Org** | University of British Columbia · Vector Institute |
| **Publisher** | ICLR 2025 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2408.08435v2) |
| **Evidence tier** | B: automated controller design outside compiler workloads |
| **Version / reviewed** | v2, 2 March 2025; reviewed 23 September 2026 |

## Key contributions

A fixed meta agent writes candidate agents as Python functions, evaluates them, and uses an archive to guide further designs. The editable object is the task-solving agent, not the outer search algorithm.

## Summary

Meta Agent Search is evaluated on reasoning, reading, mathematics, and science tasks, with transfer across domains and models. The public implementation is [ShengranHu/ADAS](https://github.com/ShengranHu/ADAS).

## Key takeaways

The ARC experiment uses 25 search iterations, 20 validation questions and 60 held-out test questions, with repeated evaluation. Other domain searches use 30 iterations. These are task scores, not compiled-program runtime measurements.

## Why it matters for this survey

Provides a design for searching over a compiler controller while keeping its improvement procedure fixed. It shares authors and research lineage with [Darwin Gödel Machine](darwin-godel-machine.md) and [Hyperagents](hyperagents.md); they are not independent replications.

## Limits / caveats

No compiler-controller benchmark is reported. An automatically designed controller is not necessarily recursively self-improving. Compare it with expert-designed and conventionally tuned controllers under the same total budget.
