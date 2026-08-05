# Slide 9: Architecture Evolution — Today → A → B

Read the timeline left to right.

Today, 2025 to 26: ad-hoc agent loops on the control plane; MLIR Triton Inductor default on a mostly GPU data plane; sparse codesign and manual bring-up.

Horizon A, 2027 to 28: jobs a through d productized and CI-gated specialize; multi-DSL with fingerprints, tool APIs, and admit; early sim and first silicon feeding ISA or dialect RFCs.

Horizon B, about 2029 to 31: the control plane itself is compiled — ADG, freeze, place; multi-backend fleets with ACF and heuristics in VCS; a steady pre-silicon loop that is still not autonomous EDA.

Closing line: the data plane never goes away; the agent graph becomes compiled, audited, and amortized.
