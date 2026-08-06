# Slide 22: Blocker 3 — Agent↔compiler contract

Blocker three: how agents talk to compilers. On-slide: four full-width bands A through D, then the `admit_record` schema. Spoken: rank the options, show the lean, explain ACF.

**A — Natural language + pasted logs.**
Demo only. Fine for lab exploration; useless for money-grade CI. No reproducible action space, no bill of materials, no regression when the model drifts. Say out loud: if your contract is chat, you do not have a product contract.

**B — Structured admit traces.**
Build CI and bill of materials. Every admitted change carries graph hash, hardware ID, compiler version, oracle results, artifact digest, policy ID. This is what Archer and AgentCompile-class review loops produce. Traces are the source of truth agents and humans audit — not the chat transcript.

**C — Typed tool interfaces.**
Required action space. MCP (Model Context Protocol — tool server standard) class servers, `mlir-opt-repl`, CompileIQ skills, FlashInfer Trace `apply()` — agents propose within schemas the compiler validates. T1 (typed agent↔compiler interfaces) unlocks C3 (free rewrite vs advisory), C5 (default path), C6 (replace vs control plane). Lean: narrow ACFs and hints, not free IR rewrite.

**D — Hybrid view.**
Natural language as a *view* over B and C — summaries and explanations for humans, not executable authority. Product UX can stay conversational; CI reads admit records.

**Show the `admit_record` block.**
Walk the fields: `graph_hash`, `hw_id`, `compiler_ver`, `action[]`, `oracle[]`, `artifact_digest`, `policy_id`. This is the portable contract across MLIR, Triton, Tile, StableHLO. ACF = Advanced Control File — portable compiler knobs that freeze into VCS.

Closing line: lean is **C + B**. Typed tools constrain actions; admit traces make them regressable. Natural language is a lens, not the compiler API.
