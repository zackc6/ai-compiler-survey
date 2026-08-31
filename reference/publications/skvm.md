# SkVM: Compiling Skills for Efficient Execution Everywhere

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Shanghai Jiao Tong University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2604.03088](https://arxiv.org/abs/2604.03088) |
| **Evidence tier** | **B** — skill AOT/JIT across models/harnesses; “LLMs as processors” is a metaphor |

## Key contributions

- Treats skills as **code** and LLMs as **heterogeneous processors**. Analyzes a large skill corpus (authors: ~118k) into primitive capabilities; profiles model×harness pairs.
- **AOT:** capability-based rewrite, environment binding, concurrency extraction. **JIT:** code solidification and adaptive recompilation at runtime.
- SkillsBench + multi-model/harness eval: higher completion, up to ~40% fewer tokens, speedups from parallelism and solidification (author).

## Summary

April 2026 SJTU compilation+VM for portable skills. Closest survey rhyme is **job (b)** / Magellan (compile a heuristic so the online path is cheaper) — but the artifact is a *skill*, not an LLVM pass. Complements [SkCC](skcc.md) (format/security IR), [SIGIL](sigil.md) (mandated CFG), and [SkillSmith](skillsmith.md) (boundary ABI). Not a data-plane VM for cubins.

## Key takeaways

- **P12/P23:** adapting the skill to the *model* (capability compile) is the skill-world analogue of “don’t put `model_id` in the kernel cache key” — here the skill *binary* may change when the LLM changes; product truth for *kernels* must still be VCS artifacts (P2-C).
- **T10:** interpreted SKILL.md vs AOT/JIT skill is now an explicit fork, same as “live harness vs compiled workflow.”
- Do not read “compiling skills” as M3 (LLM-as-`opt`).

## Why it matters for this survey

Third skill-compiler design point (portability-across-**models**, vs SkCC across **frameworks**, vs SIGIL **compliance**). Substrate only. No C6 move.

## Limits / caveats

- Headline corpus/speedup figures are author-reported.
- Capability primitives are not HW ISA counters (T5/C10 stay human).
- Title-page author lists vary across mirrors; cite the arXiv abstract + SJTU affiliations.
