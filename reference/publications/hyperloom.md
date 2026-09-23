# Hyperloom: A Multi-Agent Harness for Autonomous Inference Optimization on AMD GPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | AMD ROCm blog |
| **Type** | company |
| **Group** | Commercial products & proposals |
| **Link** | [https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html](https://rocm.blogs.amd.com/software-tools-optimization/hyperloom-optimization/README.html) |
| **Evidence tier** | **A** — e2e Instinct harness; kernel phase is delegated; state file + critic admit, not a transcript |

## Key contributions

- Closed loop on AMD Instinct for vLLM, SGLang, and xDiT: prelude baseline → framework flags/patches → **one** kernel backend → sweep across concurrency and sequence lengths → recipe knowledge base. Posted **2026-09-21**. Code: [AMD-AGI/Hyperloom](https://github.com/AMD-AGI/Hyperloom) (MIT). Docs: [ROCm Hyperloom](https://rocm.docs.amd.com/projects/hyperloom/en/latest/index.html).
- Kernel phase is not the harness. It delegates to **GEAK** (selects kernels itself) or **KernelForge** (bounded lanes on trace-picked kernels). Only one backend per phase. Hyperloom **re-measures** every accepted kernel end to end; a backend’s claimed speedup is unverified until then.
- Control plane: orchestration agent is refreshed from a **state file** (baseline, best, gain, time left), not from the growing transcript. A fresh **Critic** rules on every keep-or-revert. Patches land in a git worktree as a diff and commit only on improvement. A `SKILL.md` workload optimizer is the pack format ([agentskills.io](agent-skills-spec.md) sense), not the oracle.
- Author table, **16** unattended workloads: gains **1.35×–7.31×**, **median 1.73×**. In the published Llama-3.1-8B session, framework changes (attention backend, FP8, speculative decoding) dominate; the rewritten kernel is a smaller add. Kernel share is workload-dependent (about half the gain on one DeepSeek-V4-Pro run, author).

## Summary

AMD’s September serving harness sits above GEAK the way an e2e controller sits above a kernel agent. The mechanisms that matter here are the ones the blog says prompts cannot fix: goal drift, amnesia across sessions, and unsafe edits. The state file is the mission; the critic and the coordinator’s own benchmark are the admit; the recipe KB is warm start, not a hard constraint. That is job (a) at serving-graph scope, with classical frameworks still producing the binary.

## Key takeaways

- **T6** exists-cell: another vendor e2e keep/revert loop after GEAK v4. Still not multi-month default-path p50/p90 (**C2** open). Median 1.73× is author-reported on 16 workloads.
- **T10 / P2** color, in scope because a kernel oracle is mounted: session state is reconstructed, specialists are discarded, and `SKILL.md` is sense (1)+(2). It is not SKILL.state and not a compiler-graph IR.
- **C9** unchanged. This is peak serving on Instinct, not coverage-first ASIC bring-up. KernelForge is an AMD lane inside this blog, not [Kernel Forge](kernel-forge.md) (Michigan) and not [ForgeMegakernel](forgemegakernel.md).
- Amdahl: a kernel agent can be the wrong first spend. The Llama session’s tokens-per-GPU jump is mostly framework config.

## Why it matters for this survey

★ for **T6** and as a shipping mount of skill packaging onto a measured serving loop. Pair with [GEAK v4](geak-v4-github.md). Do not treat the takeaway “14,000 models” as the measured table — that count is not in the 16-row eval.

## Limits / caveats

- Vendor blog. Stage attribution in one session is not a causal ablation across the fleet.
- Accuracy “holds” is the blog’s gate; the public post does not specify the numerical tolerance or the A/B window length.
- KernelForge has a repo link from the blog and no separate digest in this wave.
