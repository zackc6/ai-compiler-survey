# Learning to Optimize Halide with Tree Search and Random Programs

| Field | Value |
|---|---|
| **Year** | 2019 |
| **Org** | Facebook AI Research (now Meta), UC Berkeley, MIT CSAIL, Adobe Research, Google, Stanford University |
| **Publisher** | ACM SIGGRAPH 2019 / ACM Transactions on Graphics 38(4); Halide project |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [Halide primary paper](https://halide-lang.org/papers/halide_autoscheduler_2019.pdf) |
| **Evidence tier** | **A** — non-agent learned-cost-model and coupled schedule-search comparator with budget ablations |
| **Version / reviewed** | SIGGRAPH 2019 full paper; reviewed 22 October 2026 |

## Key contributions

A cost model trained on random programs guides greedy or beam search over Halide pipeline schedules. The search jointly chooses tiling, parallelism, and producer-consumer compute/storage granularity. With more budget it benchmarks candidate schedules and optionally retrains. It is not a language-model agent.

## Summary

Figure 8 evaluates **real application pipelines** on an **Intel Core i9-7960X CPU**, against the then-current Halide master autoscheduler. Average throughput rises **50%** with greedy search, **75%** with beam search, **95%** with about **10 minutes** of autotuning, and **135%** with **three hours** of sampling and retraining; expert human schedules average **70%** above the same baseline. These are throughput gains of 1.50, 1.75, 1.95, 2.35 and 1.70 times, not GPU speedups.

## Key takeaways

- **Application denominator:** held-out image-processing and related pipelines on a five-megapixel image. The model was not trained on these applications; this is more meaningful than isolated kernel latency, but not modern transformer serving.
- **Cost:** per-application budget from greedy compilation to ~10 minutes or 3 hours. Cost-model training is separate: five rounds of 10,000 random algorithms times 32 schedules, distributed across CPU servers and V100 GPU samples. Include amortized training cost in any agent comparison.
- **Causal controls:** restricting beam search to the old schedule space yields **28%** improvement, versus **75%** with the expanded space. The authors' ablation finds much of the three-hour benefit comes from sampling more schedules rather than retraining the cost model.
- **GPU qualification:** a separate, preliminary GPU comparison reports **29%** faster greedy and **33%** faster beam than a prior GPU autoscheduler, with unsupported applications excluded. Do not transfer Figure 8 CPU numbers to GPU.
- **Validation:** compiled Halide schedules and application-specific runtime checks, not proof of numerical equivalence for arbitrary algorithms.

## Why it matters for this survey

Strong conventional methods already coordinate interdependent compiler choices. A matched study should compare fixed beam search, an OpenTuner ensemble, random search and an agent on the same Halide schedule API, identical supplied knowledge, 10-minute and three-hour budgets, CPU/GPU application throughput, correctness and failures. It is related to OpenTuner's earlier Halide case, not an independent Halide replication.

## Limits / caveats

CPU application mix is historical and GPU results are incomplete. Search-space design and feature engineering require human work. The study does not generate persistent compiler components or prove that contemporary agents lose under matched conditions.
