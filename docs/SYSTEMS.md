# System comparison

Snapshot of representative systems. Numbers are **as reported by authors**; cross-benchmark comparison is not apples-to-apples. Prefer mechanisms over headline speedups when choosing architecture.

| System | Layer | Agent shape | Correctness gate | Headline | Venue / source |
|---|---|---|---|---|---|
| Meta LLM Compiler | LLVM IR / asm | Foundation model | Compiler applies passes | ~77% of autotune size potential | CC 2025 |
| Compiler-R1 | LLVM pass order | Single agent + tools + RL | opt + IR instr count | ~8.5% IR size vs -Oz avg | NeurIPS 2025 |
| LLM-VeriOpt | LLVM IR peephole | Trained small model | Alive2 equivalence | ~90% verifiably correct | CGO 2026 |
| Magellan | Heuristics (C++) | Coding agent + AlphaEvolve | Compile + macro-benches | Beats decades of inlining heuristics | C4ML@CGO’26 / LLVM DevMtg |
| AwareCompiler | Pass sequences | Multi-turn agent–env | Compile/run rewards | Knowledge bridges features↔passes | arXiv 2025 |
| AutoPass | Pass / flags | Multi-agent, inference-only | Compile + profile evidence | Practical budgets, no offline RL | arXiv 2026 |
| HintPilot | Source pragmas | Iterative RAG refine | Compiler validates hints + tests | Up to 6.88× geo-mean vs -Ofast | ACL Findings 2026 |
| ACCLAIM | C / asm multi-level | Guide + level + test agents | LLM tests + compile | Up to 1.25× over compilers alone | arXiv 2026 |
| Reasoning Compiler | TVM schedules | LLM proposals + MCTS | TVM compile/measure | Sample-efficient vs MetaSchedule | NeurIPS 2025 |
| AgentCompile | CUDA inference | Advisor in bounded search | Template CUDA + checks + bench | ~4–5.7× vs eager (small LLMs) | arXiv 2026 |
| GEAK | Triton / AMD GPU | Gen/eval/reflect/optim | Unit tests + timing | Up to 63% exec acc; ~2.59× | AMD / arXiv 2025 |
| KernelLLM | PyTorch→Triton | Specialized 8B model | KernelBench-Triton | Strong Pass@k vs larger general LLMs | Meta HF 2025 |
| mlirAgent | MLIR / LLVM | Tool-using agents (MCP) | Pass tracking + benches | LLMs weak at direct IR rewrite | UCB BAR |
| Generative Compilation | Rust frontend | In-decoding feedback | Sealor + rustc | Compiler active during generation | arXiv 2026 |
| Compiler.next | FMware / intent | SE 3.0 vision | Multi-objective quality gates | Compile prompts/agents/params | arXiv 2025 |
| NVIDIA CompileIQ | NVCC/PTXAS knobs | Evolutionary search | Measure on real kernels | ≤15% on hot Triton/CUTLASS kernels | CUDA 13.3 blogs |
| MLGO | LLVM heuristics | RL policies in-tree | Compiler semantics | Prod inlining/regalloc | Google / LLVM |
| KernelBench | Eval harness | N/A (benchmark) | Correct + fast_p | Frontier <20% one-shot typical | ICML 2025 |

## Online vs offline agents

| Mode | When it runs | Typical artifact | Examples |
|---|---|---|---|
| **Online** | At compile / specialize time for a program or model | Pass list, hints, kernel choice, ACF knobs | HintPilot, AgentCompile, CompileIQ, Compiler-R1 inference |
| **Offline** | Compiler engineering / model training | C++ heuristics, foundation weights, datasets | Magellan, Meta LLM Compiler training, MLGO training |

## Related engineering experiments (adjacent)

| Work | Why it matters to this survey |
|---|---|
| Anthropic Claude C Compiler | Agents as *compiler writers*; harness + tests dominate |
| LLVM agent PR review Discourse thread | Compiler-specific tools >> generic SWE agents for opt review |
