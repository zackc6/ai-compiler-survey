---
name: survey
description: >-
  Maintain ai-compiler-survey on main: prediction-first digests, CLAIMS/CONFLICTS,
  ROADMAP/STACK, validate, rebuild PDF, push main. Use when editing this repo,
  adding publications, updating the agentic-compiler prediction, or publishing PDF.
---

# AI compiler survey (this repo)

Follow the personal **survey** skill with these concrete paths:

| Step | Path |
|---|---|
| North star / future | `docs/SURVEY.md` §0.1, §5 |
| Roadmap / stack | `docs/ROADMAP.md`, `docs/STACK.md` |
| Claims / conflicts | `docs/CLAIMS.md`, `docs/CONFLICTS.md` |
| Add-source loop | `docs/WORKFLOW.md` |
| Digest template | `publications/_TEMPLATE.md` |
| Index | `publications/INDEX.md` |
| Validate | `python3 scripts/validate_survey.py` |
| PDF | `python3 publish/build_pdf.py` → `publish/out/next-gen-ai-compiler-survey.pdf` |
| Status | `STATUS.md` |

## Hard rules

1. Prediction target = **agentic compiler** (jobs a–d). HW only via kernels/IR/oracles (**C10**).
2. Never average Magellan vs MLGO, vendor vs KernelBench-X, coverage vs peak — use CONFLICTS.
3. Prefer Tier A (ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer, …).
4. Work on **`main`**, commit, **`git push origin main`** — no PRs unless asked.
5. After narrative batches: validate → rebuild PDF → push.

Full method + experience: `~/.cursor/skills/survey/SKILL.md` and `survey.md`.
