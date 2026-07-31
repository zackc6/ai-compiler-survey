# Conflicting signals (keep unresolved until evidence settles)

This page records **disagreements across papers, vendor blogs, OSS repos, and forums** that matter for predicting the next-generation AI compiler and how agents change that future. We do **not** force a premature resolution; each conflict states both sides, why it matters for the prediction, and what would settle it.

Companion: [`SURVEY.md`](SURVEY.md) § Future · [`PRODUCTS.md`](PRODUCTS.md) · [`REPOS.md`](REPOS.md)

---

## How to read a conflict row

| Field | Meaning |
|---|---|
| **Claim A / Claim B** | Competing readings from primary sources |
| **Why it matters** | How the winner changes the next-gen compiler sketch |
| **Settlement signal** | What evidence would decide it |

---

## C1 — Evolve shippable C++ heuristics vs embed neural advisors (Magellan vs MLGO)

| Side | Sources | Position |
|---|---|---|
| **A — Synthesize readable heuristics** | Magellan paper/slides; AlphaEvolve lineage; OpenEvolve | Agents rewrite **EVOLVE-BLOCK** C++ inside LLVM/XLA; ship like human passes; Magellan claims inlining beats decades of manual work; slides hope to leapfrog NN policies |
| **B — Keep/improve neural MLGO** | LLVM Discourse EmitC RFC; IR2Vec+MLGO RFC; ongoing MLGO meetings (2026) | Production Chrome/Android/Fuchsia still invest in **in-tree NN advisors**; EmitC/TOSA path removes TF build deps so neural policies stay deployable |

**Why it matters.** If A wins, the next-gen control plane is an **offline evolutionary coding agent** whose output is ordinary compiler source. If B wins, the data plane keeps **learned policies** as first-class runtime advisors, and agents mainly help *train/feature* those NNs.

**Settlement signal.** Public Magellan heuristics land in llvm-project *and* displace MLGO on the same size/perf apps; or EmitC-MLGO becomes the default path for Android/Chrome while Magellan stays Google-internal.

---

## C2 — Vendor “production agent” wins vs sober benchmark ceilings

| Side | Sources | Position |
|---|---|---|
| **A — Strong commercial wins** | NVIDIA CompileIQ blog (Meta up to ~15% on TritonBench/Helion); AMD GEAK v3 blogs (repo-level HIP/Triton/FlyDSL); AlphaEvolve Cloud GA | Agent/autotune control planes already deliver meaningful production speedups |
| **B — Hard ceilings & regressions** | CompileIQ docs (often **2–3%** on highly optimized kernels); KernelBench / KernelBench-X (many correct kernels slower than eager; refine↑correctness can ↓avg speedup; fusion hard) | Headline speedups are workload-selected; iterative agents can chase correctness at the cost of performance |

**Why it matters.** Prediction of “agents become default compile” needs median/CI wins, not only cherry-picked kernels. Overclaiming delays investment in oracles and traces (§4.2–4.3).

**Settlement signal.** Reproducible public ACF/kernel agent traces with fixed compiler versions, reporting **distribution** (p50/p90) not only best case; KernelBench-X-style fusion suites remain unsolved or get solved.

---

## C3 — LLMs rewrite IR/code freely vs must stay advisory

| Side | Sources | Position |
|---|---|---|
| **A — Multi-level LLM rewrite works with tests** | ACCLAIM (compiler–LLM cooperation); GEAK generate–eval–reflect; KernelAgent | Guiding agents interleave LLM rewrites with compiler tools; tests/profiles admit candidates; speedups reported |
| **B — Direct IR transform fails** | mlirAgent (frontier models **below identity** on IR transforms); HintPilot/AgentCompile design (hints/templates only) | Unconstrained IR rewrite is unsafe/weak; successful systems **constrain** the action space |

**Why it matters.** Next-gen architecture either exposes a **wide rewrite API** (with strong oracles) or a **narrow advisory API** (hints, knob ACFs, heuristic blocks). These are different products.

**Settlement signal.** Shared agent IR contract + oracle suite where free rewrite consistently beats constrained advisors on correctness×perf; or industry standardizes on advisory-only admit gates.

---

## C4 — Kernel DSL future: Triton vs CUDA Tile (and friends)

| Side | Sources | Position |
|---|---|---|
| **A — Triton remains the agent surface** | Inductor default path; KernelBench; KernelLLM; GEAK Triton path; awesome-LLM-driven-kernel-generation catalog | Ecosystem, benchmarks, and agents already converge on Triton |
| **B — Tile / CuTe / HIP / FlyDSL fragment the surface** | NVIDIA CUDA Tile + CompileIQ; TRT-LLM Claude agents for CuTe/TileIR/Triton/CUDA; GEAK multi-language (HIP, FlyDSL, TileLang) | Vendors push hardware-native tile IRs; agents must become multi-DSL or lose peak |

