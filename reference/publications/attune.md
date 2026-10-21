# ATTUNE: Agentic Throughput Tuning for LLM Training

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Amazon (amazon-science) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [arXiv 2610.17528](https://arxiv.org/abs/2610.17528) · [HTML](https://arxiv.org/html/2610.17528v1) · [amazon-science/attune](https://github.com/amazon-science/attune) |
| **Evidence tier** | **B** — a training-recipe tuner, not a compiler, but it runs the matched-budget comparison this guide asks for (one coding agent against Bayesian optimization and random search under a common GPU-hour budget) in an adjacent systems-tuning domain; adjacent mechanism until a compiler-level counterpart exists |
| **Version / reviewed** | v1, 13 October 2026; reviewed 19 October 2026. First pass: abstract and repository README (marked **[abstract]** or **[README]**). Second pass (Claude's review run, 19 October): HTML Appendix D and Table 3 read, confirming B200 hardware, the 30-run matched budget, the GLM-4.5 comparison numbers, and the payback formula (bullet below). The lever catalogue, OptiCo and Bayesian-optimization configurations, and the remaining per-campaign tables are still unverified |

## Key contributions

- **A single coding agent as tuner.** Given a working training recipe and a GPU-hour budget, the agent runs short fixed-shape benchmark jobs (20 steps, scored on steps 5–19), profiles them, reads framework source, and "changes one lever at a time," guided by "a catalog of lessons from past campaigns" that it extends during a campaign. Diagnosis targets named in the README: exposed communication, pipeline bubbles, memory, kernel launches. Stack: Megatron-LM with slime recipes as RayJobs on Kubernetes, driven by Claude Code.
- **Correctness gate.** A configuration check classifies every changed argument as numeric, placement, or an allow-listed same-math swap (unlisted arguments count as numeric and are rejected), plus a 20-step loss-curve convergence check against the baseline using Megatron-Bridge thresholds. A recipe ships only if it passes both. This is the authors' answer to the failure mode that "a configuration can run to completion while it silently changes training."
- **TrainingThroughputBench.** A released leaderboard of the fastest known recipes for mixture-of-experts models up to 744B parameters on up to 256 GPUs, each with throughput, cost per million tokens, and a passed correctness check.

## Summary

Evaluated on four models held out from development at 64–128 GPUs, each starting from the strongest public recipe run on the authors' stack. **[abstract]** Mean throughput gains of 6.7% on Llama-3.1-405B (best campaign 11.9%) and 33.9% on GLM-4.5 (best 54.7%), whose public recipe "was written for H100"; Mixtral-8x22B's recipe is kept unchanged "where nothing it finds clears the noise band." Under a common GPU-hour budget it "beats OptiCo, Bayesian optimization and random search on GLM-4.5 and MiniMax-M2; on GLM-4.5 its mean gain is more than four times the best alternative's at less than half the GPU-hours, and on both models its tuning pays for itself within a day of training."

## Key takeaways

- **[abstract]** Matched-budget result: agent gain more than 4× the best of OptiCo, Bayesian optimization, and random search on GLM-4.5, at under half the GPU-hours. This is the comparison type the guide's first thesis-test row requires, in a configuration-tuning space rather than a code-synthesis space.
- **[abstract]** Gate: "rejects no legitimate run and catches 16 of 24 faulty runs, missing only ones that barely move the 20-step loss." Eight of twenty-four faults escape a 20-step convergence check — a measured limit of short-horizon correctness gates.
- **[abstract]** Ablation: "ties its best campaigns to one of its search rules: retrying an out-of-memory layout with recomputation." Much of the headline gain may come from one rule a conventional tuner could encode.
- **Payback (Appendix D, checked 19 October 2026 by Claude's review run):** payback days = campaign GPU-hours / (GPUs × 24 × (1 − 1/(1 + gain))); it counts only the GPU-hours the campaign used. LLM cost is reported separately (about $112 per GLM-4.5 campaign and $58 per MiniMax-M2 campaign at list price) and is not in the formula. Matched budget: 30 baseline runs per model (1,880 GPU-hours GLM-4.5, 530 MiniMax-M2, B200); GLM-4.5 means over three campaigns: ATTUNE +33.9% at 669 GPU-hours, random search +7.8%, BO+pre-filter +3.9%, OptiCo 0.0%.
- **[README]** Campaign LLM cost "about $60 to $110 at list price"; a candidate replaces the leader only if it beats it by more than the noise band.
- **Denominator:** training tokens per second per GPU over a fixed-shape 20-step window, relative to the best public recipe; not end-to-end training time, not model quality beyond a short loss match.

## Why it matters for this survey

ATTUNE sits outside the compiler but inside the thesis test. It compares one agent with declared non-agent search methods under a common budget and reports both the win and the campaign where the agent found nothing, which is the shape of evidence this guide asks agent papers to produce. Three qualifications keep it adjacent. The action space is recipe configuration (parallelism layout, recomputation, and similar levers), where an out-of-memory retry rule explains the best campaigns, so the result says more about encoding operational knowledge than about synthesis. The baselines are black-box optimizers on the same knobs, not a structured systems-tuning framework with the same knowledge. And the correctness contract is a 20-step loss match, far weaker than the numerical or equivalence contracts a kernel compiler needs. For the per-workload-versus-offline question it adds a clean payback statement: the authors report that a campaign's GPU-hours (model-call cost excluded) are repaid within a day of training on the two models tested, which is the reuse condition the guide names. Read with [Hyperloom](hyperloom.md) (agentic inference-optimization harness at AMD) and the controller-improvement sources, since the "catalog of lessons from past campaigns" is a memory-adaptation mechanism in the sense of the controller-improvement question.

## Limits / caveats

- Full text only partly read: B200 hardware, the matched budget, GLM-4.5 campaign means, and the payback formula are checked; cluster scale per experiment, OptiCo and Bayesian-optimization configurations, and the lever catalogue are unverified.
- Four held-out models, one stack (Megatron-LM with slime), one agent model family; the strongest gains are on a recipe written for different hardware, so part of the headroom is porting, not optimization.
- Short-window throughput and a 20-step loss match do not establish converged model quality; the gate misses one third of injected faults.
- Experiment that would settle more: give the Bayesian-optimization arm the same lesson catalogue as rules (including the out-of-memory-retry rule) and rerun under the same GPU-hour budget; if the gap closes, the agent's value was the knowledge, not the reasoning.
