# DARPA MOCHA / Aarno Labs: Compiler 2.0 project

| Field | Value |
|---|---|
| **Year** | 2025–2028 |
| **Type** | company |
| **Group** | Surveys & vision |
| **Link** | [https://www.aarno-labs.com/project/compiler-20/](https://www.aarno-labs.com/project/compiler-20/) |
| **Evidence tier** | **A** — funded program that instantiates Compiler 2.0 + codesign retarget goals |
| **Also** | DARPA program: [MOCHA](https://www.darpa.mil/research/programs/mocha-machine-learning) (Machine Learning and Optimization-guided Compilers for Heterogeneous Architectures) |

## Key contributions

- **MOCHA program goals** (public): cut human effort to adapt compilers to new hardware (~90% target); improve throughput/power/memory efficiency (up to ~5× claimed aspiration); open extensible foundation for heterogeneous targets.
- **Compiler 2.0 team** (Aarno + MIT CSAIL + UIUC): neuro-symbolic stack — LLM-generated **equivalence-preserving rewrites**, **equality saturation**, learned cost models, **Rocq**-verified validation, data-frugal performance modeling (tensor completion / transfer), ISA-as-rewrites for retargeting, learning-guided policies/surrogates.
- Explicit partners: Amarasinghe, Ragan-Kelley, Chlipala, Solar-Lezama, Carbin (MIT); Mendis, Solomonik (UIUC); Gordon (Aarno integration).

## Summary

Public project page for the funded realization of Amarasinghe’s Compiler 2.0 vision under DARPA MOCHA (program dates on page: Sep 2025–Sep 2028). Distinct from survey papers: it commits to a **verified ML rewrite + eqsat** pipeline and architecture description via rewrite rules — i.e., ML for construction/retarget with formal gates, not free-form LLM `opt`. Aligns with this survey’s codesign job **(d)** (cheap retarget / bring-up) and Trend E (verification in the loop).

## Key takeaways

1. Best public **implementation path** for the 2026 Ken Kennedy plenary narrative.
2. Architecture matches hybrid prediction: LLM proposes rewrites; eqsat explores; Rocq admits; learned models guide selection (**A1**, **A5**).
3. Retarget-via-rewrite-rules is a concrete codesign/compiler interface story (**H1**, **S4**) without claiming autonomous EDA (**C10**).
4. Watch for open-source releases and Year 1–3 evaluations — settlement signal for ROADMAP Horizon A.

## Why it matters for this survey

★ Program-level evidence that “next compiler” funding is going to **ML + verification + hetero retarget**, parallel to LLM kernel agents and Magellan. Wire into [`docs/SURVEY.md`](../docs/SURVEY.md) §5.4 and [`docs/ROADMAP.md`](../docs/ROADMAP.md). Prefer DARPA page for program premise; prefer Aarno page for team/tech stack.

## Limits / caveats

- Vendor/PI project page — aspirational metrics (90%, 5×) are program targets, not published results.
- Artifacts not yet a Tier A measured paper in this index; status **Watch** until OSS evals land.
