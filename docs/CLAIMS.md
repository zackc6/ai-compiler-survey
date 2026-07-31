# Prediction claims ↔ evidence

Living map from falsifiable claims to digests. Update when evidence moves status.

Status: **Supported** · **Contested** · **Watch** · **Falsified**

---

## Architecture (agentic compiler)

| ID | Claim | Status | Best evidence | Conflicts |
|---|---|---|---|---|
| A1 | Agents own search/orchestration/synthesis; compilers own lowering, legality, measure, fallback | Supported | ACCLAIM, AgentCompile, HintPilot, mlirAgent (negative) | C3, C6 |
| A2 | Four agent jobs stick: (a) online, (b) offline heuristics, (c) engineering/review, (d) bring-up/codesign | Supported | (a) CompileIQ/GEAK/AutoKernel; (b) Magellan; (c) Archer; (d) TritorX/KernelEvolve | C5, C9 |
| A3 | ACFs, evolved heuristics, verified kernels, optimization memory, bring-up corpora become first-class artifacts | Supported | CompileIQ, Magellan, KernelBlaster, TritorX | — |
| A4 | Defaults stay classical until agents win on *distributions* in CI | Contested | Vendor blogs vs CompileIQ 2–3% docs, KernelBench-X | C2 |
| A5 | Unconstrained LLM will not replace `opt`/Inductor soon | Supported | mlirAgent; hybrid Tier A dominance | C3, C6 |

## Process & stack

| ID | Claim | Status | Best evidence | Conflicts |
|---|---|---|---|---|
| P1 | Offline heuristic synthesis and MLGO neural advisors remain parallel bets through 2028 | Contested | Magellan vs EmitC-MLGO | **C1** |
| P2 | Multi-DSL / multi-vendor agent skills become normal | Watch | KForge, GEAK v3, TRT-LLM agents, Helion+CompileIQ | **C4** |
| P3 | Compiler-oracle review beats generic forge AI for opt PRs | Supported (direction) | Archer; Tier C demoted | **C7** |
| S1 | Stack reshape is control-plane agentic over classical data plane | Supported | STACK.md · A1 | C6 |
| S4 | Custom ASIC TTM increasingly gated by agentic bring-up | Supported (industrial) | TritorX, KernelEvolve | **C9** |
| S5 | Profilers/compiler internals become agent APIs | Watch | KernelEvolve MPP, Ascend hierarchical diagnosis | C3 |

## Codesign (still agentic-compiler-centric)

| ID | Claim | Status | Best evidence | Conflicts |
|---|---|---|---|---|
| H1 | Pre-silicon sim + agents provide compiler/ISA feedback before tape-out | Supported (early) | TritorX QEMU future devices | C9, C10 |
| H2 | Coverage-first agents then perf agents is the bring-up ladder | Supported | TritorX → KernelEvolve | **C9** |
| H3 | Agents will not autonomously tape out chips by ~2031; they stress compilers/ISAs | Supported (prediction) | Scope of TritorX/KernelEvolve (kernels/toolchains) | **C10** |

---

## Settlement watch

| Signal | Moves | Digests |
|---|---|---|
| Public Magellan llvm + OpenEvolve recipes | C1 | magellan, openevolve |
| EmitC-MLGO default on Android/Chrome | C1 | mlgo-emitc-rfc |
| p50/p90 public ACF/kernel traces | C2 | compileiq-*, kernelbench-x |
| Second non-Meta ASIC reproduces TritorX-class coverage | C9 | tritorx |
| Agent IR contract where free rewrite beats advisors | C3 | acclaim vs hintpilot/agentcompile |
