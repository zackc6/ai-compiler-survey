# Beyond Scaling: Self-Evolving LLM Agents for Hardware Kernel Optimization via an Experience-Driven Workflow and Experience Graph Memory

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Affiliations not verified in the accessible primary abstract |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2608.25570v1) |
| **Evidence tier** | B: kernel-specific memory-adaptation lead; full-text verification pending |
| **Version / reviewed** | v1, 26 August 2026; primary abstract reviewed 23 September 2026; reviewed 23 September 2026 |

## Key contributions

The primary abstract describes KOPE as storing kernel-optimization decisions and measured outcomes in an experience graph, then selecting relevant experience within a token budget. The foundation model remains fixed.

## Summary

This is a compiler-related lead for persistent memory adaptation across optimization tasks. It does not, from the accessible evidence, show an agent rewriting its retrieval algorithm or search workflow.

## Key takeaways

The abstract reports comparisons with CANNBot and ablations of context management and memory. Full methods, hardware setup, task splits, timing denominators, and total-budget comparability could not be verified in this review, so this digest does not promote its numerical claims into the survey's measured-results register.

## Why it matters for this survey

Test a fixed controller with and without reusable experience before attributing an improvement to controller-code evolution. This is a distinct mechanism even if the source calls it self-evolution.

## Limits / caveats

Abstract-only review: primary full-text and PDF retrieval failed. Obtain the paper and implementation, verify affiliations and evaluation splits, then compare memory reuse with cached kernels and fixed-controller baselines. No application-level or recursive-controller claim is established here.
