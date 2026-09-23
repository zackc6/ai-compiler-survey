# 幻燈片 4：六大活躍趨勢

這是 §1 的背景。幻燈片上：主張句占主導；機構標籤只是低調的註腳。口播節奏：先講主張，再點名有機構背書的例子。

**A — 混合式引導，不是把 LLM 當編譯器。**
放任 **IR**（中間表示）自由改寫很脆弱：UC Berkeley 的 mlirAgent 顯示，前沿模型在 IR 變換上甚至低於恆等變換。**LLM4IR / LaMIR**（ICML 2025；Kent State、HUST、PNNL）是互補的*理解*上界：模型能解析傾印的 LLVM 語法，但在 **CFG**（控制流圖）邊與指令級執行上失敗。贏家都會收斂行動空間——提示、**ACF**（進階控制檔）、意圖序列（IntOpt），或型別化智慧體 IR（Cake / Argus / **TIRx**）。AgentCompile（香港城市大學）輸出建議性後設資料；模板加檢查才放行 CUDA。HintPilot（浙江大學，與 Purdue 合作）插入編譯器驗證過的 pragma。Meta 的 LLM Compiler 提出 `opt` 會套用的 pass 清單。口頭強調：**面向 LLM 的 IR** 是編譯器對智慧體可見的*臉*，不是傾印 `.ll`，也不是新的 lowering 層帶。

**B — 從 RL 訓練場到 LLM 智慧體。**
把 CompilerGym 式的不透明神經策略留在健身房時代。轉向會用工具、多智慧體迴圈。Compiler-R1（ISCAS / UCAS）用 **SFT**（監督式微調）+ **RL**（強化學習）訓練工具呼叫式的 pass 搜尋。Magellan（Google DeepMind / Google）在 LLVM/XLA 內合成可出貨的 C++ 啟發式。FlowCompile（UMass Amherst、MIT、MIT-IBM Watson）離線編譯結構化 LLM 工作流程——控制面底層，不只是聊天。時間夠的話也點一下 Auto / AgentFlow 的 freeze 與 **ADG**（智慧體相依圖）。**SIGIL**（密西根）把 `SKILL.md` 編譯成 **AG-IR**（智慧體圖 IR）再降成型別化 harness——這是*技能*編譯，不是核心 admit。**DeepSeek Harness**（`dsh`）是同一家族裡已出貨的*執行期*——外掛核心 + session log——不是編譯器，也不是判定預言機。「技能」有三義：廠商編譯包（CompileIQ）≠ Agent Skills 規格 ≠ 技能編譯／\(\Sigma_t\)。

**C — MLIR + Triton 作為預設底層。**
生產 AI 路徑仍是帶機構指紋的經典堆疊：Meta PyTorch → TorchInductor → Triton（OpenAI 起源、社群維護）；並行 **StableHLO** / **HLO**（高階運算）→ OpenXLA/Google XLA 與 IREE。峰值效能往往仍在 NVIDIA 廠商函式庫、CUDA Tile、CUTLASS、FlashAttention 級核心。**MLIR**（多層中間表示）是共用的中階 IR；產品 lowering 路徑依廠商而分。

**D — 核心智慧體走向工業化。**
KernelBench（Stanford / Princeton Scaling Intelligence）要求核心既正確*又*更快；一次成功率常低於 20%，融合仍很難。幻燈片現在以 2026 年 9 月開頭：**Hyperloom**（AMD，9 月 21 日）是 Instinct 端到端 harness——核心階段委派給 GEAK 或 KernelForge，再由 harness 重測；作者在 16 個負載上的中位數是 1.73×。**MaxKernel**（Google）為 TPU 寫 **Pallas**；Mosaic 仍負責 lowering；作者在 JAXBench 上相對 XLA 的幾何平均是 1.58×。這是成熟編譯器上的峰值，不是 TritorX 級覆蓋。**Cake**（NVIDIA / CMU）仍是型別化排程的例子。**Argus**（CausalFlow / HKUST / Stanford 等）在註腳：tag 函式與編譯期 **SMT**（可滿足性模理論）；作者報告達到 MI300X 手調組合語言 **TFLOPS** 的 99–104%。**GEAK v4** 仍是 Hyperloom 底下更早的 AMD 端到端迴圈。收尾：精煉仍比速度更能可靠拉高正確率（**C2** 未結）。

**E — 驗證進入迴圈。**
疊起判定預言機階梯：單元與 golden 測試、相對參考的數值檢查、Alive2 級局部形式等價、**Argus** 編譯期 SMT、**AsmEvo**（AMD）對原始 AMDGPU 程式物件做差分檢查，以及 **T-LLM Compiler**（華為）在 PolyBench/C 上串 Alive2 + **CBMC**（C 有界模型檢查器）。AsmEvo 在 codegen *之後* 接納；不是全輸入證明，也不是放任組合語言改寫的許可。局部很強；**GPU** 競態與浮點非確定性上很弱。要拿錢上線，需要這整條階梯，不是單一檢查。

**F — 編譯器擴大可編譯物件。**
超越圖→二進位：生成式編譯迴圈中的中途解碼診斷；FMware——提示、智慧體、自由參數——在 Compiler.next（Queen's University）裡成為可編譯物件。Magellan（Google）把智慧體當樹內啟發式工程師。Anthropic 的 Claude C Compiler 展示智慧體團隊*打造*編譯器（~100kLoC Rust）——智慧體作為編譯器工程師的鄰近證據，不只是編譯期最佳化器。

幻燈片收尾：六條趨勢、一個模式——在經典底層上的混合控制面，每個例子背後都有具名機構。
