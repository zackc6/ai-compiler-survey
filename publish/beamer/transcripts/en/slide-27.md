# Slide 27: Technical Prediction — Within The Compiler (T1–T5)

Larger-font bands. For each: technique + unlocks, then Exists, then Missing.

1. **T1 Typed interfaces** → C3, C5, C6  
   Exists: CompileIQ · ACCLAIM · mlir-opt-repl · FlashInfer Trace  
   Missing: portable schemas across MLIR · Triton · Tile · StableHLO

2. **T2 Admit / fallback** → C6 hybrid  
   Exists: AgentCompile · Archer · TritonRL verifiers · FlashInfer-Bench  
   Missing: shared admit product + trusted deterministic fallback

3. **T3 Control files + replay** → C2, C5  
   Exists: CompileIQ ACFs · FlashInfer Trace + `apply()`  
   Missing: content-addressed keys; golden replay on model upgrade

4. **T4 Heuristic hooks / advisors** → C1  
   Exists: Magellan / AlphaEvolve · MLGO · EmitC PoR  
   Missing: settled Magellan vs MLGO default on named apps

5. **T5 Dialect / ISA sinks** → C9, C10  
   Exists: TritorX · KernelEvolve · Ascend diagnosis  
   Missing: first-class change-proposal surfaces (not auto tape-out)
