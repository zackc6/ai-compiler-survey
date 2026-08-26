# FlyDSL: Expert GPU Kernel Development with the Ease of MLIR Python Native DSL on AMD GPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | AMD ROCm blog |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://rocm.blogs.amd.com/software-tools-optimization/flydsl-python-native/README.html](https://rocm.blogs.amd.com/software-tools-optimization/flydsl-python-native/README.html) |
| **Evidence tier** | **B** — AMD Python+MLIR kernel DSL with CuTe-style layout algebra; GEAK already names it; not an agent product |

## Key contributions

- **FlyDSL** (Flexible Layout Python DSL): `@flyc.kernel` / `@flyc.jit` frontend + **Fly** MLIR dialect (layout algebra, coordinate mapping) → ROCDL → HSACO.
- Implements **CuTe-style** layout algebra (shape/stride/product/divide) for AMD (GMEM → LDS → VGPR; 64-thread wavefronts vs NVIDIA warps).
- Thread-level IR for expert tuning; aimed at Cutlass/CuTe migrants on Instinct.
- Code: [`ROCm/FlyDSL`](https://github.com/ROCm/FlyDSL). Named in [GEAK](geak.md) v3 multi-DSL and [KernelEvolve](kernelevolve-blog.md) (Triton / TLX / CuTe / FlyDSL).

## Summary

AMD’s vendor kernel IR launch — same miss class as TIRx/CuTe DSL. GEAK and KernelEvolve already treated FlyDSL as an agent *sink*; the survey had no digest of the language itself. Layout algebra puts FlyDSL closer to Argus/CuTe than to Cake (schedule IR, no layout algebra).

## Key takeaways

- **L4** AMD face (**C4**). Triton-only agents miss Instinct peak paths GEAK already searches.
- MLIR-native (Fly dialect) ≠ portable agent contract (T1 still per-stack).
- Not a new L-band; not LLM-as-`opt`.

## Why it matters for this survey

Tier B for **C4** / P7 multi-DSL. Cite with [GEAK](geak.md), [Argus](argus.md), [CuTe DSL](cute-dsl.md).

## Limits / caveats

- Launch blog + GitHub; blog updated 2026-03-30. No public FlyDSL agent-loop paper.
- Production inference claims ride GEAK/ROCm product blogs, not this DSL’s own A/B.
