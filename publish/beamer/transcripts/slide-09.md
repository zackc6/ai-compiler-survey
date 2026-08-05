# Slide 9: Architecture Evolution — Component Changes

Walk left to right, but spend the time inside each box — what components change.

**Control plane:** Today is ad-hoc agent loops (chat/tools, GEAK, ACCLAIM, Magellan) with no typed admit contract. Horizon A productizes jobs (a)–(d) and CI-gates specialize. Horizon B compiles the control plane itself: workflow compile, ADG check, freeze, hetero place.

**Data plane:** Today is classical MLIR/Triton/Inductor, GPU-mostly, thin tools. Horizon A makes it agent-addressable — multi-DSL fingerprints, typed tool APIs, admit, oracles. Horizon B is multi-backend fleets with ACF, heuristics, and memory as VCS artifacts — still classical lowering.

**Codesign:** Today sparse/manual. Horizon A closes early sim + first-silicon feedback into ISA/dialect RFCs. Horizon B is a steady pre-Si → bring-up → next tape-out loop, not autonomous EDA (C10).

**Artifacts:** binaries → + ACF/hints/kernels/corpora → + frozen agent workflows / cognition binaries.

Closing line: focus on which components thicken; the data plane never goes away.
