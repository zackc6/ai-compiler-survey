# Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Authors: Weichen Yu, Lesly Miculicich, Bhavana Dalvi Mishra, Jiefeng Chen, Shuo Li, Matt Fredrikson, Tomas Pfister, Long T. Le; mixed institutional affiliations, verify from PDF before final integration |
| **Publisher** | arXiv preprint |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary paper](https://arxiv.org/abs/2610.15150) |
| **Evidence tier** | B: direct controller-harness design relevance, indirect compiler evidence; not a compiler optimization result |
| **Version / reviewed** | arXiv 2610.15150, published 10 October 2026; abstract verified 4 November 2026; full PDF tables and budgets pending second reviewer |

## Key contributions

Harmony Harness formulates agent-harness adaptation as multi-objective optimization, using decomposition-based evolutionary search to maintain candidates across preference regions of a Pareto frontier. It factorizes edits into reusable general mechanisms and benchmark/environment-specific adaptations, with dynamic composition at inference time. These are separate mechanisms: a combined-method result cannot establish the causal effect of each.

## Summary

The authors evaluate security and functionality of coding-agent harnesses on SecRepoBench and BaxBench, reporting gains exceeding 10% over strong harness-evolution baselines on both benchmarks. This is agent task success, **not** kernel latency, compiler speedup, application throughput, or cost-adjusted compiler search. The paper's primary abstract does not disclose per-candidate token/GPU budgets, denominators, hardware, full failures, or confidence intervals; those require full-text verification before any quantitative claim enters the main survey.

## Key takeaways

The reported baseline is other harness-evolution systems, not matched non-agent compiler search. Two objectives are considered, but functionality and security may be aligned in these datasets; a Pareto-maintenance mechanism is not yet proven superior for strongly conflicting compiler goals. General-vs-specific factorization offers a testable hypothesis about controller transfer, not demonstrated portability across compiler targets. Do not count the paper as a 2027 qualifying compiler/serving integration.

## Why it matters for this survey

Most directly informs §5.3 controller improvement, §6 'Should the controller improve itself, and at what scope?', and the September 2027 controller checkpoint. It motivates a non-agent MOEA/D/NSGA-II controller-search arm with identical typed action space, plus single-objective, factorized/no-composition, and fixed-harness arms. Compare accepted held-out application speed, search cost, validation and cross-hardware transfer. Related families include Meta-Harness, Darwin Gödel Machine, GEPA, and AFlow; these are comparisons, not independent compiler deployment confirmations.

## Limits / caveats

Preprint, coding-agent domain, no established compiler-specific causal benefit or production adoption. Full paper's exact result table, uncertainty, budgets, model versions, ablation denominators and infrastructure failures require second-pass PDF verification. Reject any causal claim that multi-objective decomposition alone accounts for the combined improvement. Falsifier: under matched compile/measure/token budgets, conventional Pareto search with fixed tools and memory matches or beats factorized agent evolution on unseen compiler tasks.
