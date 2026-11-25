# The Winner's Curse in LLM Self-Improvement Loops: Selection Noise, Lock-in, and Acceptance Rules

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Meta · Microsoft |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2610.09239) |
| **Evidence tier** | B: quantifies how keep-if-better selection overstates controller gains; tests GEPA and MIPROv2; no compiler benchmark |
| **Version / reviewed** | October 2026 (cs.LG, cs.AI); arXiv paper text reviewed by Claude 25 November 2026 |

## Key contributions

Treats the keep-if-better step of a self-improvement loop as selection under measurement noise. When candidates are scored on a small selection set, the best-scoring candidate is often just lucky (the **winner's curse**), and the loop locks in its inflated score. The paper models this, measures it with a 600-item held-out set per task, and tests acceptance rules meant to correct it.

## Summary

Qwen models (Qwen2.5-1.5B and 7B-Instruct for the main loops, Qwen2.5-14B as a stronger proposer, Qwen3.5-4B, and Qwen3.8-27B as GEPA's reflection model) rewrite their own instructions on TREC, Banking77 and GSM8K. Every rewrite is also scored on 600 held-out gold items per task, which the loop never sees.

## Key takeaways

- After the first generation, only **4–39%** of rewrites beat the instruction they replaced. The first rewrite of the seed often did improve it (75–100% of first-generation candidates on TREC).
- Final selection-set score minus held-out score: **13.6 ± 1.7 points with 16 selection items**, **1.7 ± 0.6 with 256** (confirmatory greedy runs). The abstract states 13–20 and 1–5 points.
- Scoring the starting and current instruction on 64 items never used for selection removes the average bias, but a single estimate is still off by about 6 points (RMSE 5.7).
- **GEPA** with 16 validation items reported 38.8 points on TREC for a real gain of 19.2, and 18.8 points on Banking77 for a real gain of 1.2 ± 1.7. On GSM8K it reported 6.2 points for a program 0.9 points worse than the seed. **MIPROv2** with 16 items on Banking77 produced programs 1.6 points worse than the seed while its validation scores implied +5.
- None of the tested acceptance rules (McNemar, an anytime-valid test, select-then-confirm, two Bayes gates) beat greedy acceptance over whole runs. The fix the authors recommend is reporting held-out gains with uncertainty.

## Why it matters for this survey

[GEPA](gepa.md) is the survey's one Tier A source for evolving controller instructions on kernel tasks. This paper shows that GEPA's validation scores can overstate real gains by large margins when selection sets are small. It does not test GEPA's kernel result (NPU vector utilization from 4.25% to 26.85%), and that utilization measure is not on the same scale as these task-accuracy points, so the two cannot be compared directly. It does mean that any controller-change claim, compiler ones included, needs a selection-free held-out score of the start and end versions with its uncertainty. A compiler workload suite is often small, which is the regime where the curse is worst.

## Limits / caveats

Classification and arithmetic tasks with small models, not kernels or compilers. The size of the effect depends on task noise, so the 16-versus-256 numbers do not transfer as constants. GEPA's kernel experiments were not re-run here, and whether their selection protocol had the same small-set exposure is not checked. Two authors and no peer-reviewed venue yet. A pre-registered study is reported; what would strengthen the conclusion for this survey is a held-out rescoring of a published kernel-prompt optimization run.
