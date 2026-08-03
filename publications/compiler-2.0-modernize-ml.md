# Compiler 2.0: Using Machine Learning to Modernize Compiler Technology

| Field | Value |
|---|---|
| **Year** | 2020 |
| **Org** | MIT CSAIL |
| **Publisher** | ACM CC 2020 |
| **Type** | talk |
| **Group** | Surveys & vision |
| **Link** | [https://doi.org/10.1145/3372799.3397167](https://doi.org/10.1145/3372799.3397167) |
| **Evidence tier** | **B** — early public ML-modernization manifesto + concrete Ithemal/Vemal path |
| **Venue** | CC 2020 invited talk (ACM DL) |

## Key contributions

- States that mainstream compilers still rely on decades-old algorithms for core analyses and opts (lexing through scheduling).
- Walks a modernization path for **vectorization**: SLP → goSLP (ILP packing) → **learned** cost model (**Ithemal**) and end-to-end vectorization policy (**Vemal**).
- Thesis: automatically **learning** compiler components beats hand-maintaining heuristics and analytical cost models as architectures churn.

## Summary

Invited talk that operationalizes “Compiler 2.0” before the LLM era: replace brittle hand cost models and greedy packing heuristics with data-driven predictors and imitation/RL policies, while keeping transformations in a correctness-preserving formulation. Ithemal reportedly more than halves error vs llvm-mca-class tools on x86 basic-block throughput; Vemal outperforms LLVM SLP heuristics by imitating goSLP’s ILP decisions.

## Key takeaways

- Direct ancestor of later Compiler 2.0 keynotes: same modernization slogan, concrete MLGO-adjacent mechanisms.
- Learned **cost models + policies** sit inside classical compilers — hybrid pattern consistent with **A1/A5**.
- Complements Magellan (synthesize C++ heuristics) and MLGO (neural advisors): another “ship learned components, keep legality” bet (**C1**).

## Why it matters for this survey

Fills the Surveys & vision gap between classic MLGO papers and 2025–26 agentic systems. Cite when tracing Compiler 2.0 → MOCHA verified rewrite synthesis.

## Limits / caveats

- Scope is mainly vectorization / block throughput, not GPU kernel agents or whole-program formal.
- ACM talk abstract; prefer Ithemal/Vemal papers for numbers in deep dives.
