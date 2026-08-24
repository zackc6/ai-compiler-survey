# 幻燈片 4：六大活躍趨勢

這是 §1 的背景。幻燈片上：主張句占主導；機構標籤只是低調的註腳。口播節奏：先講主張，再點名有機構背書的例子。

**A — 混合式引導，不是把 LLM 當編譯器。**
放任 **IR**（中間表示）自由改寫很脆弱：UC Berkeley 的 mlirAgent 顯示，前沿模型在 IR 變換上甚至低於恆等變換。贏家都會收斂行動空間。AgentCompile（香港城市大學）輸出建議性後設資料；模板加檢查才放行 CUDA。HintPilot（浙江大學，與 Purdue 合作）插入編譯器驗證過的 pragma，而不是任意改寫。Meta 的 LLM Compiler 提出 `opt` 會套用的 pass 清單。口頭強調：限制行動；保留傳統施用器。

**B — 從 RL 訓練場到 LLM 智慧體。**
把 CompilerGym 式的不透明神經策略留在健身房時代。轉向會用工具、多智慧體迴圈。Compiler-R1（ISCAS / UCAS）用 **SFT**（監督式微調）+ **RL**（強化學習）訓練工具呼叫式的 pass 搜尋。Magellan（Google DeepMind / Google）在 LLVM/XLA 內合成可出貨的 C++ 啟發式。FlowCompile（UMass Amherst、MIT、MIT-IBM Watson）離線編譯結構化 LLM 工作流程——控制面底層，不只是聊天。時間夠的話也點一下 Auto / AgentFlow 的 freeze 與 **ADG**（智慧體相依圖）。**DeepSeek Harness**（`dsh`）是同一家族裡已出貨的*執行期*——外掛核心 + session log——不是編譯器，也不是判定預言機。

**C — MLIR + Triton 作為預設底層。**
生產 AI 路徑仍是帶機構指紋的經典堆疊：Meta PyTorch → TorchInductor → Triton（OpenAI 起源、社群維護）；並行 **StableHLO** / **HLO**（高階運算）→ OpenXLA/Google XLA 與 IREE。峰值效能往往仍在 NVIDIA 廠商函式庫、CUDA Tile、CUTLASS、FlashAttention 級核心。**MLIR**（多層中間表示）是共用的中階 IR；產品 lowering 路徑依廠商而分。

**D — 核心智慧體走向工業化。**
KernelBench（Stanford / Princeton Scaling Intelligence）要求核心既正確*又*更快；一次成功率常低於 20%，融合仍很難。**GEAK v4**（AMD）已不是單核心迴圈：`e2e_workflow` 先用 Amdahl 在熱的 sglang/vLLM 伺服器上分流，只對能動到吞吐量的核心再搜，並做熱伺服器 **A/B** 與輸出對等。**Cake**（NVIDIA / CMU）讓智慧體寫型別化 **Cake IR** 排程——warp 角色、屏障、記憶體層級——並勝過對照的 CUDA/PTX 搜尋；Kimi Delta Attention 已在 SGLang 驗證。**Argus**（CausalFlow / HKUST / Stanford 等）用 tag 函式與編譯期 **SMT**（可滿足性模理論）檢查版面代數；作者報告在 GEMM / attention / MoE 上達到 MI300X 手調組合語言 **TFLOPS** 的 99–104%。收尾：公開梯子上，精煉仍比速度更能可靠拉高正確率——函式庫級峰值仍是精選家族（**C2** 未結）。

**E — 驗證進入迴圈。**
疊起判定預言機階梯：單元與 golden 測試、相對參考的數值檢查、Alive2 級局部形式等價（UIUC 脈絡；LLM-VeriOpt 式獎勵）、**Argus** 編譯期 SMT 加執行緒級反例，以及 **T-LLM Compiler**（華為）在 PolyBench/C 上串 Alive2 + **CBMC**（C 有界模型檢查器）。局部很強；**GPU** 競態與浮點非確定性上很弱。要拿錢上線，需要這整條階梯，不是單一檢查。

**F — 編譯器擴大可編譯物件。**
超越圖→二進位：生成式編譯迴圈中的中途解碼診斷；FMware——提示、智慧體、自由參數——在 Compiler.next（Queen's University）裡成為可編譯物件。Magellan（Google）把智慧體當樹內啟發式工程師。Anthropic 的 Claude C Compiler 展示智慧體團隊*打造*編譯器（~100kLoC Rust）——智慧體作為編譯器工程師的鄰近證據，不只是編譯期最佳化器。

幻燈片收尾：六條趨勢、一個模式——在經典底層上的混合控制面，每個例子背後都有具名機構。
