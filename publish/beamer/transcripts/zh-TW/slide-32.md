# 幻燈片 32：組織採用問題

討論提示——不是測驗。幻燈片上：五個琥珀色問題行。口播：每題後停頓；讓現場對自己的路線圖作答。

**1. 線上（CompileIQ）vs 離線（Magellan）——哪個對得上你的釋出模型？**
工作 (a) 線上提案→量測→admit vs 工作 (b) 離線演化啟發式→C++/MLGO。產品 CI 節奏、freeze 產物、審查容量都不一樣。若你每週出核心、每季才演化啟發式，可能兩邊都要——但哪個是*預設*？C5 結算是發行說明，不是實驗室演示。

**2. 判定預言機堆疊：Alive2／golden／serving A/B——漏報誰負責？**
阻礙一的現場問題回來了。admit 過了、生產卻誤編譯時，是編譯器團隊、智慧體平台，還是 serving SRE？沒有具名所有權，判定預言機梯子會停在「別人的問題」。

**3. 智慧體可見的 IR：傾印 vs 摘要／Cake／Argus／TIRx／Gluon？**
T1 型別化介面你先投哪裡——以及 LLM 會看到*哪張臉*？傾印 LLVM/MLIR（LLM4IR：CFG／執行失敗）vs 摘要、IntOpt 式意圖、Cake IR、Argus tag、**TIRx**（TVM FFI）、Triton／**Gluon**／**TLX**、StableHLO、**CuTe DSL**，或 **TileLang**。多底層機群等不起一份 mega-schema——但每條產品線需要*一個*選定的 **面向 LLM 的 IR**，不是把 IR 貼進去。**TLX ≠ TIRx ≠ TritorX**。

**4. 編譯器*與*模型升級時，trace 怎麼快取／迴歸？**
實務上的 T3 重播契約。快取鍵：IR hash、硬體、編譯器版本、智慧體政策。什麼會弄壞 golden 重播——誰重跑智慧體、誰釘死舊產物？

**5. 中位 X% 勝的最大 $/build？每個 admitted 產物有具名維護者？**
商業阻礙二合一。每百分點增益的 token 預算；每個 ACF、核心或啟發式類的 CODEOWNER。若數字與負責人你都叫不出來，Horizon A 經濟學就沒定義。

收尾：用沉默。這五題揭露混合賭注在*這個*組織能不能落地，不是這份調查好不好看。
