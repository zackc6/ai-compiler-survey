# Learning to Optimize Halide with Tree Search and Random Programs

| Field | Value |
|---|---|
| **Year** | 2019 |
| **Org** | Facebook AI Research (now Meta) · UC Berkeley · MIT CSAIL · Adobe · Google · Stanford University (eleven authors; affiliations as printed) |
| **Publisher** | ACM SIGGRAPH 2019 / ACM Transactions on Graphics 38(4); Halide project |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [Halide primary paper](https://halide-lang.org/papers/halide_autoscheduler_2019.pdf) |
| **Evidence tier** | **A** — non-agent learned-cost-model and coupled schedule-search comparator with budget ablations |
| **Version / reviewed** | SIGGRAPH 2019 full paper; reviewed 22 October 2026 (ChatGPT); figures re-verified against the full text 4 November 2026 (Claude, NSF PAR mirror) |

## Key contributions

A cost model trained on random programs guides greedy or beam search over Halide pipeline schedules. The search jointly chooses tiling, parallelism, and producer-consumer compute/storage granularity. With more budget it benchmarks candidate schedules and optionally retrains. It is not a language-model agent.

## Summary

Figure 8 evaluates **real application pipelines** on an **Intel Core i9-7960X CPU**, against the then-current Halide master autoscheduler. Average throughput rises **50%** with greedy search and **75%** with beam search (Figure 8 caption and Section 1); about **ten minutes** of autotuning "produces schedules twice as fast as the baseline" (caption), which the Figure 8 legend labels **"autotuned (95% faster)"** — the 95% is a legend value, the prose says "twice"; **three hours** of sampling and retraining reaches **135%**; expert human schedules average **70%** above the same baseline. These are CPU throughput gains of roughly 1.50, 1.75, 1.95, 2.35 and 1.70 times, not GPU speedups.

## Key takeaways

- **Application denominator:** held-out image-processing and related pipelines on a five-megapixel image. The model was not trained on these applications; this is more meaningful than isolated kernel latency, but not modern transformer serving.
- **Cost:** per-application budget from greedy compilation to ~10 minutes or 3 hours. Cost-model training is separate: five rounds of 10,000 random algorithms times 32 schedules, distributed across CPU servers and V100 GPU samples. Include amortized training cost in any agent comparison.
- **Causal controls (Section 6.3):** with the same beam search, restricting the search to the production autoscheduler's old schedule space yields **28%** over Halide master, versus **75%** with the expanded space. With the method held fixed this isolates a large scope effect; it does not show that the search method is irrelevant. A second ablation separates the cost model from its training data: the model retrained on the authors' random programs is **82%** faster than Halide master versus **75%** with the original weights, so retraining adds about seven points. The three-hour benefit comes mostly from sampling more schedules rather than from retraining the cost model.
- **GPU qualification:** a separate, preliminary GPU comparison reports **29%** faster greedy and **33%** faster beam than a prior GPU autoscheduler, with unsupported applications excluded. Do not transfer Figure 8 CPU numbers to GPU.
- **Validation:** compiled Halide schedules and application-specific runtime checks, not proof of numerical equivalence for arbitrary algorithms.

## Why it matters for this survey

Strong conventional methods already coordinate interdependent compiler choices. A matched study should compare fixed beam search, an OpenTuner ensemble, random search and an agent on the same Halide schedule API, identical supplied knowledge, 10-minute and three-hour budgets, CPU/GPU application throughput, correctness and failures. It is related to OpenTuner's earlier Halide case, not an independent Halide replication.

## Limits / caveats

CPU application mix is historical and GPU results are incomplete. Search-space design and feature engineering require human work. The study does not generate persistent compiler components or prove that contemporary agents lose under matched conditions.
