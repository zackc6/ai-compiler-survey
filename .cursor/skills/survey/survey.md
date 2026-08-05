# Experience notes (this living survey)

Lessons from turning a bibliography into a **prediction + roadmap + commercialization + visual/PDF** artifact with a **single smooth reading path**.

## Doc architecture (hard-won)

### What broke reading

Fragmenting the narrative across satellite files (`ROADMAP`, `STACK`, `CLAIMS`, `CONFLICTS`, `TAXONOMY`, `SYSTEMS`, `WORKFLOW`, stub `COMPARISON`, plus `PRODUCTS`/`REPOS` under `docs/`) forced hop-scotch: SURVEY pointed at satellites, satellites pointed back, README listed eight “start here” files. Readers could not follow Q1→prediction→conflicts without losing context. Circular SURVEY↔ROADMAP / SURVEY↔STACK pointers were an immediate smell.

### What fixed it

| Layer | Holds | Does not hold |
|---|---|---|
| `docs/SURVEY.md` §0–§9 | Vocabulary, Q1–Q4, prediction, conflicts, claims, systems, update loop | Long digests, SKU catalogs |
| `docs/SETUP_GITHUB.md` | Maintainer git notes | Narrative |
| `reference/` | Digests, INDEX, products, repos + entry guide | Competing “source of truth” for prediction |

Fold order that worked (information-preserving):

1. **Roadmap / stack** → SURVEY §5.5 / §5.6 (prediction chapter stays contiguous).
2. **Evidence maps** → `reference/` with one `reference/README.md` entry guide.
3. **Taxonomy / comparison stub / conflicts / claims / systems / workflow** → §0.2 / §1b / §6 / §7 / §8 / §9.
4. Delete satellites only after section IDs and substantial lines are present in SURVEY.
5. Retarget **every** consumer: README, STATUS, digests, skills, `publish/assemble.py` `SECTIONS` + `rewrite_links`, helper scripts.
6. Validate + rebuild PDF before calling the batch done.

### Consolidation rules

- **Do not lose information** — compare old headings/IDs (C1–C10, A/P/S/H) and substantial lines against the new sections before delete.
- **Promote stubs away** — a file that only says “see SURVEY §X” is navigation debt; delete it.
- **PDF assemble = narrative-first** — SURVEY + thin reference guide/products/repos/INDEX; never dump all digest bodies.
- **Keep rewrite_links for legacy paths** in `assemble.py` so old digest links still resolve in the bundle.
- **Never re-fragment** — new durable content becomes a SURVEY subsection or a `reference/` evidence file, not a new top-level `docs/*.md` narrative.

### Smooth reading order (ship this in SURVEY header)

1. §0 north star + vocabulary → §1–§1b trends → §2–§4 mechanisms/gaps → §5 prediction.
2. Disagreement → §6; claim IDs → §7; system snapshot → §8.
3. Digests/SKUs/forges stay in `reference/` so the narrative does not become a catalog.
4. Maintainers: §9 + `validate_survey.py`.

## What worked (substance)

1. **Prediction-first framing** — Lead with “what wins ~2027–28 / 5 years.” Digests become purposeful; without it the repo is an awesome-list.
2. **Agentic compiler as the single target** — SW stack reshape and HW codesign stay coherent when both serve that target. Pure EDA drifts.
3. **Four agent jobs** — Online / offline heuristics / oracle review / **bring-up-codesign**. Collapsing to “agents in compilers” loses roadmap clarity.
4. **Hybrid clarified for readers** — Data-plane parts *can* be agent-generated (Magellan C++, TritorX kernels) but must **admit then execute classically**. Concern is free IR/`opt` replacement (mlirAgent below-identity; C3/C6), not “agents never touch the data plane.”
5. **Conflicts register inside the narrative (§6)** — Vendor headlines vs docs, Magellan vs MLGO, coverage vs peak, codesign vs autonomous chip. Settlement signals prevent false consensus. Living next to §5 beats a separate CONFLICTS file.
6. **Evidence tiers A/B/C** — Demote generic SCM AI; promote negative results as architecture bounds.
7. **§7 claim IDs** — Update the map without rewriting the whole narrative.
8. **Thin narrative edits** — Digest → INDEX first; deepen SURVEY §5 only when claims move.
9. **Org + Publisher on every digest** — Company/university/lab + venue/host; INDEX columns; validate requires fields; `apply_org_publisher.py` META map + rebuild for 7-column INDEX rows.
10. **Vision lineage digests** — e.g. Compiler 2.0 (CC’20 → CGO’22 → Ken Kennedy 2026) + MOCHA; SURVEY §1.5. Use **full paper titles** in INDEX (short names hid KernelEvolve).
11. **§5.7 commercialization (P1–P23)** — Ops/business problems, not only architecture: contract, memory, sub-agents, when-to-run, oracles, ownership, multi-DSL, SKU, eval, pricing, tenancy, lock-in, IP, versioning, cold start, HITL, flywheel, latency SLOs, DR, A/B, compliance, FSM, **tokens/inference/capability (P23)**.
12. **P23 conclusion** — Tokens/latency/capability **shape the SKU** (freeze artifacts, Amdahl budgets, route/distill) and **falsify LLM-as-`opt` every build**, not the hybrid control-plane bet.
13. **PDF publish only** — Prefer narrative quality in SURVEY/PDF; do not maintain in-repo diagram PPTX packs (removed).
14. **PDF publish pipeline** — Assemble SURVEY + reference guides (not digest bodies); rebuild after prediction/commercial/doc-structure edits.
15. **Validate early** — INDEX↔file sync, sections, Org/Publisher fields, totals, mojibake.
16. **Work on main only** — Living research survey: stay on `main`, commit, `git push origin main` after each coherent batch. Never create feature branches; never open PRs/MRs unless the user explicitly asks.
17. **Control-plane substrate digests** — Multi-agent workflow compilers / AGI compilers / agent DAG analysis / hetero serving (Auto, FlowCompile, AgentFlow, Hetero) are in-scope evidence for how the control plane is built—not side topics.
18. **One composition docs layout** — Same instinct as frontend “one job per section”: each SURVEY section has one job; evidence lives elsewhere.
19. **SURVEY first, then slides** — Review `docs/SURVEY.md` → draft/refine the section there until settled → only then update Beamer/presentation. Do not invent prediction content in slides ahead of the narrative.
20. **§5.8 technical prediction** — Technique-shaped view to accelerate roadmap/checkpoints: **T1–T5 within compiler/toolchain**, **T6–T10 outside**; each row = exists / missing today / accelerates which C*; shortlist money-grade oracles, replayable artifacts, portable agent interface, open ladder+data. Distinct from §4 (gap severity) and §5.7 (commercial packaging).

