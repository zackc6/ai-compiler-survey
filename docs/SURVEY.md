# Next-Gen AI Compiler Survey (expanded)

**Last updated:** 2026-08-04 (roadmap folded into §5.5)  
**Companion digests:** [`../publications/`](../publications/)  
**Status:** [`../STATUS.md`](../STATUS.md)  
**Conflicts:** [`CONFLICTS.md`](CONFLICTS.md) · **Repos map:** [`REPOS.md`](REPOS.md) · **Products:** [`PRODUCTS.md`](PRODUCTS.md)

---

## 0.1 North star

**Primary goal:** Predict the **next-generation agentic compiler** (architecture + process through ~2027–28 and ~5 years), including how it reshapes the **software stack** and **HW–SW codesign** — without drifting into general EDA.

Everything else (papers, GitHub/Gerrit, commercial SKUs, forums, ASIC bring-up studies) is **evidence** for that prediction—not a catalog for its own sake. When sources disagree, they go in [`CONFLICTS.md`](CONFLICTS.md) rather than being silently averaged.

**Executive verdict.** Compilation is shifting from **fixed pass pipelines + black-box autotuning** toward **hybrid LLM–compiler loops**. Empirically, the winning pattern is:

> **Agents own semantic search, orchestration, and artifact synthesis. Compilers own lowering, legality, measurement, and fallback.**

