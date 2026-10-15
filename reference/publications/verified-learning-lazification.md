# Verified Learning for Compiler Optimization: An LLM-Guided Architecture with Formal Control

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Pennsylvania State University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [arXiv 2609.27214](https://arxiv.org/abs/2609.27214) |
| **Evidence tier** | **B** — restricted-action rewrite with an external equivalence checker; weak performance result |
| **Version / reviewed** | v1, 23 September 2026; reviewed 15 October 2026 |

## Key contributions

A code LLM fine-tuned on lazification transformations produced by Wyvern generates candidate LLVM IR rewrites; Alive2 symbolically validates each candidate, and rejected candidates are regenerated. Correctness is enforced as an external runtime control layer rather than learned.

## Summary

On a held-out LLVM test suite of 8,422 functions, no semantic violations were observed. Wyvern remains faster on most benchmarks; 9.8% achieve comparable or better runtime under the learned system. Mean runtime is 97.29% higher than Wyvern's, attributed to a subset of slow benchmarks; fine-tuning reduces mean runtime 2.5% versus the non-fine-tuned model. Verification averages 2.46 ms per step, modest relative to compilation time.

## Key takeaways

- The architecture pattern—generate, check with an equivalence tool, regenerate—works and is cheap per step; the learned proposer does not yet match the hand-written transformation it was trained on.

## Why it matters for this survey

A small, clean instance of the restricted-action design: hints or typed rewrites checked externally. It supports the claim that checking is tractable at this granularity and the caveat that checked does not mean better. Compare [LLM-VeriOpt](llm-veriopt.md) and [Souper](souper.md).

## Limits / caveats

- One transformation, one benchmark suite, no standard `-O3` comparison.
- Runtime results are dominated by a subset of slow cases; per-benchmark distributions are not fully reported.
