# 幻燈片 4：六大活躍趨勢

這是 §1 背景。投影片上：主張文字為主；機構只在底部極小字。口頭：先講主張，再帶例子與機構。

**A — 混合引導，不是 LLM 當編譯器。**
自由 IR 改寫很脆弱：UC Berkeley 的 mlirAgent 顯示前沿模型在 IR 變換上甚至低於 identity。能成的系統會限制動作空間。City University of Hong Kong（CityU）的 AgentCompile 只產出諮詢式 metadata，再用模板＋檢查核准 CUDA。浙江大學（與 Purdue）的 HintPilot 插入編譯器可驗證的 pragma，不是任意改寫。Meta 的 LLM Compiler 提出 pass 序列，由 `opt` 執行。口頭重點：限制動作；保留古典施用器。

**B — 從 RL gym 到 LLM 智慧體。**
離開 CompilerGym 式、不透明的神經策略。轉向工具使用與多智慧體迴圈。ISCAS／UCAS 的 Compiler-R1 用 SFT＋RL 訓練 tool-calling pass 搜尋。Google DeepMind／Google 的 Magellan 在 LLVM／XLA 內合成可上線的 C++ 啟發式。UMass Amherst、MIT、MIT-IBM Watson 的 FlowCompile 離線編譯結構化 LLM workflow——這是控制平面基材，不只是聊天。時間夠可帶過 Auto／AgentFlow（freeze、ADG）。

**C — MLIR＋Triton 作為預設基材。**
生產路徑仍是帶機構指紋的古典堆疊：Meta 的 PyTorch → TorchInductor → Triton（源自 OpenAI，社群延續）；並行 StableHLO → OpenXLA／Google 的 XLA 與 IREE。峰值往往仍在 NVIDIA 廠商庫、CUDA Tile、CUTLASS、FlashAttention 類 kernel。MLIR 是共享中階 IR；產品 lowering 路徑依廠商分歧。

**D — Kernel 智慧體工業化。**
KernelBench（Stanford／Princeton Scaling Intelligence）要求正確且更快；one-shot 成功率常低於 20%，fusion 仍難。AMD 的 GEAK 在 Instinct 上對 Triton 做 generate–eval–reflect–optimize。Meta 的 KernelLLM 專精較小模型的 PyTorch→Triton。CityU 的 AgentCompile 約束 transformer 圖的 CUDA 特化。收束：細化較能抬正確性，不保證加速——這是新模型與非 NVIDIA 硬體的可攜瓶頸。

**E — 驗證進入迴圈。**
堆疊 oracle：單元／golden 測試、相對參考的數值檢查（AgentCompile 風格），再到 Alive2 級局部形式等價（Alive2 屬 UIUC／形式 IR 譜系；見於 LLM-VeriOpt 類 reward）。局部強；GPU race 與浮點非確定性仍弱。要「夠上線／夠金錢」的 admit，需要這條梯子，不是單一檢查。

**F — 編譯物件變廣。**
不只 graph→binary：解碼中診斷；FMware——prompt、智慧體、自由參數——成為 Queen’s University 的 Compiler.next 編譯物件。Google 的 Magellan 把智慧體當 in-tree 啟發式工程師。Anthropic 的 Claude C Compiler 顯示智慧體團隊能*建造*編譯器（約 10 萬行 Rust）——旁證：智慧體可當編譯器工程師，不只是編譯期最佳化器。

整頁收束：六趨勢、一個模式——混合控制平面疊在古典基材上，每個例子背後都有具名機構。
