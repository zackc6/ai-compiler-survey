# AsmEvo: Agentic Assembly-Level Optimization of AMD GPU Kernels with Functional Equivalence Verification

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2608.20711](https://arxiv.org/abs/2608.20711) |
| **Evidence tier** | **A** — post-compile AMDGPU edits; the original binary is the oracle |

## Key contributions

- Optimizes an **already compiled** AMDGPU code object. There is often no editable CUDA/Triton/HIP source and no separate reference implementation: \(K_0\) is both the deployed artifact and the behavioral oracle.
- Pipeline: recover a reassemblable form, expose profiled hot windows to a long-horizon agent, rebuild an **ABI-preserving** object, accept only after **differential checks** under the same launches. In-place patch is the conservative fallback.
- MI308X: **29/30** selected KernelBench kernels improve, **1.35×** geomean, **3.88×** max (author). MI300X production: all evaluated AITer binaries and vLLM/SGLang Triton assembly kernels improve, about **1.09× / 1.31×** and **1.18× / 1.34×** geomean/max. Posted 2026-08-21.

## Summary

Most kernel agents edit source and hope the compiler’s lowering is the performance ceiling. AsmEvo starts where that lowering stopped. The agent proposes assembly edits; a classical rebuild preserves the launcher ABI; functional equivalence against the original binary gates timing. Fast-but-wrong candidates never enter the speedup table. That is still hybrid: the agent does not become `opt` or the assembler.

## Key takeaways

- **T2** exists-cell: admit at the **code-object** boundary, not only at Triton parse / Alive2 peephole. The oracle is differential testing, not a full ISA formal semantics.
- New edit surface **below** L4 source DSLs. It does not add an L-band and does not license free SASS/AMDGCN rewrite without the diff gate (**C3-B**).
- Missed in the 2026-08-31 skill-scope fold (title is assembly, not “LLM + IR”). Same class of miss as TIRx.
- **C9** not moved. Small geomeans on production binaries are residual-peak search, not operator coverage.

## Why it matters for this survey

★ for **T2** (binary-diff admit) and for where job (a) is allowed to write. Pair with [Argus](argus.md) (compile-time SMT *before* codegen) — AsmEvo admits *after* codegen, against the shipped object. Both keep a checker outside the model.

## Limits / caveats

- Equivalence is differential under the tested launches, not a proof for all inputs.
- AMDGPU only. Recovery quality bounds what the agent can see.
- Author-selected KernelBench subset (30) and unnamed “all evaluated” production binaries — not a public p50 (**C2**).
