# AFlow: Automating Agentic Workflow Generation

| Field | Value |
|---|---|
| **Year** | 2024/25 |
| **Org** | DeepWisdom · HKUST (Guangzhou) · Renmin University of China · Nanjing University · Fudan University · KAUST · Université de Montréal / Mila · HKUST |
| **Publisher** | ICLR 2025 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2410.10762v4) |
| **Evidence tier** | B: workflow search evaluated outside compiler optimization |
| **Version / reviewed** | v4, 15 April 2025; reviewed 23 September 2026 |

## Key contributions

AFlow searches over code representing language-model workflows. Monte Carlo tree search, execution feedback, and reusable operators guide edits to the workflow.

## Summary

The paper evaluates six coding, mathematics, and question-answering benchmarks, and studies transfer to different executor models. Official code is [FoundationAgents/AFlow](https://github.com/FoundationAgents/AFlow).

## Key takeaways

The search procedure changes the target workflow; it does not establish that the search procedure rewrites itself. Reported benchmark accuracy and inference costs are separate from the cost of discovering the workflow.

## Why it matters for this survey

Suggests testing alternative sequences of profiling, synthesis, repair, and measurement in a compiler controller. Compare structured workflow search with unconstrained controller-code edits.

## Limits / caveats

No kernel-runtime or application-performance evaluation is reported. AFlow is distinct from [AgentFlow](agentflow.md), a static-analysis framework, and [FlowCompile](flowcompile.md), a workflow compiler. Similar names are not a shared mechanism or independent corroboration of compiler benefit.
