---
name: survey
description: >-
  Maintain this living survey on main: SURVEY.md first (review → write/refine
  narrative until settled), then publish slides/PDF. One reading path (§0–§9),
  reference/ evidence, prediction digests, conflicts/claims, validate, push
  main directly (no feature branches/PRs). Use when editing this repo,
  adding publications, updating the prediction, or publishing.
---

# AI compiler survey (this repo)

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
3. Refine in SURVEY.md until the section settles
4. Only then update publish/ Beamer slides + rebuild briefing PDF
5. validate → survey PDF → (beamer if settled) → STATUS → push main
```

**Do not** invent or rearrange the expert briefing from slides alone. Slides are a **downstream view** of settled SURVEY prose (self-contained on-slide, but sourced from the narrative). If the user asks for a new prediction topic (e.g. technical techniques to accelerate checkpoints), write it into **SURVEY §5** (or the fitting section) and refine there first; defer Beamer until they say it is settled or explicitly ask for slides.

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
| Expert Beamer deck | `python3 publish/build_beamer.py` → `publish/out/next-gen-ai-compiler-expert-briefing.pdf` |
| Status | `STATUS.md` |

## Hard rules

1. Prediction target = **agentic compiler** (jobs a–d). HW only via kernels/IR/oracles (**C10**).
2. Never average Magellan vs MLGO, vendor vs KernelBench-X, coverage vs peak — use SURVEY §6.
3. Prefer Tier A (ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer, …).
4. Hybrid = agents may **synthesize data-plane artifacts offline** that **admit then execute classically**; not LLM-as-`opt` online without admit (**C3/C6/A5**).
5. **One reading path** — narrative in SURVEY; evidence in `reference/`. When consolidating: keep all IDs/tables/mechanisms; retarget every link (README, digests, `assemble.py` rewrite map, skills, STATUS).
6. **Git: `main` only.** Stay on `main`; commit; `git push origin main`. Do **not** create feature branches (`cursor/*` or otherwise), do **not** open PRs/MRs — living survey, push direct unless the user explicitly asks otherwise.
7. After **settled** narrative batches: `validate` → survey **PDF** → push. Beamer only after the SURVEY text for that topic has settled (or the user explicitly asks for slides).
8. Cite **external primary sources** only — never this survey’s own repo URL/name in digests, covers, or prediction text.
9. **SURVEY → refine → slides** — never slides-first for new prediction content.

## Finish-batch checklist

```text
[ ] Digests have Org + Publisher; INDEX titles are full paper names
[ ] python3 scripts/validate_survey.py  → OK
[ ] SURVEY narrative updated/refined first (prediction topics settle in SURVEY.md)
[ ] SURVEY §6 / §7 / §5 touched if prediction moved
[ ] §5.7 updated if commercialization blockers discovered
[ ] No new satellite docs that fragment the reading path
[ ] python3 publish/build_pdf.py
[ ] python3 publish/build_beamer.py   # ONLY after SURVEY section settled / user asks
[ ] STATUS.md changelog
[ ] git checkout main (if needed) → commit → git push origin main
    # no feature branch, no PR
```

Full method + experience log: [`survey.md`](survey.md).
