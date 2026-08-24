# CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA · Carnegie Mellon University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2608.12629](https://arxiv.org/abs/2608.12629) |
| **Evidence tier** | **A** — typed agent IR + evolving verifier/cost harness; serving-validated kernels |

## Key contributions

- **Cake IR:** typed, hardware-explicit *schedule* representation (warp roles, barriers, memory tiers, pipelines) that agents author instead of raw CUDA/PTX; lowering derives addresses/phases; **no layout algebra**.
- **Localized harness:** pre-compile gates for safety / hardware conformance / data consistency / schedule semantics; cost model ranks before GPU time; numerical + serving oracles admit.
- **Harness is a target of evolution:** recurring failures become verifier rules, IR primitives, cost-model calibrations, and tactics (test-gated on a kernel corpus). Agents also propose Blackwell primitives from docs/failures.
- Clean-start Flash-KMeans on B200 (80M tokens, 3 runs): Cake IR median **1.144×** tuned FlashML vs **0.928×** for direct CUDA/PTX.
- Frontier synthesis: Kimi Delta Attention **2.05×** geo-mean over official FlashKDA, **SGLang e2e** validated; dispatcher families 1.42–2.12× across 400+ shapes; four FlashInfer PRs.

## Summary

NVIDIA / CMU paper arguing that kernel *agents* and kernel *languages* have advanced separately: agents treat the compiler as a black box (error / pass-fail / latency), while tile DSLs hide expert schedules and low-level DSLs demand a layout calculus. Cake co-designs both. Agents edit Cake IR so hardware decisions are inspectable *before* codegen; the compiler returns localized diagnostics rather than a bit; the harness itself grows when a frontier workload exposes a missing capability. CUDA/PTX remain the execution ISA — Cake IR is the **agent-facing** schedule IR. Targets Ampere–Blackwell; separates single-shape evolution from dispatcher-backed library integration.

## Key takeaways

- Direct CUDA/PTX search loses to a typed schedule IR under a matched token budget — evidence for **constrained action spaces** (C3-B) on kernels, not only LLVM.
- Localized pre-compile diagnostics + cost ranking are the admit path; on-device measure remains ground truth (C6-B).
- **Compiler evolution** (new IR primitives / verifier rules from agent failures) is T5-class *toolchain* codesign, not autonomous tape-out (C10-B).
- Cake IR is another **L4 agent surface** alongside Triton / Tile / CuTe (**C4** more contested, not settled).
- Serving validation + FlashInfer upstream PRs move past single-shape theater (T6/T8 pressure; C2 still not a public p50/p90 default-path A/B).

## Why it matters for this survey

★ prediction-critical for **T1** (typed agent IR + diagnostic contract), **T2** (pre-compile gates), **T5** (IR/verifier evolution from failures), and **C3/C4/C6**. Strengthens the hybrid lean: agents own search on a schedule IR; compilers own legality, lowering, and measure. Cite with GEAK v4 (serving A/B) and Zomboss (compile-once machine semantics on emerging ASICs).

## Limits / caveats

- NVIDIA-only (Ampere–Blackwell); Cake IR is not a portable MLIR/StableHLO/Triton contract.
- Token budgets are large (tens of millions); model fixed to GPT-5.6-sol xhigh in reported runs.
- No public Cake tree at digest time — downstream users take FlashInfer CUDA, not a Cake dependency.
