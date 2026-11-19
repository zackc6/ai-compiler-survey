# Together Compiler: Continual Compilation for AI Inference

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Together AI Research (Reyna Abhyankar, Dylan Lim, and colleagues) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Together Compiler, arXiv:2611.14681v1](https://arxiv.org/html/2611.14681v1) |
| **Evidence tier** | **A** — direct agent-in-the-loop serving-system integration with application-level evaluation, but without a matched conventional optimizer to isolate agent advantage |
| **Version / reviewed** | v1, 10 November 2026; full HTML and appendices reviewed 19 November 2026; first surfaced in 17 November discovery ledger (cited-by channel) |
| **Evidence family** | Together Compiler / TKCC, its engine, paper and Together AI reports; do not count separate descriptions of the same deployed system independently |

## Key contributions

Together Compiler (TKCC) continuously searches executable **whole-model forward-pass implementations**, not merely standalone kernels. Agents edit the inference engine's source and kernel implementations and benchmark those changes. A **persistent hot-reload engine** tests variants in a fast high-throughput tier and a slower, more representative tier. An analytical **non-agent** cost model ranks tensor/expert/pipeline/data parallelism choices before expensive search. The compiler/runtime still implements execution, cost modeling, compilation, measurement, correctness and deployment checks. The agent is a proposer; the paper's co-designed measurement and cost infrastructure is a substantial source of value.

The authors report production serving of trillions of tokens across their fleet. That is a **first-party deployment assertion**, not an independently inspected production promotion log. The new object optimized is a forward-pass implementation, not a reusable generated compiler analysis, transformation or lowering installed across subsequent toolchain releases.

## Author-reported results and denominators

- **Application throughput:** Up to **2.6× higher tokens/s** than the best published open-source InferenceX engine configurations as of **27 October 2026**, across **Kimi K3, GLM 5.3, MiniMax M3.1 Flash and DeepSeek v4.1 Flash** and multiple accelerator settings. This is an **up-to** result, not an across-model mean or isolated model effect; the paper does not give a matched non-agent search controller on the same engine/action space.
- **Workhorse model:** Up to **1.7× TPS** versus hand-optimized persistent megakernels on **Llama 1B, batch size 1**, with H100/B200 runs and varying output lengths. That comparison has a different baseline and task denominator from the InferenceX result.
- **End-to-end protocol:** The NVIDIA and AMD InferenceX AgentX workload uses **393 public agentic-coding traces (seed 42)**, pinned AIPerf **1.0.12**, and throughput per GPU counting cached input tokens in full plus output tokens over wall-clock time; P50/P90 inter-token latency is separately evaluated. The authors reran the published engine configurations and report reproducing baseline throughput, with approximately **2%** P90 interactivity discrepancy. Their Figure 7 starts with the *same parallelism strategy as the leading configuration* to reduce that confound. **Trainium2** is assessed on a different **synthetic 70k-token input** multi-turn dataset and must not be treated as a directly identical AgentX workload.
- **Optimization budget:** **24 continuous hours per model/configuration**, with **two times the engine replica size**, one for each tier; the headline says **at most two nodes per model**, not a universal fixed GPU-hour cost. Report amortized development and production infrastructure costs separately.
- **Search-system throughput:** The persistent engine admits **252× more experiments** and **11× lower agent idle time** than a restart-per-experiment RSI-Inference comparator. That is a controlled **measurement-system** comparison, *not* 252× kernel throughput, 252× application TPS, or agent superiority over non-agent search.
- **Reliability and measurement:** For the evaluated MiniMax on TensorRT-LLM setting, Table 1 gives startup-to-first-job 11 vs 3 minutes, hot reload 45 vs 17 seconds, median job completion 64 vs 28 seconds (slow vs fast), and fast-tier **3.9 crashes per 1,000 jobs** vs zero in the slow tier. The latter is a particular tier's job-crash rate, **not** the optimization campaign's total invalid-candidate/failure/rollback rate. Fast-tier approximations require a higher-fidelity gate.
- **Context ablation:** After 12 hours, a curated knowledge hub yields **25–31% less speedup** than no knowledge hub on the authors' assessed runs; simple common optimization instructions beat their specialized expert strategies. These are specific agent-harness context comparisons; they do not prove persistent compiler memory or knowledge-guided search generically harmful.

## Causal interpretation and strong non-agent alternatives

The paper is **strong first-party application-level evidence that a deployed agent-assisted compilation workflow can optimize serving systems**, not a causal demonstration that agent reasoning outperforms a matched conventional optimizer. Gains combine agent-authored source changes, the analytic parallelism cost model, persistent high-fidelity measurement, two-tier promotion, and access to whole-engine host metadata. Improvement over a baseline compiled in another engine is not an ablation of each piece.

A strong falsifier tests **the same persistent hot-reload engine and two-tier gate**, with the **same edits, compiler checks, knowledge, traffic, and 24-hour × two-replica budget**, using (a) the paper's agent, (b) EqiForge/TASO/beam/evolutionary/bandit-style non-agent optimization adapted to that action API, (c) fixed conventional tuning, and (d) agent variants with and without curated memory. Report all executed/correct/incorrect trials, accepted p50/p90 serving TPS, total accelerator-hours and tokens, regressions, promotions/rollbacks and retention on held-out traffic and hardware. The non-agent systems are **comparison designs**, not previously measured TKCC results.

## Agent / harness / compiler architectural signal

- **Problem:** traditional intermediate graphs cannot express all host-side changes relevant to data-dependent mixture-of-experts or long-sequence attention; engine restart makes high-fidelity iteration expensive.
- **Mechanism:** let the proposer inspect and rewrite source-level forward passes, with the compiler, analytics and execution harness retaining measurement, validation, cost modeling and selected promotion gates.
- **What evolves:** per-model implementations and strategy via repeated searches. A persistent versioned compiler-controller policy or reusable compiler pass is **not** shown to self-evolve by a held-out comparison.
- **Protected boundary:** high-fidelity on-traffic evaluation and numerical checks; the paper's published failure record does not establish exhaustive independent certification or automated rollback safety.
- **Design alternative:** a typed extensible intermediate representation such as TIRx might add checkability, but the two projects have not compared attainable application performance or full engineering cost.

## Limits and forecast interpretation (19 November 2026)

This is a **serious 2027 integration-predicate candidate**: the paper documents workload, hardware, shipped path assertions, baseline configuration and measurement budget more clearly than abstract-only leads. But the complete candidate-failure/promotion record and matched strong conventional optimizer baseline are not public in the reviewed text. Pending independent Claude review of what the predicate's admission criteria actually require, **do not increment the 2027 running tally (still 0/2)**. One organization could satisfy at most one of the two 2027 organizations. The full model forward pass does **not** meet the separate **2031 generated compiler component in default path across two later releases** rule.

No §5.3 thesis row, forecast call, evidence threshold, checkpoint rule, Figure 1 element or direction/timing/architecture confidence is changed by this proposed digest alone.
