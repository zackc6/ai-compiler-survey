# How Much of a Real Workload Can LLM-Generated GPU Kernels Actually Reach?

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Gaurav Agarwal · Ashish Garg · Isha Singhal (affiliations not stated) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2609.21058v1) |
| **Evidence tier** | **A** — relevance to the guide’s design choices, not a quality rating |
| **Version / reviewed** | Linked version; reviewed 2026-09-23 |

## Key contributions

Profiles the runtime share reachable by selected generated kernels and audits numerical acceptance tests.

## Summary

Seven profiles on A100 hardware suggest different optimization opportunities across workload families. Table 3 projects transformer time savings of 1.32–2.49%, rather than measuring deployed application gains.

## Key takeaways

The inference recommender profile has 58.2% addressable time; one embedding kernel accounts for 37.4%, not the full share.

## Why it matters for this survey

Profile the target before allocating kernel-generation effort. [Artifacts](https://github.com/gauravapiscean/kernel-headroom) support further checking.

## Limits / caveats

Single host/device type and one shape per profile. Library kernels are classified as already optimal, an assumption rather than proof. Projections use win-rate and speedup assumptions. These profiles neither describe KernelEvolve’s private workloads nor bound wider compiler changes.
