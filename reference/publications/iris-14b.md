# LLM Translation of Compiler Intermediate Representation

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Barcelona Supercomputing Center · Universitat Politècnica de Catalunya |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Foundation LLMs for compilers |
| **Link** | [https://arxiv.org/abs/2605.08247](https://arxiv.org/abs/2605.08247) |
| **Evidence tier** | **B** — IR↔IR *glue* (GIMPLE→LLVM); classical compilers still own `opt` |

## Key contributions

- **IRIS-14B:** 14B transformer fine-tuned for **GIMPLE → LLVM IR** translation (first dedicated IR-to-IR model, per authors).
- Training pairs from The Stack / GNU utilities compiled through GCC and LLVM; eval on ExeBench-IRIS and CodeForces-IRIS with syntactic + I/O semantic checks.
- Framed as a hybrid interoperability layer: LLM translates; GCC/LLVM still compile and optimize.

## Summary

BSC/UPC paper treating IR-to-IR translation as the job rule-based bridges (llvm-gcc, DragonEgg, Wyrm) failed to maintain. IRIS-14B outperforms general code models from 13B to ~1T by up to 44 points on their GIMPLE→LLVM task. Authors are explicit: this is **not** a replacement compiler — it is a data-driven adapter so frontends, backends, and tools (e.g. Alive2 on GCC-origin programs) can be mixed without rewriting passes.

## Key takeaways

- Translation IR is **§4.4 glue**, not a new L-band and not LLM-as-`opt`.
- Semantic gaps (statement vs SSA, memory models, EH) remain; I/O tests are the admit gate.
- Supports “portable *agent* contract over several classical sinks” rather than one universal executable IR (**C4** / A6).

## Why it matters for this survey

T1 / §4.4 / C8: interoperability without collapsing GCC and LLVM into one data-plane IR. Cite when discussing agent-visible contracts that sit *above* heterogeneous middles. Demote from ★: no product loop, no serving oracle, no kernel DSL.

## Limits / caveats

- One direction (GIMPLE→LLVM) in the reported model; reverse is discussed, not the eval.
- C-origin pairs; not MLIR/Triton/Tile.
- Accuracy on contest/real C IR ≠ production toolchain certification.
