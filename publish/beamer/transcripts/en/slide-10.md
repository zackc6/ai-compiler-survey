# Slide 10: Data plane — ~6–7 abstraction bands (not one)

This slide inventories the classical data plane from slide 8 — why “one mega-IR” is the wrong mental model. Agents unify **contracts** across bands, not a single replacement IR.

**Must-have today — L1 through L6 (left column).**
Walk each band; name the level and what lives there:

- **L1 Framework** — capture dynamism (eager/graph, autograd hooks); PyTorch/JAX-class.
- **L2 Portable graph** — **StableHLO**-class portable graphs, shard annotations; exchange layer before vendor forks.
- **L3 Mid-IR** — **MLIR** dialects, layout, pass pipelines; where most classical opt lives.
- **L4 Kernel DSL** — Triton, Helion, Tile, CuTe; tile-level programmability.
- **L5 Backend-ISA** — PTX, LLVM IR for CPU, vendor intrinsics; bring-up surface.
- **L6 Runtime-serve** — CUDA Graphs, **KV** (key-value) cache paths, serving schedulers; latency-sensitive inference.

**L7* Fleet / cluster (right, ember box).**
Maturing band: placement + collectives across nodes. Today often split across L2–L3 plus runtime glue — but once compilation means multi-node **place**, treat L7 as a real band with its own legality and cost surfaces.

**Not a new IR band (steel box).**
Power/energy → objective + oracle, not a seventh dialect. **LLM-oriented IR** → agent *face* of existing bands (T1 contract: summaries / intent / typed surface), not an L-llm. **$/token** and safety → control-plane policy and admit, not a new lowering stage. Do not invent “L8 policy IR” or “L-llm.”

**Lean — A6 / S6 (ink box).**
Keep the bands; agents unify *contracts* and orchestration — **not** one mega-IR swallowing L1–L7. Optional **L0*** for CPU/**LLVM** paths; agents sit *above* all bands via typed tools (**MCP**-class servers, Model Context Protocol).

Closing beat: six–seven bands are a feature, not fragmentation to eliminate — the e2e controller in slide 12 searches *across* them under fitness **F**.
