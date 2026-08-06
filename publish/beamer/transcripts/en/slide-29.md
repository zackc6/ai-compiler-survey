# Slide 29: Technical Prediction — Outside The Compiler (T6–T10)

Same band rhythm as slide 28, for techniques outside classical lowering. Spoken: these are equally first-class for Horizon A.

**T6 — Serving oracles / A/B → C2.**
Exists: unit/golden/Alive2 ladder, FlashInfer-Bench + `apply()`, VibeServe early serving traces. Claim: local formal is strong; product truth is serving statistics. Missing: whole-program checks, GPU race and FP nondeterminism oracles, multi-month *default-path* A/B. Unlocks C2 — median and p90 on pinned traces, not headline kernels.

**T7 — Multi-IR corpora → selectors.**
Exists: Meta LLM Compiler pass-list data, KernelBook→TritonRL, DRTriton. Claim: data beats parameter count for IR actions. Missing: versioned MLIR/Tile/StableHLO dumps plus *failed* and miscompile negatives — without negatives, RL reward-hacks. Unlocks learned selectors, not one agent IR for all vendors (C4 partial).

**T8 — Benchmark ladder → C2, C9.**
Exists: KernelBench(-X) correctness+speed, FlashInfer-Bench serving-kernel rung. Claim: ladders force comparability. Missing: full IR→kernel→fused→serving chain with cost-to-compile on every rung. Unlocks both distributional gains (C2) and second-vendor coverage playbooks (C9).

**T9 — Provenance / HITL → C7.**
Exists: Magellan reviewable C++, Archer oracle review. Claim: agents multiply drafts; process must scale review. Missing: CODEOWNERS + signed admit records + sandbox as standard practice. Unlocks demotion of generic forge AI for compiler prediction (C7).

**T10 — Workflow compile / freeze → Horizon B.**
Exists: FlowCompile offline workflow compile, Auto/AgentFlow freeze, VibeServe early. ADG (Agent Dependency Graph) check and fail-closed CI are the target. Missing: shared agent-graph IR compiled to frozen placements — Horizon B “control plane compiled,” not chat forever.

Closing beat: outside-compiler techniques supply evidence, data, and process. Enhancing only `opt`/Inductor/Triton without T6–T10 leaves you with demos that cannot settle checkpoints.
