# Slide 8: Architecture — Target Stack

Build the stack top to bottom.

Human and product intent at the edge: natural language, policy, budget.
Agent control plane: jobs a through d, with substrate for workflow compile, ADG, freeze, and hetero place.
Classical data plane stays the default path: frameworks into Inductor, XLA, MLIR, Triton, Tile, CuTe — legality, lowering, admit, fallback. Next two slides unpack how many bands that data plane still needs, and why one universal cost model is not the Horizon A bet.
Leaves: GPU NPU ASIC; VCS artifacts such as ACF, kernels, memory plans; serving runtime with freeze for replay.
Codesign feedback loops back toward ISA and dialect RFCs. Humans and EDA still own tape-out — C10.

Invariant to say out loud: the LLM guides search; it does not silently define unchecked executable behavior.

Visual note: the feedback arrow from hardware into codesign routes around the left so it does not cross the codesign block.
