# 幻燈片 11：一個通用成本模型？— 不行（Horizon A）

直接回答現場問題：「一個成本模型能不能涵蓋所有 pass——包括我們還沒發明的？」Horizon A 的答案是 **不行**。兩欄加底部尺寸標註。

**左欄 — 為什麼不能只有一個模型（琥珀框）。**
- **各層帶合法性／oracle 不同** — Alive2 認證 LLVM IR 切片；它不認證 **GPU** 競態安全或服務時等價。單一成本張量無法在 L3 與 L6 之間共用標籤。
- **選哪一層*就是*產品決策** — ACCLAIM 的 guide agent 決定*把搜尋預算花在哪個層帶*；這個 meta 決策無法化約成單一局部成本。
- **成本模型保持局部** — **MLGO**、Ansor、MetaSchedule 在同一家族內遷移（例如 LLVM inliner features），不是從 fusion → Triton → regalloc → serving A/B 塞進一個權重檔。
- **未來 pass 需要新量測標籤** — 每個新 ISA SKU 與 pass 都要新的（program, action, HW）tuple；凍結權重無法發明沒量過的硬體行為。

**右欄 — 若層帶不會合併（鋼框）。**
別等那個「唯一真 IR」。現在就 ship **可插拔介面**：
- Agent compile schema 加 admit hash——可重現的智慧體輸出。
- 型別化工具／**MCP** 級伺服器（Model Context Protocol——智慧體呼叫的型別化工具伺服器）。
- 各層帶的方言 + oracle + 目標外掛。
- **L7** 的放置／機群外掛。

**尺寸標註（底部墨框）。**
參數量**不是**瓶頸。局部顧問：常 **KB–MB**。跨層帶*提案者*：約 **7B–70B+** IR LLM——仍只是**先驗**，不是地面真值。難的是帶標籤的（program, action, HW, energy, **SLO**）tuple，每個 SKU 都要刷新。

**押注句 — 口頭說出來。**
各層帶小成本 + 可選的大型編排器——**不是**一個 mega-cost-model 吃掉 L1–L7。

銜接幻燈片 12：局部成本只是提案先驗；架構仍要在產品適應度 **F** 下追求 **e2e**（端到端）最適。
