# 幻燈片 29：技術預測 — 編譯器之外 (T6–T10)

與幻燈片 28 相同的帶狀節奏，對象是經典 lowering 之外的技術。口播：對 Horizon A 這些同樣是一等公民。

**T6 — Serving 判定預言機／A/B → C2。**
Exists：FlashInfer-Bench + `apply()` 進 SGLang/vLLM、**GEAK v4** 熱伺服器 A/B、**Hyperloom**（AMD，2026 年 9 月）端到端重測加新鮮 Critic——核心階段委派給 GEAK 或 KernelForge。主張：局部形式很強；產品真相是 serving 統計。Missing：全程式檢查、GPU 競態與浮點非確定性判定預言機、多月*預設路徑* A/B 加公開 p50/p90。Hyperloom 在 16 個負載上的中位 1.73× 是作者報告的壓力，不是 C2 結算。解鎖 C2——釘死 trace 上的中位與 p90，不是標題核心。

**T7 — 多 IR 語料 → 選擇器。**
Exists：KernelBook→TritonRL、DRTriton、**AMDKernelVault**（2026 年 9 月：約 6.2 萬筆執行驗證的 HIP 樣本與約 4 萬個 Triton 核心）。蒸餾出的 Qwen3-8B 在論文基準上正確率領先，速度並不一律領先。ComPile 與 Meta LLM Compiler 仍是 LLVM 先驗。主張：對 IR 行動，資料勝過參數數量；流利度語料是*先驗*，不是契約。Missing：版本化 MLIR/Tile/StableHLO/Pallas 傾印，加上*失敗*與誤編譯負例。解鎖學習選擇器，不是一家智慧體 IR 打遍廠商（C4 部分）。

**T8 — 基準梯子 → C2、C9。**
Exists：KernelBench、**JAXBench**（TPU 上 Pallas 對 XLA 與 Tokamax）、**KernelGenBench**（Triton 跨算子來源與六種晶片，並計每次成功的 token）。FlashInfer-Bench 與 llvm-bench 仍是其他階。主張：梯子強迫可比較。KernelGenBench 的教訓：AutoKernel 正確率可從 NVIDIA 的 87% 掉到另一晶片的 25%，每次成功算子約 500 萬 token。Missing：完整 IR→核心→融合→serving 鏈。這些新階不結算 C9。解鎖分佈增益（C2）與誠實的跨晶片比較。

**T9 — 出處／HITL → C7。**
Exists：Magellan 可審查 C++、Archer 判定預言機審查、**llvm-harness**／llvm-bench（專家審查後真正修復低於 22%）、**SkCC** 對不受信任 `SKILL.md` 的 Anti-Skill Injection。主張：智慧體放大草稿；流程必須放大審查。Missing：CODEOWNERS + 簽署的 admit 紀錄 + 沙箱成為標準做法。解鎖把通用 forge AI 從編譯器預測裡降級（C7）。SkCC 是*技能*面的 T9 著色，不是核心 CODEOWNERS。

**T10 — 工作流／技能編譯／freeze → Horizon B。**
本頁 Exists：**SIGIL ★**（`SKILL.md` → AG-IR → 型別化 harness）、**SKILL.state**（明確 \(\Sigma_t\)），以及 **Hyperloom** 的狀態檔（每一輪從檔案重建任務；`SKILL.md` 包不是判定預言機）。FlowCompile、Auto 與 DeepSeek Harness 仍在敘事裡。主張：活的 harness 不是已編譯的*編譯器產品* IR；技能 IR 不是 T1。Missing：共享智慧體圖 IR 編成凍結配置，加上失敗即關的**編譯器** CI。不要把 Hyperloom 的 serving 加速讀成 T10 結算。

收尾：編譯器外技術提供證據、資料與流程。只加強 `opt`／Inductor／Triton 而不做 T6–T10，會留下無法結算檢查點的演示。
