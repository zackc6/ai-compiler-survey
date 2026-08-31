# Slide 29: Technical Prediction — Outside The Compiler (T6–T10)

Same band rhythm as slide 28, for techniques outside classical lowering. Spoken: these are equally first-class for Horizon A.

**T6 — Serving oracles / A/B → C2.**
Exists: Alive2-class local formal, FlashInfer-Bench + `apply()` into SGLang/vLLM, **GEAK v4** warm-server A/B with output parity after Amdahl triage. Claim: local formal is strong; product truth is serving statistics. Missing: whole-program checks, GPU race and FP nondeterminism oracles, multi-month *default-path* A/B with public p50/p90. Unlocks C2 — median and p90 on pinned traces, not headline kernels.

**T7 — Multi-IR corpora → selectors.**
Exists: Meta LLM Compiler pass-list data, **ComPile** production LLVM IR pile, KernelBook→TritonRL, DRTriton. Claim: data beats parameter count for IR actions; fluency corpora are *priors*, not contracts. Missing: versioned MLIR/Tile/StableHLO dumps plus *failed* and miscompile negatives — without negatives, RL reward-hacks. ComPile/IRCoder do not close GPU/MLIR gaps. Unlocks learned selectors, not one agent IR for all vendors (C4 partial).

**T8 — Benchmark ladder → C2, C9.**
Exists: KernelBench(-X) correctness+speed, FlashInfer-Bench serving-kernel rung, **llvm-bench** (334 LLVM middle-end crash/miscompile bugs). Claim: ladders force comparability — serving kernels and compiler-bug repair are different rungs. Missing: full IR→kernel→fused→serving chain with cost-to-compile on every rung. Unlocks both distributional gains (C2) and second-vendor coverage playbooks (C9).

**T9 — Provenance / HITL → C7.**
Exists: Magellan reviewable C++, Archer oracle review, **llvm-harness** / llvm-bench (true-fix below 22% after expert review), **SkCC** Anti-Skill Injection on untrusted `SKILL.md`. Claim: agents multiply drafts; process must scale review. Missing: CODEOWNERS + signed admit records + sandbox as standard practice. Unlocks demotion of generic forge AI for compiler prediction (C7). SkCC is T9 color for *skills*, not kernel CODEOWNERS.

**T10 — Workflow / skill compile / freeze → Horizon B.**
Exists: FlowCompile offline workflow compile, Auto freeze, **DeepSeek Harness** (`dsh`) as a shipping *runtime* (plugin kernel + append-only session log), **SIGIL ★** (`SKILL.md` → AG-IR → typed harness), **SKILL.state** (explicit \(\Sigma_t\); discard reasoning after a validated update). Also SkCC / SkVM / SkillSmith (2605.15215) — four skill-compile design points; do not average them. Claim: a live harness is not a compiled *compiler-product* IR; skill IRs are not T1. Missing: shared agent-graph IR compiled to frozen placements plus fail-closed **compiler** CI — Horizon B “control plane compiled,” not chat forever. Do not read DSH star counts or SkillsBench pass rates as T10 settlement.

Closing beat: outside-compiler techniques supply evidence, data, and process. Enhancing only `opt`/Inductor/Triton without T6–T10 leaves you with demos that cannot settle checkpoints.
