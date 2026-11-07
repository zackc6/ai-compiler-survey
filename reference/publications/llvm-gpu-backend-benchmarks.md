# LLVM GPU Backend Benchmarks: reproducible kernel code-generation comparisons

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Meta / Facebook Experimental |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Validation and approximate hardware |
| **Link** | [facebookexperimental/llvm_gpu_backend_benchmarks](https://github.com/facebookexperimental/llvm_gpu_backend_benchmarks) |
| **Evidence tier** | **B** — backend-evaluation harness rather than a published agent-versus-non-agent outcome |
| **Version / reviewed** | `README.md` content blob `0999d4e3c53b0d05e306b60aac484d01669d5c97`, reviewed 5 November 2026 |

## Key contributions

This repository collects reproducible GPU kernel and IR cases for evaluating LLVM AMDGPU and NVPTX backends. Cases are intended to hold kernel sources, input shapes, expected results, compiler/build settings and a measurement driver fixed when comparing alternative code-generation, scheduling and register-allocation revisions.

## Summary

The README describes Linux, a GPU-capable LLVM toolchain and a Python 3.10+ harness. Workloads are case-specific; their subdirectories own build flags and checks. The README describes self-contained drivers, correctness checks and performance counters but **does not report an aggregate suite size, platform-by-platform throughput table, variance estimate, budget or agent comparison**. Those are missing research fields, not assumed zeros. The repository description reads "Tracking for LLVM outputs produced by various GPU kernel DSLs", and its `tools/` scripts export saved LLVM IR from the Triton AMD backend (MI350X, `gfx950`); the cases are therefore DSL-produced IR rather than hand-written kernels.

## Key takeaways

- **Denominator:** compiler backend output and individual GPU kernel performance, not end-to-end model/training throughput. This is potentially a useful controlled kernel benchmark, not a qualifying 2027 application result.
- **Baseline:** best use is comparison of LLVM revisions or codegen decisions on the same kernel, shape, hardware and measurement protocol. The README does not supply a published fixed baseline or numerical improvement.
- **Correctness and trust:** per-case expected outputs can detect tested incorrect results but do not prove universal semantic equivalence. Any compiler-generated optimization needs additional randomized/held-out inputs and relevant numerical rules.
- **Cost:** GPU time, build complexity, suite completeness and reproducibility across toolchains are not quantified in the reviewed README; those must be measured before interpreting an agentic workflow's efficiency.

## Why it matters for this survey

Separating backend changes from optimizer-choice changes is necessary to test whether agent decisions truly improve the compiler. This harness is a potential dataset/measurement arm complementary to [LLVM-Bench](llvm-bench.md) (issue-level engineering) and [CIRBench](cirbench.md) (single-shot LLVM IR rewrites), not a replication of either. Compare fixed LLVM backend revisions, hand-written lowering, automated tuning and an agent while holding input IR, code-generation target, tests and search budgets constant.

**Proposed experiment:** construct a frozen benchmark manifest with exact LLVM commits, AMDGPU and NVPTX targets, kernels/shapes, seed set, expected outputs, acceptance tolerances and per-revision runtime distributions. Compare an agent-changed backend with a rule-based/learned search, and test accepted changes on withheld kernels and the next release.

## Limits / caveats

No independent run or full inspection of the per-benchmark subdirectories was performed for this survey batch; only the repository's README was verified. Until those details and results are inspected, classify this as evaluation infrastructure, not evidence of measured benefit or target portability.
