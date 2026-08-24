# Rethinking Agentic Kernel Generation for Emerging Accelerators (Zomboss)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Michigan · The University of Texas at Austin |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://arxiv.org/abs/2608.00894](https://arxiv.org/abs/2608.00894) |
| **Evidence tier** | **A** — compiler-mediated mapping search; compile-once machine semantics vs per-workload native synthesis |

## Key contributions

- Diagnoses **direct agentic kernel generation** (KernelCraft-class): each workload re-encodes workload-*invariant* ISA/memory/sync legality from docs — 85% of Gemmini tasks re-query docs; 60% cross-family re-retrieval.
- **Zomboss:** compile machine semantics once (TensorLift → TAIDL → ACT backend) into a reusable **mapping surface**; the agent proposes only workload-dependent intents; the compiler completes, legalizes, and lowers.
- Two interface shapes: Gemmini (agent *selects* from an enumerated legal catalog) vs PLENA (agent *constrains* a region; ACT completes a batch of legal plans).
- All **56** instances (20 Gemmini + 36 PLENA) return a correct verified kernel vs 26/56 for direct neural. Geo-mean vs compiler default: **3.34×** Gemmini, **1.10×** PLENA. Token cut vs direct agentic: **71.2%** / **54.2%**.

## Summary

Michigan / UT Austin paper on *emerging* accelerators that lack a mature GPU-class backend. GPU kernel agents already presuppose a compiler boundary (CUDA/Triton → device). On new ASICs the agent is often asked to reconstruct that boundary *and* pick a mapping in one loop. Zomboss splits the jobs: a generated backend owns instruction selection, memory placement, sync, and native codegen; the agent searches tiling/layout/fusion/precision/overlap on a typed surface. Candidate-0 (compiler default) is always a verified fallback. Recasts kernel generation as **verified design-space exploration** open to neural, heuristic, or classical search.

## Key takeaways

- Strongest academic statement of **C3-B / C6-B** on non-GPU ASICs: neural search *inside* a compiler-owned legality boundary, not free ISA assembly.
- **Compile-once machine contract** (TAIDL/ACT) is the missing piece that makes GPU-style agent loops possible on new devices — job **(d)** substrate, not just “better prompts.”
- Token/coverage gains vs direct agents support P23 (tokens shape the SKU): shrinking the action space beats spending more tokens on legality reconstruction.
- **Does not settle C9.** Gemmini/PLENA are research accelerators + sim, not a second-vendor public TritorX-class bring-up on a shipping ASIC.

## Why it matters for this survey

★ for **T1** (typed mapping contract), **T2** (compiler-owned legalize + verified fallback), **T5** (machine semantics compiled into the backend), and job **(d)**. Pair with TritorX/KernelEvolve (industrial coverage→perf) and Cake (GPU schedule-IR co-design). Keeps codesign inside kernels/IR/oracles (**C10-B**).

## Limits / caveats

- Relies on TensorLift/TAIDL/ACT quality; completeness is relative to the supplied semantics.
- Simulator / research-accelerator eval; no production serving A/B.
- PLENA speedups over default are modest (1.10× geo-mean) — coverage and token cost are the headline, not peak.
