# ComPile: A Large IR Dataset from Production Sources

| Field | Value |
|---|---|
| **Year** | 2023 |
| **Org** | UC Davis · Technical University of Munich · Lawrence Livermore National Laboratory · University of Illinois Urbana-Champaign · Argonne National Laboratory · Google et al. |
| **Publisher** | arXiv · Hugging Face (`llvm-ml/ComPile`) |
| **Type** | paper |
| **Group** | Foundation LLMs for compilers |
| **Link** | [https://arxiv.org/abs/2309.15432](https://arxiv.org/abs/2309.15432) |
| **Evidence tier** | **B** — fluency-IR corpus (T7); LLVM-only, not the missing MLIR/Tile/StableHLO ladder |

## Key contributions

- Production-grade **LLVM IR** corpus from Rust, Swift, Julia, and C/C++ via compiler/package-manager hooks.
- Public subset on Hugging Face; paper-scale figures ~1.4T Llama-2 tokens / multi-TB textual IR (closed vs permissive splits differ).
- Motivation: IR-based models and in-compiler ML need structure that source-only piles omit.

## Summary

llvm-ml collaboration (Grossman, Paehler, Parasyris, Moses, Trofin, Doerfert, et al.) arguing that compiler ML is starved of *production IR*, not of GitHub source. ComPile is the large LLVM-IR pretrain/finetune pile behind later IR LLMs. For this survey it is **family-1 fluency data**: necessary fuel for Meta LLM Compiler–class priors, insufficient as an agent contract (LLM4IR: models still fail CFG/exec on LLVM text).

## Key takeaways

- T7 “exists” cell: LLVM-heavy public IR at scale.
- Does **not** close T7 missing: versioned MLIR / Triton / Tile / StableHLO + negatives.
- More IR tokens ≠ safer free rewrite (**C3**).

## Why it matters for this survey

§4.7 / **T7**: cite as the LLVM fluency corpus alongside Meta LLM Compiler’s 546B-token train. Keep distinct from KernelBook (torch↔Triton pairs). Not ★ — substrate data, prediction already assumed LLVM-centric pretrain.

## Limits / caveats

- LLVM IR only; no GPU kernel DSLs.
- License/split discipline matters for commercial research (public vs closed cuts).
- Token counts vary by vocab and dump format — use as order-of-magnitude, not a leaderboard.
