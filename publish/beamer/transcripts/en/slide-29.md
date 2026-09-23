# Slide 29: Technical Prediction — Outside The Compiler (T6–T10)

Same band rhythm as slide 28, for techniques outside classical lowering. Spoken: these are equally first-class for Horizon A.

**T6 — Serving oracles / A/B → C2.**
Exists: FlashInfer-Bench + `apply()` into SGLang/vLLM, **GEAK v4** warm-server A/B, **Hyperloom** (AMD, Sep 2026) end-to-end remeasure with a fresh critic — the kernel phase is delegated to GEAK or KernelForge. Claim: local formal is strong; product truth is serving statistics. Missing: whole-program checks, GPU race and FP nondeterminism oracles, multi-month *default-path* A/B with public p50/p90. Hyperloom’s median 1.73× on 16 workloads is author-reported pressure, not C2 settlement. Unlocks C2 — median and p90 on pinned traces, not headline kernels.

**T7 — Multi-IR corpora → selectors.**
Exists: KernelBook→TritonRL, DRTriton, **AMDKernelVault** (Sep 2026: ~62k execution-verified HIP samples and ~40k Triton kernels). The distilled Qwen3-8B leads correctness on the paper’s benches and does not uniformly lead speed. ComPile and the Meta LLM Compiler remain the LLVM priors. Claim: data beats parameter count for IR actions; fluency corpora are *priors*, not contracts. Missing: versioned MLIR/Tile/StableHLO/Pallas dumps plus *failed* and miscompile negatives. Unlocks learned selectors, not one agent IR for all vendors (C4 partial).

**T8 — Benchmark ladder → C2, C9.**
Exists: KernelBench, **JAXBench** (TPU Pallas versus XLA and Tokamax), **KernelGenBench** (Triton across operator sources and six chips, with tokens per success). FlashInfer-Bench and llvm-bench remain other rungs. Claim: ladders force comparability. KernelGenBench’s lesson: AutoKernel accuracy can fall from 87% on NVIDIA to 25% on another chip, at about 5 million tokens per successful operator. Missing: full IR→kernel→fused→serving chain. These new rungs do not settle C9. Unlocks both distributional gains (C2) and honest cross-chip comparison.

**T9 — Provenance / HITL → C7.**
Exists: Magellan reviewable C++, Archer oracle review, **llvm-harness** / llvm-bench (true-fix below 22% after expert review), **SkCC** Anti-Skill Injection on untrusted `SKILL.md`. Claim: agents multiply drafts; process must scale review. Missing: CODEOWNERS + signed admit records + sandbox as standard practice. Unlocks demotion of generic forge AI for compiler prediction (C7). SkCC is T9 color for *skills*, not kernel CODEOWNERS.

**T10 — Workflow / skill compile / freeze → Horizon B.**
Exists on-slide: **SIGIL ★** (`SKILL.md` → AG-IR → typed harness), **SKILL.state** (explicit \(\Sigma_t\)), and **Hyperloom**’s state file (the mission is rebuilt each turn; the `SKILL.md` pack is not the oracle). FlowCompile, Auto, and DeepSeek Harness stay in the narrative. Claim: a live harness is not a compiled *compiler-product* IR; skill IRs are not T1. Missing: shared agent-graph IR compiled to frozen placements plus fail-closed **compiler** CI. Do not read Hyperloom’s serving speedups as T10 settlement.

Closing beat: outside-compiler techniques supply evidence, data, and process. Enhancing only `opt`/Inductor/Triton without T6–T10 leaves you with demos that cannot settle checkpoints.