## What hurt / fix next time

| Pain | Fix |
|---|---|
| Satellite docs + circular pointers | Single SURVEY path; evidence in `reference/` only |
| Partial link rewrite after fold | Grep for deleted paths; fix README/skills/digests/`assemble.py`/STATUS in the same commit |
| Script crash mid-batch after PDF rebuild | Finish companion rewrites before commit; treat “PDF green” ≠ “links green” |
| Windows-only digest generators | Prefer Python; keep PS1 optional |
| UTF-8 BOM + INDEX mojibake | Strip BOM; validate for replacement chars |
| Digests without Evidence tier / Org | Require in template + validate day one |
| Shortened INDEX titles | Always use full paper/talk names |
| Secondary blogs as facts | Primary link rule; secondary = caveat / companion digest |
| Growing Tier C “for completeness” | Explicit demotion in SURVEY §9 |
| HW scope creep into EDA | C10: kernels/IR/oracles only |
| Headline speedups in §8 | Author-reported; prefer mechanisms |
| §5.7 only architecture problems | Survey ops/business too (P9–P23); options+pros/cons+lean |
| Forgetting PDF after narrative | Finish-batch: validate → pdf → push |
| `apply_org_publisher` INDEX regex stale | Support 7-column rows when regenerating Org/Publisher |
| Confusing “hybrid” with “agents never write passes” | Document offline data-plane synthesis vs online admit |
| Citing this survey’s own repo | External primaries only (covers, digests, prediction text) |
| Feature-branch / PR workflow on this repo | Always push `main` directly; skip `cursor/*` branches and ManagePullRequest unless asked |
| Slides/presentation ahead of SURVEY prose | Write and settle narrative in `docs/SURVEY.md` first; Beamer is a downstream view |

## Commercialization survey method (§5.7)

1. Mine §4 gaps, §6 conflicts, Tier A digests (KernelEvolve, TritorX, CompileIQ, ACCLAIM, Magellan, GEAK, Archer, CCC), `reference/products.md`.
2. For each problem: **options table + pros/cons + survey lean + “might be true” example**.
3. Separate **architecture** (contract/memory/topology) from **ops** (eval/DR/A/B) from **business** (pricing/tenancy/IP).
4. Resource envelope (tokens, inference latency, model capability) gets an explicit **verdict**: shapes SKU vs falsifies which product story.
5. Close with a checklist buyers/builders can run; point §5.5 success metrics at §5.7.

## Publish method

1. After §5.5 / §5.7 / doc-structure edits: regenerate PDF before calling the batch done.
2. `assemble.py` `SECTIONS` should track the live reading path (SURVEY + `reference/` guides), with legacy path rewrites for old digest links.
3. Do not reintroduce in-repo visual/PPTX generators unless explicitly requested.

## Minimal viable survey (if starting over)

1. One-page future sketch + falsifiers first (**in SURVEY**, not a side file).
2. SURVEY §5.5 (near + 5yr) and §5.6 layer table next.
3. 10–15 Tier A digests only under `reference/publications/` (Org/Publisher from day one).
4. SURVEY §6 for every disagreement that changes the sketch.
5. SURVEY §7 claims map before the 30th digest.
6. §5.7 stub (contract, memory, freeze path, token budget) before claiming “commercial ready.”
7. `validate_survey.py` + `build_pdf.py` before Wave B of sources.
8. Resist creating `docs/FOO.md` satellites—add a SURVEY subsection or a `reference/` evidence file.

## Success metric

A reader (or the PDF / visual deck) can answer in one sitting **without opening a second narrative file**:

1. Predicted architecture (agentic control vs classical data plane)?
2. Agent jobs (including codesign bring-up if in scope)?
3. Evidence vs noise (Tier A vs C)?
4. Which conflicts would falsify the sketch?
5. How the stack (and optional HW feedback) reshapes?
6. What must be solved to ship commercially (contract, memory, admit, freeze, tokens)—and the P23 resource verdict?
