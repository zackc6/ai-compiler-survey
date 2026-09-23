# From Minutes to Seconds: LLM-Guided Autotuning for Helion Kernels

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Meta (PyTorch/Helion team) |
| **Publisher** | PyTorch blog |
| **Type** | company |
| **Group** | Classic DL compilers |
| **Link** | [Primary source](https://pytorch.org/blog/from-minutes-to-seconds-llm-guided-autotuning-for-helion-kernels/) |
| **Evidence tier** | **A** — relevance to the design decisions, not a quality score |
| **Reviewed** | 2026-09-23 |

## Key contributions

A language model proposes tuning configurations; conventional refinement can improve them. The June 2026 report evaluates 33 kernel/shape cases on B200.

## Summary

The report finds 9.8 times fewer configurations and 6.7 times shorter tuning time, while final kernel latency is approximately equal to the conventional baseline.

## Key takeaways

Tuning efficiency and final runtime performance are separate outcomes.

## Why it matters for this survey

This updates the earlier Helion launch account: the project now reports language-model-guided tuning. It supports testing a combination of model proposals and conventional search.

## Limits / caveats

This is a first-party report. The model/conventional kernel-latency ratio is 1.009; eight cases lose more than 5%, with refinement closing six gaps. These are not universal kernel speedups.
