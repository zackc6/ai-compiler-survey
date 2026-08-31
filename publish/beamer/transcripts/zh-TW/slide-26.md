# 幻燈片 26：跨領域研究議程

從差距圖到技術圖的橋樑。幻燈片上：六個研究框，帶有顯示依賴性的箭頭。口語：說出每個主題，聯絡間隙，準備 T1-T10。

**承認和回退路徑標準。**
承認、確定性回退路徑和判定預測機梯子的共享產品語義 - 彌補間隙 4.2 並提供 T2。 智慧體編譯和Archer作為點存在；缺少的部分是每個供應商都可以迴歸的行動式承認*產品*。

** 智慧體工具/IR 模式。**
跨 MLIR、Triton、Tile、StableHLO — T1、間隙 4.4 的型別化介面。 CompileIQ、ACCLAIM、mlir-opt-repl 是存在證明；可移植模式則不然。

**開放多 IR 語料庫。**
版本化 IR 轉儲以及失敗和錯誤編譯的負面影響 — T7，差距 4.7 和 4.10。 Meta LLM編譯器和KernelBook→TritonRL顯示需求；負面因素是阻止獎勵駭客行為的因素。

**服務級別預測機。**
整個節目和製作 A/B — T6，差距 4.1。 FlashInfer-Bench + `apply()` 是服務核心梯級；多月預設路徑穩定性仍然缺失。

**出處和人工審查。**
簽署的承認記錄、程式碼所有者、沙箱 — T9、差距 4.8 和 4.9。 Magellan 可審查的 C++ 和 Archer 判定預測機審查是模板，而不是行業標準。

**控制平面編譯 MVP。**
工作流編譯、ADG 檢查、freeze、放置 — T10，缺口 4.6。FlowCompile、Auto、AgentFlow 編譯或分析圖；**SIGIL** ★ 把技能編譯成型別化 harness；**SKILL.state** 是 P2（\(\Sigma_t\)）；**DeepSeek Harness** 是活的執行期（外掛 + session log 重播）。帶失敗即關 CI 的*編譯器產品*智慧體圖 IR 仍是 Horizon B。AG-IR／SkIR 是技能 IR，不是 T1。

結束語：這六個主題在下一張幻燈片中作為技術圖 T1-T10 展開——對於每個主題：存在什麼、缺少什麼、解鎖哪個檢查點。混合精益持有：僅增強“opt”/Inductor/Triton 內部結構是不夠的。
