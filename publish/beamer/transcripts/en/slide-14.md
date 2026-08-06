# Slide 14: What ships / does not by 2028

Horizon A concrete predictions — two columns plus a pill summary. This is what “hybrid wins” looks like in production by **2028**, not lab demos.

**Left — Predicted to ship (green).**
Walk each bullet with a spoken example:

- **Agent-addressable tool interfaces** — typed **MCP**-class servers, compile schema, admit hooks on Inductor/XLA/MLIR paths.
- **Hot-path specialize, not silent default-all** — agents run on pinned traces / hot kernels; classical path remains default for long tail.
- **Magellan *and* MLGO both live** — evolutionary C++ heuristics *and* in-tree neural advisors; **C1** may settle a default, but both families persist in serious orgs.
- **Oracle PR review in serious orgs** — Archer-class oracle-gated **PR** (pull request) before agent-generated compiler changes merge.
- **Coverage-first ASIC bring-up** — job (d): correctness surface before peak perf on new **NPU**/**ASIC** SKUs; TritorX ladder.
- **Triton-family primary; multi-DSL rising** — Triton/Tile/CuTe coexist; no single kernel DSL monopoly.

**Right — Does *not* ship (ember).**
Say these as explicit non-goals — saves roadmap arguments later:

- Unconstrained LLM replaces `opt`/Inductor — no admit, no fallback.
- One agent IR for all vendors — portable graph yes; agent training surface stays fragmented (**C4**).
- Kernel agents uniformly beat eager on fusion ladders — KernelBench shows fusion still hard; refinement buys correctness first.
- Autonomous microarch tape-out — **C10**; agents stress kernels/IR, not RTL replacement.

**Pill line (center bottom).**
Horizon A success = build-**CI** gated specialize + oracles + freeze artifacts. If their 2028 plan lacks all three, they are not on the hybrid path — they are on a demo path.

Closing beat: ship column is falsifiable; use checkpoints on next slides to watch settlement.
