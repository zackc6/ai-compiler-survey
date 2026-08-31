# SkillSmith: Compiling Agent Skills into Boundary-Guided Runtime Interfaces

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AetherHeart Tech · Renmin University of China · UC San Diego |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2605.15215](https://arxiv.org/abs/2605.15215) |
| **Also** | [https://github.com/AetherHeart-AI/Aeloon](https://github.com/AetherHeart-AI/Aeloon) |
| **Evidence tier** | **B** — skill compilation to *boundary contracts* (not a workflow IR); SkillsBench is not a compiler ladder |

## Key contributions

- Diagnoses two wastes when a matched `SKILL.md` is stuffed into the reasoning loop: irrelevant context and repeated skill-specific planning.
- **Boundary-first compile:** offline, classify the package shape (workflow / dispatcher / indexed guidance) → extract operators, input schemas, policy constraints, validation evidence, fallbacks → a **runtime interface**, not a unified AG-IR/SkIR.
- Progressive disclosure of the compiled handle; lossless capsule back to the source package when the lower is incomplete. Author: −57% solve-stage tokens vs raw skills; also beats [SkVM](skvm.md) on tokens/time on the same SkillsBench slice.

## Summary

May 2026 AetherHeart / RUC / UCSD paper in the same **skill compilation** wave as [SIGIL](sigil.md) (mandated CFG), [SkCC](skcc.md) (portable SkIR + injection), and [SkVM](skvm.md) (AOT/JIT across models). SkillSmith’s bet is the *ABI*: expose a minimal guarded interface and keep the rest out of the prompt. That is P1-shaped packaging for **skills**, not the kernel admit record `{graph_hash, hw, compiler, oracle, digest}`. Code at Aeloon.

## Key takeaways

- **T10 design points now four, not one:** compliance harness (SIGIL) · portable IR (SkCC) · capability VM (SkVM) · boundary ABI (SkillSmith). Do not average them.
- **P1/P23:** compile-then-disclose cuts tokens the same *way* Auto/FlowCompile freeze agent graphs — still not serving \(F\).
- **Name collision:** this paper ≠ SkillSmith *Co-Evolving Skills and Tools* (arXiv:2606.01314) ≠ generic GitHub “SkillSmith” repos. Cite **2605.15215**.

## Why it matters for this survey

Closes the “SIGIL named SkillSmith with no digest” hole (same miss class as a named kernel DSL). Substrate only. Does **not** move C2/C6 or add an L-band.

## Limits / caveats

- SkillsBench / Agent-H / Codex / OpenCode — not KernelBench or llvm-bench.
- Boundary contract ≠ Cake IR ≠ T1 agent-compile RFC.
- Compile-time LLM cost is amortized in the paper; product CI still needs replay keys (T3).
