# Slide 25: Technical Prediction — Outside The Compiler (T6–T10)

Five outside-compiler techniques:

6. **T6** Serving oracles / A/B — FlashInfer-Bench serving traces + `apply()` raise pressure; still missing multi-month default-path A/B. Unlocks C2.
7. **T7** Multi-IR corpora — KernelBook → KernelLLM/TritonRL; DRTriton synthetic. Missing: MLIR/Tile/StableHLO + negatives. Unlocks selectors beyond LLVM-centric models.
8. **T8** Benchmark ladder — FlashInfer-Bench closes a serving-kernel rung, not the full IR→fused→serving ladder with cost-to-compile. Unlocks honest C2/C9.
9. **T9** Provenance / HITL — Magellan reviewable C++, Archer; missing CODEOWNERS + signed admit. Unlocks trusted-base shipping.
10. **T10** Workflow compile/freeze/place — FlowCompile/Auto/AgentFlow/VibeServe exist early; productized shared IR + fail-closed CI → Horizon B.
