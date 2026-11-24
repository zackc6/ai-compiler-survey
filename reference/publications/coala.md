# Cognitive Architectures for Language Agents (CoALA)

| Field | Value |
|---|---|
| **Year** | 2023/24 |
| **Org** | Princeton University |
| **Publisher** | Transactions on Machine Learning Research (TMLR) · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2309.02427](https://arxiv.org/abs/2309.02427) |
| **Evidence tier** | **C** — conceptual framework, no measurements; used here only to name the kinds of controller memory |
| **Version / reviewed** | v3, 15 March 2024 (TMLR camera-ready); abstract page reviewed 24 November 2026 |

## Key contributions

CoALA organizes language agents with ideas from cognitive science and symbolic AI: modular memory, a structured action space with internal actions (retrieval, reasoning, learning) and external ones (grounding in an environment), and a generalized decision loop. It separates **working memory** (the current context) from three long-term stores: **episodic** (past experience and trajectories), **semantic** (knowledge about the world), and **procedural** (skills, including the agent's own code and the model's weights).

## Summary

A framework and survey, not a system. The authors use it to classify existing agents and to suggest directions; nothing is benchmarked.

## Key takeaways

- The value for a compiler designer is vocabulary. "The optimizer learns from experience" can mean storing search trajectories (episodic), accumulating hardware and compiler facts (semantic), or growing a library of reusable kernels, rewrites or schedules (procedural). These have different validation and staleness problems.
- Learning is an explicit action that writes to a memory; that makes memory updates inspectable and testable separately from the search that uses them.

## Why it matters for this survey

The controller section's memory row mixes these kinds: [AKLR](aklr.md) is supplied knowledge (semantic hardware notes bundled with procedural skills and example kernels), [KOPE](kope.md) and [AccelOpt](accelopt.md) store episodic experience distilled into strategies, and procedural skill libraries are what the "evolve compiler components" path produces. Classifying sources this way prevents counting a curated hardware note and a learned experience buffer as the same evidence. Same Princeton group as [Reflexion](reflexion.md) (Yao, Narasimhan).

## Limits / caveats

- No evidence about compiler optimization; it is a taxonomy, and other taxonomies (for example the Storage, Reflection, Experience stages) cut the same space differently.
- Written in 2023; it predates most work on harness and controller self-modification covered elsewhere in the survey.
