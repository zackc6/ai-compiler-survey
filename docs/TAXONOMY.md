# Taxonomy and stack layers

## Two meanings of “AI compiler”

| Sense | Meaning | Examples |
|---|---|---|
| **Compilers for AI** | Systems that lower neural graphs to accelerators | TVM, XLA/OpenXLA, MLIR dialects, TorchInductor→Triton, IREE, TensorRT |
| **AI for compilers** | LLMs/agents that choose passes, rewrite IR, write heuristics/kernels | Meta LLM Compiler, Compiler-R1, Magellan, GEAK, HintPilot |

This survey treats **next-gen** as their **merger**: agents on the control plane, compilers on the data plane.

## LLM role taxonomy (New Compiler Stack, 2026)

From *The New Compiler Stack: A Survey on the Synergy of LLMs and Compilers* (arXiv:2601.02045):

1. **Selector** — choose among predefined compiler actions or candidates (pass lists, schedule moves, CUDA template families).
2. **Translator** — rewrite source / IR / assembly (highest correctness risk unless gated).
3. **Generator** — synthesize new compiler artifacts (heuristics in C++, kernels, tools, datasets).

Most strong 2025–26 systems are **Selectors or Generators wrapped in hybrid validation**, not free-form Translators alone.

## Agent roles in the compile loop

| Role | Job | Examples |
|---|---|---|
| Advisor / Selector | Rank candidates, label regions, suggest passes | AgentCompile, Meta LLM Compiler, AutoPass |
| Translator / rewriter | Source/IR/asm rewrite or hint insertion | ACCLAIM, HintPilot, LLM-VeriOpt |
| Artifact Generator | Heuristics, kernels, MCP tools | Magellan, GEAK, mlirAgent |
| Orchestrator | Budget, IR level, stop conditions | ACCLAIM guide agent, GEAK directors |
| Tester / critic | Tests, Alive2, profiles, refine prompts | ACCLAIM test agent, Generative Compilation |
| Search partner | Propose nodes for MCTS / evolution | Reasoning Compiler, AlphaEvolve |
| Bring-up / codesign | Coverage→perf on sim+silicon; ISA/IR feedback | TritorX, KernelEvolve, Ascend diagnosis, KForge |

## Classical AI compiler stack (substrate)

```text
Framework capture     torch.compile / Dynamo, JAX, TF graphs
        ↓
Portable HLO          StableHLO (TF/JAX/PyTorch ↔ XLA/IREE)
        ↓
MLIR dialects         multi-level lowers, rewrites, vendor dialects
        ↓
Schedule / kernels    TVM MetaSchedule, Inductor→Triton, CUDA Tile IR, CUTLASS
        ↓
Serving runtime       vLLM, FlashAttention, CUDA Graphs, decode paths
        ↓
CPU / legacy IR       LLVM opt pipelines, PGO / AutoFDO, MLGO advisors
```

## Canonical hybrid loop

```text
Capture → Analyze regions → Agent proposes
        → Compiler checks & lowers
        → Verify / test (empirical or formal)
        → Benchmark / select
        → Feedback to orchestrator
        → Fallback if unprofitable
```

**Invariant:** LLM outputs guide search; they should not silently define unchecked executable behavior.
