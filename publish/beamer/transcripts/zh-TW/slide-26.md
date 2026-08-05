# 投影片 26：技術預測 — 編譯器內部（T1–T5）

較大字型的帶狀版面。每一項：技術 + 解鎖，然後 Exists，再 Missing。

1. **T1 Typed interfaces** → C3, C5, C6  
   Exists：CompileIQ · ACCLAIM · mlir-opt-repl · FlashInfer Trace  
   Missing：跨 MLIR · Triton · Tile · StableHLO 的可攜 schema

2. **T2 Admit / fallback** → C6 hybrid  
   Exists：AgentCompile · Archer · TritonRL verifiers · FlashInfer-Bench  
   Missing：共享的接納產品 + 可信的確定性回退路徑

3. **T3 Control files + replay** → C2, C5  
   Exists：CompileIQ ACFs · FlashInfer Trace + `apply()`  
   Missing：內容定址金鑰；模型升級時的 golden replay

4. **T4 Heuristic hooks / advisors** → C1  
   Exists：Magellan / AlphaEvolve · MLGO · EmitC PoR  
   Missing：在具名應用上，Magellan vs MLGO 誰是預設已定案

5. **T5 Dialect / ISA sinks** → C9, C10  
   Exists：TritorX · KernelEvolve · Ascend diagnosis  
   Missing：一流的變更提案介面（不是自動 tape-out）
