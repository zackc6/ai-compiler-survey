# SkCC: Portable and Secure Skill Compilation for Cross-Framework LLM Agents

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Sun Yat-sen University |
| **Publisher** | arXiv · ACM CAIS 2026 (AgentSkills'26) |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2605.03353](https://arxiv.org/abs/2605.03353) |
| **Evidence tier** | **B** — SkIR portable compile + injection analysis; SkillsBench not a compiler ladder |

## Key contributions

- Problem: one `SKILL.md` deployed to many harnesses; format sensitivity (authors: up to ~40% claim) plus community-skill malware/injection (Snyk/ClawHub audit cited).
- **SkIR:** typed IR that decouples skill *semantics* from platform-specific prompt formatting; emitters per harness (\(O(m+n)\) vs \(O(m\times n)\) rewrites).
- Compile-time **Anti-Skill Injection** analyzer. SkillsBench: pass-rate lifts on Claude Code / Kimi CLI (author 21.1%→33.3% / 35.1%→48.7%); sub-10ms compile; token savings 10–46% (author).

## Summary

A classical-compiler story applied to **skill packs**, not to LLVM/Triton. SkIR is an LLM-oriented *skill* IR (kind: portable procedure), not an L4 kernel face and not the shared agent↔compiler contract (T1). Complements [SIGIL](sigil.md) (enforce mandated steps in a harness) and [SkVM](skvm.md) (adapt to model capability). Security analysis is T9-adjacent (untrusted skill = untrusted code).

## Key takeaways

- **P1/P7:** multi-harness skill portability is the same *shape* as multi-DSL compile skills — a shared IR plus emitters, not one Markdown blob.
- **T9:** compile-time injection checks are necessary if a compiler product mounts community `SKILL.md`. They are not CODEOWNERS for admitted kernels.
- **C7:** SkillsBench pass rates are not KernelBench or llvm-bench.

## Why it matters for this survey

Fills the “portable skill contract” hole next to §4.4’s missing agent-compile RFC. Does **not** replace T1 (region/action/admit across MLIR·Triton). Cite with [Agent Skills spec](agent-skills-spec.md).

## Limits / caveats

- Author security/pass numbers; no independent compiler-oracle eval.
- SkIR ≠ Cake IR ≠ AG-IR ≠ survey L1–L7.
- EvoSkill (cited) and Formal Skill / SSL stay **watchlist** — discovery or a different authoring surface, not this compile cluster.
