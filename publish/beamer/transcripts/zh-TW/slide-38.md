# 幻燈片 38：附錄 — A 級商業訊號

塑造出貨的 A 級產品。幻燈片上：公司帶 + B 級頁尾。口播：把每家當*訊號*，不是背書——他們暴露什麼機制。

**Google / DeepMind。**
AlphaEvolve Cloud（GA）——雲上的演化編碼。Magellan + MLGO 並行——啟發式合成 *與* 樹內學習顧問（C1 已在生產）。訊號：離線智慧體當輸出，與樹內神經顧問共存。

**NVIDIA。**
CompileIQ 加智慧體技能——線上特化、ACF 級控制檔，並遵循 Agent Skills 的 `SKILL.md` 規格（包裝，不是 T1）。CUDA Tile / Tile IR——硬體原生核心面。**Cake IR**（與 CMU 的研究）——型別化排程 IR 加演化驗證器；已做 serving 驗證的 KDA。TensorRT-LLM 智慧體技能——服務堆疊整合。訊號：型別化工具 + 核心 DSL + serving，不是只聊天。

**AMD。**
**GEAK v4**——在熱的 sglang/vLLM 上做 Amdahl 分流、遞迴核心工作流、熱伺服器 A/B + 輸出對等。訊號：具名廠商迴圈在追 serving **F**，不只核心 microbench。仍不是公開 p50 預設路徑（**C2**）。

**CausalFlow 等。**
**Argus**——MI300X 上的資料流不變量 + SMT；精選家族達組合語言 TFLOPS 的 99–104%。研究論文，**不是** AMD SKU。訊號：Instinct 級硬體上存在編譯期核心 admit；三個家族的峰值是 C2 *著色*，不是結算。

**Meta。**
LLM Compiler / KernelLLM — IR 與 PyTorch→Triton 特化。TritorX + KernelEvolve — 使能／拉起／協同設計迴授（工作 d）。Helion／**TLX** — 把 Triton 往上抬 vs 用 MIMW 擴充（KernelEvolve 已搜 Triton+TLX）。訊號：從可攜圖到矽迴授的完整堆疊，仍是混合。

**FlashInfer。**
FlashInfer-Bench — serving-trace 梯子，用 `apply()` 進 SGLang/vLLM。訊號：T6/T8 serving 核心階存在；結算仍要預設路徑 A/B（C2）。

**B 級基線（頁尾）。**
TensorRT-LLM、Inductor、XLA/StableHLO、FlashInfer 執行期、Modular MAX、OpenVINO、Neuron、Hexagon-MLIR — 智慧體必須互通、不能取代的資料面預設（C6-B）。

收尾：A 級告訴你廠商把賭注押在智慧體控制面哪裡；B 級是仍必須接納與 lowering 的東西。
