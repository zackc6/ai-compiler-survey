# Agentic Operator Generation for ML ASICs (TritorX)

| Field | Value |
|---|---|
| **Year** | 2025/2026 |
| **Org** | Meta |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://arxiv.org/abs/2512.10977](https://arxiv.org/abs/2512.10977) |
| **Evidence tier** | **A** — agentic PyTorch backend bring-up for custom ASICs (MTIA) + sim |

## Key contributions

- **TritorX**: FSM-orchestrated LLM loop (generate → lint → JIT → OpInfo test → debug) that writes Triton ATen kernels/wrappers for Meta **MTIA**.
- **Coverage-first** (not peak-perf): 481 unique ATen ops passing all corresponding OpInfo tests (20k+); ~84% pass rate; onboarded 80%+ of large first-/second-party models.
- Runs on **real silicon and QEMU simulation of future devices** — early HW/compiler feedback before tape-out.
- Deliberately avoids free-form tool-calling; FSM for production predictability. Learns HW quirks from compiler/crash feedback with mostly ATen docstrings (not full manuals).

## Summary

MLSys 2026 Meta paper arguing the bottleneck for new ASICs is *operator coverage*, not one more FlashAttention. Agents become the bring-up control plane of the PyTorch backend; the classical compiler/JIT/test harness remains the admit gate. Positions overnight backend generation as a practical limit case.

## Key takeaways

- **Fourth agent job emerges:** (d) *accelerator bring-up / codesign feedback* — distinct from online specialize, offline heuristic synthesis, and PR review.
- Coverage agents + later perf agents (KernelEvolve) are layered, not mutually exclusive.
- Simulation-loop agents give HW teams compiler-facing signal before silicon — codesign via the agentic compiler stack.
- Constrained FSM > open agents for production toolchain creation (**C3** flavor).

## Why it matters for this survey

Primary Tier A for **HW–SW codesign through an agentic compiler/toolchain**. Anchors §5.5 claim that next-gen agentic compilers shorten ASIC software TTM and feed ISA/IR design. Pair with [kernelevolve.md](kernelevolve.md) (perf on hetero fleet) and Ascend hierarchical diagnosis.

## Limits / caveats

- Performance tuning explicitly out of scope; coverage ≠ serving peak.
- MTIA/Triton-MTIA dialect specific; transfer assumes similar harnesses.
- OpInfo/unit coverage ≠ full serving graph correctness.
