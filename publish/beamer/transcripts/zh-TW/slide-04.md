# 投影片 4：六大活躍趨勢

用一個具體的節拍走過每個盒子——這是 §1 背景。

A — 混合指導：自由 IR 重寫很脆弱（mlir 智慧體低於身份）。獲勝者限制了行動空間——諮詢後設資料、經過驗證的提示、選擇適用的最佳化遍歷序列。名稱AgentCompile器，HintPilot，LLM編譯器。

B — RL 到智慧體：保留 CompilerGym 式的不透明策略。轉向工具使用和多智慧體迴圈、可交付 C++ 的啟發式綜合以及工作流編譯/凍結/放置。名稱 Compiler-R1、Magellan、FlowCompile。

C — MLIR + Triton 基板：PyTorch → Inductor → Triton；並行 StableHLO → XLA/IREE。 Peak 通常仍然是供應商庫、Tile、CUTLASS、FlashAttention。 MLIR 是共享的；產品路徑出現分歧。

D — 工業核心智慧體：KernelBench 想要正確、更快；一擊往往低於20%，融合困難。 GEAK、KernelLLM，AgentCompile。細化提高了正確性，但並不總是提高速度。這是新機型和便攜性的瓶頸。

E — 迴圈驗證：單位/黃金 → 數值 → Alive2 級區域性形式。本地實力雄厚； GPU 競賽和浮點非確定性方面較弱。承認需要一個堆疊的判定預示機梯子。

F — 更廣泛的編譯物件：解碼中診斷、FMware（提示/智慧體/旋鈕）、編譯器工程師的智慧體、樹內重寫的啟發式方法。編譯器.next，Magellan，克勞德 C.
