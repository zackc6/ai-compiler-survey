# Compiler 2.0: Building the Next Generation Compilers with Machine Learning (Ken Kennedy Award plenary)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | MIT CSAIL |
| **Publisher** | ACM/IEEE Ken Kennedy Award · HPCA/CGO/PPoPP/CC 2026 |
| **Type** | talk |
| **Group** | Surveys & vision |
| **Link** | [https://2026.hpca-cgo-ppopp-cc.org/details/hpca-cgo-ppopp-cc-2026-plenary-keynotes/2/Compiler-2-0-Building-the-Next-Generation-Compilers-with-Machine-Learning](https://2026.hpca-cgo-ppopp-cc.org/details/hpca-cgo-ppopp-cc-2026-plenary-keynotes/2/Compiler-2-0-Building-the-Next-Generation-Compilers-with-Machine-Learning) |
| **Evidence tier** | **A** — venue-level vision for ML-modernized compilers; ★ for §5 / ROADMAP |
| **Also** | CSAIL Forum repeat (same title); lineage: [CGO 2022](compiler-2.0-cgo2022.md), [CC'20 modernize talk](compiler-2.0-modernize-ml.md), [MOCHA/Aarno](compiler-2.0-mocha-aarno.md) |

## Key contributions

- Frames the **lost FORTRAN promise**: high-level languages once hid hardware; multicores, vectors, and accelerators pushed peak performance back to architecture-specific CUDA/PTX/intrinsics (incl. Apple/Arm SME gaps).
- Central question: can **next-gen compilers restore** “hide architecture, keep near-peak performance”?
- Answer path: **proper abstractions + machine learning** to make compilers more effective *and* radically simpler to build/retarget.
- Delivered as **2025 ACM/IEEE-CS Ken Kennedy Award** plenary at co-located HPCA/CGO/PPoPP/CC 2026 (Sydney).

## Summary

Public plenary vision from Saman Amarasinghe (MIT Commit / CSAIL). Unlike LLM-pass or FMware surveys, this talk centers the **heterogeneous-hardware abstraction crisis** and argues ML + better IRs are how compilers reclaim the portability contract. Same title reused for CSAIL Forum; technical lineage runs through the CGO 2022 “Compiler 2.0” keynote, the CC 2020 “Using ML to Modernize…” talk (Ithemal/Vemal), and the funded DARPA **MOCHA** Compiler 2.0 project (LLM rewrite synthesis + eqsat + Rocq verification).

## Key takeaways

- Vision priority is **restoring the high-level → near-peak contract**, not “replace `opt` with an LLM.”
- Aligns with this survey’s hybrid bet: ML/agents for search, modeling, and construction; classical legality/lowering stay essential.
- Closest funded instantiation: [MOCHA / Aarno Compiler 2.0](compiler-2.0-mocha-aarno.md) (2025–2028).
- Complementary to [Compiler.next](compiler-next.md) (FMware compile object) and [New Compiler Stack](new-compiler-stack-survey.md) (LLM role taxonomy)—different axes of “next compiler.”

## Why it matters for this survey

★ Predictions signal for [`docs/SURVEY.md`](../docs/SURVEY.md) §1.4 / §5.4 and [`docs/ROADMAP.md`](../docs/ROADMAP.md): codesign/retarget cost (**H1/S4**), hybrid control plane (**A1**), and verified ML rewrite pipelines (**Trend E**). Prefer this page for the 2026 abstract; prefer MOCHA digest for concrete architecture.

## Limits / caveats

- Abstract/agenda talk — not a measured system paper; do not cite as empirical speedups.
- Overlaps titles across years; cite venue+year to avoid conflating 2020/2022/2026 versions.
