# AutoKernel: Autonomous GPU Kernel Optimization via Iterative Agent-Driven Search

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | RightNow AI |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2603.21331](https://arxiv.org/abs/2603.21331) |
| **Evidence tier** | **A** — model-level Amdahl-driven agent loop + strong harness |

## Key contributions

- Open agent loop over **whole PyTorch models**: profile → Amdahl-rank bottlenecks → iterative Triton/CUDA refine.
- Five-stage correctness harness (smoke, shape sweep, adversarial numerics, determinism, edges) before recording speedups.
- Reports large wins vs eager and `torch.compile` max-autotune on H100 for RMSNorm/softmax/cross-entropy; KernelBench integration; OSS at RightNow-AI/autokernel.

## Summary

Pragmatic “expert keep/revert loop” mechanized for kernels. Less multi-agent ceremony, more overnight experiment throughput. Positions agents as online compilers for hot regions with classical validation.

## Key takeaways

- Amdahl allocation is a required control-plane policy for agentic compilers (don’t burn tokens on 5% kernels).
- Harness quality dominates architecture novelty.
- Still subject to **C2** (correct≠fast; fusion hard) — use with KernelBench-X.

## Why it matters for this survey

Tier A online-job (a) evidence and OSS reproducibility pointer for §5 / ROADMAP near-term.

## Limits / caveats

- Community leaderboard anecdotes are weaker than controlled suites.
- CUDA/Triton NVIDIA-centric vs hetero codesign papers.
