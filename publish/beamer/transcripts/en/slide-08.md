# Slide 8: Architecture — Target Stack

Build the stack top to bottom — this is the reference diagram for the rest of the architecture section. Point at each band as you speak.

**Human / product intent (top).**
Natural language at the edge, policy, budget — what the product wants (latency **SLO**, Service Level Objective; cost per token; quality bar). Intent does not compile directly; it constrains the control plane.

**Agent control plane (steel band).**
Jobs **(a)–(d)** live here. Substrate includes workflow compile (offline graph of agent steps), **ADG** (Agent Dependency Graph) check before run, **freeze** for deterministic replay, and hetero **place** (placement across devices/fleet). Typed tools and admit gates connect downward — arrow label on slide: *typed tools · admit · oracles*.

**Classical data plane (amber band) — default path stays.**
Frameworks → Inductor / XLA / **MLIR** / Triton / Tile / CuTe. Legality, lowering, admit/fallback. This is not deprecated in the prediction — it thickens with agent-addressable interfaces. Next slides unpack **multi-band L1–L7** inventory and why one universal cost model fails.

**Three leaves — artifacts and runtimes.**
- **GPU / NPU / ASIC** — sim → silicon execution targets.
- **VCS artifacts** — control files, **ACF** (Advanced Control File / CompileIQ-style control artifact), kernels, memory plans; what you diff in git after an agent run.
- **Serving runtime** — freeze for replay; production path must reproduce offline admit decisions.

**Codesign feedback (ember band).**
Loops from silicon back toward ISA / dialect RFCs. Humans and chip EDA tools still own tape-out — **C10** boundary. Agents propose; oracles and humans validate.

**Invariant — say out loud.**
LLM guides search; it does **not** silently define unchecked executable behavior. Every agent path terminates in admit or classical fallback.

Visual note: feedback arrow from hardware routes left around the codesign block — mention it so eyes follow the diagram.
