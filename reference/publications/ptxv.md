# ptxv: a binary-level verifier for Blackwell GPU kernels — execution checking over hardware schedules, proven per-output numerical bounds, and error distributions

| Field | Value |
|---|---|
| **Year** | 2026 (first public release v0.1.0; repository surfaced in the 15 November discovery ledger as new in `meta-pytorch`, pushed 5–12 November) |
| **Org** | Meta (PyTorch; the `meta-pytorch` GitHub organization; `lean_model/NOTICE.md` credits Bram Wasti's ptxv snapshot for the FP32 math-unit reconstruction) |
| **Publisher** | GitHub repository (README, `ASSUMPTIONS.md`, `BUGS.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/`) |
| **Type** | code |
| **Group** | Validation and approximate hardware |
| **Link** | [meta-pytorch/ptxv](https://github.com/meta-pytorch/ptxv) |
| **Evidence tier** | **A** — acceptance machinery that adds two layers this guide's validation contract asks for and no indexed tool provided together: schedule-exhaustive execution checking on the compiled binary, and a numerical verdict that is both a proven worst-case bound and an error *distribution* under a declared input distribution. Tier is decision relevance; it reports no detection rate over a generator's real output and no optimization result |
| **Version / reviewed** | Repository head `70143db9f205654ffebb4f3129bf3806eaf478ae` (12 November 2026), read by shallow clone on 16 November 2026. BSD licence. `CHANGELOG.md` lists v0.1.0 as the first public release (CLI, Python front end, Lean models of GB300 instructions, target specifications) with CI and headers unreleased. |

## Key contributions

ptxv takes the PTX or, preferably, the SASS of a *captured launch* (from PyTorch, Triton or CuTeDSL via `ptxv.capture()`) of an NVIDIA Blackwell kernel (sm_100a / sm_103a) and checks it in two steps.

1. **Execution.** The binary is lifted into one intermediate representation, including the SASS scoreboard and dependency-barrier bits. A simulator holds every warp, asynchronous unit (TMA, `tcgen05`, remote stores) and barrier as explicit state; an explorer with partial-order reductions visits the schedules the hardware may pick; vector clocks track the PTX memory model's happens-before relation (barriers, mbarrier phases, release/acquire with scopes, proxy fences, async completions). Two conflicting accesses left unordered, and not both morally strong, are a race; a state from which nothing can move before all threads exit is a deadlock. When every barrier phase, wait and value is determined, a certificate (E-WELLSYNC) shows that one run decides all schedules and replaces the search. Each finding carries the schedule that reaches it, replayable step by step. The result also says whether every schedule computes each output with the same operations, or which variants can occur (floating-point atomics, for example).
2. **Numerics.** Because step 1 fixed which operations produce each output on every schedule, the numerics DAG of one execution is the kernel's dataflow on every schedule: leaves are input elements, nodes are tensor-core steps, adds, fused multiply-adds and roundings, each with a model of its arithmetic (tensor-core models calibrated on GB300). `compare` proves equivalence of a candidate to a reference kernel with a per-output bound ("PROVEN L1 (same function) for every input, |C − R| ≤ … × Σ|terms|"). `errdist` evaluates the DAG under an input distribution: Tier 0 proves zero error when every rounding is exact on the inputs' lattice; Tier 2 propagates per-node rounding laws with a central-limit model, reported when its applicability checks pass and Tier 3 (bit-exact Monte Carlo through the DAG) agrees; otherwise Tier 3.

The README's worked example, cuBLAS against a Triton bf16 GEMM that sums K in reverse order, inputs N(0, 1): "P(bits differ) = 3.829e-5 (tier 3: 3.499e-5 [2.533e-5, 4.714e-5]); error in output ulps: median 0, 99% within 0, 99.9% within 0, largest seen in tier 3: 4; worst case (proven): |C − R| ≤ 2 bf16 ulps of the exact result + 3.56e-6 × Σ|a_k·b_k| + 9.2e-41". Low-precision formats (fp8, fp4, MX, NVFP4) are documented.

## Summary

**What rests on what.** `ASSUMPTIONS.md` is "the single registry" of everything a verdict relies on: each assumption has an identifier, a status (**enforced** — violating inputs give `unmodeled`, never a silent answer; **validated** against GB300 or a cross-check; **argued**; **refuted** — tested false on GB300, kept opt-in only to reproduce old verdicts; **unvalidated**), and an "if wrong" direction (a *miss* could call a buggy kernel clean; a *false alarm* could report an impossible bug). `cargo test` fails if the file, the code registry and the code tags disagree; every `ptxv check` output lists the identifiers it depends on. Unknown SASS opcodes are a hard error; an unmodeled operation or value gives an `unmodeled` finding that makes the verdict inconclusive. The README's trust statement: the instruction semantics, memory model and arithmetic units "are encoded by hand and validated against GB300 hardware; they are not a formal specification"; an audit so that unsupported *modifiers* are rejected rather than ignored "is in progress".

**Bug suite.** `BUGS.md` holds 87 (correct kernel, mutant) pairs — fixture PTX mutants, recompiled PTX mutants of JIT kernels, and SASS-patched mutants of binary-only kernels (torch, trtllm-gen, DeepEP) — each with the property that must fire and "an honest note on how the bug behaves on real hardware" over 10⁴ runs. Examples: an `expect_tx` byte-count mutant deadlocks every time on GB300; a wrong-parity first-phase wait is "1/10k wrong on GB300 (stale smem from the previous launch hides it), 10k/10k with smem scrubbed". The stated usefulness metric is the detection rate over this suite together with how often hardware reproduces each bug on its own versus under witness replay.

**Design decisions (ROADMAP, 30 October 2026).** Binary first, one IR: verification runs on the SASS lift whenever a cubin exists "because that is what executes"; when PTX also exists both are verified and verdicts must agree (a disagreement is a lifter or `ptxas` bug). No source inspection, ever. Exhaustive at the captured grid by default, with decomposition; a shrunk grid is a fallback that must pass a coverage-equivalence check. Blackwell only, on GB300s; verification itself is CPU-only. The evidence for binary-first: every real shipped kernel on the authors' machine is SASS-only (torch 2.12 `libtorch_cuda.so`: 445 sm_100a + 445 sm_103a ELFs, 0 PTX; DeepEP 0 PTX; FlashInfer's 7,564 prebuilt trtllm-gen cubins).

**Cost.** Checking needs no GPU; capture and hardware validation need a Blackwell GPU. The quick test tier ran in about 6 minutes (342 s after the build) on a 144-core machine; the full tier is about 6 hours of test time.

## Key takeaways

- **Verdict granularity.** A verdict holds for the captured inputs and launch shape, and equivalence is to a *reference kernel*, not a specification; the README's own comparison table rates these as ptxv's open gaps, and says not every proof rule has an adversarial test.
- **Two numerical outputs, not one.** A proven worst-case bound (over the reals with modeled rounding) *and* a distribution of the error under a declared input distribution, with probability that any output bit differs. This is the shape of the statistical acceptance contract this guide describes in §4.2, produced by a tool rather than by sampling alone.
- **Execution checking is on the compiled object**, including Blackwell asynchronous machinery (TMA, `tcgen05`, mbarrier phases, clusters, multi-GPU memory), which the IR-level checker [lean_kernel_verify](lean-kernel-verify.md) and the PTX-level [VOLTA](volta-gpu-equivalence.md) do not cover.
- **No detection rate over real generated kernels is reported**: the 87-pair suite is author-written mutants of fixtures and shipped kernels, not a sample of an agent's output; the roadmap's metric is defined but no aggregate figure is in the README.
- **Refuted assumptions are kept visible** (opt-in, listed in `assumes:`), and an `unmodeled` finding is inconclusive rather than PASS — the behaviour §4.2 asks for ("UNDECIDED is UNKNOWN, never PASS").

## Why it matters for this survey

For the §4.2 acceptance sequence, ptxv is the first indexed tool that supplies, on the compiled binary, both a schedule-exhaustive safety verdict and a numerical verdict with a proven bound *and* a distribution. It belongs beside [VOLTA](volta-gpu-equivalence.md) (PTX-level equivalence over the reals for CTA 0 and nominated outputs), [RESOLVE](resolve.md) (tolerance test → bitwise reduction → proof over the reals, at hours and millions of tokens per kernel) and [lean_kernel_verify](lean-kernel-verify.md) (IR-level concrete-case safety). Its design answers the "assumptions matter" caveat in the invariant-and-equivalence row of the validation table with an explicit, test-enforced registry, which is a pattern worth requiring of any checker used to accept agent-generated kernels.

For the thesis it moves no row: it is acceptance machinery usable by agent and non-agent arms alike. Its practical effect is on the wider-synthesis question (§6): a cheaper, CPU-only proof-level check on the binary lowers the cost that [RESOLVE](resolve.md) measured for proof-level acceptance, and the error-distribution tier gives a contract for kernels that are *not* equivalent but are acceptable (reordered reductions, low-precision formats). Whether it is cheap enough to sit inside a search loop is not reported.

Lineage: Meta/PyTorch; same organization as [lean_kernel_verify](lean-kernel-verify.md) and [LLVM GPU Backend Benchmarks](llvm-gpu-backend-benchmarks.md) (one Meta validation family); the Lean models of GB300 instructions (`lean_model/`, including a MUFU audit) may share lineage with *SFU-Sim* (arXiv, 10 November 2026, PENDING in the ledger). Not to be confused with `francois141/ptx_verifier` (the "Volta" analyzer repository) or with PTX Gym.

**Experiment:** run ptxv's `check`, `compare` and `errdist` over the accepted candidates of a published agent speedup study (KernelBench-Verified's or RESOLVE's 100 checker-passing kernels on Blackwell) and report the verified-only speedup, the `unmodeled` rate, wall-clock per kernel, and agreement with RESOLVE's verdicts where both apply.

## Limits / caveats

- Blackwell (sm_100a / sm_103a) only; validated on GB300; no Hopper, AMD or other targets.
- Semantics are hand-encoded and validated by probes, not derived from a vendor specification; the assumptions registry is the honesty mechanism, not a proof of soundness. The unsupported-modifier audit is incomplete.
- Verdicts are per captured launch (inputs and grid); a shape-general claim is out of scope.
- No published aggregate detection rate, no evaluation on agent-generated kernels, and no per-kernel wall-clock figures for checking.
- First public release (v0.1.0); `BUGS.md` and `ROADMAP.md` list open gaps (multicast/NVLS, multi-node) that the README does not claim.
