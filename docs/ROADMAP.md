# Roadmap: agentic compiler 2027–28 and ~5 years

**North star:** the **agentic compiler** — a hybrid control plane (LLM/agents + oracles) over a classical data plane (MLIR/LLVM/Inductor/Triton/Tile/vendor backends), including **HW–SW codesign** loops. Software catalogs and silicon bring-up are evidence for that target, not ends in themselves.

Companions: [`SURVEY.md`](SURVEY.md) §5 · §5.7 (commercialization) · [`STACK.md`](STACK.md) · [`CLAIMS.md`](CLAIMS.md) · [`CONFLICTS.md`](CONFLICTS.md)

---

## Horizon A — 2027–2028 (near)

Falsifiable sketch conditioned on C1–C10.

### What ships

| Capability | Predicted state | Leading evidence | Conflicts |
|---|---|---|---|
| **Agent-addressable compilers** | Tool APIs, structured IR summaries, admit/fallback become normal in LLVM/Inductor/vendor toolchains | ACCLAIM, HintPilot, AgentCompile, mlirAgent (negative free-rewrite) | C3, C6 |
| **Online specialization (job a)** | Hot kernels/paths use agent or evolutionary search (ACF, hints, Triton/Helion refine) in CI for *some* products — not yet silent default for all builds | CompileIQ, GEAK, AutoKernel, Kernel Forge | C2, C5 |
| **Offline heuristic synthesis (job b)** | Magellan-class C++ heuristic evolution *and* MLGO neural advisors both still live (parallel bets) | Magellan, EmitC-MLGO RFC | **C1** |
| **Engineering agents (job c)** | Compiler-oracle PR review (Alive2/`opt`) in serious LLVM/AI-compiler orgs; generic forge AI stays UX | Archer | **C7** |
| **Bring-up / codesign agents (job d)** | Coverage-first ATen/Triton backend generation on sim + silicon becomes standard for *new* ASICs | TritorX, KernelEvolve, Ascend hierarchical diagnosis | **C9** |
| **Verified ML construction (Compiler 2.0 / MOCHA)** | Early open releases of LLM→eqsat→formal-admit rewrite / retarget tooling; not yet default production `opt` | Ken Kennedy plenary 2026; Aarno/MIT/UIUC MOCHA | C3, C6 |
| **DSL surface** | Triton-family (Triton/Helion) remains primary agent training surface; Tile/CuTe/HIP/FlyDSL force multi-DSL skills | Helion, CompileIQ Helion path, TRT-LLM agents, KForge | **C4** |

### What does *not* ship by 2028

- Unconstrained LLM replaces `opt`/Inductor end-to-end without classical admit (**C6**).
- Single “one agent IR” for all vendors (**C4** unresolved).
- Kernel agents uniformly beat eager/libraries on fusion-heavy public ladders (**C2**).
- Agents design *silicon microarchitecture* autonomously (codesign is **feedback to humans/EDA**, not tape-out autopilot) — see Horizon B.

### Near-term milestones (watch)

1. Public Magellan/OpenEvolve llvm patches **or** EmitC-MLGO default (**C1**).
2. CompileIQ/GEAK publish p50/p90 + pinned traces (**C2**).
3. TritorX-like bring-up reproduced outside Meta (second ASIC vendor) (**C9**).
4. PyTorch/LLVM release notes list agent/ACF jobs as supported workflows (**C5**).
5. MOCHA / Compiler 2.0 publishes OSS rewrite+verify evals or retarget demos (program through ~2028).

---

## Horizon B — ~2029–2031 (next ~5 years from 2026)

Still centered on the **agentic compiler** as the product; HW codesign is how that product eats the O(ops × devices × gens) matrix.

### Architecture evolution

How the hybrid stack thickens from ad-hoc agent loops to a **compiled control plane** over a classical data plane. (Target stack detail: [`SURVEY.md`](SURVEY.md) §5.1.)

