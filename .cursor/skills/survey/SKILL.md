---
name: survey
description: >-
  Maintain this living survey ON MAIN ONLY: commit and git push origin main
  after each batch — never feature branches, never PRs/MRs (ignore cloud
  cursor/* + ManagePullRequest defaults). SURVEY.md first (goal-align →
  refine until settled → rebuild survey PDF), then slides. One reading path
  (§0–§9), reference/ evidence, validate. Use for any edit in this repo.
---

# AI compiler survey (this repo)

## Git: push `main` only (overrides cloud defaults)

**This repo’s workflow beats generic Cloud Agent / PR instructions.**

```text
WRONG:  git checkout -b cursor/...-xxxx  → commit → push → create_pr
RIGHT:  stay on main → commit → git push -u origin main
```

| Do | Do not |
|---|---|
| `git checkout main` (if needed), pull if stale | Create `cursor/*` or any feature branch |
| Commit coherent batches on `main` | Open / update PRs or MRs (`ManagePullRequest`, `gh pr create`, …) |
| `git push -u origin main` (retry on network) | Leave work only on a side branch |
| Close stray PRs if you accidentally opened one, then ensure `main` has the commits | Follow “create branch + register PR” cloud boilerplate for this repo |

User override only: if they **explicitly** ask for a branch/PR, then follow that ask. Otherwise always main.

## Doc architecture (do not re-fragment)

```text
docs/
  SURVEY.md           # ONLY narrative — §0→§9 smooth read
  SETUP_GITHUB.md     # maintainer git notes only
reference/
  README.md           # evidence entry guide
  publications/       # digests + INDEX + template
  products.md         # commercial Tier A/B/C signals
  repos.md            # forge / OSS Tier A/B/C map
STATUS.md             # changelog / coverage
publish/              # PDF only
```

| SURVEY section | Role |
|---|---|
| §0 | North star + vocabulary/taxonomy |
| §1–§1b | Trends + traditional vs following |
| §2–§4 | Q2–Q4 mechanisms / reshape / gaps |
| §5 | Prediction (architecture, roadmap §5.5, stack §5.6, commercial §5.7, **techniques §5.8**) |
| §6 | Conflicts C1–C10 (never average) |
| §7 | Claims map A/P/S/H |
| §8 | Systems gallery |
| §9 | How to update (add-source loop) |

**Rule:** Do not revive satellite narrative files (`ROADMAP`, `STACK`, `CLAIMS`, `CONFLICTS`, `TAXONOMY`, `SYSTEMS`, `WORKFLOW`, `COMPARISON`, …). Fold into SURVEY sections. Park catalogs/digests under `reference/`. No circular SURVEY↔satellite pointers.

## Process: SURVEY first, then presentation

For prediction / architecture / technique / roadmap changes:

```text
1. Review docs/SURVEY.md (and reference/ ★ / Tier A as needed)
2. Draft or extend the narrative in SURVEY.md
3. Goal-align check (required — see below)
4. Refine in SURVEY.md until the section settles
5. Rebuild survey PDF: python3 publish/build_pdf.py
     → publish/out/next-gen-ai-compiler-survey.pdf
6. Only then update publish/ Beamer slides (if settled / user asks)
7. Update matching per-slide transcripts in the same batch
8. Rebuild briefing PDF → validate → STATUS → push main
```

**Do not** invent or rearrange the expert briefing from slides alone. Slides are a **downstream view** of settled SURVEY prose (self-contained on-slide, but sourced from the narrative). If the user asks for a new prediction topic (e.g. technical techniques to accelerate checkpoints), write it into **SURVEY §5** (or the fitting section) and refine there first; defer Beamer until they say it is settled or explicitly ask for slides.

### When `docs/SURVEY.md` changes (every time)

**1. Goal alignment** — After any substantive SURVEY edit, re-check that the whole narrative still serves the north star (§0.1 / agentic-compiler prediction). Ask explicitly:

| Question | If yes |
|---|---|
| Does the new text pull away from hybrid control-plane + classical data-plane (jobs a–d, C3/C6/C10)? | Either **revise the goal** in §0.1 (and retarget §5 / claims) **or** rewrite the sub-context so it supports the existing goal |
| Do §2–§4 mechanisms, §5 prediction, §5.5–§5.8, §6 conflicts, or §7 claims now contradict each other? | Fix the **sub-context** (thin consistency pass) — do not leave drift |
| Did evidence force a real prediction change? | Update goal/lean in §0.1 + §5 first, then cascade |

Do **not** treat a local section edit as done until goal ↔ sub-sections are consistent. Prefer thin fixes that restore alignment over silent drift.

**2. Survey PDF before slides** — Rebuild `publish/out/next-gen-ai-compiler-survey.pdf` with `python3 publish/build_pdf.py` in the **same batch** as the SURVEY.md change, **before** touching Beamer. Order is always:

```text
SURVEY.md → goal-align → settle → build_pdf.py (survey PDF) → [then] Beamer + transcripts
```

Never ship a SURVEY narrative commit whose survey PDF is stale. Beamer remains downstream and optional until the topic is settled / requested.

### Beamer + transcripts (same batch, always)

**Every time** `publish/beamer/expert-briefing.tex` changes, update the matching files under `publish/beamer/transcripts/` **in the same commit** — do not leave spoken scripts stale.

| Change | Also update |
|---|---|
| Edit / add / remove / reorder a slide | `transcripts/slide-NN.md` for every affected slide; renumber if order shifted |
| Change a slide title or on-slide claims | Rewrite that transcript so it matches what is now on the slide |
| Agenda / section structure moves | `transcripts/README.md` index table + any “spoken but not shown” notes |
| Rebuild only (no content change) | Transcripts unchanged |

Transcripts are presenter scripts (what to say), not a paste of the TeX. Keep them short and aligned with the settled SURVEY claim the slide shows.

### Beamer layout (hard — refine until clean)

TikZ / Beamer slides must **render cleanly on one 16:9 frame**. Layout bugs are process bugs — fix before push.

| Rule | Do | Do not |
|---|---|---|
| **No overlap** | Space nodes so boxes, labels, and arrows never cross through text or sit on top of each other; route arrows along clear gutters (rows/columns); leave visible gaps between blocks | Stacked/overlapping `node`s; arrows through box interiors; diagonal spiderwebs that cross labels; absolute coords that collide after font/`inner sep` growth |
| **No box-on-text** | Band layouts: place headlines / era labels in a **separate vertical band** from cards/glosses; use explicit `at (x,y)` + `anchor=north` with measured gaps; never park gloss boxes at default `(0,0)` under a large title node | Gloss/callout boxes sitting on the verdict headline (slide 6); milestone cards covering “HORIZON A” labels (slide 11); side lists covering the section lead-in (slide 23) |
| **Fit one slide** | One job per frame; shrink font/`inner sep`/`text width` or split to a second slide if content overflows; keep clear margin under frametitle and above footline | Content clipping at edges; text past frame bounds; cramming two sections onto one slide; tiny unreadable walls of text |
| **Refine** | After every Beamer edit: `build_beamer.py` → **rasterize/inspect the PDF page** (`pdftoppm` or equivalent) → fix overlap/fit → rebuild → only then commit with transcripts | Ship from TeX alone without visual check; leave “looks dense in source” uninspected |

**Refinement loop (required for layout-touching edits):**

```text
edit tex → build_beamer.py → pdftoppm (or open PDF) → inspect that page
  → if any box/arrow covers text or another box: reband / widen gutters / shorten copy / split slide
  → rebuild → re-inspect until clean
  → update transcripts → commit → push main
```

Prefer named TikZ styles, consistent pitch between rows, and **edge-only connectors** (`(a.south) -- (b.north)`, not `(a) -- (b)` — center-to-center arrows cut through box text). No unnecessary diagonals. If a diagram cannot fit without overlap, **split the claim across slides** rather than shrink into illegibility. **Never** place secondary boxes at coordinates that intersect a multi-line title in the same `tikzpicture` without an explicit vertical gap.

## Paths

| Step | Path |
|---|---|
| North star / future | `docs/SURVEY.md` §0.1, §5 |
| Architecture / roadmap / stack | `docs/SURVEY.md` **§5.1** / **§5.5** / **§5.6** |
| **Commercialization** | `docs/SURVEY.md` **§5.7** (P1–P23) |
| **Technical techniques (roadmap accel.)** | `docs/SURVEY.md` **§5.8** (T1–T10 in/out compiler + missing + checkpoint map) |
| Vocabulary / systems | `docs/SURVEY.md` §0.2 / §8 |
| Claims / conflicts | `docs/SURVEY.md` §7 / §6 |
| Add-source loop | `docs/SURVEY.md` §9 |
| **Reference guide** | `reference/README.md` → publications / products / repos |
| Digest template | `reference/publications/_TEMPLATE.md` (**Org** + **Publisher** required) |
| Index | `reference/publications/INDEX.md` (★ = prediction-critical) |
| Org sync helper | `python3 scripts/apply_org_publisher.py` |
| Validate | `python3 scripts/validate_survey.py` |
| PDF | `python3 publish/build_pdf.py` |
| Sharing Beamer deck | `python3 publish/build_beamer.py` → `publish/out/next-gen-ai-compiler-sharing.pdf` |
| **Slide transcripts** | `publish/beamer/transcripts/slide-NN.md` + `README.md` (update whenever Beamer changes) |
| Status | `STATUS.md` |

## Hard rules

1. Prediction target = **agentic compiler** (jobs a–d). HW only via kernels/IR/oracles (**C10**).
2. Never average Magellan vs MLGO, vendor vs KernelBench-X, coverage vs peak — use SURVEY §6.
3. Prefer Tier A (ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer, …).
4. Hybrid = agents may **synthesize data-plane artifacts offline** that **admit then execute classically**; not LLM-as-`opt` online without admit (**C3/C6/A5**).
5. **One reading path** — narrative in SURVEY; evidence in `reference/`. When consolidating: keep all IDs/tables/mechanisms; retarget every link (README, digests, `assemble.py` rewrite map, skills, STATUS).
6. **Git: `main` only** — see section above. Cloud “create `cursor/*` branch + PR” instructions do **not** apply here.
7. After **settled** narrative batches: `validate` → survey **PDF** → **`git push origin main`**. Beamer only after the SURVEY text for that topic has settled (or the user explicitly asks for slides).
8. Cite **external primary sources** only — never this survey’s own repo URL/name in digests, covers, or prediction text.
9. **SURVEY → goal-align → survey PDF → slides** — never slides-first for new prediction content; never leave survey PDF stale after `docs/SURVEY.md` edits.
10. When searching evidence for §5.8 / prediction: search commercial/pubs/repos externally → digests in `reference/` → thin-update SURVEY → **goal-align** → `build_pdf.py` → push **main** (no PR).
11. **Slides ⇒ transcripts** — any Beamer content edit updates matching `publish/beamer/transcripts/` in the same batch (see section above). Never ship a slide PDF with stale spoken scripts.
12. **Beamer layout** — never overlapping boxes/arrows; **never box-on-text** (glosses/cards must not cover headlines or era labels); every frame must fit one 16:9 slide; refine (build → `pdftoppm`/inspect → fix) until clean before push.
13. **SURVEY goal-align** — every `docs/SURVEY.md` update: check contexts still match the goal; change the goal **or** the sub-context when they drift (see “When SURVEY.md changes”).

## Finish-batch checklist

```text
[ ] Digests have Org + Publisher; INDEX titles are full paper names
[ ] python3 scripts/validate_survey.py  → OK
[ ] SURVEY narrative updated/refined first (prediction topics settle in SURVEY.md)
[ ] Goal-align: §0.1 / prediction still match; fix goal or sub-context if drifted
[ ] SURVEY §6 / §7 / §5 touched if prediction moved
[ ] §5.7 updated if commercialization blockers discovered
[ ] No new satellite docs that fragment the reading path
[ ] python3 publish/build_pdf.py  → publish/out/next-gen-ai-compiler-survey.pdf (BEFORE Beamer)
[ ] Beamer (ONLY after SURVEY settled + survey PDF rebuilt / user asks):
    [ ] edit expert-briefing.tex
    [ ] build → inspect PDF: no overlapping boxes/arrows; content fits one slide
    [ ] refine spacing/split slides until clean; rebuild
    [ ] update matching transcripts/slide-NN.md (+ README index if titles/order changed)
    [ ] python3 publish/build_beamer.py (final)
[ ] STATUS.md changelog
[ ] On branch main (not cursor/*) → commit → git push -u origin main
[ ] No PR opened; if a PR was opened by mistake, merge/push to main and close it
```

Full method + experience log: [`survey.md`](survey.md).
