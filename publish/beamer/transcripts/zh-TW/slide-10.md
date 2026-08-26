# 幻燈片 10：資料面 — 約 6–7 個抽象層帶（不是一個）

這張盤點幻燈片 8 的經典資料面——為什麼「one mega-IR」是錯的思維模型。智慧體跨層帶統一**契約**，不是用單一 IR 取代全部。

**今天必備 — L1 到 L6（左欄）。**
逐層帶走；點名層級與內容：

- **L1 Framework** — 捕捉動態（eager/graph、autograd hooks）；PyTorch/JAX 級。
- **L2 Portable graph** — **StableHLO** 級可攜式圖、分片註解；廠商分叉前的交換層。
- **L3 Mid-IR** — **MLIR** 方言、layout、pass pipeline；多數經典最佳化在這裡。
- **L4 Kernel DSL** — Triton、Helion、**TileLang**、CuTe、**TIRx**（TVM Tensor IR next）；tile 級可程式設計。Helion 把 Triton 往上抬；**Gluon**／**TLX** 往下或擴充。TIRx 文件裡的搜尋階 L1–L4 是*智慧體搜尋*層級，**不是**這裡的資料面層帶。**TLX ≠ TIRx ≠ TritorX**。
- **L5 Backend-ISA** — PTX、CPU 的 LLVM IR、廠商 intrinsics；bring-up 介面。
- **L6 Runtime-serve** — CUDA Graphs、**KV**（key-value）快取路徑、服務排程器；延遲敏感的推論。

**L7* Fleet／cluster（右側，餘燼框）。**
成熟中的層帶：跨節點放置與 collective。今天常拆在 L2–L3 加執行時膠水——但一旦編譯意味著多節點 **place**，就把 L7 當真實層帶，有自己的合法性與成本介面。

**不是新的 IR 層帶（鋼色框）。**
功耗／能耗 → 目標函數 + 判定預言機，不是第七種方言。**面向 LLM 的 IR** → 既有層帶對智慧體可見的*臉*（T1 契約：摘要／意圖／型別化表面），不是 L-llm。**$/token** 與安全 → 控制面政策與 admit，不是新的 lowering 階段。別發明「L8 policy IR」或「L-llm」。

**Lean — A6 / S6（墨色框）。**
保留層帶；智慧體統一*契約*與編排——**不是**一個 mega-IR 吞下 L1–L7。CPU/**LLVM** 路徑可選 **L0***；智慧體透過型別化工具（**MCP** 級伺服器，Model Context Protocol）坐在*所有層帶之上*。

收尾：六到七個層帶是特性，不是要消滅的碎片化——幻燈片 12 的 e2e 控制器在適應度 **F** 下*跨*它們搜尋。
