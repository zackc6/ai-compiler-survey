# DRTriton: Large-Scale Synthetic Data Driven RL for Triton Kernel Generation

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Texas A&M University · Oracle |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2603.21465](https://arxiv.org/abs/2603.21465) |
| **Evidence tier** | **B** — synthetic corpus path for T7; KernelBench Level 2/3 claims |

## Key contributions

- **CSP-DAG**: constraint-satisfaction sampling of shape-valid PyTorch DAGs over operator vocabularies
- Curriculum RL with decoupled rewards (success vs speed) on ~100k synthetic programs after small SFT warmup
- Test-time search that decomposes multi-op programs into compositional kernels
- Reports strong KernelBench Level 2/3 speedup rates vs frontier chat models (paper claims; pin version when citing)

## Summary

Addresses KernelBook-scale scarcity by **synthesizing** PyTorch programs with controlled difficulty instead of only crawling GitHub. Shows synthetic-only RL can generalize to KernelBench fusion tasks. Important for the T7 “missing” cell: scalable generators, still not versioned MLIR/Tile/StableHLO with negative miscompile labels.

## Key takeaways

- Synthetic multi-op graphs are a viable T7 expansion path beyond Inductor dumps
- Curriculum + decoupled rewards matter under sparse compile/run rewards
- Does not ship a shared public corpus standard or serving ladder

## Why it matters for this survey

Updates **§5.8 T7** “what exists” with a synthetic multi-operator alternative to KernelBook. Complements [TritonRL](tritonrl.md) / [KernelBook](kernelbook.md). Keep headline % under **C2** caution.

## Limits / caveats

- Synthetic operator vocab ≠ real serving graphs; FlashInfer-Bench remains the serving-trace rung
- Negative data (miscompiles / slow-correct) still not a first-class public product
