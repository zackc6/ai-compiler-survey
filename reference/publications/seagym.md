# SEAGym: An Evaluation Environment for Self-Evolving LLM Agents

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Congjie Zheng, Chuanyi Xue, Bin Liang, Jun Yang, Changshui Zhang (affiliations not listed on the arXiv page) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2606.17546) |
| **Evidence tier** | C: evaluation protocol for harness updates; no compiler tasks |
| **Version / reviewed** | v1, 16 June 2026; arXiv abstract page reviewed by Claude 25 November 2026 |

## Key contributions

An environment that scores each harness update of a self-evolving agent on several axes at once:
- frozen update-validation;
- held-out in-distribution and out-of-distribution transfer;
- replay of older tasks, to catch regressions;
- cost records;
- snapshots of each stage of evolution.

It runs on Harbor-compatible benchmarks and was instantiated on Terminal-Bench 2.0 and Humanity's Last Exam. It compares ACE, TF-GRPO and AHE under a shared epoch and batch protocol.

## Summary

The authors argue that reporting a single task score or one sequential curve hides whether an update yields reusable gains, overfits recent tasks, raises cost, or harms older behaviour.

## Key takeaways

The abstract reports three qualitative findings:
- frequent updates may fail to improve held-out performance;
- useful intermediate snapshots may collapse later;
- source diversity and the model backend affect harness reliability.

Quantitative results are not on the abstract page and were not verified.

## Why it matters for this survey

It is a ready-made measurement design for the controller checkpoint. A compiler controller change should be logged with held-out and out-of-distribution workload scores, a replay of previously solved workloads to catch regressions, and its cost, at every accepted step. Its finding that intermediate snapshots can collapse argues for keeping versioned controller snapshots and comparing against the best earlier one, not only the latest. Related: [Harness-Delta Attribution](harness-delta-attribution.md) for decomposing a gain once it is measured.

## Limits / caveats

Abstract-level reading only. No compiler, kernel or performance tasks. Harbor-based setups have reward-hacking holes documented by [Singularity-Bench](singularity-bench.md); whether SEAGym's tasks are exposed to them is not known.
