# Slide 25: Gap map — what blocks the prediction, not a wishlist

Transition from blockers to gaps. On-slide: priority tiers HIGH, MED–HIGH, MEDIUM with numbered gap IDs. Spoken: this gates Horizon A — it is not a research wishlist.

**HIGH row — prediction stops here without these.**
4.1 production evidence: default-path A/B, distributional gains (blocker four). 4.2 correctness: money-grade oracle stack — formal → shape-grid → serving statistics (blocker one). 4.3 cost/replay: lab → CI → freeze lifecycle, cache keys, token budget (blocker two). 4.4 cross-stack: portable agent contract across MLIR, Triton, Tile, StableHLO (blocker three). 4.10 benchmarks: unified ladder with cost-to-compile — KernelBench alone is not enough.

**MED–HIGH row — accelerates but does not alone falsify.**
4.5 hardware-native interfaces: Tile IR, CuTe, vendor-specific kernel DSLs agents must address. 4.7 training data: open multi-IR corpora with negatives — T7 unlocks selectors, not just bigger LLMs.

**MEDIUM row — process and substrate.**
4.6 workflow compile: ADG (Agent Dependency Graph — static IR of the agent program) check, freeze, place — T10 path to Horizon B. FlowCompile and AgentFlow are early existence proofs; fail-closed CI on compiled agent graphs is not. 4.8 human-review process: CODEOWNERS, signed admit, HITL (human-in-the-loop) capacity — agents multiply drafts faster than review scales. 4.9 security: sandbox, provenance, supply chain — agent kernels in the TCB need the same bar as hand-written code.

**Priority rule.**
Gap map is ordered by what falsifies the prediction, not what is fashionable. Cross-stack (4.4) and benchmarks (4.10) look less sexy than bigger IR LLMs — but without them you cannot compare checkpoints across vendors.

Closing beat: if you fund one band, fund the HIGH row. Those gaps are what keep the hybrid prediction from becoming slideware. Next slide names six research themes that attack these gaps directly.
