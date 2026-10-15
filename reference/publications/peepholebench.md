# Can Coding Agents Implement Missed Compiler Optimizations? Evaluating LLM Agents on LLVM Peephole Optimizations (PeepholeBench)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Waterloo (Cheriton School of Computer Science) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [arXiv 2607.02684](https://arxiv.org/abs/2607.02684) · companion study [arXiv 2607.02370](https://arxiv.org/abs/2607.02370) |
| **Evidence tier** | **B** — coding agents on real compiler-engineering tasks; measures the correctness–profitability tension directly |
| **Version / reviewed** | v1, 2 July 2026; reviewed 15 October 2026 |

## Key contributions

Tasks are 21 resolved LLVM issues and 19 merged pull requests about missed peephole optimizations in InstCombine. Agents receive only the issue context that existed before each human fix; patches are judged on behavioral validity and on profitability (the optimization actually fires without regressions) against the human patch. Agents: Claude Code (Sonnet 4.6), Gemini CLI (Gemini 3 Flash), Codex CLI (GPT-5.4 and GPT-5.4 mini).

## Summary

Per-test-case validity is high for every agent (97.0–98.5%; human patches 98.4%). Profitability is where they differ: Gemini 3 Flash 16.5% per test case (human 16.4%), the others 8.8–9.0%. On the pass@3 non-regressive-profitability metric against the human patch, the best agent reaches 42% of PRs; counting PRs with at least one profitable run, 8 of 19 (Gemini), 7 (Sonnet, GPT-5.4), 5 (GPT-5.4 mini). "No agent matches human developers on both dimensions at once."

## Key takeaways

- Dominant failure modes: overly narrow transformations and misuse of LLVM-specific mechanisms. Existing test suites rarely expose these errors—a finding that matters for any plan to let agents land compiler changes with CI as the only gate.

## Why it matters for this survey

Evidence for the compiler-as-optimization-target trend and for the review question: agent-written compiler patches are usually valid and often unprofitable, so profitability checks and compiler-specific review are needed beyond test passage. Complements [Archer](archer-paper.md) on agentic review and [AutoPass](autopass.md) on evidence-guided tuning.

## Limits / caveats

- 40 small InstCombine tasks; results may not transfer to larger passes or to GPU compilers.
- Agent versions move quickly; the per-agent ranking is a snapshot.
- Profitability is measured on the benchmark's own inputs, not on downstream applications.
