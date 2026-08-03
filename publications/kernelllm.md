# Meta KernelLLM (Hugging Face)

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Meta |
| **Publisher** | Hugging Face |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://huggingface.co/facebook/KernelLLM](https://huggingface.co/facebook/KernelLLM) |

## Key contributions

- 8B Llama fine-tuned for PyTorch鈫扵riton
- Trained on paired torch/triton data
- Competitive Pass@k on KernelBench-Triton

## Summary

Specialized small model demonstrating that domain-focused fine-tunes can rival much larger general LLMs on Triton kernel generation.

## Key takeaways

- Specialization > scale for narrow compiler DSLs
- Complements Meta LLM Compiler (IR) with Triton focus

## Why it matters for this survey

This source informs the living survey in `docs/SURVEY.md` (trends, agent roles, process reshape, and/or gaps). Prefer the primary link above when citing.
