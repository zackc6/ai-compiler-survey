# 幻燈片 10：資料面 — 約 6–7 個抽象層帶（不是一個）

這張盤點幻燈片 8 的經典資料面——為什麼「one mega-IR」是錯的思維模型。智慧體跨層帶統一**契約**，不是用單一 IR 取代全部。

**今天必備 — L1 到 L6（左欄）。**
逐層帶走；點名層級與內容：

- **L1 Framework** — 捕捉動態（eager/graph、autograd hooks）；PyTorch/JAX 級。
- **L2 Portable graph** — **StableHLO** 級可攜式圖、分片註解；廠商分叉前的交換層。
- **L3 Mid-IR** — **MLIR** 方言、layout、pass pipeline；多數經典最佳化在這裡。
- **L4 Kernel DSL** — Triton、Helion、Tile、CuTe；tile 級可程式設計。
- **L5 Backend-ISA** — PTX、CPU 的 LLVM IR、廠商 intrinsics；bring-up 介面。
- **L6 Runtime-serve** — CUDA Graphs、**KV**（key-value）快取路徑、服務排程器；延遲敏感的推論。

**L7* Fleet／cluster（右側，餘燼框）。**
成熟中的層帶：跨節點放置與 collective。今天常拆在 L2–L3 加執行時膠水——但一旦編譯意味著多節點 **place**，就把 L7 當真實層帶，有自己的合法性與成本介面。

**不是新的 IR 層帶（鋼色框）。**
功耗／能耗 → 目標函數 + oracle，不是第七種方言。**$/token** 與延遲 **SLO**（服務水準目標）→ **控制面政策**，不是新的 lowering 階段。安全 → 溯源與 admit 閘門。別發明「L8 policy IR」——政策在層帶之上。

**Lean — A6 / S6（墨色框）。**
保留層帶；智慧體統一*契約*與編排——**不是**一個 mega-IR 吞下 L1–L7。CPU/**LLVM** 路徑可選 **L0***；智慧體透過型別化工具（**MCP** 級伺服器，Model Context Protocol）坐在*所有層帶之上*。

收尾：六到七個層帶是特性，不是要消滅的碎片化——幻燈片 12 的 e2e 控制器在適應度 **F** 下*跨*它們搜尋。
