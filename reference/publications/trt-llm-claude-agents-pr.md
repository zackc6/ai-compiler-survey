# TensorRT-LLM PR: Claude agents/skills for kernels and compile

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA |
| **Publisher** | GitHub (TensorRT-LLM) |
| **Type** | code |
| **Group** | Commercial products & proposals |
| **Link** | [https://github.com/NVIDIA/TensorRT-LLM/pull/12831](https://github.com/NVIDIA/TensorRT-LLM/pull/12831) |

## Key contributions

- Specialized agents for CUDA, Triton, CuTe, TileIR kernels
- Skills for Nsight profiling and TRT-LLM compilation (local/SLURM)
- Agents embedded in a production inference compiler repo

## Summary

Evidence that a flagship commercial LLM inference stack is wiring coding agents into kernel/compile workflows—multi-DSL agent surface inside TensorRT-LLM.

## Key takeaways

- Conflict C4: multi-DSL (not Triton-only) agent skills
- Bridges DataPlane-Serve SKU with ControlPlane-Agent tooling

## Why it matters for this survey

Evidence for next-gen prediction and [`docs/SURVEY.md`](../../docs/SURVEY.md) §6. Prefer the primary link when citing.
