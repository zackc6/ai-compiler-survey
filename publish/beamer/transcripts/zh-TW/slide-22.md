# 幻燈片 22：阻礙 3 — 智慧體↔編譯器契約

第三項阻礙：智慧體怎麼跟編譯器說話。幻燈片：A 到 D 四個全寬層帶，然後 `admit_record` schema。口播：排序選項、講 lean、解釋 ACF。

**A — 自然語言 + 貼 log。**
只能 demo。Lab 探索可以；拿錢的 CI 沒用。沒有可重現行動空間、沒有物料清單、模型漂移時沒回歸。口頭說：契約若是聊天，你就沒有產品契約。

**B — 結構化 admit trace。**
Build CI 與物料清單。每筆 admitted 變更帶 graph hash、硬體 ID、編譯器版本、oracle 結果、artifact digest、policy ID。Archer 與 AgentCompile 級審查迴圈產出的就是這個。Trace 是智慧體與人稽核的 ground truth——不是聊天紀錄。

**C — 型別化工具介面。**
必要的行動空間。**MCP**（Model Context Protocol——工具伺服器標準）級伺服器、`mlir-opt-repl`、CompileIQ skills、FlashInfer Trace `apply()`——智慧體在編譯器會驗證的 schema 內提案。T1（型別化智慧體↔編譯器介面）解鎖 C3（自由改寫 vs 建議）、C5（預設路徑）、C6（替換 vs 控制面）。Lean：窄 ACF 與 hint，不是自由 IR 改寫。

**D — 混合視圖。**
自然語言是 B 與 C 的*視圖*——給人的摘要與解釋，不是可執行權威。產品 UX 可以一直對話；CI 讀 admit record。

**展示 `admit_record` 區塊。**
走過欄位：`graph_hash`、`hw_id`、`compiler_ver`、`action[]`、`oracle[]`、`artifact_digest`、`policy_id`。這是跨 MLIR、Triton、Tile、StableHLO 的可攜契約。**ACF** = 進階控制檔——可攜編譯器旋鈕，freeze 進 VCS。

收尾句：lean 是 **C + B**。型別化工具收斂行動；admit trace 讓它們可回歸。自然語言是透鏡，不是編譯器 API。