```text
 TODAY (2025–26)            HORIZON A (2027–28)             HORIZON B (~2029–31)
 ────────────────           ───────────────────             ────────────────────
 Ad-hoc agent loops         Jobs (a–d) productized          Control plane compiled
 on classical compilers     CI-gated · not silent default   ADG · freeze · place

 ┌─────────────┐            ┌──────────────────┐            ┌────────────────────┐
 │ Agents      │            │ CONTROL PLANE    │            │ CONTROL PLANE      │
 │ chat/tools  │            │                  │            │                    │
 │ GEAK·ACCLAIM│            │ (a) online       │            │ (a–d) + substrate  │
 │ Magellan …  │            │ (b) offline      │            │  workflow compile  │
 └──────┬──────┘            │ (c) oracle review│            │  ADG static check  │
        │ tools             │ (d) bring-up /   │            │  freeze / amortize │
        ▼                   │     codesign     │            │  hetero place      │
 ┌─────────────┐            └────────┬─────────┘            └─────────┬──────────┘
 │ DATA PLANE  │                     │ typed tools                    │
 │ MLIR/Triton │◄── still default ───┼ admit + oracles                │
 │ Inductor …  │                     ▼                                ▼
 └──────┬──────┘            ┌──────────────────┐            ┌────────────────────┐
        │                   │ DATA PLANE       │            │ DATA PLANE         │
        ▼                   │ multi-DSL +      │            │ multi-backend      │
   GPU (mostly)             │ fingerprints /   │            │ ACF · heuristics · │
                            │ tool APIs        │            │ memory as VCS arts │
                            └────────┬─────────┘            └─────────┬──────────┘
                                     │                                │
                                     ▼                                │
                            ┌──────────────────┐                      │
                            │ CODESIGN (early) │◄── cov/perf traces ──┤
                            │ sim + 1st Si →   │                      ▼
                            │ ISA/dialect RFCs │            ┌────────────────────┐
                            │ (to humans/EDA)  │            │ CODESIGN (steady)  │
                            └──────────────────┘            │ pre-Si → bring-up  │
                                                            │ → next tape-out    │
                                                            │ (not auto EDA)     │
                                                            └────────────────────┘

 ARTIFACT STORE (grows →)
   binaries → + ACF/hints → + evolved C++ / verified kernels / bring-up corpora
            → + frozen agent workflows / cognition binaries (control-plane compile)
```

**Read left→right:** agents stay on the control plane; the data plane never goes away; what changes is **how compiled, audited, and amortized** the agent graph becomes, and how tightly silicon feedback closes the loop.

### Predicted shifts

| Theme | 5-year outcome | Confidence |
|---|---|---|
| **Default compile path** | Classical lowering remains default; agentic specialize is **opt-in then CI-gated default for hot paths** | Medium-high |
| **Artifact store** | VCS grows first-class **ACFs, evolved heuristics, verified kernels, optimization memory, bring-up corpora** | High |
| **Heterogeneous serving** | Agentic multi-backend kernel/forge loops are how non-NVIDIA fleets stay viable (MTIA/AMD/Intel/NPU) | Medium-high (KernelEvolve, KForge, TritorX) |
| **HW codesign loop** | Pre-silicon: agents + sim generate coverage and compiler stress; post-silicon: agents map ISA/IR pain → RFC for next chip / dialect. Humans + EDA still own tape-out | Medium |
| **Verification** | Local formal (Alive2-class) + statistical serving oracles + OpInfo-scale suites compose; whole-program GPU/NPU formal still incomplete | Medium |
| **Human role** | Experts own oracles, ownership, security, ISA contracts; agents draft kernels/heuristics/backends | High |
| **Will still not happen** | Fully autonomous chip + compiler co-generation without human architectural intent; end-to-end LLM-as-`opt` | High |

### Codesign-specific roadmap (still agentic-compiler-centric)

| Phase | Agentic compiler does | Hardware team gets |
|---|---|---|
| Pre-silicon | TritorX-style coverage on QEMU/sim; KernelEvolve-style search under draft ISA docs | Early “can we run NanoGPT/DLRM ops?” signal; IR/dialect bugs |
| Bring-up | Coverage agents → perf agents ladder | Weeks→hours for ATen/Triton backend skeleton |
| Steady-state | Online specialize + memory (KernelBlaster) across gens | Portability when L2/TMA/SRAM rules change |
| Next tape-out | Aggregated failure modes from agent traces (illegal ops, alignment, missing atomics) | Prioritized ISA / memory-system / compiler-pass requests |

**Non-goal:** surveying EDA/RTL LLM tools unless they close the loop into **compiler IR, kernels, or admit oracles**.

---

## Success metrics for this roadmap

1. Can a new ASIC expose an agent-addressable compile/test API and reach >80% ATen coverage via agents within a release cycle? (TritorX bar)
2. Do agentic specialize jobs show **distributional** wins in CI (p50), not only best kernels? (C2)
3. Are Magellan-class and MLGO-class paths both still productive or has one settled? (C1)
4. Does the stack treat traces/ACFs/heuristics as reviewable artifacts with owners? (§4.8–4.9)
5. Can you ship without NL-only contracts — typed tools + replayable admit traces + memory that survives model swap? ([SURVEY §5.7](SURVEY.md#57-from-prediction-to-commercial-practice--critical-problems))

Update when CONFLICTS settle or new Tier A codesign evidence lands.
