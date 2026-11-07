# lean_kernel_verify: Lean-checked GPU kernel safety from compiler IR

| Field | Value |
|---|---|
| **Year** | 2026 (public repository observed in 2026-10-20 discovery ledger) |
| **Org** | Meta / Facebook Research |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Validation and approximate hardware |
| **Link** | [facebookresearch/lean_kernel_verify](https://github.com/facebookresearch/lean_kernel_verify) |
| **Evidence tier** | **B** — executable validation infrastructure for kernel generators, not a measured application gain or full mathematical equivalence |
| **Version / reviewed** | `README.md` GitHub content blob `f76519ffc7440520b034c39a056def8d79563543`, reviewed 5 November 2026; no pinned release evaluation |

## Key contributions

The lean_kernel_verify (LKV) prototype obtains the GPU compiler's actual intermediate representation (IR) from TLX/Triton or NVIDIA CuTe DSL (rather than trusting a manually transcribed kernel model), translates a supported subset to a small kernel IR (KIR), and checks concrete launch cases against Lean 4 propositions using `native_decide`. It examines address bounds and overflow, output coverage exactly once, participating role/barrier agreement, `mbarrier` protocol and a CuTe-specific tensor-memory ordering rule. The project exposes `PASS`, `FAIL`, `ERROR` and `UNDECIDED` per compiled variant, case input and specification.

## Summary

The project targets Blackwell `sm_100` CuTe DSL (including some two-cooperative-thread-array cases) and TLX/Triton `sm_100`/`sm_103`. Host code and compiler can produce IR on a CPU-only machine and the Lean layer can run without a GPU. The README gives an illustrative fixture where a floor-divided grid leaves tail outputs unwritten: for `N=100` and `N=40`, two concrete P0-3 violations are reported. This is a functionality test, **not** a measured bug-detection rate over production kernels.

## Key takeaways

- **Acceptance contract:** the proof is about a specific host-selected compiled variant, annotated concrete shapes/inputs, the extracted IR semantics and selected safety specs; **it is not a universal proof for arbitrary shapes or a floating-point/numerical equivalence check**. Independently measure numerical agreement and application performance.
- **Trust base:** relied-on compiler IR, translators/op tables, Lean evaluation and phase-ledger algorithm. The project states that the phase ledger for several rules is argued sound but not itself formally proved. A PASS does not guarantee the entire GPU's race/deadlock freedom or any operation below compiler IR.
- **Support envelope:** missing or unsupported IR operations cause refusals. TLX/Triton cross-CTA and two-CTA protocols, loop-carried pointer constructs and side-effecting inline assembly are not generally supported; some CuTe two-CTA cases are covered. Do not imply general CUDA C++ support.
- **Deployment cost:** no production false-positive/false-negative rate, total analysis-throughput benchmark, GPU-speedup result, model API budget or deployment cost is published in the reviewed README. The example's ~0.4–0.5-second per-fixture Lean checks are **not** representative corpus verification throughput.
- **Reproducibility caveat:** `lkv.py check` and Lean fixtures work from a standalone clone, but the documented end-to-end `lkv.py run` and `export` still depend on a Buck2 monorepo environment. Lean version 4.34.0; supported CuTe DSL versions listed as 4.4.2 and 4.6.1.

## Why it matters for this survey

An agentic compiler needs a trustworthy independent acceptance process, but a checker does not require an agent to operate. Use LKV as a candidate **safety checker arm**, complementary to [RESOLVE](resolve.md), [Measuring the Checker](measuring-the-checker.md) and mathematical equivalence approaches such as [VOLTA](volta-gpu-equivalence.md) (OOPSLA 2026) and Racer (arXiv 2610.28429, not yet digested). These are not equivalent contracts: bounded safety checks cannot replace numeric or application evaluation. A common checker can be used by either an agent or conventional search; consequently this evidence does not move the adaptive-agent thesis row or the 2027 tally.

**Proposed experiment:** stratify held-out TLX/CuTe kernels by shape, control flow, barriers and hardware; inject address, missing-write, barrier, race and numerical defects; compare LKV with differential fuzzing, sanitizer, a mathematical checker and full-runtime tests. Measure false accepts, false rejects, undecided outcomes, per-configuration overhead and total acceptance cost, and test the same checker on outputs of a conventional optimizer and an agent at matched budgets.

## Limits / caveats

The README documents interfaces and small fixtures, not a peer-reviewed precision/recall study or a field deployment. Verification is limited by the frontend coverage, hand-authored input/case contracts, the abstraction of compiler IR and the phase-ledger reasoning. It cannot establish a speedup or long-lived autonomous acceptance. The full text of VOLTA (whose repository and abstract are digested) and of Racer should be read before claiming that these tools solve the same problem.
