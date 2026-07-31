# Source-control & OSS evidence (tiered for next-gen prediction)

**Purpose:** Map GitHub / Gerrit / googlesource artifacts to the survey **prediction** (next-gen compiler + how agents change the future). This is **not** an exhaustive forge catalog.

Companion: [`SURVEY.md`](SURVEY.md) §5 · [`CONFLICTS.md`](CONFLICTS.md) · [`PRODUCTS.md`](PRODUCTS.md)

---

## Evidence tiers

| Tier | Meaning | Use in prediction |
|---|---|---|
| **A — Reshapes compile** | Agents change heuristics, kernels, knobs, or compiler review with domain oracles | Primary evidence for §5 |
| **B — Substrate** | Data-plane hosts agents must address | Required context; not “agent future” alone |
| **C — Delivery / HITL only** | Generic forge AI or tangential hosting | Demoted; cite only for conflict C7 |

---

## Tier A — agents reshape compilation

| Repository | Forge | Future role | Gaps / conflicts |
|---|---|---|---|
| [cuhk-s3/Archer](https://github.com/cuhk-s3/Archer) + [paper](https://arxiv.org/html/2607.01808) | GitHub | Compiler-oracle PR review (Alive2/LLUBI/`opt`) | §4.2, §4.8; conflict **C7** |
| [algorithmicsuperintelligence/openevolve](https://github.com/algorithmicsuperintelligence/openevolve) | GitHub | OSS AlphaEvolve-style loop (Magellan OSS path) | §4.1, **C1** |
| [cornell-zhang/heurigym](https://github.com/cornell-zhang/heurigym) | GitHub | Agentic heuristic bench incl. compiler tasks | §4.10 |
| [amazon-science/acclaim](https://github.com/amazon-science/acclaim) + [paper](https://arxiv.org/abs/2604.04238) | GitHub | Multi-level compiler↔LLM cooperation (online job a) | Q2/Q3; §5.4 |
| [ucb-bar/mlirAgent](https://github.com/ucb-bar/mlirAgent) | GitHub | MCP + fingerprints; **negative** free-IR-rewrite result | §4.5; **C3** |
| [Mind4Compiler/Compiler-R1](https://github.com/Mind4Compiler/Compiler-R1) | GitHub | Tool-using RL pass agent | Q2 |
| [ZJU-PL/hintpilot](https://github.com/ZJU-PL/hintpilot) | GitHub | Constrained hint/pragma synthesis | **C3** advisory path |
| [ScalingIntelligence/KernelBench](https://github.com/ScalingIntelligence/KernelBench) | GitHub | Kernel LLM benchmark | Trend D; **C2** |
| [BonnieW05/KernelBenchX](https://github.com/BonnieW05/KernelBenchX) (if public) / paper | GitHub | Correctness≠perf ceilings | **C2** |
| [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent) | GitHub | PyTorch→verified Triton agents | Trend D |
| [AMD-AGI/GEAK](https://github.com/AMD-AGI/GEAK) / [GEAK-agent](https://github.com/AMD-AGI/GEAK-agent) | GitHub | Vendor multi-agent kernel + serving opt | Trend D; **C2/C4** |
| [NVIDIA/CompileIQ](https://github.com/NVIDIA/CompileIQ) | GitHub | Evolutionary compiler Advanced Controls → ACF | §4.3; **C2/C5** |
| [anthropics/claudes-c-compiler](https://github.com/anthropics/claudes-c-compiler) | GitHub | Agents-as-compiler-engineers | Trend F; **C6** |
| [flagos-ai/awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) | GitHub | Living kernel-agent bibliography | Trend D watchlist |

**Magellan** itself remains mostly internal (paper + [LLVM Dev Meeting slides](../publications/magellan-llvm-slides.md)); track OSS via OpenEvolve + HeuriGym until a public Magellan tree appears (**C1**). Slides next-steps: OpenEvolve OSS path; XLA green-field / auto-sharding — folded into [`SURVEY.md`](SURVEY.md) §5.4.

---

## Tier B — substrate (data plane hosts)

| Repository | Why it matters for prediction |
|---|---|
| [llvm/llvm-project](https://github.com/llvm/llvm-project) | Host for MLGO, Magellan heuristics, Archer reviews |
| [google/ml-compiler-opt](https://github.com/google/ml-compiler-opt) | Neural advisor training stack (parallel bet to Magellan) |
| [facebookresearch/CompilerGym](https://github.com/facebookresearch/CompilerGym) | RL pass-order gym — substrate for Selector agents, not agent future alone |
| [triton-lang/triton](https://github.com/triton-lang/triton) | Default GPU DSL many agents target |
| [openxla/xla](https://github.com/openxla/xla) / StableHLO | Portable AI compiler IR; Magellan XLA experiments |
| PyTorch (`torch.compile` / Inductor) | Default DL compile path agents must plug into |
| [NVIDIA/TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) | Production serve stack; [PR #12831](https://github.com/NVIDIA/TensorRT-LLM/pull/12831) adds Claude kernel/compile agents (**C4**) |

---

## Tier C — demoted (delivery channel only)

These show demand to put LLMs **inside** code review UX. They are **not** next-gen compiler semantics unless wired to Alive2/`opt`/KernelBench-class oracles (conflict **C7**).

| Project | Link | Note |
|---|---|---|
| Gerrit `ai-code-review` | [googlesource](https://gerrit.googlesource.com/plugins/ai-code-review/) | Generic diff LLM |
| ReviewAI Gerrit plugin | [amarula/reviewai-gerrit-plugin](https://github.com/amarula/reviewai-gerrit-plugin) | Sidebar chat |
| GerritForge AI provider | [GerritForge/ai-review-agent-provider](https://github.com/GerritForge/ai-review-agent-provider) | Interface layer only |

**Open opportunity (still Tier A if built):** Gerrit/GitHub plugin that **calls compiler oracles** before commenting — Archer pattern on Gerrit.

---

## Implications for the predicted future

1. **SCM is part of the control plane** only when oracles are present (Archer), not when a chatbot comments on a diff (Tier C).
2. **Offline heuristic evolution** (OpenEvolve/Magellan) and **online knob/kernel agents** (CompileIQ/GEAK) are both Tier A — different jobs (**C5**).
3. **Negative results are Tier A too** — mlirAgent’s below-identity IR rewrite bounds the architecture (§5.1).
4. Prefer Tier A/B when enriching digests; do not grow Tier C catalogs.

Digests: [`../publications/INDEX.md`](../publications/INDEX.md).
