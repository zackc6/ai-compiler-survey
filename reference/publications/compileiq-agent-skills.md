# CompileIQ agent-skills: AGENTS.md-aware optimization campaigns

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA |
| **Publisher** | NVIDIA CompileIQ docs / GitHub |
| **Type** | company |
| **Group** | Commercial products & proposals |
| **Link** | [https://nvidia.github.io/CompileIQ/stable/install.html](https://nvidia.github.io/CompileIQ/stable/install.html) |
| **Evidence tier** | **A** — vendor ships agent skills as the control-plane UX for compile autotune |

## Key contributions

- Ships an agent-agnostic skill set under `agent-skills/` following the agentskills.io `SKILL.md` convention
- Skills cover bootstrap → booster-pack → search-space → author-objective → run-search → validate-result (Welch t-test) → debug
- Install script mounts skills into Claude Code, Codex, Cursor, Copilot, and other AGENTS.md-aware agents

## Summary

CompileIQ’s product surface is no longer only a Python HPO API that emits ACFs. NVIDIA documents a **coding-agent skill pack** that drives optimization campaigns with an explicit admit step (`compileiq-validate-result`) before shipping. This is a concrete commercial packaging of the hybrid loop: agents orchestrate search; compiler controls + measurement remain the data plane; ACFs stay the portable artifact.

## Key takeaways

- Agent skills are becoming a first-class **SKU interface** for vendor compile autotune (§5.7)
- Recommended order encodes budget discipline: try booster packs before paying for full search
- Validation skill (Welch’s t-test) acknowledges flaky speedups — aligns with gap **4.3**

## Why it matters for this survey

Strengthens online job **(a)** and commercialization claims (P1 contract, P5 when-to-run, P9 eval) without settling **C2** (still no public p50/p90 ACF traces). Complements [`compileiq-docs-expectations.md`](compileiq-docs-expectations.md) and [`compileiq-github.md`](compileiq-github.md).

## Limits / caveats

- Skills automate the search UX; they do not by themselves prove median production wins
- Docs still caveat ~2–3% on highly optimized kernels (**C2** side B)
- Agent coverage depends on the host IDE mounting the skills correctly
