# KernelEvolve: Scaling Agentic Kernel Coding for Heterogeneous AI Accelerators at Meta

| Field | Value |
|---|---|
| **Year** | 2025/2026 |
| **Org** | Meta |
| **Publisher** | ISCA 2026 · arXiv |
| **Type** | paper |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://arxiv.org/abs/2512.23236](https://arxiv.org/abs/2512.23236) |
| **Venue** | ISCA 2026 (arXiv:2512.23236) |
| **Evidence tier** | **A** — production-scale agentic kernels across NVIDIA / AMD / MTIA |
| **Also** | [Meta Engineering blog](kernelevolve-blog.md) (Ranking Engineer Agent series, 2026-04-02) |

## Key contributions

- Production agent framework for **ads-ranking** kernels across **NVIDIA, AMD, and Meta MTIA** (plus CPU paths).
- Graph search (greedy / MCTS / evolution) over Triton (+ Triton-TLX) with hardware knowledge injection for proprietary ISA/memory.
- Federated profiling (**MPP**) tying MLIR/Proton/NCU/MTIA Insight so agents see cross-stack evidence, not only source feedback.
- Reports high operator coverage and KernelBench pass rates across platforms; framed as TCO/latency at Meta scale.

## Summary

Companion industrial systems paper to TritorX: where TritorX maximizes *bring-up coverage*, KernelEvolve maximizes *performance* of serving kernels under heterogeneous hardware generations. The agentic compiler here is a multi-backend coding+search control plane grounded in profilers and retrieved HW manuals.

## Key takeaways

- Heterogeneous fleets make manual O(ops × HW) kernel matrices economically impossible — agents become mandatory control plane.
- **Knowledge injection** for unseen ASICs is as important as the base LLM.
- Cross-stack profilers are part of the agentic compiler contract (gap §4.2/4.4).
- Strengthens **C4/C5**: multi-DSL, multi-HW online agents in production.

## Why it matters for this survey

Tier A evidence that the **target future agentic compiler** is multi-accelerator and codesign-aware: HW manuals + counters + IR enter the admit/feedback loop. Use with TritorX for coverage→perf ladder on custom silicon.

## Limits / caveats

- Ads-ranking / Meta infra specific; public reproducibility limited.
- Headline coverage/pass numbers need careful scope reading vs KernelBench-X ceilings (**C2**).
