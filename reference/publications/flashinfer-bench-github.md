# flashinfer-ai/flashinfer-bench

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | FlashInfer / NVIDIA · UW · CMU collaborators |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://github.com/flashinfer-ai/flashinfer-bench](https://github.com/flashinfer-ai/flashinfer-bench) |
| **Evidence tier** | **A** — shipping benchmark + Trace dataset + apply workflow |

## Key contributions

- Open Python package + docs for FlashInfer-Bench evaluation
- Hugging Face FlashInfer-Trace / contest datasets
- Integration path used by MLSys 2026 AI Kernel Generation Contest (starter kit, B200 tracks)

## Summary

OSS home for the FlashInfer-Bench virtuous cycle: Trace schema, dataset hooks, leaderboard/evaluation, and production `apply()` substitution into FlashInfer consumers (SGLang/vLLM lineage). Contest starter kit (`flashinfer-bench-starter-kit`) shows agent baselines (e.g. OpenEvolve) writing Triton/CUDA against fused MoE, sparse attention, gated delta-net tracks.

## Key takeaways

- Concrete open ladder rung for serving kernels with a deploy hook
- Agent contest surface makes agent skill comparable under fixed HW

## Why it matters for this survey

Code companion to [FlashInfer-Bench paper](flashinfer-bench.md). Tier A repo for **T6/T8** and **C2**. Add to [`repos.md`](../repos.md) Tier A.

## Limits / caveats

- Contest/tracks evolve; pin Trace schema + HW when citing numbers
- Not a substitute for Alive2-class formal oracles on LLVM IR
