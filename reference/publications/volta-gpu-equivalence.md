# Equivalence Checking of ML GPU Kernels (VOLTA)

| Field | Value |
|---|---|
| **Year** | 2026 (OOPSLA2; arXiv first posted November 2025) |
| **Org** | Stanford University · Microsoft Research India (arXiv v3 paper; Rahul Sharma is now at Google DeepMind, as the OOPSLA 2026 programme lists, but the work was performed at Microsoft Research) |
| **Publisher** | Proceedings of the ACM on Programming Languages, OOPSLA2 2026; arXiv; author source repository |
| **Type** | paper |
| **Group** | Validation and approximate hardware |
| **Link** | [OOPSLA paper](https://doi.org/10.1145/3839470) · [official code and evaluation](https://github.com/willtunnels/volta) · [arXiv 2511.12638](https://arxiv.org/abs/2511.12638) |
| **Evidence tier** | **A** — compiler-specific equivalence/race checker with formal guarantees in a declared semantics; not an application-speedup or agent-versus-non-agent comparison |
| **Version / reviewed** | OOPSLA 2026 author source README blob `a17361bba8ed87042db28c172badef988b3662e8` and results provenance `294a880ddec9add5ac7eed82cefef68569e905bd`; reviewed 5 November 2026. arXiv v3 dated 16 August 2026 (submission history v1 16 November 2025, v2 18 November 2025, v3 16 August 2026, checked on the arXiv abstract page 6 November 2026); the 12 and 14 August 2026 dates below are result runs, a different event; full 28-page paper not independently audited in this batch |

## Key contributions

VOLTA checks an original NVIDIA GPU kernel and an optimized kernel at **PTX** level. It symbolically executes each, detects supported data races/deadlocks and compares the resulting symbolic outputs. The comparison is **over real arithmetic**: floating-point inputs/operations are modeled as mathematical real numbers, not IEEE-754 rounding semantics. Its equivalence decision procedure covers polynomial and exponential expressions, including algebraic identities common in matrix multiplication, convolution and softmax/attention.

## Summary

The author's repository describes two phases: symbolic execution of all threads within **CTA 0**, with input and output footprints, then proof that all nominated output elements agree as expressions over the reals. The grid/block launch parameters are modeled, but the paper's comparison presumes structurally symmetric CTAs and the same corresponding per-CTA output footprint. The checker is **sound** under its supported abstract semantics and **complete only for a specified expression class**, including `+ - * / exp` rational-exponential forms and selected `max/min` patterns. Other operations can be uninterpreted atoms, preserving soundness without guaranteeing completeness. A failed/unsupported/unknown proof is not positive evidence of equivalence.

## Key takeaways

- **Supported scope:** CUDA/CUTLASS lowered to PTX with statically resolvable tensor extents, memory addresses and branch targets under a structured-CTA launch; `syncthreads`, `syncwarp` and selected implicit tensor-core barriers are modeled. `arrive` and `wgmma` asynchronous primitives are **not supported**. Cross-CTA interaction and transformations that change the CTA-to-CTA output footprint fall outside its guarantee.
- **Numerical contract:** a proof over the reals is *not* a proof of exact bitwise floating-point equivalence, stable error tolerance, deterministic reduction order or model-level quality. It can prove a correct mathematical rearrangement that changes actual rounding. Apply declared numerical/statistical tests and real GPU execution separately.
- **Paper-evaluation workload and cost:** official `volta-bench` describes **39 benchmark cases**, across reductions, matrix multiplication, convolution, attention, agent-generated kernels, TileLang, and race checks. It records separate VC generation and solving, default **10 iterations** per timed phase with median and coefficient of variation. The archived full run is dated **12 August 2026** on a **128-core 2.25 GHz AMD EPYC 7742** machine with **995 GB RAM** and Z3 **4.8.12**. A 14 August correction remeasured three racy reduction cases after recompiling with a matched 128-thread block size. These are the authors' reported reproducibility conditions; this survey has not rerun them.
- **Baseline:** the source provides Z3 as an alternative solver on the same verification conditions, with a **10-minute per-query** timeout for the paper's sampled exponential cases. The no-axiom exponential encoding may produce `unknown`, while adding an exponent axiom may run until timeout. These are **verifier capability and cost** comparisons, **not** GPU kernel/runtime speedups.
- **Resource caveat:** full-footprint attention verification can consume tens of GiB of memory and may need a large-memory server. `--sample 1` reduces verifier cost by checking only one output per array — this is a different *coverage denominator* from checking all outputs. Do not confuse a fast single-element proof with full coverage.

## Why it matters for this survey

Together with [lean_kernel_verify](lean-kernel-verify.md), [RESOLVE](resolve.md), and [Measuring the Checker](measuring-the-checker.md), VOLTA provides a substantive **non-agent checker** for agent-generated or conventionally generated compiler artifacts. It addresses mathematical equivalence under a chosen formalization, whereas lean_kernel_verify addresses concrete-case safety properties and RESOLVE combines testing, reduction and selected proof. Their guarantees and denominators differ: no one tool establishes safety, exact floating-point fidelity, model quality and application performance at once. A checker can be shared between a deterministic tuner and an agent, so VOLTA does not support claiming autonomous agent reasoning wins or a qualifying 2027 agent integration.

**Proposed experiment:** freeze an identical set of handwritten, learned/search and agent-generated PTX kernels; inject races, boundary errors, precision-sensitive near-ties, and CTA shape changes. Compare real and IEEE acceptance, lean_kernel_verify, VOLTA, RESOLVE, differential/fuzz testing, verifier runtime/memory and the UNKNOWN/unsupported rates at multiple input shapes. Record whether a generator's apparent speedup survives all acceptance layers. A proof-level pass is not application performance.

## Limits / caveats

The primary repository README and raw-result provenance were verified; the paper's tables and exact per-case pass rates have not yet been independently rechecked. The formal guarantee is in an abstract arithmetic model with static addresses/structured CTA restrictions; some newer Blackwell asynchronous operations are out of scope. Hardware implementation behavior below PTX is not proven. Treat incompatible cases as **UNKNOWN / unproved**, not as safe, and do not convert an inconclusive proof automatically into either success or a correctness failure.
