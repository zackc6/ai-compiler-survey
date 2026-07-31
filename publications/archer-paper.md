# Archer: Towards Agentic Review for Compiler Optimizations

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Type** | paper |
| **Group** | Source control & review agents |
| **Link** | [https://arxiv.org/html/2607.01808](https://arxiv.org/html/2607.01808) |

## Key contributions

- First agentic review tool specialized for compiler optimization patches
- Obligation-guided analysis from historical bug fixes
- Deterministic validation guard (Alive2/LLUBI/opt) before admitting findings
- Evaluated on hundreds of recent LLVM GitHub PRs

## Summary

Presents Archer, an LLM agent that reviews LLVM optimization PRs with compiler-specific knowledge and executable evidence, reporting high rates of semantic bugs in open and closed PRs and arguing that generic code-review agents are insufficient for compilers.

## Key takeaways

- SCM (GitHub PRs) is a first-class surface for AI-compiler agents
- Evidence-gated comments are the right pattern for HITL
- Directly supports survey gaps 4.2, 4.5, 4.8

## Why it matters for this survey

Mapped in `docs/REPOS.md` to SCM/review context and to gaps in `docs/SURVEY.md` 搂4. Prefer the primary link above when citing.
