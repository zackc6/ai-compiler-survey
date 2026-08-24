# 幻燈片 39：附錄 — A 級開放儲存庫

依工作類型的 A 級開放儲存庫。幻燈片上：兩條帶 + 層級註。口播：把儲存庫對到工作 (a)–(d) 與層級語意。

**離線／審查／啟發式。**
OpenEvolve、HeuriGym — 演化啟發式搜尋。Archer — 判定預言機閘控的拉取請求審查。**llvm-harness** — LLVM 工具 + llvm-bench + 自動修復／自動審查（Archer 系譜）。Compiler-R1 — 工具呼叫 pass 搜尋（SFT+RL）。mlirAgent — IR 變換基線（脆弱；當 C3 的負壓有用）。工作 (b) 離線與工作 (c) 工程審查。

**線上／核心／使能拉起。**
ACCLAIM、CompileIQ — 線上提議→量測→接納。**GEAK v4**、KernelAgent — 核心迴圈，現在也有端到端 serving。KernelBench(-X) — 正確性與速度梯子。FlashInfer-Bench — serving trace。AutoKernel、Helion — 核心 DSL 面。TritorX / KernelEvolve / **Zomboss** — 模擬／矽→方言，或一次編譯對映（工作 d）。工作 (a) 線上與 (d) 使能／拉起。

**層級定義。**
A = 智慧體 + 領域判定預言機改變啟發式、核心、旋鈕或審查——與預測相關。B = 智慧體掛上去的資料面宿主。C = 只有通用 forge AI——工具有用，對檢查點結算降級（C7）。頁尾：**DeepSeek Harness** *不是* A 級——智慧體執行期（外掛／session log），不是編譯器判定預言機。

**討論怎麼用。**
有人引用儲存庫時問：A 級機制還是 C 級演示？指到工作字母——它是 freeze 產物、用判定預言機接納，還是只聊天？

收尾：這是給混合預測策展的 forge 地圖——不是每個標了「compiler AI」的 GitHub 儲存庫。
