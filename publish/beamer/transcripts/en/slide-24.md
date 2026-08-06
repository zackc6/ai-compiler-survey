# Slide 24: Blocker 5 — Ownership, security, human review

Blocker five closes the commercial deep-dive. On-slide: three boxes — trusted-base risk, ownership, human-review capacity — plus the bottom callout. Spoken: three pressures, then the lean and C7.

**Trusted-base risk.**
Agent kernels, evolved heuristics, and control files enter the TCB (trusted computing base). A miscompiled kernel or bad Magellan patch ships like any other production code — liability does not care that an LLM drafted it. Oracle admit passing is necessary; it is not sufficient for security review.

**Ownership.**
CODEOWNERS per artifact class, signed provenance on admit records, sandboxed proposal execution. Joint version pins across compiler, model, and agent policy. Customer must own outputs — generic cloud agent terms are not a compiler supply-chain story.

**Human-review capacity.**
Agents raise draft volume; reviewers become the bottleneck. Magellan ships reviewable C++; Archer gates pull requests with oracles. Lean: human CODEOWNER + signed admit + sandbox. Oracle auto-merge only for **narrow** action classes — pragma hints, known-safe tile configs — not open-ended kernel rewrites.

**C7 — demote generic forge AI.**
Bottom callout: GitHub Copilot-class SCM AI ≠ compiler-oracle review. Forge AI helps authors; it does not replace Alive2, golden tests, or serving A/B. Checkpoint C7 says demote generic forge AI for prediction purposes — domain oracles and admit machinery are what matter.

Closing line: freeze artifacts you can regress; sign what you ship; keep humans in the loop for anything that enters the trusted base. Agents multiply drafts — your process must multiply qualified reviewers or narrow the merge surface.
