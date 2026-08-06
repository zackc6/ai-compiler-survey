# Slide 3: Trend backdrop — two stacks converging

This is the §1 era slide — set history before the six trends on the next frame.

**The timeline spine.**
Walk left to right on the horizontal axis:

- **2018–22 — DL compilers:** TensorFlow XLA, TVM, Glow era. “Compilers for AI” mature but **fragmented substrate** — many graph IRs, vendor forks, no single agent addressability layer.
- **2020–23 — RL gyms:** CompilerGym and cousins — reinforcement learning (**RL**) policies inside opaque gym environments. Research-rich; shippable heuristics rare. The field is leaving this era.
- **2023–24 — LLM enters IR:** Large models propose pass lists, hints, and IR (**Intermediate Representation**) edits. mlirAgent-class work shows free rewrite is fragile; the community pivots toward constrained actions.
- **2025–26 — Agentic hybrid:** Tool-using agents, offline heuristic synthesis, kernel agents with verify-in-the-loop. This is *today* on the slide — highlighted steel/amber.
- **2027+ — ?** Deliberately open. The briefing’s job is to argue a *testable* hybrid path, not prophecy.

**Two stacks below the line.**
Left box: **Compilers for AI** — mature stacks (PyTorch → Inductor → Triton, StableHLO → XLA/IREE), production legality and lowering, but fragmented and not yet uniformly agent-callable. Right box: **AI for compilers** — rapid hybrid growth: Magellan-style offline eng, GEAK-style kernel loops, Archer-style oracle-gated **PR** (pull request) review. The stacks are *converging*, not colliding.

**Punchline — say it out loud.**
Next-gen does **not** mean throw away **LLVM** or **MLIR** (Multi-Level IR). It means make them **agent-addressable**: typed tools, admit gates, measured oracles, version-controlled artifacts — while deterministic lowering and build-**CI** (continuous integration) regressability stay on the classical data plane.

Closing beat: two stacks, one direction — hybrid control plane over substrates you already ship.
