# 幻燈片 8：架構 — 目標堆疊

由上往下講這條堆疊。

邊緣是人／產品意圖：自然語言、政策、預算。
智慧體控制平面：工作 (a)–(d)，底下還有 workflow compile、ADG、freeze、異質放置。
經典資料平面仍是預設路徑：框架進 Inductor／XLA／MLIR／Triton／Tile／CuTe——合法性、lowering、admit、fallback。接下來兩張投影片會拆開：資料平面還需要幾層，以及為什麼「一個通用成本模型」不是 Horizon A 的賭注。
末端：GPU／NPU／ASIC；版本庫產物（ACF、kernel、memory）；serving runtime（freeze 以便重播）。
協同設計回授指向 ISA／dialect RFC。流片仍由人與 EDA 擁有——C10。

口頭不變式：LLM 引導搜尋；它不默默定義未檢查的可執行行為。

視覺：硬體回授箭頭從左側繞進 codesign，避免穿過 codesign 方塊。
