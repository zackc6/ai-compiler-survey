# 幻燈片 29：技術預測 — 編譯器之外 (T6–T10)

與幻燈片 28 相同的帶狀節奏，對象是經典 lowering 之外的技術。口播：對 Horizon A 這些同樣是一等公民。

**T6 — Serving 判定預言機／A/B → C2。**
Exists：Alive2 級局部形式、FlashInfer-Bench + `apply()` 進 SGLang/vLLM、**GEAK v4** 在 Amdahl 分流後做熱伺服器 A/B 與輸出對等。主張：局部形式很強；產品真相是 serving 統計。Missing：全程式檢查、GPU 競態與浮點非確定性判定預言機、多月*預設路徑* A/B 加公開 p50/p90。解鎖 C2——釘死 trace 上的中位與 p90，不是標題核心。

**T7 — 多 IR 語料 → 選擇器。**
Exists：Meta LLM Compiler 的 pass 清單資料、**ComPile** 生產 LLVM IR 堆、KernelBook→TritonRL、DRTriton。主張：對 IR 行動，資料勝過參數數量；流利度語料是*先驗*，不是契約。Missing：版本化 MLIR/Tile/StableHLO 傾印，加上*失敗*與誤編譯負例——沒有負例，RL 會鑽獎勵漏洞。ComPile／IRCoder 補不上 GPU／MLIR 缺口。解鎖學習選擇器，不是一家智慧體 IR 打遍廠商（C4 部分）。

**T8 — 基準梯子 → C2、C9。**
Exists：KernelBench(-X) 正確性+速度、FlashInfer-Bench serving 核心階、**llvm-bench**（334 個 LLVM 中端崩潰／誤編譯缺陷）。主張：梯子強迫可比較——serving 核心與編譯器缺陷修復是不同階。Missing：完整 IR→核心→融合→serving 鏈，每一階都報編譯成本。解鎖分佈增益（C2）與第二供應商覆蓋劇本（C9）。

**T9 — 出處／HITL → C7。**
Exists：Magellan 可審查 C++、Archer 判定預言機審查、**llvm-harness**／llvm-bench（專家審查後真正修復低於 22%）。主張：智慧體放大草稿；流程必須放大審查。Missing：CODEOWNERS + 簽署的 admit 紀錄 + 沙箱成為標準做法。解鎖把通用 forge AI 從編譯器預測裡降級（C7）。

**T10 — 工作流編譯／freeze → Horizon B。**
Exists：FlowCompile 離線工作流編譯、Auto/AgentFlow freeze、**DeepSeek Harness**（`dsh`）作為已出貨*執行期*——外掛核心 + 只附加的 session log（resume / fork / replay）。主張：活的 harness 不是已編譯的智慧體圖 IR。Missing：共享智慧體圖 IR 編譯成凍結配置，加上失敗即關 CI——Horizon B「控制面被編譯」，不是永遠聊天。VibeServe 仍是早期 serving 堆疊著色；不要把 DSH 星數讀成 T10 結算。

收尾：編譯器外技術提供證據、資料與流程。只加強 `opt`／Inductor／Triton 而不做 T6–T10，會留下無法結算檢查點的演示。
