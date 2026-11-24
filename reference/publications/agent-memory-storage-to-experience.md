# From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Hong Kong Baptist University · South China Normal University · Hong Kong University of Science and Technology · National University of Singapore · University of Science and Technology Beijing |
| **Publisher** | Findings of ACL 2026 · arXiv |
| **Type** | paper |
| **Group** | Surveys & vision |
| **Link** | [ACL Anthology](https://aclanthology.org/2026.findings-acl.2069/) · [arXiv 2605.06716](https://arxiv.org/abs/2605.06716) |
| **Evidence tier** | **C** — survey; organizes the memory mechanisms behind the controller section |
| **Version / reviewed** | Findings of ACL 2026, pp. 41622–41652, DOI 10.18653/v1/2026.findings-acl.2069; arXiv v1, 7 May 2026; PDF (first two thirds) reviewed 24 November 2026 |

## Key contributions

Proposes three stages of agent memory: **Storage** (keep trajectories), **Reflection** (refine them, as in Reflexion), and **Experience** (abstract across trajectories into reusable rules, skills or weights). The Experience stage is split into explicit experience (natural-language policies or executable entities such as skill libraries), implicit experience (fine-tuning or latent variables), and hybrids that cache explicit experience and periodically compress it into weights. It singles out cross-trajectory abstraction and memory-guided exploration as the frontier.

## Summary

A qualitative survey with no cross-method quantitative comparison. It barely touches code optimization; the one kernel work it cites is [AccelOpt](accelopt.md), as an example of experience turned into executable entities.

## Key takeaways

- Open problems it names that transfer directly to compilers: **staleness** (outdated knowledge "fails without overt indication"; it calls for decay policies), **contamination** (errors written to memory propagate unless additions and deletions are governed), and **evaluation** (benchmarks for the Experience stage are "significantly insufficient", since existing datasets mostly test retrieval).

## Why it matters for this survey

Its three stages line up with the controller section's ladder: retrieval of past attempts, reflection within a job, and reusable experience across jobs. The survey's open question is whether the third stage helps compiler optimization under equal budgets; this survey confirms that the general memory literature has no benchmark that would answer it either. Read with [CoALA](coala.md), which classifies the same mechanisms by memory type rather than by stage.

## Limits / caveats

- Recent preprints in its coverage are not peer-reviewed; the paper says so.
- General-agent scope; conversational benchmarks such as LongMemEval and LoCoMo, which it reviews, measure recall, not optimization.
