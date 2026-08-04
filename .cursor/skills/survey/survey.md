# Experience notes (this living survey)

Lessons from turning a bibliography into a **prediction + roadmap + commercialization + visual/PDF** artifact.

## What worked

1. **Prediction-first framing** — Lead with “what wins ~2027–28 / 5 years.” Digests become purposeful; without it the repo is an awesome-list.
2. **Agentic compiler as the single target** — SW stack reshape and HW codesign stay coherent when both serve that target. Pure EDA drifts.
3. **Four agent jobs** — Online / offline heuristics / oracle review / **bring-up-codesign**. Collapsing to “agents in compilers” loses roadmap clarity.
4. **Hybrid clarified for readers** — Data-plane parts *can* be agent-generated (Magellan C++, TritorX kernels) but must **admit then execute classically**. Concern is free IR/`opt` replacement (mlirAgent below-identity; C3/C6), not “agents never touch the data plane.”
5. **Conflicts register** — Vendor headlines vs docs, Magellan vs MLGO, coverage vs peak, codesign vs autonomous chip. Settlement signals prevent false consensus.
6. **Evidence tiers A/B/C** — Demote generic SCM AI; promote negative results as architecture bounds.
7. **CLAIMS.md IDs** — Update the map without rewriting the whole narrative.
8. **Thin narrative edits** — Digest → INDEX first; deepen SURVEY §5 / STACK only when claims move.
9. **Org + Publisher on every digest** — Company/university/lab + venue/host; INDEX columns; validate requires fields; `apply_org_publisher.py` META map + rebuild for 7-column INDEX rows.
10. **Vision lineage digests** — e.g. Compiler 2.0 (CC’20 → CGO’22 → Ken Kennedy 2026) + MOCHA funded path; SURVEY §1.5 vision map. Use **full paper titles** in INDEX (short names hid KernelEvolve).
11. **§5.7 commercialization (P1–P23)** — Turning prediction into practice needs ops/business problems, not only architecture: contract (NL vs structured traces vs typed tools), memory (scratchpad ≪ dense ≪ VCS), sub-agents, when-to-run, oracles, ownership, multi-DSL, SKU, then eval, pricing, tenancy, model lock-in, IP, joint versioning, cold start, HITL capacity, flywheel, latency SLOs, DR, A/B, compliance, FSM orchestration, **tokens/inference/capability (P23)**.
12. **P23 conclusion** — Tokens/latency/capability **are** commercial problems for always-on online agents; they **shape the SKU** (freeze artifacts, Amdahl budgets, route/distill) and **falsify LLM-as-`opt` every build**, not the hybrid control-plane bet.
13. **Diagram-first visuals** — `build_visual.py` 1920×1080 posters + full-bleed visual PPTX (not table/bullet decks). Rebuild with PDF after §5/§5.7 moves.
14. **PDF publish pipeline** — Assemble narrative docs (not all digest bodies); include Org note; rebuild after prediction/commercial edits.
15. **Validate early** — INDEX↔file sync, sections, Org/Publisher fields, totals, mojibake.
16. **Work on main** — Living research survey: push `main` after each coherent batch; no PR theater unless asked.

## What hurt / fix next time

| Pain | Fix |
|---|---|
| Windows-only digest generators | Prefer Python; keep PS1 optional |
| UTF-8 BOM + INDEX mojibake | Strip BOM; validate for replacement chars |
| Digests without Evidence tier / Org | Require in template + validate day one |
| Shortened INDEX titles | Always use full paper/talk names (discoverability) |
| Secondary blogs as facts | Primary link rule; secondary = caveat / companion digest |
| Growing Tier C “for completeness” | Explicit demotion in WORKFLOW |
| HW scope creep into EDA | C10: kernels/IR/oracles only |
| Headline speedups in SYSTEMS | Author-reported; prefer mechanisms |
| §5.7 only architecture problems | Survey ops/business too (P9–P23); keep option+pros/cons+lean |
| Forgetting PDF/visuals after narrative | Finish-batch: validate → pdf → visual → pptx → push |
| `apply_org_publisher` INDEX regex stale | Support 7-column rows when regenerating Org/Publisher |
| Confusing “hybrid” with “agents never write passes” | Document offline data-plane synthesis vs online admit |

## Commercialization survey method (§5.7)

When expanding “how to ship the prediction”:

1. Mine §4 gaps, CONFLICTS, Tier A digests (KernelEvolve, TritorX, CompileIQ, ACCLAIM, Magellan, GEAK, Archer, CCC), PRODUCTS.
2. For each problem: **options table + pros/cons + survey lean + “might be true” example**.
3. Separate **architecture** (contract/memory/topology) from **ops** (eval/DR/A/B) from **business** (pricing/tenancy/IP).
4. Resource envelope (tokens, inference latency, model capability) gets an explicit **verdict**: shapes SKU vs falsifies which product story.
5. Close with a checklist buyers/builders can run; point §5.5 success metrics at §5.7.

## Visual / publish method

1. Visuals = one composition per slide (orbit, ladder, bands, gauges)—night-forge palette; avoid purple/cream-terracotta/broadsheet clichés.
2. Editorial PPTX can stay idea-led; visual PPTX embeds PNGs full-bleed.
3. After §5.5 / §5.7 edits: regenerate **both** PDF and visuals before calling the batch done.

## Minimal viable survey (if starting over)

1. One-page future sketch + falsifiers first.
2. SURVEY §5.5 (near + 5yr) and STACK layer table next.
3. 10–15 Tier A digests only (Org/Publisher from day one).
4. CONFLICTS for every disagreement that changes the sketch.
5. CLAIMS map before the 30th digest.
6. §5.7 stub (contract, memory, freeze path, token budget) before claiming “commercial ready.”
7. `validate_survey.py` + `build_pdf.py` + `build_visual.py` before Wave B of sources.

## Success metric

A reader (or the PDF / visual deck) can answer in one sitting:

1. Predicted architecture (agentic control vs classical data plane)?
2. Agent jobs (including codesign bring-up if in scope)?
3. Evidence vs noise (Tier A vs C)?
4. Which conflicts would falsify the sketch?
5. How the stack (and optional HW feedback) reshapes?
6. What must be solved to ship commercially (contract, memory, admit, freeze, tokens)—and the P23 resource verdict?