**Why it matters.** Training data, tool APIs, and “one agent IR” bets succeed or fail with this choice (§4.4, §4.7).

**Settlement signal.** One DSL becomes the dominant *agent training* corpus; or a portable tile IR wins; or multi-DSL agents (TRT-LLM skills pattern) become the norm.

---

## C5 — Online compile-time agents vs offline compiler-engineering agents

| Side | Sources | Position |
|---|---|---|
| **A — Online (in the compile/serve loop)** | CompileIQ ACFs; HintPilot; AgentCompile; GEAK on serving stacks; AlphaEvolve Cloud for algo search | Users pay tokens/GPU at optimize time; artifacts are configs/kernels per workload |
| **B — Offline (change the compiler once)** | Magellan; MLGO training; Archer PR review; Anthropic Claude C Compiler | Agents change **source of the compiler** or review PRs; users get classical `-O3`/`opt` afterward |

**Why it matters.** These are two different “agent futures.” A hybrid org may need both, but roadmaps and cost models differ.

**Settlement signal.** Which path shows up as the *default* flag or CI job in PyTorch/LLVM/CUDA release notes over 12–24 months.

---

## C6 — Agents replace compilers vs agents are the control plane

| Side | Sources | Position |
|---|---|---|
| **A — Agents can build/replace large compiler surfaces** | Anthropic CCC (~100kLoC Rust compiler); some HN/forum optimism | Agent teams author compilers; classical eng bottleneck shrinks |
| **B — Hybrid control/data plane is the durable pattern** | New Compiler Stack survey; mlirAgent limits; ACCLAIM cooperation framing; vendor stacks still ship TRT-LLM/Inductor/XLA | Data plane (lowering, legality, measure) stays classical; agents search/synthesize/advise |

**Why it matters.** Our survey’s executive verdict bets on **B**. A would rewrite goals toward “agent-authored compilers” as the primary object.

**Settlement signal.** A production AI stack whose *default* lowering path is agent-generated without a classical admit/fallback compiler underneath—not a research demo.

---

## C7 — Generic SCM AI review vs compiler-oracle review

| Side | Sources | Position |
|---|---|---|
| **A — Forge AI is enough** | Gerrit ai-code-review / ReviewAI / native AI chat; generic GitHub PR bots | Put LLM on the diff; scale human review |
| **B — Compiler-specialized tools required** | Archer (Alive2/LLUBI/`opt`); LLVM Discourse agent-PR experience | Miscompiles need domain oracles; generic review is HITL UX only |

**Why it matters for *this* survey.** Generic Gerrit plugins are **weak evidence** for next-gen *compilers*; Archer-class tools are strong. Cataloguing forge plugins without oracles misaligns with the prediction goal.

**Settlement signal.** A Gerrit/GitHub bot that blocks merge on failed Alive2/KernelBench-class checks becomes default in llvm-project or a major AI compiler.

---

## C8 — “AI compiler” means DL graph compilers vs LLM-for-LLVM

| Side | Sources | Position |
|---|---|---|
| **A — Compilers for AI models** | TVM/XLA/Inductor/TRT-LLM/OpenVINO product docs | Next-gen = better graph→device stacks (Tile, StableHLO, Neuron NKI) |
| **B — AI for compilers** | Magellan, LLM Compiler, Compiler-R1, Archer | Next-gen = agents inside LLVM/XLA/kernel eng |

**Why it matters.** Commercial catalogs over-weight A; research catalogs over-weight B. Prediction must keep **both stacks converging**, with agents as the cross-cut—not pick one catalog.

**Settlement signal.** (Already partially here.) Products that expose agent APIs *on* DL compilers (CompileIQ, GEAK, Magellan→XLA) are the convergence proofs.

---

## Working stance for this survey (until settlement)

1. Prefer **hybrid control/data plane** (C6-B) as the prediction baseline.
2. Treat Magellan-style **heuristic synthesis** and MLGO **neural advisors** as **parallel production bets** (C1 unresolved).
3. Discount single-number vendor speedups without distribution/oracle context (C2).
4. Assume **constrained actions + strong oracles** until free rewrite proves itself (C3).
5. Demote generic SCM AI plugins to Tier C evidence (C7).
6. Keep DL-compiler products as **Tier B baselines**, not as the definition of next-gen (C8).

Update this file when a conflict gains a decisive public settlement.
