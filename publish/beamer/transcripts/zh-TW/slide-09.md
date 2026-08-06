# 幻燈片 9：架構演進 — 元件變化

**由左到右**走過三個時代——TODAY（2025–26）、HORIZON A（2027–28）、HORIZON B（~2029–31）。四列：CTRL、DATA、CODE（codesign）、ART（產物）。在每個格子*裡面*多花時間——真正變的是什麼。

**控制面列（鋼色）。**
- *Today：* 臨時智慧體迴圈——聊天／工具、GEAK、ACCLAIM、Magellan 實驗——**沒有型別化 admit** 契約；每個團隊各自重造編排。
- *Horizon A：* 工作 **(a)–(d)** 產品化——線上／離線／審查／bring-up 成 SKU；build-**CI** 門控 specialize 變常態。
- *Horizon B：* 控制面**被編譯**——工作流程編譯、**ADG** 檢查、freeze、可稽核的智慧體圖像編譯器二進位一樣攤銷。不是「更大的聊天」；是編譯過的編排。

**資料面列（琥珀色）。**
- *Today：* 經典 **MLIR**/Triton/Inductor，以 **GPU** 為主；智慧體工具很薄。
- *Horizon A：* **智慧體可定址**——多 DSL 指紋、型別化工具 API、熱路徑 admit、各層帶接上 oracle。
- *Horizon B：* **多後端機群**——**ACF**、啟發式、記憶體規劃成 **VCS** 產物；經典 lowering *仍在*底下跑。

**Codesign 列（餘燼色）。**
- *Today：* 稀疏／手動；人類 bring-up 主導；sim↔編譯器迴圈很弱。
- *Horizon A：* 早期回饋——sim + 首片矽 → ISA／方言提案；TritorX / KernelEvolve 級。
- *Horizon B：* 穩定的矽前 → bring-up → 下一顆晶片迴圈——**不是**自主設計（**C10**）。

**產物列（低調）。**
- *Today：* 二進位 + 稀疏 hints。
- *Horizon A：* + 控制檔／核心／C++ 啟發式／語料庫。
- *Horizon B：* + 凍結的智慧體工作流程（認知二進位——可重播的智慧體圖）。

**幻燈片頁尾收尾句。**
元件由左→右變厚；資料面留著；智慧體圖被編譯並攤銷。口頭說：重點是*哪些元件變厚*——資料面永遠不會消失。銜接到幻燈片 10：那是資料面裡的層帶盤點。
