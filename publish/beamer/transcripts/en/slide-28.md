# Slide 28: Technical Prediction — Within The Compiler (T1–T5)

Within-compiler techniques in band layout. On-slide: each row is technique + unlocks, Exists, Missing. Spoken: claim → evidence → gap for all five.

**T1 — Typed interfaces → C3, C5, C6.**
Exists: CompileIQ agent skills, **Cake IR**, **Argus** tags, **TIRx**, **TileLang LSP**, **Pallas** block specs and memory spaces (MaxKernel’s TPU face; Mosaic still lowers), **IntOpt** intent, **LLM4IR** as the *negative*. Claim: **LLM-oriented IR** is the agent-visible face — schemas, not paste-and-pray. Missing: portable summaries and actions across MLIR, Triton/Gluon/TLX, Tile, Cake, Argus, TIRx, **Pallas** — today every stack re-glues. Unlocks narrow ACFs/hints over free rewrite (C3) and named default paths in release notes (C5).

**T2 — Admit / fallback → C6 hybrid.**
Exists on this slide: **Argus** layout-algebra + SMT, **AsmEvo** differential checks against the original AMDGPU code object, and ForgeMegakernel’s **mid-state oracle** during generation. Archer, Cake gates, and FlashInfer-Bench remain in the narrative. Claim: hybrid means classical lowering or a checker still admits. Missing: shared admit *product* plus trusted deterministic fallback every vendor documents. Unlocks C6-B — control plane, not compiler replacement.

**T3 — Control files + replay → C2, C5.**
Exists: CompileIQ ACFs, FlashInfer Trace + `apply()` into SGLang/vLLM. Claim: freeze artifacts are how you get zero LLM at serve. Missing: content-addressed cache keys; golden replay when the model or compiler upgrades. Unlocks median/p90 evidence on pinned traces (C2).

**T4 — Heuristic hooks / advisors → C1.**
Exists: Magellan/AlphaEvolve shippable C++, MLGO in-tree advisors, EmitC June 2026 PoR (plan of record: inliner → Android/Fuchsia → Chrome). Claim: parallel bets — evolutionary C++ *and* learned advisors both live. Missing: settled default on named apps — public Magellan patches displacing MLGO or EmitC-MLGO customer default.

**T5 — Dialect / ISA sinks → C9, C10.**
Exists: TritorX, KernelEvolve, **Cake** harness evolution (recurring failures become verifier rules / IR primitives), **Zomboss** compile-once TAIDL/ACT backends. Claim: coverage before peak; machine semantics should be compiled, not re-prompted. Missing: first-class change-*proposal* surfaces — not autonomous microarch tape-out (C10 rejected).

Closing line: within-compiler work constrains and admits; it does not replace lowering. Next slide: T6–T10 outside the compiler — where most settlement evidence must come from.
