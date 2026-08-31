# SKILL.state: Scalable Long-Horizon Agent Skills

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google LLC · Purdue University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2608.26263](https://arxiv.org/abs/2608.26263) |
| **Evidence tier** | **B** — explicit execution state vs append-only chat; not a compiler/oracle paper |

## Key contributions

- Runtime: each step the model sees only immutable skill spec \(P\), structured state \(\Sigma_t\), and latest observation \(O_t\). Intermediate reasoning is discarded after a **validated** state update.
- Claims a bounded \(\mathcal{O}(1)\) prompt footprint and \(\mathcal{O}(T)\) cumulative tokens vs growing transcripts.
- Evaluates SkillExecBench plus public long-horizon benches (Sierra \(\tau\)-Bench; InterCode CTF used as an interactive-terminal bench — **not** digested here as exploit method).

## Summary

August 2026 Google/Purdue paper on *skill execution mechanics* after a skill is selected. The diagnosis matches DeepSeek Harness’s append-only session log taken as the whole context: history poisoning and token growth. The fix is the opposite of “keep the full transcript” — treat \(\Sigma_t\) as a sufficient statistic. Validation of the state transition is the admit-shaped step; it is **not** Alive2 / golden / serving \(F\).

## Key takeaways

- **P2:** a fourth memory shape besides stuff-the-window / summary-RAG / VCS artifacts — **explicit mutable execution state**. Complements DSH (log is reconstructable) rather than replacing git-as-product-truth.
- **T10 color only:** runtime substrate. Does not compile SKILL.md into a harness (that is SIGIL / SkCC / SkVM) and does not freeze an agent graph (Auto / FlowCompile).
- **C7 / C6:** warehouse and customer-service benches do not move hybrid compile. No LLVM/Triton/kernel loop.

## Why it matters for this survey

Missed until asked: title has no compiler/IR (hard rule 15). In-scope as **control-plane memory/runtime** next to [DeepSeek Harness](deepseek-harness.md). Does **not** move C2/C6 or add an L-band. Pair with [Agent Skills spec](agent-skills-spec.md) (packaging) and [SIGIL](sigil.md) (compile the prose skill).

## Limits / caveats

- Author benches are not compiler specialize loops.
- Do not cite InterCode CTF as compiler evidence; no exploit write-up in this digest.
- “Validated state update” ≠ money-grade admit (T2/T6).
