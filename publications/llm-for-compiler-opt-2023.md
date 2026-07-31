# Large Language Models for Compiler Optimization

| Field | Value |
|---|---|
| **Year** | 2023 |
| **Type** | paper |
| **Group** | Foundation LLMs for compilers |
| **Link** | [https://arxiv.org/abs/2309.07062](https://arxiv.org/abs/2309.07062) |

## Key contributions

- 7B model emits LLVM pass lists
- Auxiliary tasks: predict instr counts and optimized IR
- ~3% IR size improvement over -Oz without thousands of compiles

## Summary

Early demonstration that transformers can choose optimization pass sequences for code size, keeping correctness by executing real compiler passes.

## Key takeaways

- Template for safe LLM-compiler cooperation
- Authors emphasize model IR output is untrusted
- Spawned HN discussion clarifying phase ordering vs neural rewrite

## Why it matters for this survey

This source informs the living survey in `docs/SURVEY.md` (trends, agent roles, process reshape, and/or gaps). Prefer the primary link above when citing.
