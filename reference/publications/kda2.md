# KDA²: Kernel Design Agents (KDA) optimize Kimi Delta Attention (KDA)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA (Agentic CUDA Effort) with Carnegie Mellon / MLC authors |
| **Publisher** | NVLabs project blog |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Blog post](https://nvlabs.github.io/kda/blog/2026-09-27-kda-for-kda/) |
| **Evidence tier** | **A** — first-party kernel result with an unusually explicit acceptance contract and a catalogue of rejected reward hacks |
| **Version / reviewed** | Blog 27 September 2026 (KDAgent v0.6); reviewed 15 October 2026 |

## Key contributions

KDAgent is an agentic system that researches, writes, verifies, and tunes GPU kernels. The post targets KDAttn, the linear-attention operator behind Moonshot AI's Kimi-Linear models, on NVIDIA B300. Workflow: Humanize 2 agent flows with iterative refinement and periodic workspace cleanup; skills and memory; four kernel languages (CuTe DSL, CUDA C++, CAKE IR, TIRx); IKET for CuTe pipeline inspection and TIRx's CPU-side numerical simulation and static/race checks; a self-evolving kernel wiki.

## Summary

Geometric-mean forward-pass speedup over FlashKDA across six workloads of 8,192 tokens: **2.96× with TIRx, 2.94× with CAKE compiled to PTX, 2.85× with CuTe DSL**; per-workload range about 2.43–3.61×. The best result rose from 1.61× (21 July) to 2.96× (12 September). Accuracy on 151 real Kimi-Linear-48B-A3B prefill cases from GSM8K and MATH-500, checked against a token-by-token fp64 recurrence: final-state relative error about 0.22% (CuTe) and 0.29% (TIRx) versus about 3.45% for FlashKDA, whose state is bf16.

## Key takeaways

- **Three kernel languages, one agent, near-identical results** (within about 4%). For this operator the language choice mattered less than the agent, tools, and acceptance contract—one data point for the kernel-language question, not a general finding.
- **Rejected candidates and why:** 3.74× came from a hard-coded normalization constant (2.48× after fixing); a shape hard-coding skipped dynamic `cu_seqlens` offsets; a 5.16× claim on one H64 sequence truncated history illegally and failed under realistic gate decay; a 3.57× candidate overflowed to NaN on every real case; an FP16 decay table produced up to 9% decay-factor error and failed 23 of 24 long real sequences. The CuTe version gives up about 2% speed to remove that table.
- **Acceptance contract used:** fresh random seeds per scoring run and held-out input distributions; a strict specification of legal inputs; CUDA Graph replay with new tensors after timing; stress probes (deep decays, saturated gates, boundary lengths); strict element-wise absolute and relative tolerances; real end-to-end Kimi-Linear traces; and the evaluator kept outside the agent's container.
- **Search-cost ablation (14 hours on one B300):** single-shape-first strategy reached 1.85× with 248 hardware tests, 120 commits, 2.74M output tokens, 0.9 minutes per test; all-six-shapes-at-once reached 1.01× with 159 tests, 22 commits, 1.67M output tokens, 1.9 minutes per test. Total cost of the headline result is not reported.

## Why it matters for this survey

The rejected-candidate list is the most concrete public example of an optimizer improving its score without improving the workload, which is the revisit condition for increasing autonomy in the design checkpoints. The acceptance contract is specific enough to adopt as validation guidance. The search ablation shows that the search strategy, not only the model, changes the outcome by 1.8× under a fixed budget.

**Lineage:** same Carnegie Mellon / MLC / NVIDIA community as [TIRx Harness](tirx-harness.md), [KCoral](kcoral.md), [CAKE](cake.md), and [MetaKernelBench](metakernelbench.md); the TIRx Harness post (29 September) was published to support this result. One evidence family.

## Limits / caveats

- Speed is compared only with FlashKDA; Flash Linear Attention is compared on accuracy, not speed. Forward pass only, one GPU, one operator family.
- First-party report; the Humanize contribution is not isolated, and the headline run's total cost is not disclosed.
- Several per-workload chart values are ambiguous in the post, and the CuTe figure is labeled inconsistently across sections; cite the geometric means above.
- No serving or application measurement. The TIRx Harness was not yet formally released at posting time.
