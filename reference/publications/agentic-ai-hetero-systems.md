# Efficient and Scalable Agentic AI with Heterogeneous Systems

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Stanford · Gimlet Labs · Intel |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2507.19635](https://arxiv.org/abs/2507.19635) |
| **Evidence tier** | **B** — hetero serving infra for agent graphs; codesign-adjacent |

## Key contributions

- Agentic workloads are dynamic graphs: multimodal IO, retrieval, multiple LLM calls, tool calls — not static inference.
- Argues homogeneous high-end single-vendor infra is too costly for scale-out.
- System design for **dynamic orchestration** of agent workloads across **heterogeneous** CPUs/accelerators (multi-vendor, multi-performance tiers).

## Summary

Same ecosystem as KForge (Gimlet / Asgar). Positions hetero compute as the deployment plane for sub-agent graphs—parallel to KernelEvolve’s hetero *kernel* story, but at agent-serving level. Supports STACK layers 7–8 and commercial tenancy/cost (P10/P11) for control-plane products.

## Key takeaways

- Future agentic compilers that spawn sub-agents inherit **serving hetero** constraints, not only compile hetero.
- Orchestration across cheap/fast tiers is part of P23/P10 (don’t run every specialist on frontier GPUs).
- Complements TritorX/KernelEvolve (compile/bring-up) with runtime placement.

## Why it matters for this survey

Control-plane + codesign substrate: how multi-agent compiler loops run affordably on mixed silicon. Cite with [kforge.md](kforge.md), KernelEvolve, §5.7 P10/P11/P23.

## Limits / caveats

- Infra/systems paper; not a pass/kernel synthesis result.
- Early preprint; validate claims against later deployments.
