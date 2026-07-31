# Source-control repositories matched to survey context

This page catalogs **GitHub / Gerrit / googlesource** artifacts related to next-gen AI compilers and agentic compilation, and maps each to the survey narrative in [`SURVEY.md`](SURVEY.md). Digests (where added) live under [`../publications/`](../publications/).

**Reading tip:** Hosting forge matters for *how* agents attach to review:

| Forge | Typical use in this space | Agent attachment style |
|---|---|---|
| **GitHub** | LLVM PRs, research code, vendor OSS (GEAK, CompileIQ, KernelBench) | PR bots / offline agents (`--pr N`), Actions CI |
| **Gerrit** (Google/Android/Chromium-class) | Large proprietary + some OSS review flows | In-change `/review` plugins, sidebar agents, votes |
| **googlesource** | Gerrit plugins, Chromium/Android adjacent | Same plugin model as Gerrit |

LLVM itself is primarily reviewed on **GitHub PRs** today; Android/Chromium-scale orgs often remain on **Gerrit**—hence both appear below.

---

## 1. Map: repo → survey section / gap

| Repository | Forge | Survey match | Primary gaps / themes |
|---|---|---|---|
| [cuhk-s3/Archer](https://github.com/cuhk-s3/Archer) + [paper](https://arxiv.org/html/2607.01808) | GitHub | §2 agents (tester/critic), §3 HITL reshape, §4.8 HITL, §4.2 correctness | Compiler-specific PR review >> generic SWE agents |
| [gerrit ai-code-review plugin](https://gerrit.googlesource.com/plugins/ai-code-review/) | googlesource/Gerrit | §4.8 HITL, §4.9 security (generic AI review) | In-change `/review`; **not** compiler-specialized |
| [amarula/reviewai-gerrit-plugin](https://github.com/amarula/reviewai-gerrit-plugin) | GitHub→Gerrit | §4.8 | Sidebar Review Agent on Gerrit changes |
| [GerritForge/ai-review-agent-provider](https://github.com/GerritForge/ai-review-agent-provider) | GitHub | §4.8, §4.5 interfaces | Provider API for Gerrit native AI chat (v3.14+) |
| [llvm/llvm-project](https://github.com/llvm/llvm-project) | GitHub | Substrate for MLGO, Magellan, Archer, LLM-VeriOpt | Production IR data plane |
| [google/ml-compiler-opt](https://github.com/google/ml-compiler-opt) | GitHub | §1b traditional ML-in-compiler, Trend B | Offline training for in-tree MLGO advisors |
| [facebookresearch/CompilerGym](https://github.com/facebookresearch/CompilerGym) | GitHub | Trend B, §4.10 benchmarks | RL gym / pass-order env |
| [Mind4Compiler/Compiler-R1](https://github.com/Mind4Compiler/Compiler-R1) | GitHub | Q2 tool-using agents | SFT+RL pass tuner code |
| [ZJU-PL/hintpilot](https://github.com/ZJU-PL/hintpilot) | GitHub | Hybrid Selector via hints | Semantics-preserving pragma synthesis |
| [ucb-bar/mlirAgent](https://github.com/ucb-bar/mlirAgent) | GitHub | §4.5 agent interfaces, Magellan-adjacent | MCP tools + IR fingerprints |
| [algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve) | GitHub | Magellan/AlphaEvolve lineage, §4.3 reproducibility claims | OSS AlphaEvolve-style evolution (Magellan slides cite OpenEvolve path) |
| [cornell-zhang/heurigym](https://github.com/cornell-zhang/heurigym) | GitHub | Magellan related work, §4.10 | Agentic heuristic benchmark incl. **compiler** tasks (e-graph, parallelism) |
| [ScalingIntelligence/KernelBench](https://github.com/ScalingIntelligence/KernelBench) | GitHub | Trend D, §4.10 | GPU kernel LLM benchmark harness |
| [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent) | GitHub | Trend D, Q2 kernel agents | PyTorch→verified Triton agent pipeline |
| [AMD-AGI/GEAK](https://github.com/AMD-AGI/GEAK) / [GEAK-agent](https://github.com/AMD-AGI/GEAK-agent) | GitHub | Trend D, production kernel agents | Triton/HIP/serving optimization agents |
| [NVIDIA/CompileIQ](https://github.com/NVIDIA/CompileIQ) | GitHub | §1b / Trend C vendor control-plane | Evolutionary search over NVCC/PTXAS controls |
| [anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) | GitHub | Trend F agents-as-compiler-engineers, §4.8/4.9 | Full agent-written C compiler; harness/tests central |
| [facebook/KernelLLM](https://huggingface.co/facebook/KernelLLM) | HF (model card + code refs) | Trend D specialization | Small Triton specialist model |
| Discourse: [agent PR review thread](https://discourse.llvm.org/t/automated-review-with-agents-30-bugs-on-207-prs/90093) | Discourse→GitHub PRs | Precursor discussion to Archer | Experience report on LLVM opt PR agents |

---

## 2. Deep dive: SCM-native agent review

### 2.1 GitHub + LLVM — Archer (compiler-specialized)

- **Paper:** *Archer: Towards Agentic Review for Compiler Optimizations* ([arXiv:2607.01808](https://arxiv.org/html/2607.01808))
- **Code:** [cuhk-s3/Archer](https://github.com/cuhk-s3/Archer)
- **How it uses SCM:** Takes an **LLVM GitHub PR id**, loads pass knowledge, analyzes the patch in a local LLVM tree, validates with Alive2 / LLUBI / `opt`, emits evidence-backed review comments (PoC required).
- **Reported signal:** On recent LLVM PRs, finds a high rate of semantic bugs in open/closed optimization patches (paper: ~21% open / ~11% closed in their window)—underscoring **§4.8 review-capacity gap**.
- **Survey match:** Strongest existing answer to “agents in source control for compilers.” Contrasts with generic PR bots: **domain toolkit + validation guard**.

Matches gaps:

- **4.2 Correctness at scale** — executable validation before comment admission  
- **4.5 Hardware-native / compiler-native interfaces** — `verify`, `difftest`, `trans`, workflow tools  
- **4.8 HITL** — intended as *additional reviewer*, not merge authority  
- **4.9 Security** — still needs policy on auto-posting comments / trust of PoCs  

### 2.2 Gerrit — AI review plugins (general-purpose)

These are **source-control product integrations**, usually **not** compiler-IR aware:

| Project | Link | Mechanism | Survey caution |
|---|---|---|---|
| Gerrit `ai-code-review` plugin | [googlesource](https://gerrit.googlesource.com/plugins/ai-code-review/) | Post patch-set → LLM comments; `/review`, `/review_last`; optional votes; ChatGPT/Ollama/Azure | Generic diff review; weak for miscompile hunting without Alive2-class tools |
| ReviewAI Gerrit plugin | [amarula/reviewai-gerrit-plugin](https://github.com/amarula/reviewai-gerrit-plugin) | Sidebar chat on Change page; provider routes | Same: HITL UX, not compiler oracle |
| GerritForge AI Review Agent Provider | [GerritForge/ai-review-agent-provider](https://github.com/GerritForge/ai-review-agent-provider) | Backend for Gerrit v3.14+ native AI chat | Interface layer (§4.5), still needs compiler tools behind it |

**Match to context:** Shows industry demand to put agents **inside** Gerrit (Android/Chromium-class workflows). For *AI compilers*, treat these as **delivery channels**; Archer-style toolkits are the **semantic payload**. Combining them is an open opportunity (gap **4.4/4.5**): Gerrit plugin that calls Alive2/`opt`/KernelBench, not only ChatGPT on the diff text.

### 2.3 Host vs research repos

| Role | Examples |
|---|---|
| **Production compiler host** | `llvm/llvm-project`, OpenXLA/XLA, PyTorch (Inductor/Triton) |
| **Training / advisor infra** | `google/ml-compiler-opt` |
| **Agent / benchmark research** | CompilerGym, Compiler-R1, Archer, HeuriGym, KernelBench, KernelAgent, mlirAgent |
| **Vendor agent products** | GEAK, CompileIQ, KernelLLM |
| **Agent-built compiler artifact** | `anthropics/claudes-c-compiler` |

---

## 3. Research & vendor code repos (non-review, still SCM-hosted)

Grouped by survey theme.

### Heuristic synthesis / evolution (Magellan family)

| Repo | Why it matters |
|---|---|
| [openevolve](https://github.com/algorithmicsuperintelligence/openevolve) | OSS AlphaEvolve-style loop; Magellan slides mention open-source via OpenEvolve |
| [cornell-zhang/heurigym](https://github.com/cornell-zhang/heurigym) | Benchmark for LLM-crafted heuristics; includes **compiler** problems (e-graph extraction, intra-op parallelism) |
| Magellan paper itself | Evolves C++ into Google’s internal LLVM/XLA trees (production inlining narrative)—**not fully OSS** yet |

### Pass / hint / IR agents

| Repo | Why it matters |
|---|---|
| [CompilerGym](https://github.com/facebookresearch/CompilerGym) | Classic env for pass RL |
| [Compiler-R1](https://github.com/Mind4Compiler/Compiler-R1) | Tool-using RL pass agent |
| [hintpilot](https://github.com/ZJU-PL/hintpilot) | Hint synthesis with compile/profile loop |
| [mlirAgent](https://github.com/ucb-bar/mlirAgent) | MCP + fingerprints; negative result on direct IR rewrite |

### GPU kernel agents & benches

| Repo | Why it matters |
|---|---|
| [KernelBench](https://github.com/ScalingIntelligence/KernelBench) | Standard LLM→kernel eval |
| [KernelAgent](https://github.com/meta-pytorch/KernelAgent) | Multi-agent Triton generation + verify |
| [GEAK](https://github.com/AMD-AGI/GEAK) | AMD vendor agent for kernels + serving |
| [CompileIQ](https://github.com/NVIDIA/CompileIQ) | Tune compiler knobs, not source |

### Agents writing compilers

| Repo | Why it matters |
|---|---|
| [claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) | SCM history of agent-authored compiler; test harness as product |

---

## 4. Implications for this survey

1. **SCM is part of the control plane.** Next-gen AI compilation is not only “LLM proposes passes”; it is also “agents sit on PRs/Changes and gate merges” (Archer, Gerrit plugins).
2. **Specialize the reviewer.** Gerrit/GitHub AI plugins without compiler oracles address UX (§4.8) but not miscompiles (§4.2). Archer is the reference design for compiler-aware SCM agents.
3. **Reproducibility spans forges.** Agent compile traces (§4.3) should key off `(commit, PR/Change, tool versions, admit artifacts)` whether the host is GitHub or Gerrit.
4. **Open Magellan-class loops** currently lean on OpenEvolve + HeuriGym + mlirAgent rather than a single public Magellan monorepo—track that under §4.1 production evidence / OSS gap.
5. **Security (§4.9):** auto-voting Gerrit plugins and auto-commenting PR agents expand the attack/review surface; prefer evidence-gated posting (Archer’s validation guard pattern).

---

## 5. Suggested watchlist (update this table as repos appear)

| Watch | Reason |
|---|---|
| LLVM GitHub Actions + Archer-like bots | Path to default opt-PR review |
| Gerrit plugin + Alive2/`opt` integration | Bridge general AI review → compiler oracles |
| Open-sourcing Magellan / AlphaEvolve compiler tasks | Offline heuristic synthesis reproducibility |
| KernelAgent + KernelBench CI templates | Standard kernel-agent regression |
| CompileIQ ACF artifacts in kernel repos | Trace/cache pattern for §4.3 |

Digests for newly added SCM sources are listed in [`../publications/INDEX.md`](../publications/INDEX.md) under group **Source control & review agents**.
