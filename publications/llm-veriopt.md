# LLM-VeriOpt: Verification-Guided RL for LLM-Based Compiler Optimization

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [https://2026.cgo.org/details/cgo-2026-papers/37/LLM-VeriOpt-Verification-Guided-Reinforcement-Learning-for-LLM-Based-Compiler-Optimi](https://2026.cgo.org/details/cgo-2026-papers/37/LLM-VeriOpt-Verification-Guided-Reinforcement-Learning-for-LLM-Based-Compiler-Optimi) |

## Key contributions

- Alive2 signals in GRPO rewards
- Small Qwen-3B trained as peephole optimizer
- ~90% verifiably correct; emergent opts beating instcombine in 20% cases

## Summary

CGO 2026 paper showing formal verification feedback can train small LLMs to perform correct LLVM IR peephole optimizations better than larger untuned models.

## Key takeaways

- Verification-in-the-loop is a major correctness path
- Small specialized models can beat large general ones
- Scope is local peephole, not whole-program

## Why it matters for this survey

This source informs the living survey in `docs/SURVEY.md` (trends, agent roles, process reshape, and/or gaps). Prefer the primary link above when citing.
