# Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | University of British Columbia · Vector Institute · Sakana AI |
| **Publisher** | ICLR 2026 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2505.22954v3) |
| **Evidence tier** | B: agent-code evolution with a partly fixed outer loop |
| **Version / reviewed** | v3, 12 March 2026; reviewed 23 September 2026 |

## Key contributions

Coding agents modify themselves, and an archive retains variants that may support later improvements. Evaluation is empirical rather than a proof that every change is beneficial.

## Summary

The study evaluates coding-agent changes on SWE-bench and Polyglot. It keeps foundation-model weights fixed and includes comparisons that remove self-improvement or open-ended exploration. Code is available through the [authors' project page](https://sakana.ai/dgm/).

## Key takeaways

The paper explicitly keeps archive maintenance and parent selection fixed. Improving agent code therefore does not mean that every part of the improvement process evolves.

## Why it matters for this survey

Suggests retaining several controller variants instead of accepting only immediate gains. The maintenance and evaluation costs of that archive must be measured. [ADAS](adas.md) and [Hyperagents](hyperagents.md) share its research lineage.

## Limits / caveats

Coding-task success is not compiler optimization. The evidence neither proves unlimited improvement nor establishes that a more capable coding agent will propose better compiler experiments. Test that transfer directly.
