# AKLR: Agentic Kernel Library for ROCm (agent-first kernel library with a knowledge-base on/off study)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD (AMD-AGI organization on GitHub) |
| **Publisher** | GitHub repository (`.github/README.md` and `docs/kernel_rosetta_stone.md`) |
| **Type** | code |
| **Group** | GPU kernels & inference compilers |
| **Link** | [AMD-AGI/AKLR](https://github.com/AMD-AGI/AKLR) · [study pinned at `a12866b`](https://github.com/AMD-AGI/AKLR/blob/a12866b1e40e86ea6aff7ac24cbe5634132f6b2e/docs/kernel_rosetta_stone.md) |
| **Evidence tier** | **A** — a public same-agent *knowledge-base on/off* ablation for kernel search (supplied-knowledge assistance, not learned memory); informs the memory-versus-procedure question and the 2027 controller checkpoint's supplied-knowledge arm, but has no fixed-controller or non-agent arm and no application denominator |
| **Version / reviewed** | Repository created 2026-10-29 00:24 UTC (authenticated metadata check by ChatGPT, 8 November 2026). Figures below are from `docs/kernel_rosetta_stone.md` at commit `a12866b` (blob `5379138388f368c0bf941cc9bb6c869755dcd62a`), independently fetched and reconciled by both agents in the Review thread on 8 November 2026 (entries 10:22 HKT, 02:26 UTC, 12:07 HKT, 04:10 UTC). Not re-fetched by the 9 November sweep run (fetch permission unanswered); **re-fetched 9 November 2026 (~01:25 UTC) by the Claude GitHub Action** at the same pinned commit: the GEMM figures (5 h 20 min / about $52 against 14 h 46 min / about $205; final 1.300× at 11 h 36 min and 1.289× at 15 h 50 min; 12 h and 24 h budgets) held, and the acceptance-protocol and knowledge-entry notes below come from that read. |

## Key contributions

AKLR describes itself as "Agentic Kernel Library for ROCm, the agent-first kernel library". Instead of shipping only compiled kernels, it packages three things an optimization agent can read: a **knowledge base** of hardware and kernel-design notes for AMD Instinct GPUs, **skills** (reusable procedures for the agent), and **example kernels** (178 in the GEMM study, 168 in the mixture-of-experts study; the two bundles differ, so no single "168-kernel" treatment exists). The claim being tested is that an agent given this material reaches a target speed sooner and cheaper than the same agent without it.

The repository's study (`docs/kernel_rosetta_stone.md`) is the evidence. It runs one agent, Claude Opus 5.5, on one AMD MI355X GPU per arm, against the vendor library AITER as the baseline, and compares a **with-bundle** arm (knowledge + skills + example kernels) to a **no-bundle** arm on two tasks. The score is a kernel-level mean speedup over AITER across 13 problem sizes. There is **one run per arm per task** ("This was one run each way").

## Summary

**Task 1 — bf16 GEMM**, N = 16384, K = 2048, 13 M sizes (M = 1–4096). The document states that AKLR had no kernel for this shape and that the knowledge base never mentions it. Budgets were unequal: 12 h with the bundle, 24 h without.

| Measure | With bundle | Without bundle |
|---|---|---|
| Time and estimated spend to reach 1.28× over AITER | 5 h 20 min, about $52 | 14 h 46 min, about $205 |
| Score at 8 h | 1.286× | 1.177× |
| Final score (time, spend) | 1.300× (11 h 36 min, about $133) | 1.289× (15 h 50 min, about $230) |

**Task 2 — GLM-5.2 mixture-of-experts layer**, MXFP4 weights, the shard shape used when "the model is split across four GPUs" (tensor-parallel 4), 13 batch sizes (1–4096 tokens). Each arm ran on **one** MI355X for 15 h; both arms ran at the same time. Kernels for this model were removed from both copies of the library, but related mixture-of-experts designs at other splits remained in the knowledge base.

| Measure | With bundle | Without bundle |
|---|---|---|
| Time and estimated spend to reach 1.165× over AITER | 7 h 24 min, about $87 | 14 h 54 min, $170 |
| Score at 8 h | 1.176× | 1.047× |
| Score at 10 h | 1.184× | 1.056× |

The 1.165× threshold is **defined after the fact** as the best score the no-bundle arm ever reached, in its last round at 14 h 54 min; the baseline's time-to-threshold is therefore its whole run by construction. The document gives no final score or total spend for the with-bundle mixture-of-experts run beyond the 10 h point. Spend-to-threshold is estimated from total spend, not metered at the threshold.

## Key takeaways

- **The cleaner numbers are the matched-time comparisons.** At 8 h the bundle is ahead by 0.109 (GEMM) and 0.129 (mixture of experts); at 10 h the mixture-of-experts gap is 0.128. The two readings come from the same single run per arm, so the steady gap rules out a one-timepoint artifact within that run but is not a replication. The time-to-threshold ratios (about 2.8× and 2.0× in wall-clock, about 3.9× and 2.0× in spend) are weaker because the GEMM budgets differ and the mixture-of-experts threshold was chosen retrospectively.
- **Reported final GEMM scores are close.** 1.300× against 1.289× after 11.6 h and 15.8 h; with one run per arm and no uncertainty estimate, these runs cannot establish whether attainable quality differs. What the study does show on this task is a time and spend saving to a fixed target.
- **Denominator.** All scores are kernel-level means over 13 sizes against AITER on one GPU. Nothing is integrated into a compiler or serving stack, and no application throughput is reported.
- **Treatment is a bundle.** Knowledge, skills and example kernels are switched together. The study cannot say which part carries the effect, and a reference-library gain is not a procedure improvement.
- **Acceptance protocol (read 9 November 2026 at `a12866b`).** Each round the agent must "check it is still correct, time it" and "keep the change only if it beats the best so far by more than the noise"; the repository's tools "check each kernel for correctness". The document states **no numeric tolerance, no description of the correctness test inputs and no noise threshold**.
- **Knowledge-entry format.** The knowledge base is 123 pages organized by operator (GEMM; mixture of experts and grouped GEMM; attention) with 16 case studies of delivered kernels, holding 1,204 findings "each recording how it was measured and where it came from". The study does not say whether the findings were written by people or distilled from earlier agent runs.
- **Size range.** On GEMM, "at the largest sizes (M ≥ 1024) neither run improved on AITER"; the gains are at small and medium M.
- **Still not reported:** regressions (the score tables show best-so-far, which hides drops), rejected candidates and run-to-run variance.

## Why it matters for this survey

AKLR is the right *shape* of evidence for the controller-improvement row of the thesis test (§5.3) and for the §6 question "Should the controller improve itself, and at what scope?": supplied knowledge lowering search cost to a fixed target. It is a public experiment that resembles the **supplied-knowledge arm** named in the September 2027 controller checkpoint, which asks that a curated-reference gain not be scored as a procedure improvement. Read that way, AKLR is evidence about **supplied-knowledge assistance** — close to, but not the same as, the memory-adaptation choice in §6, because the bundle is supplied before the search rather than learned during it (the study does not say how its 1,204 findings were produced) — and not about a controller-procedure change: the same agent runs in both arms, so the weakening clause "against a fixed controller with equivalent memory and resources" is exactly what the no-bundle arm lacks.

It therefore does not move the row in either direction, and it enters the 2027 running tally as **recorded, not qualifying** (kernel-level, no compiler/serving integration, no application evaluation, one organization). It belongs with the same organization's [Hyperloom](hyperloom.md), [GEAK](geak-v4-github.md) and [AMDKernelVault](amdkernelvault.md) as one AMD evidence family, and should be read beside [KDA²](kda2.md) (NVIDIA's agent-plus-expert-design kernel loop) and [D2K-Bench](d2k-bench.md), which also measure what supplied expert design knowledge adds to a frontier agent.

**Experiment that would move the row:** the same knowledge-on/off ablation on held-out GEMM, attention and mixture-of-experts *families*, repeated seeds, equal budgets and toolchain versions, separate knowledge-only / skills-only / kernels-only / combined arms, a fixed controller with equivalent memory, and a strong non-agent tuner (hipBLASLt tuning or a Magnitude-class search) under the same budget, with regressions and end-to-end acceptance reported. Rerunning the same two tasks would not.

## Limits / caveats

One run per arm; unequal GEMM budgets (12 h against 24 h); retrospective mixture-of-experts threshold; spend estimated from totals; treatment is a bundle; related mixture-of-experts designs remained in the knowledge base, so the transfer is within a close family rather than to a new workload family; no non-agent tuner and no fixed-controller comparator; kernel-level means only; one model, one GPU type, one organization; the document itself says "This was one run each way". Every figure above was verified by both agents at the pinned commit on 8 November; the GEMM figures, acceptance wording and knowledge-entry format were re-read on 9 November. The study makes no priority claim. Correctness tolerances and test inputs are not stated.
