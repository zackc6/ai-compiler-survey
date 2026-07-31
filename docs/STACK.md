# How the agentic compiler reshapes the stack (SW + HW codesign)

**Focus:** not “AI software in general,” but how an **agentic compiler** changes layers from framework UX down to silicon feedback.

Companions: [`ROADMAP.md`](ROADMAP.md) · [`SURVEY.md`](SURVEY.md) §5 · [`TAXONOMY.md`](TAXONOMY.md) · [`CONFLICTS.md`](CONFLICTS.md)

---

## Layer map (today → agentic)

| Layer | Classical role | Reshape by agentic compiler | Evidence |
|---|---|---|---|
| **1. Model / framework** | `torch.compile`, JAX/TF export | Agents consume graphs/regions; Amdahl-rank hot ops; write kernels back into eager/compile path | AutoKernel, Kernel Forge, AgentCompile |
| **2. Kernel DSL** | CUDA / Triton / Helion / Tile / CuTe / HIP | DSL becomes **agent training + search surface**; Helion raises abstraction; multi-DSL skills required | Helion, GEAK, CompileIQ, KForge, TRT-LLM agents PR |
| **3. Portable IR** | StableHLO, MLIR dialects | Must expose fingerprints, tool APIs, legality; free rewrite fails | mlirAgent, StableHLO, MLIR |
| **4. Compiler mid/back** | LLVM/XLA/Inductor/NVCC passes | Offline agents evolve heuristics; online agents pick passes/hints/ACFs; MLGO advisors persist | Magellan, MLGO, ACCLAIM, HintPilot, CompileIQ |
| **5. Oracles & profilers** | Unit tests, Alive2, NCU | Become **admit gates + reward**; federated profilers (MPP) required for hetero HW | Archer, LLM-VeriOpt, KernelEvolve, Ascend diagnosis |
| **6. Artifacts / VCS** | Binaries, schedules | **ACFs, evolved C++, verified kernels, optimization memory, bring-up corpora** | CompileIQ, Magellan, KernelBlaster, TritorX |
| **7. Serving runtime** | vLLM, TRT-LLM, custom ads stacks | Agent loops specialize serving kernels; must not break graph-level opts | GEAK, KForge vs TRT-LLM, KernelEvolve |
| **8. Silicon / sim** | Manual bring-up, ISA docs | Agents generate backends on **sim + silicon**; traces inform next ISA/IR (codesign) | TritorX, KernelEvolve, Ascend NPU paper |

---

## Four agent jobs on the stack

```text
(a) Online specialize     → layers 1–2–4–5–7   (CompileIQ, GEAK, AutoKernel, ACCLAIM)
(b) Offline evolve        → layer 4 (+ artifacts) (Magellan / AlphaEvolve)
(c) Oracle engineering    → layers 4–5–6         (Archer, CCC-adjacent)
(d) Bring-up / codesign   → layers 2–5–8         (TritorX, KernelEvolve, Ascend diagnosis, KForge)
```

Job **(d)** is the HW-codesign extension: still an **agentic compiler/toolchain** problem (kernels, dialects, tests), not general chip LLM design.

---

## Stack reshape theses (claim IDs)

| ID | Thesis | Status |
|---|---|---|
| S1 | Control plane becomes agentic; data plane stays classical | Supported — see CLAIMS A1 |
| S2 | Portability shifts from “write once IR” to “agent + oracle per backend” while IR remains necessary substrate | Contested — C4, C8 |
| S3 | New first-class artifacts (ACF/heuristics/memory/traces) change CI and code review | Supported — A3 |
| S4 | Custom ASIC competitiveness increasingly depends on agentic bring-up latency | Supported (industrial) — TritorX/KernelEvolve; watch second-vendor repro — C9 |
| S5 | Profilers and compiler internals move from human IDE tools to **agent APIs** | Watch — KernelEvolve MPP, Ascend hierarchy |

---

## What *not* to confuse with stack reshape

| Lookalike | Why it is weaker for *this* survey |
|---|---|
| Generic coding agents on app repos | No compile oracles → Tier C |
| Pure EDA/RTL LLM without kernel/IR loop | Out of scope unless tied to compiler admit |
| Vendor SKU lists without agent/oracle APIs | Tier B baselines only |

---

## Reading order

1. [`ROADMAP.md`](ROADMAP.md) horizons A/B  
2. This file’s layer table  
3. [`CLAIMS.md`](CLAIMS.md) A*/S*/P*  
4. Digests ★ in INDEX under *HW codesign* and *GPU kernels*
