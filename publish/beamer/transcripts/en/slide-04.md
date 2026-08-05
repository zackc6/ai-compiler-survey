# Slide 4: Six active trends

Walk each box with one concrete beat — this is the §1 backdrop.

A — Hybrid guidance: free IR rewrite is fragile (mlirAgent below identity). Winners constrain the action space — advisory metadata, validated hints, pass lists that opt applies. Name AgentCompile, HintPilot, LLM Compiler.

B — RL to agents: leave CompilerGym-style opaque policies. Move to tool-using and multi-agent loops, heuristic synthesis as shippable C++, and workflow compile / freeze / place. Name Compiler-R1, Magellan, FlowCompile.

C — MLIR + Triton substrate: PyTorch → Inductor → Triton; parallel StableHLO → XLA/IREE. Peak often still vendor libs, Tile, CUTLASS, FlashAttention. MLIR is shared; product paths diverge.

D — Kernel agents industrial: KernelBench wants correct and faster; one-shot often under 20%, fusion hard. GEAK, KernelLLM, AgentCompile. Refinement raises correctness but not always speed. This is the bottleneck for new models and portability.

E — Verify in the loop: unit/golden → numerical → Alive2-class local formal. Strong locally; weak on GPU races and floating-point nondeterminism. Admit needs a stacked oracle ladder.

F — Broader compile object: mid-decode diagnosis, FMware (prompts/agents/knobs), agents as compiler engineers, heuristics rewritten in-tree. Compiler.next, Magellan, Claude C.
