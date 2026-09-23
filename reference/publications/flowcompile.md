# FlowCompile: An Optimizing Compiler for Structured LLM Workflows

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | UMass Amherst · MIT · MIT-IBM Watson AI Lab |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2605.13647](https://arxiv.org/abs/2605.13647) |
| **Evidence tier** | **A** — compile-time optimization of sub-agent workflow graphs (accuracy–latency) |

## Key contributions

FlowCompile treats structured language-model workflows as a compilation target. It searches model choices, reasoning budgets, and workflow configurations before deployment, seeking useful accuracy and latency tradeoffs.

## Summary

This is optimization of the workflow that runs agents. It is not evidence that the workflow independently rewrites its own optimizer, nor a measured evaluation of a compiler agent.

## Key takeaways

A compiler controller could be optimized offline and reused. Whether compiling its workflow improves kernel-search quality, total search time, or application performance needs a compiler-specific comparison.

## Why it matters for this survey

Provides a structured alternative to broad controller-code synthesis. Compare fixed workflows, searched configurations, and generated workflows under the same task and budget. [AFlow](aflow.md) generates workflows; [AgentFlow](agentflow.md) analyzes agent dependencies. They are different systems.

## Limits / caveats

Targets general language-model workflows. Accuracy and agent latency must not be reported as compiled-application speedups. Reusing or compiling a workflow does not by itself establish recursive self-improvement.
