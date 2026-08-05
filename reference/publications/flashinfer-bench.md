# FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Washington · Carnegie Mellon University · NVIDIA · UC Berkeley |
| **Publisher** | MLSys 2026 |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://proceedings.mlsys.org/paper_files/paper/2026/file/37e44c4b5321605735be9761f9b758fc-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2026/file/37e44c4b5321605735be9761f9b758fc-Paper-Conference.pdf) |
| **Evidence tier** | **A** — closes T6/T8 “exists” gap for serving-trace kernels with production `apply()` |

## Key contributions

- **FlashInfer Trace** JSON schema: Definition × Workload × Solution × Evaluation for agent↔system communication
- Curated dataset from real LLM serving traces (not synthetic uniform shapes)
- Correctness + performance benchmarking with isolation against reward hacking; low-bit / stochastic sampling support
- Public leaderboard for LLM/agent GPU programming
- **`apply()`** dynamic substitution into production engines (SGLang, vLLM) with near-zero overhead

## Summary

MLSys 2026 paper that treats AI-generated kernels as a **production integration problem**, not only a codegen scoreboard. Agents emit Solutions against Trace Definitions; workloads come from real serving traffic; winning kernels are swapped into FlashInfer-backed engines without rewriting SGLang/vLLM. Positions a closed loop: generate → measure on serving traces → deploy → improve agents.

## Key takeaways

- Moves the evaluation surface from single-kernel benches toward **serving-graph** workloads
- Schema + `apply()` are portable artifact contracts (adjacent to control-file / replay thinking)
- Still kernel-operator scoped (attention/GEMM/MoE/sampling families), not whole-program compile oracles

## Why it matters for this survey

Primary Tier A evidence for **§5.8 T6** (serving-level measurement + deploy path) and **T8** (ladder rung above KernelBench). Strengthens **C2** settlement pressure: public pinned traces with correctness×speed. Cite with [GitHub digest](flashinfer-bench-github.md). Complements CompileIQ ACFs (control files) with a **serving-kernel** substitution surface.

## Limits / caveats

- Does not yet provide multi-month default-path A/B attribution or GPU-race/FP contracts across whole graphs
- Ladder is still FlashInfer-operator-centric, not IR→kernel→fused→full-serve unified across compilers
