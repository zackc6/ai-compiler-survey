# Slide 9: Architecture evolution — component changes

Walk **left to right** across three eras — TODAY (2025–26), HORIZON A (2027–28), HORIZON B (~2029–31). Four rows: CTRL, DATA, CODE (codesign), ART (artifacts). Spend time *inside* each cell — what actually changes.

**Control plane row (steel).**
- *Today:* Ad-hoc agent loops — chat/tools, GEAK, ACCLAIM, Magellan experiments — **no typed admit** contract; every team reinvents orchestration.
- *Horizon A:* Jobs **(a)–(d)** productized — online/offline/review/bring-up as SKUs; build-**CI** gated specialize becomes normal.
- *Horizon B:* Control plane **compiled** — workflow compile, **ADG** check, freeze, audited agent graph amortized like a compiler binary. Not “bigger chat”; compiled orchestration.

**Data plane row (amber).**
- *Today:* Classical **MLIR**/Triton/Inductor, **GPU**-mostly; agent tools thin.
- *Horizon A:* **Agent-addressable** — multi-DSL fingerprints, typed tool APIs, admit on hot path, oracles wired per band.
- *Horizon B:* **Multi-backend fleets** — **ACF**s, heuristics, memory plans as **VCS** artifacts; classical lowering *still* runs underneath.

**Codesign row (ember).**
- *Today:* Sparse/manual; human bring-up dominant; weak sim↔compiler loop.
- *Horizon A:* Early feedback — sim + first silicon → ISA/dialect proposals; TritorX / KernelEvolve-class.
- *Horizon B:* Steady pre-silicon → bring-up → next chip loop — **not** autonomous design (**C10**).

**Artifacts row (mute).**
- *Today:* binaries + sparse hints.
- *Horizon A:* + control files / kernels / C++ heuristics / corpora.
- *Horizon B:* + frozen agent workflows (cognition binaries — replayable agent graphs).

**Closing line on slide footer.**
Components thicken left→right; data plane stays; agent graph becomes compiled and amortized. Say it: focus on *which components thicken* — the data plane never goes away. Bridge to slide 10: here is the band inventory inside that data plane.
