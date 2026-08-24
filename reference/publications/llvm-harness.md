# Agentic Harness for Real-World Compilers (llvm-harness)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | SUSTech · ETH Zurich · The Chinese University of Hong Kong |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Source control & review agents |
| **Link** | [https://arxiv.org/abs/2603.20075](https://arxiv.org/abs/2603.20075) |
| **Evidence tier** | **A** — compiler-specific tools + llvm-bench; job (c) harness, not generic SWE |
| **Also** | [https://github.com/dtcxzyw/llvm-harness](https://github.com/dtcxzyw/llvm-harness) |

## Key contributions

- **llvm-harness:** agent-friendly LLVM tools, domain skills, and two PoC agents — `llvm-autofix-mini` (middle-end repair) and `llvm-autoreview` (PR review; Archer lineage).
- **llvm-bench:** 334 reproducible LLVM *middle-end* bugs (crashes + miscompiles), ~1.4 reproducers and 722 regression tests each; easy/medium/hard splits; **llvm-bench live** = last-year subset.
- Frontier models drop from ~60% on SWE-bench Verified-class work to ~38% on llvm-bench live; harness lifts ~**62%**; autofix-mini beats harness-enhanced SOTA by ~**22%**. After LLVM-developer review, true end-to-end fix rate stays **below 22%**.
- GitHub (2026-05): Archer integrated into `llvm-autoreview`; &gt;50 real LLVM bugs claimed via PR review.

## Summary

March 2026 systems paper (updated harness through mid-2026) arguing that compiler engineering is *not* generic SWE: sparse bug reports, deep IR/pass expertise, and miscompile risk need a specialized tool/skill/bench stack. Complements Archer (oracle-gated *review*) with a *repair* harness and a living bug ladder. Expert review is the real admit gate for “fixed.”

## Key takeaways

- Job **(c)** needs **compiler-shaped tools + oracles**, not a larger generic coding agent (**C7-B**).
- llvm-bench live is a T8-adjacent rung for *compiler correctness engineering* (crashes/miscompiles), orthogonal to KernelBench serving ladders.
- Sub-22% true-fix after human review is a **shipping bound**: agents draft, humans/oracles admit (A1, C6-B).
- Missed in the prior August digest wave; still the best public LLVM-agent *harness* paper.

## Why it matters for this survey

Tier A for engineering/review (job c) and **C7**. Cite with [Archer](archer-paper.md). Do not read as “agents replace compiler engineers.”

## Limits / caveats

- Middle-end only; performance bugs explicitly deprioritized.
- True-fix rate after expert review is the number that matters — raw agent pass rates overstate.
- Repair ≠ optimization; does not move C1/C2/C4.
