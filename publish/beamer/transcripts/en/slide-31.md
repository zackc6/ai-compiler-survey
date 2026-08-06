# Slide 31: Technical Prediction — Critical Missing Parts Now

Highest-leverage bets to accelerate Horizon A. On-slide: four numbered bands with “w/o → consequence” on the right. Spoken: prioritize these before peripheral compiler internals.

**1. Money-grade oracle stack (T2 + T6) — w/o → demos.**
Local formal (Alive2-class) → shape-grid diff → statistical serving oracles → staged rollout. T2 admit machinery and T6 serving A/B together — not unit tests alone. Blocker one and gap 4.2 converge here. Without this ladder, agents produce fast-but-wrong kernels that pass cheap checks.

**2. Replayable artifact contract (T3) — w/o → CI rejects.**
Control files, kernels, heuristics with content-addressed cache keys and golden replay on model/compiler upgrade. ACF freeze is the product shape. Without replay, every agent run is a one-off; build CI cannot regress, and freeze-before-serve is impossible.

**3. Portable agent compile interface (T1) — w/o → re-glue.**
Summaries, actions, admit records portable across MLIR, Triton, Tile, StableHLO. Every vendor today wires bespoke tool servers. Without T1, hybrid stacks fragment — you ship a demo per substrate, not a platform.

**4. Open ladder + multi-IR data (T7 + T8) — w/o → incomparable.**
Correctness × speed × dollars-per-compile on a unified ladder, plus negative (failed) examples in corpora. KernelBench headlines without cost-to-compile and serving rungs cannot settle C2 or C9.

**Survey lean footer.**
T1–T5 ship as product surfaces inside the compiler boundary; T6–T10 are equally first-class — mostly outside classical lowering. E2E-optimal-seeking under F (product fitness: latency, energy, $/token, quality, cluster) needs all ten; soft merge M1 unifies the optimizer, not the execution substrate.

Closing beat: fund these four first. Everything else is acceleration on top of evidence and contracts you do not yet have.
