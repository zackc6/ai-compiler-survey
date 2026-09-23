# Meta-Harness: End-to-End Optimization of Model Harnesses

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Stanford University · KRAFTON · MIT |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2603.28052v1) |
| **Evidence tier** | B: automated controller-code search with separate test evaluation |
| **Version / reviewed** | v1, 30 March 2026; reviewed 23 September 2026 |

## Key contributions

An agent searches harness code while inspecting previous code, scores, and execution traces through a filesystem. The task model stays frozen. [Official implementation](https://github.com/stanford-iris-lab/meta-harness) and an [author project page](https://yoonholee.com/meta-harness/) accompany the paper.

## Summary

The editable harness controls prompting, retrieval, memory, and orchestration. The proposer receives search-set feedback, with test results withheld until final evaluation.

## Key takeaways

The text-classification experiment evaluates 40 proposed harnesses over 20 iterations. Mean test accuracy across three datasets increases from ACE's 40.9% to 48.6%, with smaller input context. These are classification results, not compiler speedups. Other experiments study mathematical reasoning and terminal tasks.

## Why it matters for this survey

Suggests an inspectable outer loop for compiler-controller engineering: preserve raw evidence and let the proposer retrieve relevant records. Some authors overlap with GEPA; keep organizational dependence visible.

## Limits / caveats

Searching target harnesses is not proof that the proposing system improves its own search algorithm. Compiler transfer and search-cost amortization require separate experiments. Match total resources, not only the number of candidate evaluations.
