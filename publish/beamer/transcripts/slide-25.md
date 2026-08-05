# Slide 25: Technical Prediction — Outside The Compiler (T6–T10)

Same rhythm as slide 24: technique + unlocks, then Exists, then Missing.

6. **T6 Serving oracles / A/B** → C2  
   Exists: unit/golden/Alive2 · FlashInfer-Bench + `apply()` · VibeServe judges  
   Missing: whole-program / GPU-race / FP contracts; multi-month default-path A/B  
   (FlashInfer-Bench = pressure, not C2 settlement.)

7. **T7 Multi-IR corpora** → Selectors  
   Exists: Meta LLM Compiler · KernelBook → TritonRL · DRTriton synth  
   Missing: versioned MLIR / Tile / StableHLO + failed / miscompile negatives

8. **T8 Benchmark ladder** → C2, C9  
   Exists: KernelBench(-X) · FlashInfer-Bench serving-kernel rung  
   Missing: full IR → kernel → fused → serving + cost-to-compile

9. **T9 Provenance / HITL** → C7  
   Exists: Magellan reviewable C++ · Archer oracle review  
   Missing: CODEOWNERS + signed admit records + sandbox for proposals

10. **T10 Workflow compile / freeze** → Horizon B  
    Exists: FlowCompile · Auto · AgentFlow · VibeServe (early)  
    Missing: shared agent-graph IR + fail-closed CI (productize → Horizon B)
