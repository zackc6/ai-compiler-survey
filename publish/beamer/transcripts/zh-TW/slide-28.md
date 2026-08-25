# 幻燈片 28：技術預測 — 在編譯器內 (T1–T5)

帶狀佈局的編譯器內技術。幻燈片上：每列是技術 + 解鎖、Exists、Missing。口播：五條都走主張 → 證據 → 缺口。

**T1 — 型別化介面 → C3、C5、C6。**
Exists：CompileIQ 智慧體技能、**Cake IR**（型別化排程，沒有版面代數）、**Argus** tag 函式／斷言、**IntOpt** 意圖序列（經典實現）、**LLM4IR** 作為*負例*（裸 LLVM 傾印在 CFG／執行上失敗）。主張：**面向 LLM 的 IR** 是智慧體可見的臉——schema，不是貼上然後祈禱。Missing：跨 MLIR、Triton、Tile、Cake、Argus 的可攜摘要與行動——今天每個堆疊都重黏。解鎖窄 ACF／提示壓過自由改寫（C3），以及發行說明裡的具名預設路徑（C5）。

**T2 — 接納／回退 → C6 混合。**
Exists：Archer 判定預言機閘控 PR、**Cake** 編譯前安全／符合性閘、**Argus** 版面代數 + SMT（零執行期、執行緒級反例）、FlashInfer-Bench。主張：混合意味經典 lowering 仍在 admit 底下跑。Missing：共享的 admit *產品*，加上每個廠商文件都信得過的確定性回退。解鎖 C6-B——控制面，不是編譯器替換。

**T3 — 控制檔 + 重播 → C2、C5。**
Exists：CompileIQ ACF、FlashInfer Trace + `apply()` 進 SGLang/vLLM。主張：freeze 產物是服務時零 LLM 的做法。Missing：內容定址快取鍵；模型或編譯器升級時的 golden 重播。解鎖釘死 trace 上的中位／p90 證據（C2）。

**T4 — 啟發式掛鉤／顧問 → C1。**
Exists：Magellan/AlphaEvolve 可出貨 C++、MLGO 樹內顧問、EmitC 2026 年 6 月 PoR（紀錄計畫：inliner → Android/Fuchsia → Chrome）。主張：平行賭注——演化 C++ *與* 學習顧問都活著。Missing：具名應用上的已結預設——公開 Magellan 補丁取代 MLGO，或 EmitC-MLGO 客戶預設。

**T5 — 方言／ISA 匯流排 → C9、C10。**
Exists：TritorX、KernelEvolve、**Cake** 工具架演化（反覆失敗變成驗證規則／IR 原語）、**Zomboss** 一次編譯的 TAIDL/ACT 後端。主張：覆蓋先於峰值；機器語意應被編譯，不要重提示。Missing：一流的變更-*提案*面——不是自主微架構流片（C10 拒絕）。

收尾：編譯器內工作是約束與接納；它不取代 lowering。下一張：編譯器外的 T6–T10——多數結算證據必須從那裡來。
