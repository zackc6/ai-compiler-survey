# TritonRL: Training LLMs to Think and Code Triton Without Cheating

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Amazon · multi-institution |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2510.17891](https://arxiv.org/abs/2510.17891) |
| **Evidence tier** | **B** — strong T7/T2-adjacent RL recipe; KernelBench-scoped |

## Key contributions

- 8B Triton specialist trained from KernelBook + DeepSeek-R1 distilled reasoning traces
- Multi-layer verifiers against Triton reward hacking (rule + LLM judges)
- Hierarchical Reward Decomposition (HRD): separate credit for planning vs implementation
- KernelBench SOTA among Triton-specialist models; competitive with much larger frontiers

## Summary

Shows that open KernelBook-scale data plus anti-cheat verification and structured RL rewards can produce small Triton generators that rival large general models on KernelBench. Complements KernelLLM (SFT) with RL and explicit anti-hacking machinery — a preview of money-grade local oracles for kernel admit.

## Key takeaways

- Reward hacking is a first-class compiler-data problem, not a footnote
- Verifiers ≈ nascent T2 admit gates for Triton generation
- Still single-kernel bench; not serving-trace or multi-IR

## Why it matters for this survey

Evidence for **§5.8 T7** (open Triton corpora usage) and **T2/T6** (verification before reward). Cite with [KernelBook](kernelbook.md). Does not settle **C2** distributional serving wins.

## Limits / caveats

- Affiliation string is author-inferred (Amazon-linked coauthors); treat as research paper not AWS SKU
- Open-source recipe claim should be checked against release artifacts when citing reproducibility
