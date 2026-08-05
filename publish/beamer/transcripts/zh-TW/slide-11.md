# 幻燈片 11：一個通用成本模型？— 否（Horizon A）

直接回答：「能不能訓練一個成本模型，涵蓋所有最佳化 pass（含未來）？」

左側——為什麼不行。各層帶的合法性與 oracle 不同：Alive2 不能證明 GPU race 或 serving 等價。選擇在哪一層花預算本身就是產品（ACCLAIM 的 guide agent）。成本模型保持局部：MLGO、Ansor、MetaSchedule 在同一族內有效，無法從 fusion → Triton → regalloc → serving A/B 一路通用。未來 pass／新 ISA 需要新的實測標籤；凍結權重無法憑空預測未量測硬體行為。

右側——若產業沒有收斂乾淨的 L2／L4／L7 IR，不要乾等。改走可插拔介面：agent compile schema、typed tools／MCP 級伺服器、dialect＋oracle＋objective plugins、以及機群放置 plugins（L7）。

尺寸註記：參數量不是瓶頸。上線的局部 advisor 常是 KB–MB；跨層帶的 proposer 看起來像 7B–70B+ 的 IR LLM，卻仍只是 prior。真正難的是標註好的（程式、動作、硬體、能耗、SLO）元組，且每換 SKU 要更新。押注：每層小成本模型＋可選大型編排器——不是一顆吃掉 L1–L7 的巨型成本模型。
