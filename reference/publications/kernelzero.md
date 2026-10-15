# KernelZero: Co-Evolving Proposer and Coder for Continuously Improved GPU Kernel Generation

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Institute of Computing Technology, Chinese Academy of Sciences · University of Chinese Academy of Sciences · Institute of Software, CAS · Institute of AI for Industries, CAS |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [arXiv 2609.33074](https://arxiv.org/abs/2609.33074) |
| **Evidence tier** | **B** — offline model and curriculum improvement; correctness-dominated results on an older GPU |
| **Version / reviewed** | v1, 27 September 2026; reviewed 15 October 2026 |

## Key contributions

A 7-billion-parameter Coder writes CUDA or Triton kernels for PyTorch modules produced by a Proposer. The Proposer generates modules from API sets and targets the Coder's current weaknesses; the two are optimized in alternation (four rounds of 20 steps each), forming an automatic curriculum. Training uses Correctness-Aware Group Relative Policy Optimization, which optimizes performance only after correctness is reliable.

## Summary

KernelBench pass@1: CUDA 75.8% (Level 1) and 69.6% (Level 2); Triton 77.2% and 72.5%. Pass@10 for CUDA reaches 100% and 97%. The authors report the 7B model exceeding Claude 4.5 Sonnet on CUDA and DeepSeek-V4-Pro on Triton under their protocol. Speed is weaker: fast₁@1 (correct and faster than PyTorch in one sample) is 17.6% and 2.4% for CUDA, 43.9% and 65.4% for Triton; fast₁@10 for CUDA is 29% and 12%.

## Key takeaways

- Correctness gains are large; speed gains are modest for CUDA and better for Triton. The ablation shows RL moving one operator (tensor matrix multiplication) from 0.12× to 4.42×, with others at 1.09–1.25×.
- Compute: NVIDIA A100-80GB; one 20-step Proposer update about 3.1 hours on 12 GPUs, one Coder update about 4.5 hours on 8 GPUs; total GPU-hours and cold-start distillation compute not reported.

## Why it matters for this survey

A representative of the offline path—improve the code-generation model and its curriculum rather than the search loop. It belongs in the comparison of training resources, search resources, and attained speed, alongside [TritonRL](tritonrl.md) and [DRTriton](drtriton.md). It does not inform the controller or compiler-evolution questions.

## Limits / caveats

- A100 evaluation, so results do not speak to Hopper or Blackwell features; KernelBench baselines are eager PyTorch.
- Pass rates measure correctness under the benchmark's own checker (see [Measuring the Checker](measuring-the-checker.md)).
- No application-level evidence; comparisons with frontier models use the authors' protocol.
