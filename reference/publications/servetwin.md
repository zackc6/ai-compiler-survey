# ServeTwin: A Benchmark-Validated Simulator for Distributed LLM Architecture Exploration

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Samsung Advanced Institute of Technology |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | HW codesign & bring-up |
| **Link** | [arXiv 2610.02732](https://arxiv.org/abs/2610.02732) |
| **Evidence tier** | **B** — a measurement-calibrated serving simulator; the kind of instrument the 2036 co-design predicate requires, not a co-design result |
| **Version / reviewed** | v1, 2 October 2026; reviewed 15 October 2026 |

## Key contributions

ServeTwin pairs analytical timing with a stateful, closed-loop serving simulation: request completion, scheduling, queue state, and KV-cache evolution feed back on each other, including prefill–decode disaggregation and multi-turn agent workloads. A trace generator (iSTAGE) derives per-iteration traces from model and engine specifications without profiling the target hardware, accounting for ragged batches and engine mechanisms such as CUDA-graph batch padding. It exposes a vLLM-compatible interface and runs unmodified serving benchmarks. Execution time is decomposed into throughput, scheduler, and runtime costs so that recalibration is confined to the component that changed.

## Summary

Two validations with separate denominators. (1) InferenceX: the steady-state throughput–interactivity frontier for DeepSeek-R1 (671B MoE, FP8) on H200, B200, and GB200 NVL72, validated against the **public performance data published by SemiAnalysis**, not the authors' own telemetry—**3.6% mean error across 27 operating points, all within 10%**, with the model calibrated on a subset of those points (3.5%) and evaluated on the held-out remainder (3.7%); the paper does not break the 27 points down by platform. (2) LMBenchmark multi-turn on the authors' own two-H100 setup with Dynamo and vLLM—**9.9% error** (per-scenario −23% to +14%). Also: iSTAGE step time 3.7% median on mixed batches; disaggregated transfer 3.1%; extreme concurrency 7–12%. A separate GB200 decode-step comparison (section 4.8) is explicitly a transferred platform-model prediction, not a measurement.

## Key takeaways

- Pre-silicon sweeps: HBM bandwidth and capacity each at 0.7×, 1×, 1.4× show the preferred tradeoff reversing with workload state; tripling bandwidth and cutting scheduler/runtime cost 40% at concurrencies up to 2,048 shifts the bottleneck from memory to scheduler and runtime overheads.
- The section 4.8 GB200 decode result is a transferred-model prediction; the InferenceX frontier points are third-party published measurements rather than the authors' own; several model families are covered only by analytical templates.

## Why it matters for this survey

The ten-year co-design predicate accepts "a simulator calibrated against measurements" as a venue for joint hardware-parameter and execution-strategy search. ServeTwin is a concrete example of what that calibration looks like—published error against public benchmarks on measured hardware, with a stated recalibration scope—and therefore a reference point for judging future claims. It is not itself a co-design search and contains no agent; it supplies the instrument, not the result. Also relevant to the "optimization is expanding beyond isolated kernels" trend: the decision space it models (disaggregation, KV placement, scheduler cost) is the cluster-level space the survey expects agents to be tested on.

## Limits / caveats

- Validation covers two benchmarks and two measured model families; errors rise at extreme concurrency and on the largest TTFT misses.
- The sweeps are sensitivity analyses, not equal-cost design comparisons.
- Component changes require recalibration; the paper's own LLMServingSim comparison used a relaxed KV budget.
