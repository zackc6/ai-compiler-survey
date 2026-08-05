# Slide 8: Architecture — Target Stack (§5.1)

Build the stack top to bottom.

Human and product intent at the edge: natural language, policy, budget.
Agent control plane: jobs a through d, with substrate for workflow compile, ADG, freeze, and hetero place.
Classical data plane stays the default path: frameworks into Inductor, XLA, MLIR, Triton, Tile, CuTe — legality, lowering, admit, fallback.
Leaves: GPU NPU ASIC; VCS artifacts such as ACF, kernels, memory plans; serving runtime with freeze for replay.
Codesign feedback loops back toward ISA and dialect RFCs. Humans and EDA still own tape-out — C10.

Invariant to say out loud: the LLM guides search; it does not silently define unchecked executable behavior.

Visual note: the feedback arrow from hardware into codesign routes around the left so it does not cross the codesign block.
