# Compiler-Grounded Hierarchical Diagnosis for LLM-Based Triton Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Huawei Technologies |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://arxiv.org/abs/2607.23089](https://arxiv.org/abs/2607.23089) |
| **Evidence tier** | **A** — compiler-grounded agents on Ascend NPU Triton |

## Key contributions

- Reframes LLM kernel opt as **progressive cross-layer diagnosis**: pattern triage → profiling → IR attribution → compiler-source escalation → evidence-backed Triton rewrites.
- Implemented for **Triton on Ascend NPUs** (NPUKernelBench-derived Ascend 950 suite).
- Reports geo-mean **4.35×** / median **2.73×** initial→optimized Triton on 37 converted ops (distribution reported; not uniform).
- Offline retrospective synthesis builds reusable pattern families across operators.

## Summary

Huawei systems paper arguing surface compile/profile feedback is insufficient on emerging accelerators: agents must ground rewrites in IR and backend pass constraints. Escalation hierarchy keeps expensive compiler-source reasoning rare — a design pattern for agentic compilers on non-CUDA silicon.

## Key takeaways

- Codesign implication: opaque NPU backends force **compiler-in-the-loop agents**, not CUDA-pretrained one-shot codegen.
- Hierarchy is a concrete control-plane API (when to escalate) for future agentic compilers.
- Supports **C3-B** (constrain/evidence) while still doing source rewrites.
- Distribution reporting is the right anti-pattern vs cherry-picked speedups (**C2**).

## Why it matters for this survey

Extends agentic-compiler evidence beyond NVIDIA/AMD to **NPU codesign**. Complements TritorX/KernelEvolve (Meta MTIA) with Ascend diagnosis depth.

## Limits / caveats

- Cohort after failed Torch→Triton conversions; scope is converted ops.
- Causal ablation of hierarchy left to future work.