Agents reshape the **control plane** more than they replace the **data plane**. A fourth job — **accelerator bring-up / codesign feedback** on sim+silicon — is now Tier A evidence (TritorX, KernelEvolve), still centered on kernels/IR/oracles. See [§5](#5-future-prediction-what-next-gen-looks-like) (incl. roadmap §5.5), [`STACK.md`](STACK.md), [§6](#6-conflicts-pointer), [§4](#4-whats-missing--under-covered-q4).

**Sub-agent substrate (in scope).** Multi-agent **workflow compilers**, **AGI compilers** that freeze agent graphs into deployable artifacts, **static analysis of agent DAGs**, and **heterogeneous agent serving** are first-class evidence for how the control plane is built, secured, and productized—not side topics. Digests: [Auto](../publications/auto-agi-compiler.md), [FlowCompile](../publications/flowcompile.md), [AgentFlow](../publications/agentflow.md), [Heterogeneous agentic AI](../publications/agentic-ai-hetero-systems.md).

---

## 1. What’s the trend now? (Q1)

### 1.1 Two stacks converging

| Stack | Question it answers | Maturity |
|---|---|---|
| Compilers for AI | How do we lower neural graphs to GPUs/TPUs efficiently? | Mature substrate (TVM/XLA/MLIR/Triton); still fragmented |
| AI for compilers | How do we choose passes, write heuristics/kernels, use feedback? | Rapid 2023–2026 growth; hybrid systems dominate |

“Next generation” is not “throw away LLVM/MLIR.” It is **making those stacks agent-addressable**: structured summaries, bounded candidate spaces, tool APIs, and reward oracles.

### 1.2 Era timeline

| Era | Label | What changed |
|---|---|---|
| 2018–2022 | DL compilers mature | TVM/Ansor, XLA, Glow; MLIR born from TF/XLA needs; cost-model autotune |
| 2020–2023 | ML-for-compiler RL | Autophase, CompilerGym, MLGO inlining/regalloc; neural policies hard to ship |
| 2023–2024 | LLM enters IR | Pass-list LLMs; Meta LLM Compiler foundation models; compiler feedback loops |
| 2025–2026 | Agentic hybrid era | Multi-agent tuners, verifier-RL, heuristic synthesis, Triton kernel agents, generative compilation, vendor CompileIQ / GEAK |

### 1.3 Six active trends (detailed)

#### Trend A — Hybrid guidance, not LLM-as-compiler

Direct LLM IR rewrite is repeatedly fragile. mlirAgent reports frontier models scoring **below identity** on IR transforms. Systems that succeed constrain the LLM:

- **AgentCompile:** LLM emits advisory metadata only; templates + checks + benchmarks admit CUDA.
- **HintPilot:** LLM inserts compiler-validated pragmas/attributes, not arbitrary rewrites.
- **Meta LLM Compiler / Compiler-R1:** LLM proposes pass sequences; `opt` applies them.

#### Trend B — From RL gyms to LLM agents

CompilerGym exposed LLVM passes as OpenAI Gym environments (Autophase features, IR instruction-count rewards). That lowered the barrier for RL researchers but policies were often opaque and brittle across compiler versions.

2024–26 shifts toward:

1. **Foundation models** pretrained on IR/asm (Meta LLM Compiler: 546B tokens).
2. **Tool-using agents** trained with SFT+RL (Compiler-R1).
3. **Inference-only multi-agent tuners** that avoid heavy offline training (AutoPass).
4. **Program-synthesis of heuristics** that land as ordinary C++ (Magellan), recovering deployability that neural-in-the-compiler lacked.
5. **Control-plane substrate for sub-agents:** compile/freeze agent workflows ([FlowCompile](../publications/flowcompile.md), [Auto](../publications/auto-agi-compiler.md)), analyze agent programs as ADGs ([AgentFlow](../publications/agentflow.md)), and place agent stages on hetero serving ([Heterogeneous agentic AI](../publications/agentic-ai-hetero-systems.md))—so multi-agent compiler loops become compiler-shaped, not only chat-shaped.

#### Trend C — MLIR + Triton as default substrate

Practical GenAI path today:

```text
PyTorch → Dynamo/Inductor → Triton → PTX/CUDA (or CUDA Tile IR)
```

Parallel portable path:

```text
Framework → StableHLO → XLA or IREE → device backends
```

MLIR remains the shared engineering substrate even when product branding differs (OpenXLA, Triton internals, vendor AI compilers, CIRCT). Industry critique (Modular/Lattner) notes fragmentation and that open MLIR AI dialects have not always matched CUDA peak for LLM inference—hence Triton, CUTLASS, FlashAttention, and now CUDA Tile / CompileIQ.

#### Trend D — Kernel agents go industrial

Writing GPU kernels is the bottleneck for new model architectures and non-NVIDIA portability.

- **KernelBench (ICML 2025):** 250 PyTorch tasks; metric `fast_p` = correct **and** faster than baseline. Frontier models still often <20% one-shot; iterative refinement helps.
- **KernelBench-X:** refinement raises correctness but can **hurt** average speedup; many correct kernels still lose to eager; fusion tasks remain hard.
- **GEAK (AMD):** generator/evaluator/reflector/optimizer loop for Triton on Instinct; reported up to ~63% execution accuracy and ~2.59× speedup on suites.
- **Meta KernelLLM:** 8B model specialized for PyTorch→Triton; competitive Pass@k vs much larger general models on KernelBench-Triton.
- **AgentCompile:** compiler-bounded CUDA specialization for transformer inference graphs.

#### Trend E — Verification enters the loop

Correctness strategies, from weakest to strongest (local):

1. Compile + unit tests / LLM-generated tests (ACCLAIM).
2. Numerical checks vs reference path (AgentCompile).
3. Round-trip / recompile checks (LLM Compiler disassembly).
4. Formal semantic equivalence (Alive2 in LLM-VeriOpt rewards).

Formal coverage is still mostly **local peephole / IR**. Whole-program GPU races and FP nondeterminism lack equally strong oracles.

#### Trend F — Compilers broaden their object

- **Generative Compilation:** sealors complete partial Rust so the compiler can diagnose **during** LLM decoding—not only after file completion.
- **Compiler.next:** treat FMware (prompts, agents, free parameters) as a multi-objective search/compile problem for SE 3.0.
- **Anthropic Claude C Compiler:** agent teams *build a compiler* (~100kLoC Rust) capable of Linux kernel builds—adjacent but important: agents as compiler engineers, not only compile-time optimizers.
- **Magellan / AlphaEvolve:** agents rewrite the heuristic C++ inside production compilers (Google reports production inlining usage and XLA experiments).

### 1.4 Venue map

| Community | What to watch |
|---|---|
| CGO / CC / ASPLOS / PLDI / MLSys | Systems + compilers; **Compiler 2.0** Ken Kennedy Award plenary (HPCA/CGO/PPoPP/CC 2026) |
| NeurIPS / ICML (+ C4ML) | Methods + KernelBench / Reasoning Compiler / Compiler-R1 |
| ACL Findings | HintPilot-style SE/NLP crossover |
| LLVM Discourse (LLVM ♥ ML workshop) | MLGO, Magellan, agent PR review |
| Vendor blogs | NVIDIA CUDA Tile/CompileIQ, AMD GEAK, Meta KernelLLM/LLM Compiler, DeepMind AlphaEvolve, Modular |
| DARPA / labs programs | **MOCHA** (ML + optimization-guided compilers for hetero HW) |

### 1.5 Public vision works (what’s out there)

Besides system papers, several **public agendas** shape the “next compiler” debate. Digests live under Surveys & vision in [`../publications/INDEX.md`](../publications/INDEX.md).

| Vision | Axis | Digest |
|---|---|---|
| **Compiler 2.0** (Amarasinghe; CC’20 → CGO’22 → Ken Kennedy plenary 2026) | Restore high-level→near-peak on accelerators; ML + better abstractions to *build/retarget* compilers | [compiler-2.0-cgo2026](../publications/compiler-2.0-cgo2026.md) ★ · lineage [’22](../publications/compiler-2.0-cgo2022.md) · [’20](../publications/compiler-2.0-modernize-ml.md) |
| **MOCHA / Aarno Compiler 2.0** (funded) | LLM rewrite synthesis + eqsat + Rocq; data-frugal cost models; ISA-as-rewrites | [compiler-2.0-mocha-aarno](../publications/compiler-2.0-mocha-aarno.md) ★ |
| **New Compiler Stack** survey | LLM as Selector / Translator / Generator; hybrid systems win | [new-compiler-stack-survey](../publications/new-compiler-stack-survey.md) |
| **Compiler.next** | Broaden compile object to FMware (prompts, agents, knobs) | [compiler-next](../publications/compiler-next.md) |
| **MLIR formal theories** | Read AI compilation through formal lenses | [mlir-formal-theories](../publications/mlir-formal-theories.md) |
| **Automated kernel generation** survey | Kernel-agent landscape in the LLM era | [automated-kernel-generation-survey](../publications/automated-kernel-generation-survey.md) |
| **IEEE Pulse** LLM-compilers outlook | Challenges / future direction essay | [ieee-pulse-llm-compilers](../publications/ieee-pulse-llm-compilers.md) |

**Not treated as current vision peers here:** pre-LLM CACM “Compiler Research: The Next 50 Years” (2008 NSF workshop); Carbon toolchain modernization talks (orthogonal to AI/agent control planes). Industry substrate critiques (e.g. Modular on MLIR fragmentation) stay in Trend C.

---

## 1b. Traditional AI compilation vs following trends

This section compares the **classic AI/DL compiler stack** (graph capture → fixed/autotuned lowering → kernels → runtime) with the **2024–2026 agentic / LLM-hybrid trends** summarized above. The point is not “old bad / new good,” but where each side wins and what the hybrid should keep.

### What “traditional” means here

| Layer | Traditional approach | Representative systems |
|---|---|---|
| Front-end | Trace/export graphs; op fusion by rules | TorchDynamo/Inductor, TF/JAX → HLO/StableHLO |
| Mid-end | Dialect lowers + handwritten passes | MLIR, XLA, TVM Relay/TIR |
| Schedule / autotune | Cost models + evolutionary / template search | AutoTVM, Ansor, MetaSchedule |
| Heuristics | Expert C++ thresholds (inline, regalloc, …) | LLVM `-O3`, MLGO neural advisors (still in-tree) |
| Kernels | Libraries + expert CUDA/Triton/CUTLASS | cuDNN, FlashAttention, hand Triton |
| Correctness | Compiler semantics + unit/golden tests | Deterministic passes; limited formal at scale |
| Serving | Separate runtime stack | vLLM, TensorRT-LLM, CUDA Graphs |

### Dimension-by-dimension comparison

| Dimension | Traditional AI compilation — pros | Traditional — cons | Following trends (LLM/agent hybrid) — pros | Trends — cons / new risks |
|---|---|---|---|---|
| **Correctness model** | Decades of pass engineering; miscompile rates low for common paths | Misses intent-level opts; hard to prove GPU/FP whole-program | Gates (Alive2, tests, templates) can keep compiler as source of truth | Untamed LLM rewrite is unsafe; oracles still local |
| **Search / adaptation** | Autotune finds strong schedules given enough trials | Sample-inefficient; weak transfer across shapes/HW/versions | Language priors + MCTS/agents cut samples; multi-level creativity | Token cost, nondeterminism, hard-to-replay traces |
| **Heuristic maintenance** | Human-readable, reviewable C++ | High expert cost; stale vs new HW/models | Magellan-style synthesis of deployable heuristics; MLGO learned advisors | Ownership, regression, supply-chain of agent code |
| **Kernel specialization** | Peak performance when experts invest | Does not scale to every new op/HW (esp. non-NVIDIA) | GEAK/KernelLLM/AgentCompile automate explore–measure loops | Correct ≠ fast (KernelBench-X); fusion still hard |
| **Production readiness** | Default paths in PyTorch/XLA/LLVM/CUDA | Fragmented stacks; peak often needs vendor libs | Vendor moves (CompileIQ, GEAK, Magellan prod inlining) show traction | Few agent loops are *default* compile flags yet |
| **Portability** | StableHLO / MLIR aim at framework↔compiler portability | Dialects and Triton/Tile/PTX still siloed | Agents can retarget kernels across AMD/NVIDIA in principle | No standard agent IR/tool contract across stacks |
| **Compile object** | Graph → binary/kernels | Does not cover prompts, agents, FMware knobs | Compiler.next / generative compilation broaden the object | Early vision; quality gates immature |
| **Human role** | Experts write passes/kernels; long review cycles | Bottleneck on rare expertise | Agents draft; humans review/orchestrate | Review capacity & security become the bottleneck |
| **Cost model** | Compile-time CPU + autotune GPU hours (known) | Autotune walls for huge spaces | Can reduce search trials | Adds LLM $ / latency; budgets poorly standardized |
| **Explainability** | Pass lists and schedules are inspectable | Why a heuristic fired can still be opaque | Natural-language rationales + traces possible | Rationales may not match true causal opts |

### Pros of staying traditional (when to *not* force agents)

1. **Stable, regressable defaults** — `-O3`, Inductor, XLA pipelines are battle-tested across millions of builds.
2. **Deterministic CI** — same IR in → same binary out (modulo known nondeterminism); agent loops break that unless carefully cached.
3. **Clear ownership** — a pass has a maintainer; an agent trajectory often does not.
4. **Peak library kernels** — FlashAttention/CUTLASS still dominate many hot paths without an LLM in the loop.
5. **Formal/tooling maturity** — Alive2, LLVM lit, FileCheck, and vendor validators assume classical artifacts.

### Pros of following trends (when agents earn their keep)

1. **Per-program / per-model specialization** beyond what global heuristics allow (pass order, hints, CompileIQ knobs).
2. **Faster exploration** of kernel and schedule spaces with language priors (Reasoning Compiler, GEAK).
3. **Closing the intent gap** — algorithm-level rewrites compilers cannot invent (ACCLAIM), when tests gate them.
4. **Compiler engineering leverage** — synthesize heuristics/passes (Magellan) or review opt PRs with domain tools (LLVM Discourse agent review).
5. **New surfaces** — mid-decode diagnostics (Generative Compilation); FMware multi-objective compile (Compiler.next).

### Synthesis: keep the substrate, change the control plane

```text
Traditional strengths to preserve
  deterministic lowering · library kernels · CI regressability · formal local checks

Trend strengths to adopt
  advisory search · multi-agent orchestration · heuristic synthesis · profile/verifier feedback

Anti-pattern
  replace opt/Inductor with unconstrained LLM codegen and hope tests catch it
```

**Recommendation:** treat traditional AI compilers as the **data plane** and agent/LLM methods as an optional **control plane** with admit/fallback. Measure success by (a) production default adoption, (b) replayable traces, (c) oracle strength—not by microbench speedups alone.

---

## 2. How do agents help AI compilation? (Q2)

### 2.1 Mechanisms (why it works)

1. **Sample efficiency** — Language priors propose plausible schedules/passes instead of blind evolutionary samples (Reasoning Compiler vs MetaSchedule-style search).
2. **Correctness envelope** — Constraining interventions to hints, templates, verified IR, or pass lists avoids unconstrained codegen failures.
3. **Multi-level creativity** — Compilers miss purpose-level rewrites; LLMs can restructure algorithms when tests gate acceptance (ACCLAIM).
4. **Compiler engineering itself** — Agents write maintainable heuristics/passes (Magellan, mlirAgent) rather than shipping opaque neural nets inside `opt`.
5. **Feedback densification** — Profilers, compiler diagnostics, Alive2, and Fast Feedback turn sparse rewards into iterative refine loops.

### 2.2 Closed loop (canonical)

See [`TAXONOMY.md`](TAXONOMY.md). Variants:

| Variant | Twist |
|---|---|
| Generative Compilation | Feedback mid-decode via sealors |
| Reasoning Compiler | LLM proposals expand MCTS nodes |
| Magellan | Evolutionary mutate of C++ heuristics + Vizier autotune |
| ACCLAIM | Multi-level budgeted agents + test agent |
| GEAK | Reflexion-style generate–eval–reflect–optimize on GPU |
| CompileIQ | Evolutionary search over **compiler internal knobs** (not source) |

### 2.3 What agents should *not* own

- Unchecked IR/assembly emission as production code without admit gates.
- Silent replacement of numerical kernels without golden or statistical checks.
- Orchestration without reliable tool-calling (ACCLAIM: open models fail on malformed tool calls before code quality).

---

## 3. Can agents reshape compilation processes? (Q3)

**Short answer:** Yes for the **control plane**; no (so far) for wholesale replacement of deterministic lowering.

These reshape claims are **evidence for** [§5 Future prediction](#5-future-prediction-what-next-gen-looks-like). The hard limits below—and the gaps in [§4](#4-whats-missing--under-covered-q4)—are the **blockers** to that predicted future. Tiered repo/product evidence: [`REPOS.md`](REPOS.md), [`PRODUCTS.md`](PRODUCTS.md).

### 3.1 Old → new process map

| Legacy process | Agent-reshaped process | Evidence |
|---|---|---|
| Fixed `-O2/-O3/-Oz` pipelines | Per-program pass search with LLM/RL policies | Compiler-R1, AwareCompiler, AutoPass, LLM Compiler |
| Hand-tuned heuristics in C++ | Agents synthesize/evolve heuristic code | Magellan (LLVM inlining/regalloc; XLA) |
| Black-box evolutionary autotune | Context-aware LLM proposals + structured search | Reasoning Compiler (TVM + MCTS) |
| Compile → fail → human fix | Compiler feedback during partial generation | Generative Compilation |
| Experts write Triton/CUDA | Agent generate–eval–reflect–optimize | GEAK, KernelBench agents, KernelLLM |
| Single IR level optimization | Multi-agent choose abstraction level | ACCLAIM |
| Compile source → binary | Compile intent / FMware knobs | Compiler.next (vision) |
| Generic NVCC heuristics | Per-kernel evolutionary compiler controls | NVIDIA CompileIQ |
| Humans write the compiler | Agent teams implement a C compiler | Anthropic CCC (engineering experiment) |

### 3.2 Hard limits

1. **Direct IR transformation** by LLMs can underperform identity; search/heuristic synthesis wins more reliably (mlirAgent).
2. **KernelBench-X:** iterative refine can raise pass rates while average speedup falls; ~46% of correct kernels still slower than eager in their setting.
3. **Tool-calling quality** of open models can break multi-agent compilers before code skill does (ACCLAIM).
4. **Formal verifiers** cover local equivalences; they do not yet bless end-to-end GPU serving stacks.
5. **Cost & reproducibility** of agent compile loops (tokens, nondeterminism, hardware noise) remain open (Compiler.next call-to-action).

### 3.3 Practical architecture recommendation

Design agent-shaped compilers as:

```text
bounded candidate spaces
+ structured IR / region summaries
+ advisory LLM
+ deterministic materialize
+ empirical and/or formal admit
+ fallback
```

Split **offline** compiler-engineering agents (Magellan-style heuristic synthesis) from **online** compile-time agents (HintPilot / AgentCompile / CompileIQ).

---

## 4. What’s missing / under-covered? (Q4)

The gaps below are not a separate “wishlist”—they are the **blockers to the [§5](#5-future-prediction-what-next-gen-looks-like) predicted future** (agent-addressable data plane, three agent jobs, first-class artifacts, classical defaults until CI proves agents). Coverage is uneven. Each gap spells out **what exists**, **what is missing**, **why it blocks that future**, and **what “done” could look like**. Digests: [`../publications/`](../publications/). Evidence maps (Tier A/B/C): [`REPOS.md`](REPOS.md), [`PRODUCTS.md`](PRODUCTS.md).

### Gap map (priority snapshot)

| # | Gap | Severity now | Who feels it first |
|---|---|---|---|
| 4.1 | End-to-end production evidence | High | Framework / compiler vendors |
| 4.2 | Correctness at scale | High | Anyone shipping kernels or IR rewrites |
| 4.3 | Cost & reproducibility of agent loops | High | CI / release engineering |
| 4.4 | Cross-stack interoperability | High | Multi-backend platforms |
| 4.5 | Hardware-native agent interfaces | Medium–High | Agent + compiler tool builders |
| 4.6 | FMware / agent-app compilation | Medium | LLM-app / SE 3.0 platforms |
| 4.7 | Training data for compilers | Medium–High | Foundation-model builders |
| 4.8 | Human-in-the-loop compiler engineering | Medium | LLVM/XLA maintainer orgs |
| 4.9 | Security / supply chain | Medium (rising) | Prod infra & open-source |
| 4.10 | Unified benchmarks | High | Research + industry comparison |

---

### 4.1 End-to-end production evidence

**What exists.** Many papers report kernel-, pass-, or microbench-level wins: Compiler-R1 on IR instruction count; HintPilot on PolyBench; Reasoning Compiler on selected serving kernels; AgentCompile / GEAK on model or kernel suites; Magellan talks claim production inlining use; NVIDIA CompileIQ quotes ≤15% on already-hot GEMM/attention.

**What is missing.** Few agent or LLM methods are the **default** path in PyTorch Inductor, OpenXLA/XLA, or LLVM trunk for arbitrary user programs. Wins are often:

- opt-in flags or research forks;
- evaluated on curated kernels, not full training/serving stacks;
- hard to attribute (custom GEMV / CUDA Graphs / KV cache vs “LLM guidance”).

**Why it blocks progress.** Without default-path evidence, orgs cannot justify always-on agent compile cost or review burden. Survey claims risk overstating readiness.

**Done looks like.** Public A/B on major frameworks (e.g., Inductor default vs agent-specialized decode path) with regression suites, rollout flags, and multi-month stability—similar to how MLGO reported persistent QPS gains after deployment.

---

### 4.2 Correctness at scale

**What exists.**

| Oracle | Strength | Weakness |
|---|---|---|
| Compiler applies passes (LLM Compiler, Compiler-R1) | Semantics of passes inherited | Cannot invent new transforms safely |
| Unit / LLM-generated tests (ACCLAIM) | Catches many functional bugs | Under-approximates; flaky tests |
| Numerical checks vs reference (AgentCompile) | Good for kernels with goldens | Tolerance games; training vs infer numerics |
| Alive2 / formal (LLM-VeriOpt) | Strong local IR equivalence | Peephole/local; not GPU concurrency |
| Round-trip disassembly checks | Partial trust signal | Exact-match rates still modest |

**What is missing.** Oracles for:

- **Whole-program** semantic equivalence after multi-level agent rewrites;
- **Floating-point** contracts (reassoc, TF32/BF16, reduction order);
- **GPU races**, async copies, warp divergence, and memory model bugs;
- **Serving-level** behavioral equivalence (sampling, KV layout, speculative decode).

**Why it blocks progress.** KernelBench-X already shows correct kernels can be slow; the dual risk is “fast but subtly wrong.” Formal methods that stop at peephole leave the highest-value agent actions (fusion, schedule, algorithm rewrite) under-governed.

**Done looks like.** Layered admit policy: local formal where possible → differential testing on shape grids → statistical serving checks → staged rollout. Shared open oracles for Triton/CUDA Tile IR, not only LLVM IR.

---

### 4.3 Cost & reproducibility of agent compile loops

**What exists.** Fast Feedback (~10× iterate vs full IR in-loop); CompileIQ produces portable Advanced Controls Files; some papers fix seeds or report sample budgets; Compiler.next explicitly calls for reproducible intent compilation and shared traces.

**What is missing.**

- Standardized **cost models** (tokens + compile minutes + GPU-hours per % gain);
- **Deterministic replay** of agent decisions across model versions;
- **Cacheable compilation traces** keyed by (IR hash, HW, compiler version, agent policy);
- CI policies for flaky speedups (hardware noise, DVFS, contention).

**Why it blocks progress.** A compile that costs $N of LLM calls and cannot be reproduced is not a compiler feature—it is an experiment. Release engineering will reject it.

**Done looks like.** Trace format + content-addressed cache (pass list / hints / ACF / kernel artifact) checked into build systems; budget SLOs; golden replay tests when upgrading the agent model.

---

### 4.4 Cross-stack interoperability

**What exists.** StableHLO for framework↔compiler graphs; MLIR as a shared *idea*; Triton as a de-facto GPU DSL; vendor bridges (experimental Triton→Tile IR).

**What is missing.** A portable contract for **agent-visible** state:

| Concept | Needed across stacks | Today |
|---|---|---|
| Region / fusion candidate | Common schema | Ad hoc per paper |
| Constraint set (shapes, aliasing, HW) | Shared vocabulary | Embedded in prompts |
| Action space (pass, hint, schedule, template) | Enumerated & versioned | Closed per system |
| Reward / admit result | Structured feedback | Free-text logs |
| Artifact identity | Hashable outputs | Often lost |

Dialects, Triton, CUDA Tile IR, PTX, and LLVM IR remain siloed; an agent tuned on one stack rarely transfers.

**Why it blocks progress.** Every new agent re-implements glue. Multi-backend companies cannot share learnings.

**Done looks like.** An “agent compile interface” RFC (perhaps on StableHLO or MLIR) defining summaries, actions, and admit records—similar in spirit to how PJRT standardized runtime plugins.

---

### 4.5 Hardware-native agent interfaces

**What exists.** mlirAgent: structural IR fingerprinting, knowledge graphs, MCP tool suites; Compiler-R1 tool calls (`instrcount`, etc.); GEAK hardware feedback loops; CompileIQ search spaces over NVCC/PTXAS internals ([NVIDIA/CompileIQ](https://github.com/NVIDIA/CompileIQ)); **SCM-side tool APIs** in Archer (`verify`, `difftest`, `trans`, workflow) bound to a local `llvm-project` checkout; Gerrit AI Agent Provider APIs for in-UI chat (generic LLMs unless extended).

**What is missing.** **Standards**, not demos:

- Common fingerprint / provenance for pass effects;
- Vendor-neutral MCP (or equivalent) tool schemas for “compile / verify / bench”;
- Safe sandboxes for executing agent-proposed kernels at scale;
- First-class exposure of HW counters to agents without scraping profiler text.

**Why it blocks progress.** Agents without structured interfaces fall back to brittle prompt-and-pray over `opt` stdout.

**Done looks like.** LLVM/MLIR/Triton tool APIs that agents can call with typed I/O; fingerprinting as a supported analysis; conformance tests for tool servers.

---

### 4.6 FMware / agent-app compilation

**What exists.** Compiler.next vision: compile prompts, agent topologies, and free parameters under multi-objective quality gates; generative compilation couples compilers into coding agents; industry agent harnesses (Claude C compiler) stress test construction. Concrete substrate is arriving: [FlowCompile](../publications/flowcompile.md) (compile-time optimize structured LLM workflows), [Auto](../publications/auto-agi-compiler.md) (freeze witnessed-deterministic agent spans into WASM “cognition binaries”), [AgentFlow](../publications/agentflow.md) (Agent Dependency Graphs for static analysis), and [heterogeneous agent serving](../publications/agentic-ai-hetero-systems.md) (place dynamic agent graphs across CPU/accelerator tiers).

**What is missing.** Mature analogues of DL compilers for FMware:

- Stable IRs for prompt/tool graphs (ADG is a candidate, not yet a shared standard);
- Compilation that **fails closed** when quality thresholds miss;
- Interoperability between “prompt/workflow compilers” and classical model compilers;
- Shared traces for community learning (Compiler.next call-to-action #10).

**Why it blocks progress.** LLM applications (and agentic *compiler* control planes) still tune by hand and folklore while DL graphs enjoy decades of compiler investment. Without workflow-compile + freeze + ADG checks, multi-agent compiler products stay demo-grade.

**Done looks like.** Reproducible FMware / agent-workflow compile pipelines with gold labels, cost/latency/quality Pareto fronts, static ADG admit, and CI that blocks regressions—parallel to how model zoos ship compiled artifacts today.

---

### 4.7 Training data for compilers

**What exists.** Meta LLM Compiler: 546B tokens of LLVM-IR/assembly + compiler-emulation instruction data; KernelLLM: ~25k torch↔Triton pairs (KernelBook); Compiler-R1 reasoning dataset (~19.6k); CompilerGym workloads; MLGO training corpora (often internal).

**What is missing.** Large, open, **versioned** corpora for:

- MLIR dialects (linalg, scf, affine, vendor dialects);
- Triton / Tile IR / PTX paired with schedules and performance labels;
- StableHLO graphs with lowering outcomes;
- Negative data (failed compiles, miscompiles, slow kernels) for critics/verifiers.

**Why it blocks progress.** Without data, Selector/Generator models stay LLVM-centric or overfit KernelBench. Follow-ons to Meta LLM Compiler for modern AI IRs remain sparse.

**Done looks like.** Public “ImageNet for compilers” 2.0: multi-IR, multi-HW, with licenses cleared for commercial research—building on CompilerGym’s original ambition.

---

### 4.8 Human-in-the-loop compiler engineering

**What exists.** Magellan produces reviewable C++ heuristics; **Archer** ([paper](https://arxiv.org/html/2607.01808), [GitHub](https://github.com/cuhk-s3/Archer)) agentically reviews **LLVM GitHub PRs** with Alive2/LLUBI evidence gates; LLVM Discourse threads report similar agent PR review experience; **Gerrit** hosts general AI review plugins ([ai-code-review](https://gerrit.googlesource.com/plugins/ai-code-review/), [ReviewAI](https://github.com/amarula/reviewai-gerrit-plugin), [GerritForge provider](https://github.com/GerritForge/ai-review-agent-provider)) used in large-org change workflows; Anthropic CCC emphasizes harnesses; Lattner commentary stresses tests as the real product. See [`REPOS.md`](REPOS.md) for the SCM map.

**What is missing.** Process answers, not only models:

- Who **owns** agent-written passes six months later?
- How do code reviews differ when the author is an agent?
- When do humans override agent heuristics after HW refresh?
- How to mix agent draft + expert finalize without review collapse?

**Why it blocks progress.** Productivity gains reverse into maintenance debt if agent artifacts are unowned. Generic SWE agents underperform on opt review without domain tools—so HITL design is research-worthy.

**Done looks like.** Documented workflows: agent proposes → automated oracle gate → human review checklist → ownership assignment → regression corpus update. Metrics for review time vs bugs escaped.

---

### 4.9 Security / supply chain

**What exists.** Sparse public discussion: Anthropic author notes unease about unverified deployed code; classical compiler supply-chain concerns (trusting opt, binary provenance); almost no dedicated papers in this survey’s catalog on adversarial agent kernels.

**What is missing.**

- Threat models for **malicious or buggy agent kernels** (silent wrong answers, side channels, DoS via pathological schedules);
- Provenance signing for agent-generated heuristics/kernels;
- Sandbox policies for compile-time execution of untrusted proposals;
- SBOM-like records: which model, prompt, tools, and admit gates produced an artifact.

**Why it blocks progress.** As Magellan/GEAK/CompileIQ-style artifacts enter production binaries, they become part of the trusted computing base.

**Done looks like.** Security reviews required for agent-admitted artifacts; reproducible builds; allowlists for online agents; red-team suites for kernel agents.

---

### 4.10 Unified benchmarks

**What exists (fragmented).**

| Suite | Measures | Blind spot |
|---|---|---|
| CompilerGym / Autophase-style | LLVM IR size / pass RL | Not GPU serving |
| PolyBench / HumanEval-CPP (+ HintPilot) | CPU runtime with hints | Not IR agents or kernels |
| KernelBench / KernelBench-X / TritonBench | GPU kernel correct+fast | Not full serving graphs |
| Paper-specific serving kernels | Attention/MoE/MLP slices | Not comparable across papers |
| Vendor internal suites | Production truth | Closed |

**What is missing.** A **shared ladder**:

1. CPU IR opt (size + runtime),
2. Single kernels (CUDA/Triton/Tile),
3. Fused regions,
4. Full LLM serving graphs (prefill/decode, batch, long context),
5. Multi-objective (latency, throughput, memory, quality),

with fixed hardware profiles, reference docks, and leaderboards that separate **correctness**, **performance**, and **cost-to-compile**.

**Why it blocks progress.** Cross-paper “speedup” comparisons are currently nearly meaningless; the field cannot tell if Selector/Generator methods are improving the same problem.

**Done looks like.** A community benchmark consortium (LLVM ♥ ML + MLSys + vendor tracks) publishing versioned tasks and forbidding cherry-picked single-kernel headlines without the full ladder.

---

### Cross-cutting research agenda (from the gaps)

| Theme | Near-term work | Depends on gaps |
|---|---|---|
| Admit & fallback standards | Spec for hybrid pipelines | 4.1, 4.2, 4.3 |
| Agent compile IR / tools | RFC + MCP schemas | 4.4, 4.5 |
| Open multi-IR corpora | MLIR/Triton/Tile datasets | 4.7, 4.10 |
| Serving-level oracles | Diff tests + statistical checks | 4.2, 4.10 |
| Provenance & HITL | Ownership + signing workflows | 4.8, 4.9 |
| FMware compile MVP | Quality-gated prompt/agent search | 4.6, 4.3 |

### Follow-on questions for an org adopting this

1. Online compile-time agents (HintPilot/AgentCompile/CompileIQ) vs offline heuristic synthesis (Magellan)—which matches your release model?
2. What is the correctness oracle—Alive2, golden kernels, or serving A/B—and who owns false negatives?
3. Which IR is the agent contract—LLVM IR, MLIR dialect, Triton, StableHLO, CUDA Tile IR?
4. How do you cache and regress agent compile traces across compiler *and* model upgrades?
5. What is the max $/build or tokens/build you will spend for a median X% win?
6. Who is the named maintainer of each agent-admitted artifact after merge?

---

## 5. Future prediction (what next-gen looks like)

Falsifiable sketch for **~2027–2028**, conditioned on conflicts in [`CONFLICTS.md`](CONFLICTS.md).

### 5.1 Architecture

Hybrid stack: agents orchestrate; classical compilers execute; silicon feeds the next dialect/ISA RFC. The control plane is itself becoming a compile target (workflow IR → analyze → freeze → place).

```text
                      HUMAN / PRODUCT INTENT
                 (NL at the edge · policy · budget)
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AGENT CONTROL PLANE         lab → CI-gated → hot-path specialize   │
│                                                                     │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│   │ (a) ONLINE│  │ (b) OFFLINE│ │ (c) ENG.  │  │ (d) BRING │        │
│   │ specialize│  │  evolve   │  │  review   │  │  -UP      │        │
│   │ propose · │  │ heuristics│  │ oracle PR │  │ coverage→ │        │
│   │ measure · │  │ / passes  │  │ / src edit│  │ perf on   │        │
│   │ admit     │  │ →C++/MLGO │  │           │  │ sim + Si  │        │
│   └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘        │
│         └──────────────┴───────┬──────┴──────────────┘              │
│                                │                                    │
│   ┌────────────────────────────▼──────────────────────────────┐     │
│   │ SUBSTRATE — sub-agent architecture                         │    │
│   │ workflow compile │ ADG analysis │ freeze/amortize │ place  │    │
│   │ (FlowCompile)    │ (AgentFlow)  │ (Auto)          │ hetero │    │
│   └────────────────────────────────────────────────────────────┘    │
└────────────────────────────────┬────────────────────────────────────┘
                                │
        typed tools · admit records · oracles · FSM / plan bounds
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CLASSICAL DATA PLANE                          default path stays   │
│                                                                     │
│   Framework / graph                                                 │
│          │                                                          │
│          ▼                                                          │
│   Inductor · XLA · MLIR · Triton · Helion · Tile · device libs      │
│          │                                                          │
│   legality · lowering · cost models                                 │
│   golden / Alive2 / OpInfo · admit / fallback                       │
└────────┬─────────────────────┬─────────────────────┬────────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
  GPU / NPU / ASIC      VCS artifacts         Serving runtime
  (sim → silicon)       ACF · kernels ·       specialize hot paths;
                        heuristics ·          freeze for replay
                        memory · traces
        │
        └──── coverage / perf / illegal-op traces ────┐
                                                      ▼
                         ┌────────────────────────────────────────┐
                         │  HW–SW CODESIGN FEEDBACK               │
                         │  agent failures → ISA / dialect /      │
                         │  memory-system RFCs                    │
                         │  (humans + EDA own tape-out — C10)     │
                         └────────────────────────────────────────┘
```

1. **Compiler becomes agent-addressable**, not agent-replaced — structured summaries, fingerprints, tool APIs, admit/fallback (mlirAgent: free IR rewrite loses to identity).
2. **Four agent jobs stick:** (a) online specialization, (b) offline heuristic/pass synthesis, (c) compiler engineering & review, (d) accelerator bring-up / codesign feedback.
3. **New first-class artifacts:** ACFs, evolved C++ heuristics, verified kernels, optimization memory, bring-up corpora, replayable traces — **and** frozen agent workflows / cognition binaries when the control plane itself is compiled.
4. **Defaults stay classical** until agents win on *distributions* in CI; hot kernels, size-critical apps, and *new ASICs* adopt first.
5. **Will not happen soon:** unconstrained LLM replaces `opt`/Inductor without oracles (**C6**); autonomous chip tape-out via compiler agents (**C10**).

**Sub-agent / workflow-compile substrate (must consider).** The control plane is itself becoming a compile target:

| Line | Claim for agentic compilers | Digest |
|---|---|---|
| **AGI compiler / freeze** | Compile agent traces → deployable artifacts; amortize inference | [Auto](../publications/auto-agi-compiler.md) ★ → **P23** |
| **Workflow compile** | Spec/graph → typed workflow configs across accuracy–latency | [FlowCompile](../publications/flowcompile.md) ★ → **P3/P18** |
| **Agent static analysis** | ADG + typed deps for audit, injection, unsafe tools | [AgentFlow](../publications/agentflow.md) → **P1/P22** |
| **Heterogeneous serving** | Place agent stages across NPU/GPU/CPU under SLOs | [Heterogeneous agentic AI](../publications/agentic-ai-hetero-systems.md) → **P10/P22** |

Without these, “agentic compiler” collapses to either unconstrained LLM loops or a classical compiler with a chatbot glued on.

### 5.2 How agents change the future (process)

| Legacy | Agent-changed future | Confidence |
|---|---|---|
| Experts hand-write heuristics | Offline agents propose reviewable C++/MLGO features | High (Magellan/MLGO both shipping paths — conflict C1) |
| Autotune black boxes | Versioned search artifacts (ACF, traces) in VCS | Medium-high (CompileIQ design) |
| Scarce kernel experts | Multi-agent kernel loops with profiler oracles | Medium (vendor blogs strong; KernelBench-X ceilings — C2) |
| Human-only opt PR review | Compiler-oracle agents on PRs/Changes | Medium (Archer; generic forge AI is not enough — C7) |
| Single DSL (CUDA) expertise | Multi-DSL agent skills (Triton/Tile/CuTe/HIP) | Medium (TRT-LLM agents PR; GEAK v3 — C4) |

### 5.3 What would falsify this prediction

- A major AI stack ships **default** lowering with no classical admit/fallback and sustained correctness.
- Magellan-class synthesis **and** MLGO neural advisors both disappear from production (neither path).
- Kernel agents plateau forever below eager on fusion-heavy suites with no industrial workaround (libraries-only forever).

### 5.4 Near-term signals conditioning the sketch

From Magellan LLVM Dev Meeting slides ([digest](../publications/magellan-llvm-slides.md)), ACCLAIM ([arXiv:2604.04238](https://arxiv.org/abs/2604.04238), [digest](../publications/acclaim.md)), and HW-codesign agents:

| Signal | Implication for §5 | Watch |
|---|---|---|
| Magellan OSS via **OpenEvolve + OSS models** | Offline job (b) becomes reproducible outside Google | Public recipes / llvm patches (**C1**) |
| Magellan **XLA** auto-sharding / graph-rewrite green-field | Offline agents invent heuristics where human expertise is thin | End-to-end XLA pipeline eval (slides: WIP) |
| ACCLAIM multi-level compiler↔LLM cooperation ([code](https://github.com/amazon-science/acclaim)) | Online job (a) is orchestration across levels + test admit, not IR replacement | Tool-calling quality; GPU/serving ports |
| **TritorX** coverage on MTIA + future-device sim | Job **(d) bring-up/codesign** enters the agentic compiler | Second-vendor repro (**C9**) |
| **KernelEvolve** hetero NVIDIA/AMD/MTIA perf agents | Production multi-HW control plane | Public traces vs KernelBench-X (**C2**) |
| Ascend **compiler-grounded** Triton diagnosis | Non-CUDA NPUs need IR/pass escalation, not CUDA-pretrained guess | Hierarchy ablations |
| Helion + CompileIQ ACF path | DSL substrate agents specialize | **C4** vs Tile/CuTe |
| **Compiler 2.0** Ken Kennedy plenary + **MOCHA** (LLM rewrites ⊕ eqsat ⊕ Rocq; retarget-via-rewrites) | Venue+funding align on verified ML construction / hetero retarget — not free LLM-`opt` | OSS releases & Year 1–3 evals ([digest](../publications/compiler-2.0-cgo2026.md), [MOCHA](../publications/compiler-2.0-mocha-aarno.md)) |

### 5.5 Roadmap — Horizon A (2027–28) and Horizon B (~2029–31)

Falsifiable sketch conditioned on C1–C10. Architecture target is [§5.1](#51-architecture); commercialization packaging is [§5.7](#57-from-prediction-to-commercial-practice--critical-problems); layer map is [`STACK.md`](STACK.md).

**Executive 5-year bet (still agentic-compiler-centric):** classical data planes remain; agentic control planes become how orgs survive O(ops × devices × generations). HW codesign appears as **sim/silicon feedback into IR/ISA/dialects**, not autonomous tape-out (**C10**). New artifacts (ACFs, heuristics, memories, bring-up corpora) sit beside binaries in VCS — and, later, frozen agent workflows when the control plane itself is compiled.

#### 5.5.1 Horizon A — 2027–2028 (near)

##### What ships

| Capability | Predicted state | Leading evidence | Conflicts |
|---|---|---|---|
| **Agent-addressable compilers** | Tool APIs, structured IR summaries, admit/fallback become normal in LLVM/Inductor/vendor toolchains | ACCLAIM, HintPilot, AgentCompile, mlirAgent (negative free-rewrite) | C3, C6 |
| **Online specialization (job a)** | Hot kernels/paths use agent or evolutionary search (ACF, hints, Triton/Helion refine) in CI for *some* products — not yet silent default for all builds | CompileIQ, GEAK, AutoKernel, Kernel Forge | C2, C5 |
| **Offline heuristic synthesis (job b)** | Magellan-class C++ heuristic evolution *and* MLGO neural advisors both still live (parallel bets) | Magellan, EmitC-MLGO RFC | **C1** |
| **Engineering agents (job c)** | Compiler-oracle PR review (Alive2/`opt`) in serious LLVM/AI-compiler orgs; generic forge AI stays UX | Archer | **C7** |
| **Bring-up / codesign agents (job d)** | Coverage-first ATen/Triton backend generation on sim + silicon becomes standard for *new* ASICs | TritorX, KernelEvolve, Ascend hierarchical diagnosis | **C9** |
| **Verified ML construction (Compiler 2.0 / MOCHA)** | Early open releases of LLM→eqsat→formal-admit rewrite / retarget tooling; not yet default production `opt` | Ken Kennedy plenary 2026; Aarno/MIT/UIUC MOCHA | C3, C6 |
| **DSL surface** | Triton-family (Triton/Helion) remains primary agent training surface; Tile/CuTe/HIP/FlyDSL force multi-DSL skills | Helion, CompileIQ Helion path, TRT-LLM agents, KForge | **C4** |

##### What does *not* ship by 2028

- Unconstrained LLM replaces `opt`/Inductor end-to-end without classical admit (**C6**).
- Single “one agent IR” for all vendors (**C4** unresolved).
- Kernel agents uniformly beat eager/libraries on fusion-heavy public ladders (**C2**).
- Agents design *silicon microarchitecture* autonomously (codesign is **feedback to humans/EDA**, not tape-out autopilot) — see Horizon B.

##### Near-term milestones (watch)

1. Public Magellan/OpenEvolve llvm patches **or** EmitC-MLGO default (**C1**).
2. CompileIQ/GEAK publish p50/p90 + pinned traces (**C2**).
3. TritorX-like bring-up reproduced outside Meta (second ASIC vendor) (**C9**).
4. PyTorch/LLVM release notes list agent/ACF jobs as supported workflows (**C5**).
5. MOCHA / Compiler 2.0 publishes OSS rewrite+verify evals or retarget demos (program through ~2028).

#### 5.5.2 Horizon B — ~2029–2031 (next ~5 years from 2026)

Still centered on the **agentic compiler** as the product; HW codesign is how that product eats the O(ops × devices × gens) matrix.

##### Architecture evolution

How the hybrid stack thickens from ad-hoc agent loops to a **compiled control plane** over a classical data plane. Target stack detail: [§5.1](#51-architecture).

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

##### Predicted shifts

| Theme | 5-year outcome | Confidence |
|---|---|---|
| **Default compile path** | Classical lowering remains default; agentic specialize is **opt-in then CI-gated default for hot paths** | Medium-high |
| **Artifact store** | VCS grows first-class **ACFs, evolved heuristics, verified kernels, optimization memory, bring-up corpora** | High |
| **Heterogeneous serving** | Agentic multi-backend kernel/forge loops are how non-NVIDIA fleets stay viable (MTIA/AMD/Intel/NPU) | Medium-high (KernelEvolve, KForge, TritorX) |
| **HW codesign loop** | Pre-silicon: agents + sim generate coverage and compiler stress; post-silicon: agents map ISA/IR pain → RFC for next chip / dialect. Humans + EDA still own tape-out | Medium |
| **Verification** | Local formal (Alive2-class) + statistical serving oracles + OpInfo-scale suites compose; whole-program GPU/NPU formal still incomplete | Medium |
| **Human role** | Experts own oracles, ownership, security, ISA contracts; agents draft kernels/heuristics/backends | High |
| **Will still not happen** | Fully autonomous chip + compiler co-generation without human architectural intent; end-to-end LLM-as-`opt` | High |

##### Codesign-specific roadmap (still agentic-compiler-centric)

| Phase | Agentic compiler does | Hardware team gets |
|---|---|---|
| Pre-silicon | TritorX-style coverage on QEMU/sim; KernelEvolve-style search under draft ISA docs | Early “can we run NanoGPT/DLRM ops?” signal; IR/dialect bugs |
| Bring-up | Coverage agents → perf agents ladder | Weeks→hours for ATen/Triton backend skeleton |
| Steady-state | Online specialize + memory (KernelBlaster) across gens | Portability when L2/TMA/SRAM rules change |
| Next tape-out | Aggregated failure modes from agent traces (illegal ops, alignment, missing atomics) | Prioritized ISA / memory-system / compiler-pass requests |

**Non-goal:** surveying EDA/RTL LLM tools unless they close the loop into **compiler IR, kernels, or admit oracles**.

#### 5.5.3 Success metrics for this roadmap

1. Can a new ASIC expose an agent-addressable compile/test API and reach >80% ATen coverage via agents within a release cycle? (TritorX bar)
2. Do agentic specialize jobs show **distributional** wins in CI (p50), not only best kernels? (C2)
3. Are Magellan-class and MLGO-class paths both still productive or has one settled? (C1)
4. Does the stack treat traces/ACFs/heuristics as reviewable artifacts with owners? (§4.8–4.9)
5. Can you ship without NL-only contracts — typed tools + replayable admit traces + memory that survives model swap? ([§5.7](#57-from-prediction-to-commercial-practice--critical-problems))

Update when CONFLICTS settle or new Tier A codesign evidence lands.

### 5.6 Stack reshape pointer

Layer-by-layer SW + codesign map: [`STACK.md`](STACK.md). Claim IDs: [`CLAIMS.md`](CLAIMS.md).

### 5.7 From prediction to commercial practice — critical problems

§5 predicts a **hybrid** agentic compiler. Shipping that as a product (CompileIQ-class, GEAK-class, Magellan-in-CI, TritorX-style bring-up) forces engineering choices that papers usually skip. Below: **critical problems → option sets with pros/cons → survey-leaning defaults**. Treat “might be true” options as hypotheses to settle in production, not dogma.

**Problem map (architecture → ops → business).** P1–P8 = control/data-plane productization; P9–P22 = eval, money, tenancy, legal, versioning, cold start, HITL capacity, flywheel, latency, DR, A/B, compliance, orchestration predictability, attribution—drawn from §4 gaps, CONFLICTS, Tier A digests (KernelEvolve, TritorX, CompileIQ, ACCLAIM, Magellan, GEAK, Archer, CCC), and adjacent agent-production literature (deterministic boundaries, admit-record provenance).

| ID | Problem | Lean (one line) |
|---|---|---|
| P1 | Agent↔compiler contract | Typed tools + structured admit traces; NL only at human edge |
| P2 | Context / memory loss | Scratchpad ≪ dense skills ≪ **VCS** as product truth |
| P3 | Sub-agents vs monolith | Specialists + orchestrator + shared trace bus; **compile/analyze** the agent graph (FlowCompile/AgentFlow/Auto) |
| P4 | When agents may run | CI/hot-path → freeze artifacts; not always-on default |
| P5 | Oracles for money | Layered admit + named false-negative owners |
| P6 | Ownership / supply chain | CODEOWNERS + signed provenance + sandbox |
| P7 | Multi-DSL portability | Multi-skill + HW RAG; IR is substrate not sole API |
| P8 | What customers buy | Flag/SKU + frozen artifacts; bring-up = internal/platform |
| P9 | Eval for agents-as-products | Public p50/p90 + private canaries; always show cost-to-compile |
| P10 | Unit economics / pricing | Sell artifacts + CI quotas; not raw token burn |
| P11 | Multi-tenancy / SaaS | Prefer customer-owned CI; cloud needs isolation+residency |
| P12 | Model-provider lock-in | Pluggable models + golden replay; distill when rights exist |
| P13 | Legal / IP of outputs | Customer owns artifacts; opt-in telemetry only |
| P14 | Joint versioning | Pin agent+compiler+HW+model in admit records |
| P15 | Cold start new HW | Coverage SLA then perf SLA (**C9**) |
| P16 | HITL review bandwidth | Oracle auto-merge narrow; humans CODEOWN rewrites |
| P17 | Trajectory flywheel ownership | Closed for hetero prod; open traces for heuristic research |
| P18 | Interactive latency SLOs | Interactive = lab tier; batch freeze = product |
| P19 | DR / corrupted tree | Allowlisted edits + canary rollback |
| P20 | Production A/B platform | Required before “production default” marketing |
| P21 | Compliance / ISA RAG | Customer-hosted manuals; learn from compiler feedback when needed |
| P22 | Deterministic orchestration | FSM/plan + LLM judgment; not free tool-calling as default |
| P23 | Tokens / inference / model capability | **Yes, hard problems** — but mostly for *online* always-on paths; freeze artifacts + route/distill + Amdahl budgets make them manageable |

#### P1 — What is the agent↔compiler contract?

Agents must exchange state with the data plane. The medium of that contract is a product decision.

| Option | What it is | Pros | Cons |
|---|---|---|---|
| **A. Natural language only** | Prompts + free-text tool stdout (`opt` logs, NCU dumps pasted into chat) | Fast to prototype; matches coding-agent UX | Brittle; non-replayable; model upgrades break CI; no typed admit |
| **B. Structured logs / traces** | JSON/protobuf records: IR fingerprint, action enum, oracle result, cost, artifact hash | Replayable; cacheable; audit/SBOM-friendly; CI-regressable | Schema design cost; vendors disagree on fields |
| **C. Typed tool APIs (MCP-class)** | `compile` / `verify` / `bench` / `profile` with typed I/O (mlirAgent, Archer, Compiler-R1 tools) | Clear action space; sandboxes; versionable | Needs toolchain investment; still need a trace store behind tools |
| **D. Hybrid: NL for humans, structured for machines** | Engineers chat; agents speak schemas; NL is a *view* over traces | HITL-friendly without sacrificing replay | Two surfaces to keep consistent |

**Survey lean.** Prefer **C + B** as the product contract; use **D** at the human edge. Pure **A** is fine for demos, not for commercial compile paths (§4.3–4.5). Concrete artifact shapes already exist: CompileIQ **ACFs**, KernelEvolve **MPP** profiler federation, ACCLAIM tool-calling over clang components.

**Example (might be true).** The durable contract is not “the prompt,” but a **versioned admit record**: `{graph_hash, hw_id, compiler_ver, action[], oracle[], artifact_digest, policy_id}`. NL rationales are optional commentary attached to that record.

**Also commercially.** Who governs the schema (vendor vs LLVM/StableHLO RFC)? What is the **fail mode** when the contract breaks (silent wrong admit vs hard fail)? Keep chat UX as a *view* over traces so SaaS does not create two sources of truth.

#### P2 — Context-window / memory loss across long optimize loops

Kernel and heuristic search run for hours and hundreds of trials. The agent forgets early failures, successful tilings, and HW constraints.

| Option | Mechanism | Pros | Cons |
|---|---|---|---|
| **A. Stuff the window** | Ever-growing chat of logs + code | Simple | Hits context limits; attention dilutes; expensive |
| **B. Dense session memory** | Compress trajectory → summary / skill cards / vector store (KernelEvolve skill library; KernelBlaster persistent CUDA KB) | Survives long runs; transferable across tasks | Compression loses edge cases; retrieval can be wrong |
| **C. External artifact memory (VCS)** | Check in ACFs, kernels, heuristics, admit traces; agent loads by hash | Durable across jobs/models; reviewable; SBOM-ready | Needs ownership & review process (§4.8–4.9) |
| **D. Many short-lived sub-agents** | Fresh agent per trial/op/HW; orchestrator holds only pointers | Avoids context rot; parallelizable | Coordination overhead; may rediscover failures without shared store |
| **E. Hybrid: sub-agents + dense + VCS** | Orchestrator + specialists; dense working memory; promote winners to VCS | Matches industrial KernelEvolve / ACCLAIM shapes | Highest systems complexity |

**Survey lean.** Commercial practice needs **E**, with a hard rule: **anything that affects a release build must live in C (external artifacts), not only in chat**. Dense memory is for *search acceleration*; VCS memory is for *product truth*.

**Example (might be true).** Treat the LLM context as a **scratchpad**, dense memory as a **L2 cache of skills**, and git as **durable store**. If the model is swapped, scratchpad dies, L2 may warm-start, git must still rebuild the binary identically.

**Also commercially.** Multi-tenant skill/RAG isolation; **invalidate** dense memory on compiler/HW upgrades (KernelBlaster across gens); decide whether customer trajectories may train vendor skills (P13/P17).

#### P3 — Many sub-agents vs one dense-memory agent

| Option | Pros | Cons | Best fit |
|---|---|---|---|
| **Monolith agent + dense memory** | Simpler ops; one policy to eval | Jack-of-all-trades; noisy tools confuse one policy | Small orgs; single DSL |
| **Specialist sub-agents** (gen / debug / perf / verify / HW-RAG) | Clear skills; parallel search; mirrors ACCLAIM / GEAK / KernelEvolve | Orchestration bugs; cost multiplies; inconsistent styles | Multi-HW / multi-DSL products |
| **Hierarchy** (orchestrator + workers + judge) | Budget control; staged admit | Judge can be wrong; latency | Production CI with spend caps |
| **Compiled / analyzed topology** (workflow IR + ADG + freeze) | Topology is a compile object: Pareto configs, static checks, amortize hot spans | Needs IR + adapters; early ecosystem | Any SLA’d multi-agent product |

**Survey lean.** For commercial multi-accelerator stacks, **specialists + orchestrator** win; invest early in a **shared admit/trace bus** so sub-agents do not keep private incompatible memories (ties to P1–P2). Treat the topology itself as compiler-shaped: **FlowCompile**-style offline workflow search, **AgentFlow**-style ADG audit, **Auto**-style freeze of witnessed-deterministic spans.

**Also commercially.** Budget per specialist (ACCLAIM); tool-calling quality can fail before code skill; support must debug multi-agent traces. Prefer **deterministic orchestration + LLM judgment** (TritorX FSM, GEAK v3) over unbounded free tool-calling for SLA’d products (→ P22).

#### P4 — Online cost, flaky speedups, and “when may the agent run?”

| Option | Pros | Cons |
|---|---|---|
| **Always-on online agent at compile** | Max specialization | $ and nondeterminism; release engineering rejects |
| **CI / nightly specialize → freeze artifact** | Replayable defaults; human review window | Stale vs new shapes; slower iteration |
| **Hot-path trigger only** (Amdahl rank, p99 decode) | Spend where it pays (AutoKernel-style) | Trigger policy itself needs ownership |
| **Offline-only (Magellan)** | Users see classical `-O3` | Misses per-model serving wins |

**Survey lean.** Commercial default: **CI/nightly or hot-path → freeze ACF/kernel into VCS**; interactive online agents as an opt-in lab mode until budgets and replay are boring (§4.1, §4.3, **C5**).

**Also commercially.** Publish budget SLOs (`$/build`, tokens/%gain, GPU-hours); flaky-speedup CI policy under HW noise; separate **interactive latency tiers** (P18) from batch freeze; who pays for GPU (vendor cloud vs customer cluster) (P10).

#### P5 — Correctness oracles strong enough for money

| Option | Pros | Cons |
|---|---|---|
| Unit / golden / OpInfo | Cheap; TritorX-proven for coverage | Misses subtle perf-correct bugs |
| Numerical tol vs reference | Kernel-friendly | Tolerance games; training≠infer |
| Local formal (Alive2) | Strong when applicable | Peephole; weak on GPU concurrency |
| Serving A/B + canaries | Catches product regressions | Slow; expensive; attribution hard |
| Layered admit (all of the above) | Defense in depth | Process heavy |

**Survey lean.** **Layered admit** is the only commercial-grade answer (**§4.2**). Ship with explicit **false-negative owners**.

**Also commercially.** Cover FP contracts, GPU races, serving equivalence (§4.2)—not only unit tests. Oracle cost can erase single-digit CompileIQ wins (**C2**). Decide liability when layered admit passes and production still miscompiles. Top layer needs a real A/B platform (P20).

#### P6 — Ownership, security, and supply chain of agent code

Agent-written heuristics/kernels are still production code.

| Option | Pros | Cons |
|---|---|---|
| Agent PRs as human-owned | Clear CODEOWNERS | Reviewer bottleneck |
| Auto-merge under oracle gates | Scale | Oracles incomplete → silent breakage |
| Signed provenance (model, prompt, tools, admit) | Audit / SBOM-like | New infra |
| Sandbox + no network for codegen | Reduces exfil / supply risk | Slows tool use |

**Survey lean.** **Human CODEOWNER + signed admit provenance + sandbox**; auto-merge only for narrow action classes with strong oracles (Archer-style), not free rewrite (**C7**, §4.8–4.9).

**Also commercially.** Threat model beyond “sign something”: malicious kernels, prompt/tool injection, DoS schedules (§4.9). CCC-style “not for production” disclaimers signal culture until harness+oracles are boring. Legal/IP assignment of outputs is separate (P13). HITL *capacity* is separate (P16). DR when agents edit trunk (P19).

#### P7 — Multi-DSL / multi-vendor portability

| Option | Pros | Cons |
|---|---|---|
| One DSL to rule them (e.g. Triton-only agents) | Focused data | Breaks on Tile/CuTe/HIP/FlyDSL (**C4**) |
| Multi-skill agents + HW RAG | Matches KernelEvolve / KForge / GEAK | Training and eval explode |
| Lower to portable IR, agents on IR only | Theory-nice | Free IR rewrite weak (mlirAgent); still need device skills |

**Survey lean.** **Multi-skill + HW RAG** commercially; portable IR remains the *substrate*, not the sole agent language (**C3**, **C4**).

**Also commercially.** Cold-start productization for new ASICs (P15); sell **coverage SLA vs perf SLA** separately (**C9**); eval-matrix cost across DSLs is a P&L item (P9/P10).

#### P8 — Product packaging: what customers buy

| Option | Pros | Cons |
|---|---|---|
| Compiler flag / autotune SKU (CompileIQ) | Familiar; ACF portability story | Gains may be single-digit on hot kernels (**C2**) |
| Cloud optimize service | Recurring revenue; centralized HW | Data gravity; reproducibility across tenants |
| Internal platform only (Meta Ranking Engineer Agent) | Fits ads/ASIC TTM | Hard to productize externally |
| OSS agent harness + paid oracles/HW | Ecosystem | Support burden |

**Survey lean.** Near term: **flag/SKU + frozen artifacts** for external customers; **internal platforms** for ASIC bring-up. Do not sell “chat with your compiler” as the sole SKU.

**Also commercially.** Pricing/unit economics (P10); multi-tenancy (P11); map SKUs to jobs (a)/(b)/(c)/(d)—CompileIQ flags ≠ TritorX bring-up platforms ≠ AlphaEvolve-style cloud coding agents ([`PRODUCTS.md`](PRODUCTS.md)).

#### P9 — Eval & benchmarks for agents-as-products

Buyers need **distributions and cost**, not best-kernel blogs (**C2**, §4.1, §4.10).

| Option | Pros | Cons |
|---|---|---|
| Vendor-private suites only | Matches production truth | Buyers cannot verify |
| Public ladder only (KernelBench → fusion → serving) | Comparable; CI-friendly | May understate internal wins; maintain cost |
| Customer-workload certification | Sells on their fleet | Slow sales cycle |
| **Hybrid: public p50/p90 + private canaries** | Honest marketing + real SLAs | Two reporting systems |

**Survey lean.** Hybrid; **always report cost-to-compile beside speedup**. Evidence: KernelBench-X ceilings, CompileIQ docs 2–3% on hot kernels, GEAK eval suites, §5.5 p50/p90 milestone.

#### P10 — Unit economics & pricing

Token + GPU cost can dominate single-digit gains (§4.3; ACCLAIM budgets).

| Option | Pros | Cons |
|---|---|---|
| Per optimize-job / GPU-hour | Aligns with cloud cost | Punishes thorough search |
| **Per frozen artifact (ACF/kernel)** | Matches “ship artifacts” | Hard to price before search |
| Outcome-based (% latency / $ saved) | Easy ROI story | Attribution wars (P24-class); baseline games |
| **Seat + CI quota** | Predictable OpEx | Leaves headroom on huge wins |

**Survey lean.** **Artifact license + CI quota** near term; avoid pure outcome pricing until A/B attribution (P20) exists. Do not sell unbounded token burn.

#### P11 — Multi-tenancy, SaaS isolation, data gravity

| Option | Pros | Cons |
|---|---|---|
| Fully managed cloud optimize | Recurring $; rare HW | Leakage risk; residency; attack surface |
| Customer VPC / on-prem agent + cloud model API | Data local | Model lock-in |
| Fully air-gapped local models | Regulated buyers | Weaker models; support cost |
| **Artifact-only: customer CI runs searcher** | Least SaaS risk | Harder recurring revenue |

**Survey lean.** **Customer-owned CI** for external compile SKUs; VPC/air-gap for ASIC bring-up with proprietary ISA docs (KernelEvolve-class RAG).

#### P12 — Model-provider lock-in & swap survivability

| Option | Pros | Cons |
|---|---|---|
| Single frontier API | Best tool-calling today | Price/quality cliff |
| **Pluggable backends + golden replay CI** | Survives swaps | Quality floor = weakest model |
| Distill specialists on flywheel | Cheap, controllable | Needs data rights (P13/P17) |
| Offline artifacts only; model in eng CI | Users see deterministic `-O3` | Misses online specialize $ |

**Survey lean.** **Pluggable + replay**; distill when rights exist (KernelEvolve RL path; Magellan/OpenEvolve OSS signal). Customer default path remains frozen classical artifacts (**C5**).

#### P13 — Legal / IP ownership of agent-generated artifacts

| Option | Pros | Cons |
|---|---|---|
| **Customer owns outputs; vendor owns weights** | Clean procurement | Blocks silent flywheel on customer data |
| Shared improvement / opt-in telemetry | Improves product | Enterprises often refuse |
| OSS-license artifacts by default | Ecosystem | Leaks differentiation |
| Work-for-hire + indemnification SKU | Enterprise-friendly | Expensive legal |

**Survey lean.** **Customer owns ACFs/kernels/heuristics**; telemetry **opt-in only**; never silent training on customer graphs (§4.7–4.8; CCC production caution).

#### P14 — Joint versioning (agent + compiler + HW + model)

| Option | Pros | Cons |
|---|---|---|
| **Content-addressed admit records in VCS** | Replayable; SBOM-ready | Schema tax (P1) |
| Lockstep vendor releases | Simple support matrix | Slow; multi-vendor fleets break |
| **Policy bundles** (“optimize profile vN”) | Productizable | Bundle sprawl |
| Re-optimize on any bump | Always fresh | Cost explosion |

**Survey lean.** **Admit records + policy bundles**; forbid silent re-optimize without budget SLO (§4.3 cache keys).

#### P15 — Cold start for new HW / ISA (bring-up productization)

| Option | Pros | Cons |
|---|---|---|
| **Coverage-first SKU then perf SKU** | Matches **C9** ladder; sellable milestones | Coverage ≠ serving peak |
| Perf-only from day one | Clear ROI narrative | Fails ASIC TTM |
| **Sim-first pre-silicon agents** | Early codesign feedback | Sim fidelity gaps |
| Human skeleton + agent fill | Predictable ownership | Slower agent narrative |

**Survey lean.** **Coverage → perf** with explicit SLAs; sim-first when pre-silicon (TritorX, KernelEvolve RAG, Ascend diagnosis).

#### P16 — Human review bandwidth (HITL capacity)

Agents raise draft volume; reviewers become the bottleneck (§1b, §4.8, **C7**).

| Option | Pros | Cons |
|---|---|---|
| Human owns every merge | Safest | Does not scale |
| **Oracle auto-merge narrow; human for rewrites** | Archer-scalable | Oracle holes |
| Quota reviews/week + prioritization | Capacity planning | Good patches wait |
| **Compiler-oracle review agents as force multiplier** | Matches C7-B | Still needs human CODEOWNER |

**Survey lean.** **B + D**; publish review-time vs escaped-bug metrics (§4.8 done-looks-like).

#### P17 — Trajectory / flywheel ownership

| Option | Pros | Cons |
|---|---|---|
| **Fully closed trajectories** | Moat (Meta/AMD/NVIDIA) | Weak external trust |
| Public anonymized traces (Compiler.next #10) | Research + smaller vendors | May leak HW limits |
| Federated / siloed memories | Privacy-preserving | Hard systems |
| Sell data foundation as SKU | Clear ownership | Few buyers |

**Survey lean.** **Closed** for hetero production agents; **open traces** for CPU/IR heuristic-evolution research (Magellan/OpenEvolve). ieee-pulse: data scarcity is already a field limiter.

#### P18 — Interactive latency SLOs vs batch optimize

| Option | Pros | Cons |
|---|---|---|
| Promise interactive “chat optimize” | Attractive UX | Hours-long MCTS breaks support |
| **Lab tier (best-effort) vs product tier (batch freeze)** | Honest SLOs | Two products to explain |
| Hard timeout + partial artifact | Bounded cost | Users get weak results |
| Offline-only eng tools | Simplest SLA | Misses serving specialize |

**Survey lean.** **Lab vs product tiers**; product default = batch/CI freeze (P4). TritorX “overnight,” KernelEvolve long search, CompileIQ evolutionary runs are batch-shaped.

#### P19 — Disaster recovery when agents corrupt trees

| Option | Pros | Cons |
|---|---|---|
| Branch-only writes + revert bots | Clear blast radius | Slower landing |
| **Allowlisted edit surfaces (EVOLVE-BLOCK)** | Magellan pattern | Constrains creativity |
| **Signed release + canary auto-rollback** | Production-grade | Needs P20 |
| Immutable artifact store; never live-rewrite trunk heuristics | Strongest safety | Slower iteration |

**Survey lean.** **Allowlist + canary rollback** for compiler-source agents; branch-only for repo-level kernel agents (GEAK v3 multi-file patches).

#### P20 — Production A/B & experimentation platform

| Option | Pros | Cons |
|---|---|---|
| Serving canaries only | Real regressions | Slow; expensive |
| **Shadow compile + offline replay benches** | Cheap gate | Misses serving numerics |
| Full experimentation platform | Settles **C2**; funds outcome pricing | Large eng investment |
| Trust vendor blogs | Zero cost | Not commercial-grade |

**Survey lean.** Shadow/replay as default gate; canaries/full platform **before** any “production default” claim (§4.1; MLGO persistent-QPS bar).

#### P21 — Compliance: export, residency, proprietary ISA docs

| Option | Pros | Cons |
|---|---|---|
| No proprietary manuals in cloud RAG | Lower risk | Weak cold start |
| **Customer-hosted RAG corpora** | Residency OK | Integration pain |
| Certified regions + export classification | Enterprise sales | Slow GTM |
| **Learn from compiler/crash feedback only** | TritorX-like | Slower perf ramp |

**Survey lean.** **Customer-hosted manuals** when selling to silicon vendors; else prefer compiler-feedback learning over exporting ISA corpora.

#### P22 — Deterministic orchestration vs free LLM judgment

Adjacent agent-production work stresses **deterministic boundaries** and moving the LLM out of the hot execution loop; TritorX deliberately uses an FSM rather than free tool-calling. Control-plane substrate papers sharpen the same lean: [AgentFlow](../publications/agentflow.md) ADGs make agent programs analyzable; [FlowCompile](../publications/flowcompile.md) pushes config search offline; [heterogeneous agent serving](../publications/agentic-ai-hetero-systems.md) places stages under cost/SLO policies rather than “run everything on the biggest GPU.”

| Option | Pros | Cons |
|---|---|---|
| Free tool-calling agent | Flexible | Hard to SLA; runaway loops/cost |
| **Plan/FSM + LLM fills bounded slots** | Predictable; auditable | Less “agent magic” marketing |
| Compile-then-execute (LLM offline only) | Aligns hybrid prediction; Auto/FlowCompile path | Needs strong offline jobs (b)/(d) + workflow compile |
| Soft max-steps + human gate | Practical | Caps autonomy |

**Survey lean.** **FSM/plan + bounded LLM slots** for any SKU with an SLA; free tool-calling stays lab-tier (ties P3/P4/P12; supports **C6-B**). Prefer ADG/static checks before deploy and hetero placement policies for cost.

#### P23 — Tokens, inference performance, and model capabilities

**Question.** Will LLM **token burn**, **inference latency/throughput**, and **model capability gaps** block turning the hybrid prediction into commercial practice?

**Short answer.** **Yes — they are first-class commercial problems**, especially for always-on online agents. They are **not** show-stoppers for the hybrid bet if products **freeze artifacts**, **Amdahl-budget** search, and **route/distill** models. They *are* show-stoppers for “chat with the compiler on every build” without spend and latency SLOs.

##### Evidence from this survey’s corpus

| Dimension | What we see | Digests / sections |
|---|---|---|
| **Token / $ cost** | Agent loops multiply spend vs one-shot chat; cost poorly standardized (tokens + GPU-hours per % gain); ACCLAIM must *distribute budget* across levels; AutoKernel warns not to burn tokens on tiny Amdahl slices; ieee-pulse stresses cost/data limits in HPC | §4.3, P4/P10; `acclaim`, `autokernel`, `ieee-pulse-llm-compilers`, Compiler.next CTAs |
| **Inference latency** | Kernel/heuristic search is hours-scale (MCTS/evolution, TritorX overnight, CompileIQ evolutionary runs)—not interactive TTFT; multi-agent tool loops add wall-clock even when tokens are cheap | P18; `tritorx`, `kernelevolve`, `compileiq-*` |
| **Model capability — codegen** | Frontier one-shot KernelBench often weak (<~20% `fast_p`); iterative refine helps; specialized small models (KernelLLM 8B) can compete on narrow tasks | `kernelbench`, `kernelllm`, Trend D |
| **Model capability — IR rewrite** | Free IR transforms can score **below identity** (mlirAgent); capability ≠ safe data-plane replacement | `mliragent`, **C3**, A5 |
| **Model capability — tools** | Open models often fail **tool-calling** before code quality (ACCLAIM); multi-agent compilers die on malformed tools | `acclaim`, §3.2 |
| **Model capability — sample efficiency** | Language priors can cut search vs blind autotune (Reasoning Compiler, AutoPass inference-only); Magellan/AlphaEvolve spend offline then ship classical code | `reasoning-compiler`, `autopass`, `magellan` |
| **Mitigations already shipping** | Freeze ACF/kernel into VCS; HW RAG + skills (KernelEvolve); distill/RL specialists on trajectories; Fast Feedback (~10× vs full IR in-loop); offline job (b) so users never pay LLM at `-O3` time | P2/P4/P12; CompileIQ ACF; Magellan |
| **Control-plane freeze / workflow compile** | [Auto](../publications/auto-agi-compiler.md): compile witnessed-deterministic agent spans → WASM cognition binaries + deopt; [FlowCompile](../publications/flowcompile.md): offline Pareto configs for sub-agent workflows; hetero placement avoids frontier GPUs for every stage | `auto-agi-compiler`, `flowcompile`, `agentic-ai-hetero-systems`; §4.6 |

**Adjacent industry signal (agent production, not compiler-specific).** Agentic tasks commonly cost **many×** chatbot tokens (iterative tool use + context re-send—“communication tax”; code-review-like stages dominate token share in agentic SE studies). Prompt caching, model routing (small models for easy steps), and context compaction are becoming mandatory FinOps—not optional polish. This reinforces compiler-agent design: **fewer, higher-value LLM calls** behind oracles beat chatty multi-agent refinement in the hot path—and **compile/freeze the agent graph** when spans are deterministic (Auto), rather than re-paying tokens every run.

##### Options (how products respond)

| Option | Pros | Cons |
|---|---|---|
| **A. Always-on frontier model at every compile** | Max freshness | Token+latency blow up; release eng rejects; capability still needs oracles |
| **B. Batch/CI optimize → freeze artifact** (hybrid default) | Amortize tokens over many serves; replayable | Stale vs new shapes; needs re-optimize policy |
| **C. Route + distill** (frontier orchestrator, small specialists; KernelEvolve-style RL) | Cuts $/task and often latency | Needs trajectory rights (P13/P17); tool-calling quality still gates open models |
| **D. Capability firewall** (LLM only in bounded actions; classical data plane executes) | Capability gaps don’t miscompile by default | Limits “agent authors the opt” narrative |
| **E. Ignore and hope prices fall** | Simple story | Volume of agent loops can outrun $/token declines |

##### Conclusion (survey stance)

1. **Tokens will be a problem** for any product that keeps the LLM in the **online compile loop** without budgets. Treat token burn as OpEx tied to **%gain and p50 wins** (**C2**, P9/P10)—not as a vanishing cost.  
2. **Inference performance will be a problem** for interactive UX; it is **acceptable** for overnight/CI specialize if SLOs are honest (P18). Do not market batch search as chat.  
3. **Model capabilities will be a problem** in three distinct ways—and they are easy to confuse:  
   - **Weak one-shot kernel/IR skill** → needs search + oracles, not a bigger prompt;  
   - **Unsafe free rewrite** even when fluent → keep data plane classical (**C3**/A5);  
   - **Fragile tool-calling** on open models → blocks multi-agent SKUs before “coding IQ” does.  
4. **Therefore:** under the hybrid prediction, these resource/capability limits **shape the SKU** (freeze, Amdahl trigger, route/distill, FSM bounds) more than they **falsify** agentic compilers. They **do** falsify “LLM-as-`opt` every build” as a commercial default.  
5. **Watch metrics that settle this:** tokens (or $) per admitted %gain; p50 wall-clock of optimize jobs; tool-call success rate by model tier; win rate after model swap with golden replay (P12/P14).

**Example (might be true).** A viable commercial control plane spends frontier tokens on **orchestrating a few dozen oracle-gated trials** for Amdahl-hot regions, distills a specialist for the common cases, and ships an ACF/kernel that serves **millions of inferences with zero LLM calls**—so token and capability risk sit in eng CI, not in the customer’s critical path.

#### Commercial checklist (if you are building this)

**Architecture**
1. Contract = typed tools + structured admit traces (not NL alone).  
2. Memory = scratchpad ≪ dense skills ≪ **VCS artifacts**.  
3. Topology = orchestrator + specialists + shared trace bus; prefer FSM/plan for SLA paths.  
4. Agents run in CI/hot-path → **freeze** before default-on.

**Trust & ops**
5. Layered oracles + named false-negative owners.  
6. CODEOWNERS + signed provenance + sandbox; allowlisted edits + canary rollback.  
7. Joint version pins: agent policy + compiler + HW + model.  
8. Eval ladder: public distributions + private canaries; always show **cost-to-compile**.  
9. A/B / shadow gates before “production default” marketing.  
10. HITL capacity plan (oracle auto-merge narrow; measure review bandwidth).

**Business & compliance**
11. SKU = regressable artifacts (+ CI quota), not chat sessions alone.  
12. Customer owns outputs; telemetry opt-in; pluggable models with golden replay.  
13. Multi-DSL skills; coverage SLA then perf SLA for new silicon.  
14. Tenancy/residency story for ISA RAG and customer graphs.  
15. Support runbooks: replay packs, spend caps, severity for oracle misses.  
16. **Resource envelope (P23):** budget tokens/$ per %gain; no always-on frontier in default compile; route/distill; measure tool-call success and optimize wall-clock SLOs.

**Still blocks / changes packaging:** §4.1–4.5, §4.7–4.10; conflicts **C2** (gains pay?), **C3** (API width), **C5** (default-on), **C7** (oracle review), **C9** (coverage vs peak). Resource/capability envelope: **P23**.

---

## 6. Conflicts (pointer)

Search results often disagree (vendor headlines vs docs, Magellan vs MLGO, free rewrite vs advisory-only, Triton vs Tile, online vs offline agents, coverage vs peak bring-up, compiler codesign vs autonomous EDA). **Do not collapse these into a false consensus.**

→ Full write-up: [`CONFLICTS.md`](CONFLICTS.md) (C1–C10).

Working stance used in §5: hybrid control/data plane; Magellan and MLGO as parallel bets; discount single-number speedups; constrain actions until oracles prove free rewrite; demote generic SCM AI as Tier C; codesign via coverage→perf agent ladder (**C9**), not autonomous chip design (**C10**).

---

## 7. How to read this repo

1. Skim **§0.1 North star**, **§5 Future prediction** (architecture §5.1 + roadmap §5.5), then [`STACK.md`](STACK.md).
2. If shipping commercially: read **§5.7** (P1–P22: contract, memory, eval, pricing, tenancy, IP, DR, …).
3. Check [`CLAIMS.md`](CLAIMS.md); read [`CONFLICTS.md`](CONFLICTS.md) when two sources disagree.
4. Use [`SYSTEMS.md`](SYSTEMS.md) for concrete systems.
5. Use [`REPOS.md`](REPOS.md) / [`PRODUCTS.md`](PRODUCTS.md) as **Tier A/B/C evidence for the prediction**, not forge/SKU catalogs.
6. Use [`../publications/INDEX.md`](../publications/INDEX.md) (prefer ★ — ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer).
7. Contribute via [`WORKFLOW.md`](WORKFLOW.md); validate with `python3 scripts/validate_survey.py`.
8. Track progress in [`../STATUS.md`](../STATUS.md).

**One-page success check:** (1) Predicted agentic compiler? → §5.1 / §5.5. (2) Four agent jobs including codesign bring-up? → §5.1 / STACK. (3) Evidence vs noise? → Tier A vs C. (4) Commercial blockers? → §5.7.
