# Experience notes (ai-compiler-survey)

Lessons from turning a bibliography into a **prediction + roadmap + PDF** artifact.

## What worked

1. **Prediction-first framing** — Lead with “what wins ~2027–28 / 5 years.” Digests become purposeful; without it the repo is an awesome-list.
2. **Agentic compiler as the single target** — SW stack reshape and HW codesign stay coherent when both serve that target. Pure EDA drifts.
3. **Four agent jobs** — Online / offline heuristics / oracle review / **bring-up-codesign**. Collapsing to “agents in compilers” loses roadmap clarity.
4. **Conflicts register** — Vendor headlines vs docs, Magellan vs MLGO, coverage vs peak, codesign vs autonomous chip. Settlement signals prevent false consensus.
5. **Evidence tiers A/B/C** — Demote generic SCM AI; promote negative results (mlirAgent below-identity) as architecture bounds.
6. **CLAIMS.md IDs** — Update the map without rewriting the whole narrative.
7. **Thin narrative edits** — Digest → INDEX first; deepen §5/ROADMAP/STACK only when claims move.
8. **PDF publish pipeline** — Assemble narrative docs (not 95 digest bodies); rebuild after prediction edits; track PDF on `main`.
9. **Validate early** — INDEX↔file sync, section presence, totals, mojibake catch bulk-generation rot.
10. **Work on main** — For a living personal/research survey, PR theater slows the loop; push `main` after each coherent batch.

## What hurt / fix next time

| Pain | Fix |
|---|---|
| Windows-only digest generators | Prefer Python; keep PS1 optional |
| UTF-8 BOM + INDEX mojibake | Strip BOM; validate for replacement chars |
| Digests without Evidence tier | Require tier in template day one |
| Secondary blogs as facts | Primary link rule; secondary = caveat |
| Growing Tier C “for completeness” | Explicit demotion in WORKFLOW |
| HW scope creep into EDA | C10-style conflict: kernels/IR/oracles only |
| Headline speedups in SYSTEMS | Author-reported; prefer mechanisms |
| Forgetting PDF after narrative edits | Finish-batch checklist includes rebuild |

## Minimal viable survey (if starting over)

1. One-page future sketch + falsifiers first.
2. ROADMAP (near + 5yr) and STACK layer table next.
3. 10–15 Tier A digests only.
4. CONFLICTS for every disagreement that changes the sketch.
5. CLAIMS map before the 30th digest.
6. `validate_survey.py` + `publish/build_pdf.py` before Wave B of sources.

## Success metric

A reader (or the PDF) can answer in one sitting:

1. Predicted architecture (agentic control vs classical data plane)?
2. Agent jobs (including codesign bring-up if in scope)?
3. Evidence vs noise (Tier A vs C)?
4. Which conflicts would falsify the sketch?
5. How the stack (and optional HW feedback) reshapes?
