# GEAK v4: end-to-end GPU performance optimization system (GitHub release)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Commercial products & proposals |
| **Link** | [https://github.com/AMD-AGI/GEAK/releases](https://github.com/AMD-AGI/GEAK/releases) |
| **Evidence tier** | **A** — vendor e2e serving workflow: Amdahl triage + warm-server A/B + parity gate |
| **Also** | [repo README](https://github.com/AMD-AGI/GEAK) · [MLA case study](geak-mla-rocm-blog.md) · [v3 blog](geak-v3-rocm-blog.md) |

## Key contributions

- **v4.0.0 (2026-07-08):** redesign from a single-kernel agent into an e2e Instinct optimizer.
- **`e2e_workflow`:** profile a *warm* sglang/vLLM server → rank kernels by `pct_gpu_time × achievable_speedup` → cheap config/backend sweeps first → recurse into `kernel_workflow` only for kernels that can move model throughput → reversible overlays → **warm-server A/B**, engagement proof, **output parity**, throughput / noise-band gating.
- **Deterministic JS Workflows** own budget, fan-out, verification, recursion, and stop; LLMs do judgment (analysis, authoring, debug, integration).
- `kernel_workflow` remains first-class (Triton / HIP / CK / FlyDSL / …) with Director → TechLead → specialists and independent per-patch measure.
- `perf_knowledge` operator×backend×GPU×dtype matrix; expert skills seed directions but never replace on-box validation.

## Summary

AMD’s public GEAK tree now ships the commercial shape of **§5.1.3 e2e-optimal-seeking**: product fitness is serving throughput, local kernel search is a subroutine, and admit is a warm-server A/B with parity — not a microbench. Orchestration is compiled-ish (JS workflows) rather than an unbounded chat loop (P22 / T10-adjacent). Requires Claude Code ≥2.1.177 for dynamic workflows; Instinct MI (gfx942/gfx950), ROCm 6+, rocprof*.

## Key takeaways

- First **named vendor product** that makes serving-level A/B + Amdahl triage the *default control-plane loop* (T6 exists cell moves).
- Does **not** settle **C2**: still no public p50/p90 + cost-to-compile across pinned HW/compiler versions; case studies remain workload-selected ([MLA blog](geak-mla-rocm-blog.md)).
- Multi-DSL kernel path + e2e serve path sharpens **C4** (agents must be multi-DSL) and **C5** (online, in the serve loop).
- Deterministic orchestration + LLM judgment matches the survey’s SLA lean (P3/P22).

## Why it matters for this survey

★ for **T6**, **§5.1.3**, **C2** (pressure, not settlement), and commercial job **(a)**. Update products/repos Tier A from “GEAK v3 repo-level” to “GEAK v4 e2e serving.” Pair with FlashInfer-Bench (`apply()`) and Cake (serving-validated kernels on NVIDIA).

## Limits / caveats

- AMD Instinct + sglang/vLLM only; Claude Code as the agent host is a SKU constraint.
- Release notes are mechanism-rich, number-poor — cite the MLA blog for a concrete e2e figure, with C2 caveats.
- Reversible overlays are not yet a portable “agent compile interface” RFC (T1 still missing vendor-neutral schemas).
