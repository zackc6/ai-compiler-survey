# CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Toronto · Standard Kernel |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2604.01489](https://arxiv.org/abs/2604.01489) |
| **Evidence tier** | **A** — agentic kernel synth on CuTe (not Triton); delayed profiling; KernelBench eval |

## Key contributions

- Generate–test–refine agent loop that emits **CuTe** kernels rather than raw CUDA or Triton
- **Delayed profiling**: withhold Nsight-style metrics until structural correctness/baseline performance stabilizes, then refine
- On KernelBench L1+L2 (209 tasks): average **1.71×** vs PyTorch; beats CudaForge (**0.89×**) at comparable per-task cost; code at [github.com/taratt/cutegen](https://github.com/taratt/cutegen)

## Summary

CuTeGen argues that the agent training surface matters: CuTe exposes tiling/layout/data-movement structure while keeping low-level control (including inline PTX), making iterative refinement more stable than raw CUDA and more hardware-specific than Triton. The delayed-profiling schedule is an explicit anti-myopia design for agent loops—structure first, knob-tuning second.

## Key takeaways

- Multi-DSL agent skills are not optional (**C4**): Triton-family agents leave a CuTe/CUTLASS lane underexplored
- Profiling-as-reward too early can trap agents in tile-size local optima — relevant to §5.7 when-to-run / oracle design
- Still hybrid: compile + numerical checks + timed admit gate the loop

## Why it matters for this survey

★ for prediction: strengthens job **(a)** kernel agents and SURVEY §5.5 DSL surface / **C4** (Triton vs Tile/CuTe). Complements Helion+CompileIQ and KForge multi-DSL evidence. Prefer the arXiv primary; code link is companion.

## Limits / caveats

- Benchmark is KernelBench L1/L2, not full serving stacks or default Inductor path (gap **4.1**)
- Authors report 76/209 tasks beating PyTorch — not universal wins
- CudaForge comparison depends on matching generation budgets; treat headline 1.71× as author-reported
