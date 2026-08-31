# Agent Skills (`SKILL.md`) open specification

| Field | Value |
|---|---|
| **Year** | 2025–26 |
| **Org** | Anthropic (origin) · agentskills.io ecosystem |
| **Publisher** | agentskills.io / GitHub · Anthropic Engineering |
| **Type** | company |
| **Group** | Agent control-plane substrate |
| **Link** | [https://agentskills.io/specification](https://agentskills.io/specification) |
| **Also** | [GitHub spec](https://github.com/agentskills/agentskills) · [Anthropic engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
| **Evidence tier** | **B** — de facto **packaging** format for agent procedures; not a compiler admit surface |

## Key contributions

- A **skill** is a directory with `SKILL.md`: YAML frontmatter (`name`, `description`, optional license / compatibility / metadata / `allowed-tools`) plus Markdown instructions; may bundle `scripts/`, `references/`, `assets/`.
- **Progressive disclosure:** load name+description for every installed skill (~100 tokens); load the body only when matched; load extra files on demand.
- Originated at Anthropic (Claude Skills, 2025); published as an open spec (2025-12). Adopted by many coding-agent products. [CompileIQ agent-skills](compileiq-agent-skills.md) already follows this convention.

## Summary

This is the *language* of portable agent procedures — analogous to digesting CuTe DSL because agents sit on it, not only CuTeGen. It is **intent/action packaging** (P1 option A/D), not a typed compile interface (T1) and not an admit record (T3). Scripts inside a skill can be classical code; the Markdown body is still interpreted by the model unless a **skill compiler** (SIGIL / SkCC / SkVM) lowers it.

## Key takeaways

- **P1/P2:** `SKILL.md` is a reusable prompt+resource pack with cheap discovery. It is not `{graph_hash, hw, compiler, oracle, digest}`. Chat/skill UX must stay a *view* over traces if used on a compile SLA path.
- **Three senses of “skill”** in this survey: (1) vendor **compile** packs (CompileIQ, TRT-LLM); (2) this **SKILL.md** format; (3) **skill compilation / execution state** (SIGIL, SkCC, SkVM, SKILL.state). Do not collapse them.
- **C7:** installing a compiler-themed skill does not make the harness a compiler oracle.

## Why it matters for this survey

CompileIQ already named the convention with **no spec digest** (same class of miss as a named kernel DSL without a language digest). Substrate for T10 skill-compile papers. Does **not** settle C3/C6.

## Limits / caveats

- Spec does not require oracles, replay keys, or fail-closed quality gates.
- Community skill corpora have reported malware/injection risk (cited by SkCC); treat untrusted skills as untrusted code.
- Adoption counts in secondary blogs are not Tier A.
