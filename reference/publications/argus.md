# ARGUS: Agentic GPU Optimization Guided by Data-Flow Invariants

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | CausalFlow · HKUST · Tsinghua University · Stanford · UCAS · UC Riverside |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2604.18616](https://arxiv.org/abs/2604.18616) |
| **Evidence tier** | **A** — compile-time data-flow invariants + SMT admit; peak-competitive kernels on MI300X |

## Key contributions

- Diagnoses why agent kernels stay far from libraries: peak needs coordinated tiling / staging / pipelining / scheduling, but agents get **sparse pass/fail** tests and cannot localize global layout/alias/sync bugs.
- **Argus DSL:** tile-based Pythonic language (CuTe / TileLang-like) with **tag functions** (symbolic annotations through data/control flow) and **tag assertions** (conformity / separation at use sites).
- **Compile-time admit:** abstract interpretation over a **layout algebra** + SMT (Z3); tags never materialize at runtime. Failures return a counterexample: **thread · data element · program point**.
- **ICRL planner** treats prompts as mutable parameters; rewards = invariant violations + runtime; retrieves GPU tactics from a persistent knowledge base.
- AMD **MI300X**: GEMM / flash attention / MoE (authors: >90% of LLM-inference GPU time) reach **99–104%** of hand-optimized assembly TFLOPS (e.g. hipBLASLt / AITER); **2–1543×** geo-mean vs prior agentic systems on those families. KernelBench: **100%** Level 1 and **90%** Level 2 *correct*.

## Summary

April 2026 CausalFlow / HKUST / Stanford et al. paper that puts **data-flow invariants** (an information-flow idea) into the GPU agent loop. The compiler owns legality of how tiles are choreographed into MFMA layouts; the agent owns which optimizations to try and which invariants to draft. Complements [Cake](cake.md) (NVIDIA schedule IR, *no* layout algebra, localized gates) with the opposite IR bet: **keep a layout algebra** and discharge it with SMT. Prototype is MI300X; authors claim the design generalizes to NVIDIA. No public tree cited at digest time.

## Key takeaways

- Strongest **T2** kernel-side formal-ish admit below Triton: compile-time SMT + concrete counterexamples, not only golden/unit tests.
- **C3-B:** free CUDA/HIP search is the failure mode they measure (2–600× behind libraries); the constrained DSL + invariant feedback is the fix.
- **C4:** Argus DSL is another L4 agent surface (alongside Triton / Tile / CuTe / Cake IR / TileLang).
- **C2:** 99–104% of assembly on three families is Claim A *color*, not settlement — MI300X, selected ops, author protocol; KernelBench numbers are **correctness**, not `fast_p` / serving A/B.
- Path-insensitive analysis is the tractability caveat (can miss path-dependent bugs).

## Why it matters for this survey

★ for **T1** (tag/assert contract), **T2** (SMT/AI admit + counterexample feedback), **C3**, and **C4**. Pair with Cake (schedule IR, NVIDIA) and GEAK v4 (serving A/B, same AMD fleet). Reinforces hybrid: agents search; compiler verifies choreography before GPU time. Does **not** move the goal toward unconstrained LLM-as-`opt`.

## Limits / caveats

- Eval is MI300X kernel families + KernelBench correctness — not a multi-month default-path serving A/B (**C2** open).
- Path-insensitive; invariants are synthesized by the agent (wrong invariant ⇒ false confidence).
- 2–1543× vs “existing agentic systems” is family-dependent and baseline-sensitive; do not average into CompileIQ 2–3% docs.
- No public implementation URL in the preprint.
