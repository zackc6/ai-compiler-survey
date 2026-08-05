# 幻燈片 10：資料平面 — 約 6–7 個抽象層帶（不是一層）

這是架構投影片裡「經典資料平面」背後的清單。

今天必備六層：L1 框架擷取；L2 可攜式圖（StableHLO 級，含可攜分片標註）；L3 中階 IR（MLIR、版面配置、pass）；L4 kernel DSL（Triton / Helion / Tile / CuTe）；L5 後端與 ISA；L6 執行時與 serving（CUDA Graphs、KV 路徑）。

L7 機群／叢集正在成熟：放置與集合通訊。今天常拆在 L2–L3 加 runtime，但一旦「編譯」意指多節點放置，就要當成真正的一層。

不必各自長成新 IR 的：功耗／能量 → 目標＋oracle；$/token 與延遲 SLO → 控制平面政策；安全 → 出處與 admit。可選 L0 給 CPU／LLVM 路徑。

口頭結語：保留這些層帶；智慧體統一的是契約與編排，不是一個巨型 IR。對應主張 A6／S6。
