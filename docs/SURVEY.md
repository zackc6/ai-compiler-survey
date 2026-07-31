# Next-Gen AI Compiler Survey (expanded)

**Last updated:** 2026-07-31  
**Companion digests:** [`../publications/`](../publications/)  
**Status:** [`../STATUS.md`](../STATUS.md)

---

## 0. Executive verdict

Compilation is shifting from **fixed pass pipelines + black-box autotuning** toward **hybrid LLM–compiler loops**. Empirically, the winning pattern is:

> **Agents own semantic search, orchestration, and artifact synthesis. Compilers own lowering, legality, measurement, and fallback.**

Agents are reshaping the **control plane** of compilation more than replacing the **data plane**. See [§1b](#1b-traditional-ai-compilation-vs-following-trends) for a traditional-vs-trends pros/cons comparison, and [§4](#4-whats-missing--under-covered-q4) for ten under-covered gaps (production evidence, correctness at scale, cost/reproducibility, interoperability, agent interfaces, FMware, training data, HITL, security, unified benchmarks).

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
| CGO / CC / ASPLOS / PLDI / MLSys | Systems + compilers |
| NeurIPS / ICML (+ C4ML) | Methods + KernelBench / Reasoning Compiler / Compiler-R1 |
| ACL Findings | HintPilot-style SE/NLP crossover |
| LLVM Discourse (LLVM ♥ ML workshop) | MLGO, Magellan, agent PR review |
| Vendor blogs | NVIDIA CUDA Tile/CompileIQ, AMD GEAK, Meta KernelLLM/LLM Compiler, DeepMind AlphaEvolve, Modular |

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

The trends above are real, but coverage is uneven. Below, each gap is spelled out with **what exists**, **what is missing**, **why it blocks progress**, and **what “done” could look like**. Digests cited live under [`../publications/`](../publications/).

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

**What exists.** mlirAgent: structural IR fingerprinting, knowledge graphs, MCP tool suites; Compiler-R1 tool calls (`instrcount`, etc.); GEAK hardware feedback loops; CompileIQ search spaces over NVCC/PTXAS internals.

**What is missing.** **Standards**, not demos:

- Common fingerprint / provenance for pass effects;
- Vendor-neutral MCP (or equivalent) tool schemas for “compile / verify / bench”;
- Safe sandboxes for executing agent-proposed kernels at scale;
- First-class exposure of HW counters to agents without scraping profiler text.

**Why it blocks progress.** Agents without structured interfaces fall back to brittle prompt-and-pray over `opt` stdout.

**Done looks like.** LLVM/MLIR/Triton tool APIs that agents can call with typed I/O; fingerprinting as a supported analysis; conformance tests for tool servers.

---

### 4.6 FMware / agent-app compilation

**What exists.** Compiler.next vision: compile prompts, agent topologies, and free parameters under multi-objective quality gates; generative compilation couples compilers into coding agents; industry agent harnesses (Claude C compiler) stress test construction.

**What is missing.** Mature analogues of DL compilers for FMware:

- Stable IRs for prompt/tool graphs;
- Compilation that **fails closed** when quality thresholds miss;
- Interoperability between “prompt compilers” and classical model compilers;
- Shared traces for community learning (Compiler.next call-to-action #10).

**Why it blocks progress.** LLM applications still tune by hand and folklore while DL graphs enjoy decades of compiler investment.

**Done looks like.** Reproducible FMware compile pipelines with gold labels, cost/latency/quality Pareto fronts, and CI that blocks regressions—parallel to how model zoos ship compiled artifacts today.

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

**What exists.** Magellan produces reviewable C++ heuristics; LLVM Discourse agent PR review reports bugs with compiler-specific tools; Anthropic CCC emphasizes harnesses; Lattner commentary stresses tests as the real product.

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

## 5. How to read this repo

1. Skim this file for the narrative (including **§1b** traditional vs trends and **§4** gaps).
2. Use [`SYSTEMS.md`](SYSTEMS.md) for a comparison table of concrete systems.
3. Use [`../publications/INDEX.md`](../publications/INDEX.md) as the bibliography.
4. Open individual digests for key contributions and takeaways.
5. Track what’s done / next in [`../STATUS.md`](../STATUS.md).
