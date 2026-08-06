# Slide 26: Cross-Cutting Research Agenda

Bridge from gap map to technique map. On-slide: six research boxes with arrows showing dependencies. Spoken: name each theme, tie to gaps, tee up T1–T10.

**Admit & fallback standards.**
Shared product semantics for admit, deterministic fallback, and oracle ladders — closes gaps 4.2 and feeds T2. AgentCompile and Archer exist as points; the missing piece is a portable admit *product* every vendor can regress.

**Agent tool / IR schemas.**
Typed interfaces across MLIR, Triton, Tile, StableHLO — T1, gap 4.4. CompileIQ, ACCLAIM, mlir-opt-repl are existence proofs; portable schemas are not.

**Open multi-IR corpora.**
Versioned IR dumps plus failed and miscompile negatives — T7, gaps 4.7 and 4.10. Meta LLM Compiler and KernelBook→TritonRL show demand; negatives are what stop reward hacking.

**Serving-level oracles.**
Whole-program and production A/B — T6, gap 4.1. FlashInfer-Bench + `apply()` is the serving-kernel rung; multi-month default-path stability is still missing.

**Provenance & human review.**
Signed admit records, CODEOWNERS, sandbox — T9, gaps 4.8 and 4.9. Magellan reviewable C++ and Archer oracle review are templates, not industry standard.

**Control-plane compile MVP.**
Workflow compile, ADG check, freeze, place — T10, gap 4.6. FlowCompile, Auto, AgentFlow are early; shared agent-graph IR with fail-closed CI is Horizon B substrate.

Closing line: these six themes unpack as the technique map T1–T10 on the next slides — for each: what exists, what is missing, which checkpoint it unlocks. Hybrid lean holds: enhancing only `opt`/Inductor/Triton internals is not enough.
