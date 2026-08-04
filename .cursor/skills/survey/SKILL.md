---
name: survey
description: >-
  Maintain this living survey on main: prediction-first digests (Org/Publisher),
  CLAIMS/CONFLICTS, SURVEY §5 (architecture + roadmap + commercialization),
  validate, rebuild PDF + diagram visuals + PPTX, push main. Use when
  editing this repo, adding publications, updating the agentic-compiler
  prediction, or publishing.
---

# AI compiler survey (this repo)

| Step | Path |
|---|---|
| North star / future | `docs/SURVEY.md` §0.1, §5 |
| Architecture / roadmap / stack | `docs/SURVEY.md` **§5.1** / **§5.5** / **§5.6** |
| **Commercialization** | `docs/SURVEY.md` **§5.7** (P1–P23) |
| Claims / conflicts | `docs/CLAIMS.md`, `docs/CONFLICTS.md` |
| Add-source loop | `docs/WORKFLOW.md` |
| **Reference guide** | `reference/README.md` → publications / products / repos |
| Digest template | `reference/publications/_TEMPLATE.md` (**Org** + **Publisher** required) |
| Index | `reference/publications/INDEX.md` (Org/Publisher columns; ★ for prediction-critical) |
| Org sync helper | `python3 scripts/apply_org_publisher.py` (after META map edits) |
| Validate | `python3 scripts/validate_survey.py` |
| PDF | `python3 publish/build_pdf.py` → `publish/out/next-gen-ai-compiler-survey.pdf` |
| Editorial PPTX | `python3 publish/build_pptx.py` |
| **Visual pack** | `python3 publish/build_visual.py` → `out/visual/*.png` + `*-visual.pptx` |
| Status | `STATUS.md` |

## Hard rules

1. Prediction target = **agentic compiler** (jobs a–d). HW only via kernels/IR/oracles (**C10**).
2. Never average Magellan vs MLGO, vendor vs KernelBench-X, coverage vs peak — use CONFLICTS.
3. Prefer Tier A (ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer, …).
4. Hybrid means **agents can generate data-plane artifacts offline** (heuristics/kernels) that **execute classically**; it does **not** mean LLM-as-`opt` online without admit (**C3/C6/A5**).
5. Work on **`main`**, commit, **`git push origin main`** — no PRs unless asked.
6. After narrative batches: `validate` → **PDF + visual + pptx** → push.
7. Cite **external primary sources** only — do not reference this survey’s own repository URL/name in digests, covers, or prediction text.

## Finish-batch checklist

```text
[ ] Digests have Org + Publisher; INDEX titles are full paper names
[ ] python3 scripts/validate_survey.py  → OK
[ ] CLAIMS / CONFLICTS / SURVEY §5 touched if prediction moved
[ ] §5.7 updated if commercialization blockers discovered
[ ] python3 publish/build_pdf.py
[ ] python3 publish/build_visual.py   # diagram-first, not table slides
[ ] python3 publish/build_pptx.py     # optional editorial deck
[ ] STATUS.md changelog
[ ] git commit && git push origin main
```

Full method + experience log: [`survey.md`](survey.md).
