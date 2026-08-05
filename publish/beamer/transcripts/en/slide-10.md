# Slide 10: Data plane — ~6–7 abstraction bands (not one)

This is the inventory behind the classical data plane on the architecture slide.

Must-have today: six bands. L1 framework capture. L2 portable graph — StableHLO-class, including portable shard annotations. L3 mid-IR — MLIR, layout, passes. L4 kernel DSL — Triton, Helion, Tile, CuTe. L5 backend and ISA. L6 runtime and serving — CUDA Graphs, KV paths.

L7 fleet and cluster is maturing: placement and collectives. Today it often lives split across L2–L3 plus runtime, but once compilation means multi-node place, treat it as a real band.

What does *not* need its own IR: power and energy are objectives plus oracles; dollars-per-token and latency SLOs are control-plane policy; safety is provenance and admit. Optional L0 for CPU/LLVM paths.

Lean to say out loud: keep the bands; agents unify contracts and orchestration — not one mega-IR. Claim A6 / S6.
