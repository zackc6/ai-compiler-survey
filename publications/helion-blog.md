# Helion: A High-Level DSL for Performant and Portable ML Kernels (PyTorch blog)

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Type** | company |
| **Group** | Classic DL compilers |
| **Link** | [https://pytorch.org/blog/helion/](https://pytorch.org/blog/helion/) |
| **Evidence tier** | **B** — substrate DSL agents and CompileIQ already target |

## Key contributions

- PyTorch-native “PyTorch with tiles” DSL compiling to **Triton** with implicit autotune search spaces.
- Reports geomean speedups over eager beating `torch.compile` max-autotune and many hand Triton kernels on B200 / MI350X.
- Positions Helion between PyTorch productivity and Triton/CUDA control; Linux Foundation contribution path noted in related pages.

## Summary

Raises the agent-addressable surface: one Helion kernel → thousands of Triton configs. CompileIQ product docs already list Helion as a first-class ACF target — stack convergence signal.

## Key takeaways

- Agentic compilers will specialize **Helion/Triton/Tile** configs, not only raw CUDA.
- Autotune-at-DSL-layer reduces need for free IR rewrite (**C3**).
- Portability claims matter for hetero codesign, still below TritorX/KernelEvolve ASIC story.

## Why it matters for this survey

Tier B substrate for § stack reshape and **C4** (DSL fragmentation vs Triton-family consolidation).

## Limits / caveats

- Autotune minutes/kernel; production needs pinned configs.
- Not itself an LLM agent — agents sit above it.
