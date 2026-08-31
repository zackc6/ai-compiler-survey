# SIGIL: Compiling Agent Skills into Typed Harnesses

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Michigan |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2607.27309](https://arxiv.org/abs/2607.27309) |
| **Also** | [https://github.com/sigilagent/sigil](https://github.com/sigilagent/sigil) |
| **Evidence tier** | **B** ★ — **skill compilation**: SKILL.md → AG-IR → executable harness (T10-class); not an AI-for-`opt` compiler |

## Key contributions

- Diagnoses prose skills: the model re-derives control flow every run and **skips mandated steps** (authors: ~66% Applicable-Mandate Compliance on 33 public `SKILL.md` files).
- **Skill compilation:** extract source-grounded requirements → closed Agent Instruction Set → **AG-IR** (ownership, data flow, control flow) → **deterministic** lower to executable Jac/OSP. Model judgment stays in typed slots only.
- Compiled harnesses raise mean AMC to **88.6%** and cut runtime tokens ~2.4–6× (author). Code + docs at sigilagent.

## Summary

Michigan paper that treats `SKILL.md` as **source**, not as the execution IR. Closest cousin in this survey is [FlowCompile](flowcompile.md) / [Auto](auto-agi-compiler.md) / [AgentFlow](agentflow.md): compile or analyze the *agent procedure*. Distinct from [DeepSeek Harness](deepseek-harness.md) (live plugin runtime) and [SKILL.state](skill-state.md) (bounded prompt via \(\Sigma_t\)). Related skill compilers (same wave, **not** averaged): [SkCC](skcc.md) (SkIR + security), [SkVM](skvm.md) (capability AOT/JIT), [SkillSmith](skillsmith.md) (boundary ABI, 2605.15215 — not the co-evolve SkillSmith 2606.01314).

## Key takeaways

- **T10 exists cell grows:** compiling a skill into a typed harness is now a named paradigm, not only workflow-IR papers.
- **Hybrid rhyme, different plane:** “model owns judgment; code owns mechanism” is C6-B *shape* on the **agent** program, not on Inductor/Triton. Do not cite SIGIL as “agents replaced `opt`.”
- **P1/P22:** mandated checks become graph nodes (gates), not hope-the-model-read-the-bullet. Still not serving \(F\) or Alive2.

## Why it matters for this survey

★ for **T10** / §4.6: control-plane *compile* of SKILL.md. Strengthens Horizon B substrate. Does **not** move C2/C6 or job (a) kernel admit. Pair with the [Agent Skills spec](agent-skills-spec.md) (input format).

## Limits / caveats

- Evaluation is public `SKILL.md` files (PDF/CSV/ops), not specialize-a-kernel traces.
- AG-IR is not a shared industry RFC; Jac/OSP is one lowering.
- “Compile oracle” in SIGIL docs is a skill-faithfulness gate, not T2 compiler admit.
