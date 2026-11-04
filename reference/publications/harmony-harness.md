# Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google Cloud AI Research (six authors) · Google DeepMind (Shuo Li) · Carnegie Mellon University (Matt Fredrikson) |
| **Publisher** | arXiv preprint |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary paper](https://arxiv.org/abs/2610.15150) |
| **Evidence tier** | B: direct controller-harness design relevance, indirect compiler evidence; not a compiler optimization result |
| **Version / reviewed** | arXiv 2610.15150, published 10 October 2026; full-text primary figures and limitations independently checked by Claude 4 November 2026 |

## Key contributions

Harmony Harness formulates agent-harness adaptation as multi-objective optimization, using decomposition-based evolutionary search to maintain candidates across preference regions of a Pareto frontier. It factorizes edits into reusable general mechanisms and benchmark/environment-specific adaptations, with dynamic composition at inference time. These are separate mechanisms: a combined-method result cannot establish the causal effect of each.

## Summary

The authors evaluate security and functionality of coding-agent harnesses on SecRepoBench and BaxBench, reporting average secure-and-functional pass (F∧S) of **76.7% on SecRepoBench** against **51.1%** for the best of three Meta-Harness variants and **48.9%** for Darwin Gödel Machine (DGM); on BaxBench, **61.3%** against **52.4%**, an **8.9 percentage-point absolute** or approximately **17% relative** improvement. The authors' abstract-level “exceeding 10%” claim for BaxBench refers to relative improvement, not percentage points. This is agent task success, **not** kernel latency, compiler speedup, application throughput, or cost-adjusted compiler search. The reported SecRepoBench train/held-out IN/held-out OUT splits each have 30 tasks, results average three runs, and no confidence intervals are reported. The held-out OUT F∧S is 66.7% versus 43.3% for the best Meta-Harness variant; one task is 3.3 percentage points. Cross-benchmark transfer from BaxBench to CWEval is reported at +13.9/+14.3 F∧S points for C/C++, languages absent from BaxBench. These are coding-agent task results, not compiler application measurements.

## Key takeaways

The baselines are three Meta-Harness variants and DGM (a scalarized-reward evolutionary agent), not matched non-agent compiler search. Both harness proposer and task solver use **gemini-3.6-flash**, so the study cannot separate harness-update ability from harness-utilization ability. The strategy ablation scores **76.7** for Tchebycheff decomposition versus **70.0** for weighted-sum. The component ablation reports **63.3** for Tchebycheff joint evolution, **66.7** after factorization, and **76.7** after adding dynamic orchestration; the authors do not isolate composition without factorization. Two objectives are considered, but functionality and security may be aligned in these datasets; a Pareto-maintenance mechanism is not yet proven superior for strongly conflicting compiler goals. General-vs-specific factorization offers a testable hypothesis about controller transfer, not demonstrated portability across compiler targets. Do not count the paper as a 2027 qualifying compiler/serving integration.

## Why it matters for this survey

Most directly informs §5.3 controller improvement, §6 'Should the controller improve itself, and at what scope?', and the September 2027 controller checkpoint. It motivates a non-agent MOEA/D/NSGA-II controller-search arm with identical typed action space, plus single-objective, factorized/no-composition, and fixed-harness arms. Compare accepted held-out application speed, search cost, validation and cross-hardware transfer. Meta-Harness and Darwin Gödel Machine are direct experimental baselines, not independent confirmations of Harmony; GEPA and AFlow are adjacent mechanisms, not compiler deployment confirmations.

## Limits / caveats

Preprint, coding-agent domain, no established compiler-specific causal benefit or production adoption. The authors explicitly limit their instantiation to secure code generation. They report matched token budgets but not total evolution/development cost for main runs; settings include 5–6 decomposition subproblems and 3–4 generations, and per-task solving uses approximately 31.9K, 58.2K, and 63.1K tokens in reported conditions. No confidence intervals are given; the narrow Pareto fronts do not exercise the claimed non-convex-front advantage. A complete GPU/wall-clock cost and failure ledger is unavailable. Add supplied-knowledge and non-agent Pareto arms, a no-factorization-with-composition arm, and crossed proposer/solver models to isolate mechanisms. Reject any causal claim that multi-objective decomposition alone accounts for the combined improvement. Falsifier: under matched compile/measure/token budgets, conventional Pareto search with fixed tools and memory matches or beats factorized agent evolution on unseen compiler tasks.
