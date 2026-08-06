# Slide 5: Keep substrate, change control plane

This slide translates the six trends into a product decision: what to **preserve** vs what to **adopt**. Two columns plus an anti-pattern banner.

**Preserve — the classical data plane (left, green).**
These are non-negotiable for production compilers:

- **Deterministic lowering** — same IR in, same legal binary out; no silent nondeterminism in the default path.
- **Library kernels** — vendor-tuned GEMM, attention, collectives; agents propose *around* them, not instead of them on day one.
- **Build-CI regressability** — every admit candidate runs through pinned traces; a win must reproduce in **CI** (continuous integration), not only in a notebook.
- **Local formal checks** — Alive2-class legality on LLVM IR slices; cheap enough to run per proposal.

Say it: the execution substrate you already trust stays. Agents do not get to bypass legality because the model is confident.

**Adopt — the hybrid control plane (right, steel).**
This is where 2025–31 budget should flow:

- **Advisory search** — pass lists, pragmas, hints, narrow rewrite APIs — not free-form codegen into `opt`.
- **Multi-agent orchestration** — propose → measure → reflect loops; workflow compile and freeze for replay.
- **Heuristic synthesis** — Magellan-class offline evolution into shippable C++ checked into tree.
- **Profile / verifier feedback** — profiles, microbenchmarks, and stacked oracles close the loop on admit.

**Anti-pattern — say it firmly (ember banner).**
Replacing `opt`/Inductor with **unconstrained LLM codegen** — no typed tools, no admit hash, no classical fallback. That is C3/C6 failure mode: wide rewrite API with weak oracles. The survey rejects it for Horizon A; hold hybrid (**C6-B**).

Closing beat: keep substrate, change control plane — the settled SURVEY lean in one slide.
