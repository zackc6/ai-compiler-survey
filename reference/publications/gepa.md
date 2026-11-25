# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | UC Berkeley · Stanford University · BespokeLabs.ai · University of Notre Dame · Databricks · MIT |
| **Publisher** | ICLR 2026 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2507.19457v2) |
| **Evidence tier** | A: limited kernel-specific evidence for improving controller instructions |
| **Version / reviewed** | v2, 14 February 2026; full PDF, particularly the code-optimization experiments; reviewed 23 September 2026 |

## Key contributions

GEPA uses execution feedback to evolve prompts for fixed-model systems. [Official code](https://github.com/gepa-ai/gepa) exposes reflective optimization separately from the target application.

## Summary

Its kernel experiments change instructions supplied to a refinement agent. They are preliminary evidence for controller-prompt optimization, not compiler-component generation.

## Key takeaways

The AMD XDNA2 experiment uses early NPUEval and GPT-4o with up to ten sequential refinements. A single evolved prompt obtains 26.85% mean vector utilization versus 4.25% initially; the 30.52% result uses a prompt portfolio. A separate NVIDIA V100 experiment covers 35 KernelBench tasks, up to five refinements, and a plotted search budget reaching about 3,000 rollouts. More than 20% of tasks produce a correct kernel faster than PyTorch eager.

## Why it matters for this survey

Start with versioned instruction changes before permitting broad workflow rewrites. Evaluate the accepted controller on applications that did not supply its search feedback.

## Limits / caveats

These are kernel metrics, not application speedups or a complete held-out controller-transfer study. Prompt search has an additional cost. Baseline precision and hidden correctness tests need a modern replication. The paper does not show the GEPA search procedure rewriting itself. [The Winner's Curse in Self-Improvement Loops](winners-curse-self-improvement.md) (October 2026) re-ran GEPA with 16 validation items on TREC, Banking77 and GSM8K: reported gains of 38.8, 18.8 and 6.2 points against held-out gains of 19.2, 1.2 ± 1.7 and −0.9. The kernel experiments here were not re-run, and their selection-set sizes have not been rechecked against that finding (added 25 November 2026).
