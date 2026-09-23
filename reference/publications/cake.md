# CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA · Carnegie Mellon University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Version 1](https://arxiv.org/abs/2608.12629v1) |
| **Evidence tier** | **A** — agent-facing representation and evolving compiler feedback |

## Key contributions

CAKE exposes schedules and hardware decisions through a typed representation. Its compiler and evaluation harness localize failures; recurring limitations can motivate changes to representations, checks, and tools.

## Summary

Agents and compiler infrastructure are developed together. The representation is translated into CUDA/PTX code and then machine code; CUDA source is not itself an instruction set.

## Key takeaways

For one B200 Flash-KMeans shape at 80 million tokens, three runs per environment yield median best speedups of 1.144 for CAKE and 0.928 for direct CUDA/PTX, relative to tuned FlashML. Their ranges overlap.

## Why it matters for this survey

Compare complete programming environments and test compiler co-evolution. This experiment does not isolate the representation’s effect from feedback and tooling.

## Limits / caveats

The reported 2.05-times geometric-mean Kimi Delta Attention gain is a kernel result across six B200 shapes, with separate SGLang application validation. It is not a 2.05-times application speedup. Results are author evaluations with large search budgets; broader transfer remains open.
