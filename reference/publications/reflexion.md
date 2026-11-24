# Reflexion: Language Agents with Verbal Reinforcement Learning

| Field | Value |
|---|---|
| **Year** | 2023 |
| **Org** | Northeastern University · Massachusetts Institute of Technology · Princeton University |
| **Publisher** | NeurIPS 2023 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2303.11366](https://arxiv.org/abs/2303.11366) |
| **Evidence tier** | **C** — foundational episodic-memory mechanism used by kernel agents; no compiler workload |
| **Version / reviewed** | v4, 10 October 2023; PDF reviewed 24 November 2026 |

## Key contributions

Instead of updating weights, the agent turns task feedback (a failed test, an environment signal) into a written self-reflection and stores it in an episodic memory buffer that conditions the next attempt. The memory is a bounded sliding window of reflections.

## Summary

With GPT-4, HumanEval Python pass@1 rises from 80.1% to 91.0%, and on the hardest 50 Rust problems from 60.0% to 68.0%. On MBPP Python, Reflexion (77.1%) trails the 80.1% baseline. In AlfWorld it improves on strong baselines by an absolute 22% over 12 trials; on HotPotQA, about 20%. On WebShop it does not significantly beat ReAct.

## Key takeaways

- The authors state the limits that matter for kernel work: optimization through text can settle into local minima; the method relies on the model's self-evaluation; test-driven evaluation struggles with non-deterministic, hardware-dependent or concurrent code; flaky generated tests yield false positives and negatives.
- Gains are per-task retries with memory of earlier failures, not transfer of learned experience to new tasks.

## Why it matters for this survey

Many kernel agents run "Reflexion-style" loops ([GEAK](geak.md) names it), so this is the mechanism behind a large share of the agent evidence. Its own caveat about hardware-dependent and non-deterministic tests is why the survey requires validation contracts outside the agent's control. Episodic memory in the [CoALA](coala.md) sense; same Princeton group.

## Limits / caveats

- Coding benchmarks measure functional correctness, not performance; nothing here bears on optimization quality.
- The comparison is against the same model without reflection, not against search or tuned sampling at equal cost.
