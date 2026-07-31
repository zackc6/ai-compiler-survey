# AgentCompile: An LLM-Guided Compiler for Direct CUDA Inference

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/html/2606.07665](https://arxiv.org/html/2606.07665) |

## Key contributions

- LLM advisory metadata only
- Compiler-defined bounded CUDA candidate spaces
- End-to-end speedups vs PyTorch eager on small LLMs

## Summary

Hybrid inference compiler where the LLM prioritizes candidates but templates, checks, validation, and fallback remain compiler-controlled.

## Key takeaways

- Textbook hybrid architecture
- Separates guidance claims from kernel/runtime effects

## Why it matters for this survey

This source informs the living survey in `docs/SURVEY.md` (trends, agent roles, process reshape, and/or gaps). Prefer the primary link above when citing.
