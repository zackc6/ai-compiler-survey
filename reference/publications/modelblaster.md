# ModelBlaster: Closing the Performance Gap through Learning-Augmented Agents Across Models, Kernels and Hardware Backends

| Field | Value |
|---|---|
| **Year** | 2026 (arXiv v1, 3 November 2026) |
| **Org** | NVIDIA, with UC Berkeley for two authors (affiliations as read in the full text by both agents, Review thread 10–11 November 2026) |
| **Publisher** | arXiv (2611.04104); `ucb-bar/ModelBlaster` on GitHub for the RISC-V flow |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2611.04104](https://arxiv.org/abs/2611.04104) · [HTML v1](https://arxiv.org/html/2611.04104) · [ucb-bar/ModelBlaster](https://github.com/ucb-bar/ModelBlaster) |
| **Evidence tier** | **A** — agreed by both agents (10–11 November): a memory-augmented agent loop run across three hardware backends with a conventional-compiler arm (TVM) and a vendor-compiler arm (QNN), which informs the cross-target and supplied-knowledge decisions. Tier is decision relevance, not a confidence upgrade: none of its comparators is a matched-budget strong search baseline |
| **Version / reviewed** | arXiv v1 HTML read in full by ChatGPT (10 November, 11:41 HKT and 11 November, 09:28 and 10:27 HKT) and by the Claude GitHub Action (10 November 03:53 and 04:47 UTC; 11 November 01:33 and 02:45 UTC, characters 0–147,802); every number below was reported by both reads and reconciled in the Review thread. The 16 November sweep runner could not reach arXiv; it read the `ucb-bar/ModelBlaster` repository (head `811ef1d`, 30 October 2026) by shallow clone. Digest wording for the comparator classes, the three operator subsets, the 46/48 denominators and per-platform cost was agreed in the thread before this digest was written. |

## Key contributions

ModelBlaster extends [KernelBlaster](kernelblaster.md) (NVIDIA · UC Berkeley; continual cross-task CUDA optimization via memory-augmented in-context reinforcement learning) from single kernels to models and to three hardware backends: CUDA on NVIDIA GPUs, OpenCL on a Qualcomm Adreno 650, and RISC-V vector (RVV) intrinsics on a Saturn vector core. One harness runs a graph-level flow (the "model-level optimizer") and a kernel-level loop with a persistent, typed performance-state memory; the same agent and memory are reused across targets. The repository `ucb-bar/ModelBlaster` is the RISC-V side of the flow: PyTorch → quantization (fp32/fp16/int8, mixed precision) → per-operator kernel generation (reference, hand-curated, or LLM-written, with an optional verify-then-beam-search optimize pass over spike or FireSim cycle counts) → Zephyr build → validation on spike, RTL simulation or FireSim, with a persistent cache of verified kernels and targets including Gemmini and a Saturn outer-product unit. Its README reports no measurements and does not cite the paper; the platform match (Saturn V256D128, FireSim) is the basis for treating it as the paper's RVV artifact.

## Summary

**CUDA (Table 3; §4.2, §4.4).** Geometric-mean speedups over PyTorch eager of **1.850 / 5.576 / 5.182** on KernelBench Levels 1–3 on an **L40S**, and **1.69×** on SOL-ExecBench (the 115-problem aggregate in §4.2; Table 3 lists Level 1 2.241 and Level 2 1.138) on a **B200**. The introduction says "On B200, ModelBlaster achieves … 1.85×", which contradicts the table; the abstract is ambiguous. The table-supported hardware is recorded and the discrepancy flagged. §4.4 and Appendix D.3 give the Level-3 result over **46** problems; Appendix C.2 bills the Level-3 headline sweep as **48** problems for about **$3,500** at list prices (about **$73 per problem**, the paper's own denominator). The paper does not reconcile the two counts; both are recorded as given. A separate 22-problem CUDA sample run with gpt-5.1 gives geometric-mean token use of 2,297,652 (Level 1) and 1,600,997 (Level 2) per problem.

**Adreno 650, FP16 KernelBench Level 1 (Appendix A.1).** Three comparisons on three *different* operator subsets, which must not be read as one three-way benchmark: ModelBlaster over the **QNN SDK compiler** (Qualcomm's commercial OpenCL toolchain, applied to 52 operators) **5.80×, n = 42**; ModelBlaster over **TVM's default Adreno pipeline "without per-operator autotuning"** (TVM covers 42 of the 52) **1.69×, n = 39** — **2.30×** on the 16 compute-bound operators and **1.50×** on the 32 operators that take TVM's optimized pipeline; TVM over QNN **3.36×, n = 37**, and **1.21×** on the 8 compute-bound operators. TVM wins on several operators. The paper leaves autotuned TVM to future work, noting it "would improve TVM at a large offline search cost".

**RISC-V vector, Saturn V256D128 in FireSim (Appendix A.2).** Against ExecuTorch with XNNPACK across 70 common kernels: **44 of 70 wins, 2.74× geometric mean, 1.39× median**; Conv2d 1 of 11 wins at 0.09×, Conv1d 0 of 5 at 0.06×. Cycles measured on a single core in FireSim, not fabricated silicon; XNNPACK's packing, microkernel and dispatch capabilities are unavailable to the generated-kernel harness, so neither the wins nor the losses are a controlled agent-versus-non-agent result.

**Ablations.** The memory-versus-fresh ablation (fresh memory **1.67× slower**) was run on "an earlier version of the flow" (Appendix B.1) that the paper says is not comparable with the L40S headline sweeps. The graph-flow ablation uses eight Level-3 problems with one seed each, and the paper says differences of about 10% are within noise. **No LLM spend, tokens, wall-clock or engineering effort is reported for the Adreno or RVV experiments.**

## Key takeaways

- **Comparator classes differ, and none tests the thesis's first row.** QNN is a vendor compiler/SDK stack; TVM is an open, rule-based default pipeline with no per-operator autotuning; ExecuTorch/XNNPACK is a deployment framework with tuned microkernels; PyTorch eager is a framework baseline. None is a matched-budget tuned-search arm. TVM is the closest compiler-pipeline comparison and shows headroom over default rules only. A baseline that untuned TVM beats by 3.36× is not strong on this operator set.
- **Denominators.** CUDA Level 3 is model latency over PyTorch eager on 46 KernelBench models (not deployment integration); Adreno and RVV are per-operator kernel ratios. No serving or training throughput is reported.
- **Cost belongs to CUDA only.** About $3,500 for 48 Level-3 problems on an L40S; do not assign it to either embedded target. The Adreno result is evidence of performance portability against a default pipeline, not of productivity or cost-effectiveness.
- **Memory effect is unquantified under the current flow.** The 1.67× figure is from an earlier flow and cannot be attributed to the persistent knowledge base in the headline configuration.
- **Cross-target reuse is "the same harness demonstrated across three backends"**, not an isolated memory benefit or a quantified engineering saving.

## Why it matters for this survey

ModelBlaster is the broadest public cross-backend agent flow with a conventional compiler in the comparison, which is why both agents rated it Tier A for the cross-target and memory decisions. For the §5.3 table it moves nothing: row 1 (adaptive reasoning adds value over strong search) is untested in either direction because no comparator is budget-matched; row 5 (controller improvement) is informed only by an earlier-flow memory ablation; row 6 has no interaction-controlled design. For the §5.5.1 running tally it is a **lead, not a candidate**: kernel-level and model-latency results against eager, with no compiler or serving integration that ships a new action or backend. For the §6 reuse question and the portability objective, the Adreno and RVV results are real evidence that one harness can reach three targets, with the deployer's objection kept in view: on a phone or an embedded core the shipped vendor stack *is* the baseline, and beating it is the portability result the secondary objectives ask for, even though it does not test the thesis.

Lineage: KernelBlaster (same authors and method); `ucb-bar` also hosts mlirAgent. Read beside [KForge](kforge.md) (cross-platform kernel generation), [TritorX](tritorx.md) (operator coverage on a new ASIC) and [ACT](act-backend.md) (non-LLM backend generation), and beside [AKLR](aklr.md) for the supplied-knowledge question.

**Experiment that would settle the row-1 question (agreed by both agents):** MetaSchedule-tuned TVM and an optimized QNN configuration on the same 39 Adreno operators, with the same acceptance contract, operator coverage and GPU wall-time budget, the full LLM, compile and profile spend and time-to-result reported per operator, equal implementation affordances on RVV, the memory on/off ablation rerun under the current flow, and an application-level evaluation.

## Limits / caveats

- Hardware inconsistency between the introduction/abstract (B200) and Table 3 (L40S for KernelBench; B200 for SOL-ExecBench).
- Untuned TVM; QNN weak on much of the operator set; XNNPACK comparison under unequal affordances; eager as the CUDA baseline.
- 46 evaluated versus 48 costed Level-3 problems, unreconciled; one seed per graph-flow ablation problem; no Adreno/RVV cost.
- RVV numbers are simulator cycles on one core; the repository's own README warns that spike "is blind to cache locality" and that FireSim should be used for memory-realistic profiling.
- The 16 November sweep did not re-read the paper; the digest relies on two independent full-text reads that agree on every figure used.
