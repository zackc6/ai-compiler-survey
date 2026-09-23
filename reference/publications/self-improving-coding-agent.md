# A Self-Improving Coding Agent

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | University of Bristol · iGent AI |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2504.15228v2) |
| **Evidence tier** | B: controller-code self-modification on coding tasks |
| **Version / reviewed** | v2, 16 May 2025; reviewed 23 September 2026 |

## Key contributions

The Self-Improving Coding Agent selects an agent from its archive to edit the agent codebase. Its utility combines task score, cost, and time; model weights are unchanged.

## Summary

The evaluated changes include editing tools and code navigation. This is modification of the agent implementation, beyond remembering a previous answer.

## Key takeaways

A 15-iteration run costs approximately US$7,000 in model calls. Evaluation includes fixed random subsets of 50 SWE-bench Verified and 50 LiveCodeBench questions, plus synthetic tasks. The SWE-bench subset rises from 17% to a peak of 53%; the last reported iteration is 51%. Strong reasoning-model baselines leave less improvement in another experiment.

## Why it matters for this survey

Motivates proposing changes to a compiler controller's tooling. Its utility weights are a study choice, not this guide's performance-first objective.

## Limits / caveats

Repeated scores on the optimization benchmark do not establish fresh-task transfer. The result is not a full SWE-bench score or compiler-performance result. Compare independently held-out tasks, include development expense, and test whether simpler controller changes suffice.
