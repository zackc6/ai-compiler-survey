# 幻燈片 25：差距圖 — 阻礙預測的是什麼，不是願望清單

從阻礙過渡到差距。幻燈片上：HIGH、MED–HIGH、MEDIUM 優先層，帶編號缺口 ID。口播：這卡住 Horizon A——不是研究願望清單。

**HIGH 列 — 沒有這些，預測就停在這裡。**
4.1 生產證據：預設路徑 A/B、分佈增益（阻礙四）。4.2 正確性：拿錢級判定預言機堆疊——形式 → 形狀網格 → serving 統計（阻礙一）。4.3 成本／重播：lab → CI → freeze 生命週期、快取鍵、token 預算（阻礙二）。4.4 跨堆疊：可攜 **面向 LLM 的 IR** 契約（摘要／意圖／型別化表面／admit）跨 MLIR、Triton、Tile、StableHLO——不是一份傾印的 LLVM IR（阻礙三；LLM4IR）。4.10 基準：帶編譯成本的統一梯子——單靠 KernelBench 不夠。

**MED–HIGH 列 — 會加速，但單靠它證不了偽。**
4.5 硬體原生介面：Tile IR、CuTe、智慧體必須面對的廠商核心 DSL。4.7 訓練資料：帶負例的開放多 IR 語料——T7 解鎖選擇器，不只是更大的 LLM。

**MEDIUM 列 — 流程與底層。**
4.6 工作流／技能編譯：ADG（智慧體相依圖——智慧體程式的靜態 IR）檢查、freeze、放置——到 Horizon B 的 T10 路徑。FlowCompile 與 AgentFlow *編譯或分析*圖；**SIGIL** 把 `SKILL.md` → AG-IR → harness；**DeepSeek Harness** *跑*一棵活的外掛樹加 session log；**SKILL.state** 用明確的 \(\Sigma_t\) 取代越來越長的逐字稿。技能 IR 不是 T1。失敗即關的**編譯器產品** CI 仍缺。4.8 人工審查流程：CODEOWNERS、簽署 admit、HITL（人在迴圈內）容量——智慧體產出草稿的速度比審查擴得快。4.9 安全：沙箱、溯源、供應鏈——TCB 裡的智慧體核心要跟手寫程式碼同一標準。SkCC 的 Anti-Skill Injection 是對不受信任 `SKILL.md` 的 T9 著色，不是核心 CODEOWNERS。

**優先規則。**
差距圖按什麼會證偽預測排序，不是按什麼流行。跨堆疊（4.4）與基準（4.10）看起來沒有更大的 IR LLM 那麼吸睛——但沒有它們，你無法跨廠商比較檢查點。

收尾：若只能資助一條帶，資助 HIGH 列。那些缺口是混合預測不致變成投影片軟體的原因。下一張點名直接打這些缺口的六個研究主題。
