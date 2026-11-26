# KernelOPT: Dispatch-Aware Agentic Search for GPU Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Red Hat (PyTorch team; four authors as interns) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2609.30059](https://arxiv.org/abs/2609.30059) |
| **Evidence tier** | **A** — directly relevant integration-aware optimization with fallback-inclusive outcomes; the experiment does not isolate the causal contribution of dispatch awareness or agent reasoning |
| **Version / reviewed** | v1 24 September, v2 6 October, [v3 19 November 2026](https://arxiv.org/html/2609.30059v3); v3 reviewed 26 November 2026. Same evidence family, not a new source. |

## Key contributions

The compiler's generated artifacts and library dispatch guide the optimization. The agent can synthesize an alternative model implementation or rewrite generated Triton kernels, while preserving existing vendor-library calls in the artifact route. Profiling-guided beam search uses the reported settings T=5, N=4, K=4, B=4 per isolated target, with early stopping and additional synthesis/model-level retries. A static, numerical, assembled-model correctness and performance cascade controls candidate acceptance; a 1.03x performance threshold defines optimization. The cross-run strategy tracker and supplied benchmark-derived guidelines are documented mechanisms, not demonstrated controller improvement.

## Summary

v3 clarifies the interpretation of the original 250-problem KernelBench study. Each problem runs on an H200, with Claude Sonnet 4.6 and a warmed-up Inductor max_autotune baseline. There is one terminal outcome per problem, not a repeated-search experiment.

| Level | Total | Optimized | Matched | Fallback | Baseline-substituted geomean | Median | Opt-only geomean |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 100 | 36 | 48 | 16 | 1.40x | 1.01x | 2.54x |
| 2 | 100 | 23 | 43 | 34 | 1.15x | 1.00x | 1.84x |
| 3 | 50 | 11 | 4 | 35 | 1.07x | 1.00x | 1.37x |

The total is 70 optimized, 95 matched and 85 fallback-labelled cases (73 performance regressions, five final verification failures, seven with no generated kernel). Fallback-labelled cases are assigned 1x in the aggregate; three L1 cases retain generated Triton final-model files, and two L3 cases have ambiguous saved-artifact provenance. Therefore the geomeans describe the stated aggregation convention, not a remeasurement of every saved final model. Against eager the reported geomeans are 1.72x, 1.79x and 1.56x on 99, 100 and 39 timed cases respectively.

## Key takeaways

- **Arithmetic contract matters.** Sixteen optimized matrix-product cases explicitly use lower-precision inputs or TF32 and one leaves dot precision to defaults/environment. Assigning 1x to these 17 cases produces level geomeans 1.14x, 1.07x and 1.04x; they account for 57.4% of the summed log-speedup. This is a sensitivity analysis, not matched-precision re-timing or an attribution of the residual gain.
- **Headroom is heterogeneous.** The largest factor, 88.63x, comes from replacing dense diagonal matrix multiplication by row scaling; it is not a generic GEMM result. Omitting the five factors at least 10x gives geomeans 1.245x, 1.112x and 1.072x over 96/99/50 problems. Isolated kernel gains may disappear in the assembled model.
- **Search costs.** The authors report approximately 1,100 H200 GPU-hours and 115 million LLM tokens, not a monetary cost. Individual L3 jobs range from six minutes to 66 hours. The timing harness uses separate processes and input generators, with 25 ms warmup and 100 ms repetition; one outcome per problem leaves search variability unmeasured.
- **Acceptance is not equal precision.** The model-level numerical test and performance gate are valuable but tolerances do not establish that the baseline and optimized code perform the same arithmetic. Report precision and model-quality contracts independently of the search procedure.

## Why it matters for this survey

The work is direct evidence for testing integrated application-aware search rather than treating standalone kernels as the final target. It is also a useful negative constraint: the benchmark-wide median is nearly unchanged and performance/verification fallbacks are common. A conventional algebraic rewrite pass could capture structured simplifications without agent search. Compare agents with symbolic simplification plus Inductor max_autotune, a deterministic profiling-guided search and a learned policy, controlling action spaces, precision, feedback and total cost. Cross dispatch context and synthesis availability, repeat on sealed workload families, retain the accepted artifact hash and report every failure. Compare both runtime gain and development payback; do not conflate cached experience with a changed controller.

## Limits / caveats

Fixed-shape KernelBench workloads, one GPU type and one LLM; overlap with model training data unassessed. No matched-precision rerun, repeated per-problem search or matched conventional search-policy arm; no production application integration or A/B evidence. The main results remain author-reported, not independently reproduced. v3 does not qualify the 2027 integration predicate or the 2027 controller checkpoint, and does not change the thesis verdict. The revised claims should replace, not add to, the v2 evidence family.

Source maintenance: v3 was found by ChatGPT's independent version audit on 26 November 2026, not by the discovery ledger. The ledger strips arXiv version suffixes when deduplicating against the index, so revisions of indexed papers do not appear. Claude checked the v3 figures above against the arXiv HTML the same day. They are the outcome table, medians, the precision and tail sensitivity analyses, the provenance notes for L1-041/047/049 and L3-018/044, the 6 min–66 h L3 job range, the timing harness settings and the statement on training-data overlap.
