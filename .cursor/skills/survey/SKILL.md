---
name: survey
description: >-
  Maintain this living survey on main: one SURVEY reading path (§0–§9),
  reference/ evidence store, prediction-first digests (Org/Publisher),
  §6 conflicts / §7 claims, §5 architecture+roadmap+commercialization,
  validate, rebuild PDF, push main. Use when editing
  this repo, adding publications, reorganizing docs, updating the
  agentic-compiler prediction, or publishing.
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
| §5 | Prediction (architecture, roadmap §5.5, stack §5.6, commercial §5.7) |
| §6 | Conflicts C1–C10 (never average) |
| §7 | Claims map A/P/S/H |
| §8 | Systems gallery |
| §9 | How to update (add-source loop) |

**Rule:** Do not revive satellite narrative files (`ROADMAP`, `STACK`, `CLAIMS`, `CONFLICTS`, `TAXONOMY`, `SYSTEMS`, `WORKFLOW`, `COMPARISON`, …). Fold into SURVEY sections. Park catalogs/digests under `reference/`. No circular SURVEY↔satellite pointers.

## Paths

| Step | Path |
|---|---|
| North star / future | `docs/SURVEY.md` §0.1, §5 |
| Architecture / roadmap / stack | `docs/SURVEY.md` **§5.1** / **§5.5** / **§5.6** |
| **Commercialization** | `docs/SURVEY.md` **§5.7** (P1–P23) |
| Vocabulary / systems | `docs/SURVEY.md` §0.2 / §8 |
| Claims / conflicts | `docs/SURVEY.md` §7 / §6 |
| Add-source loop | `docs/SURVEY.md` §9 |
| **Reference guide** | `reference/README.md` → publications / products / repos |
| Digest template | `reference/publications/_TEMPLATE.md` (**Org** + **Publisher** required) |
| Index | `reference/publications/INDEX.md` (★ = prediction-critical) |
| Org sync helper | `python3 scripts/apply_org_publisher.py` |
| Validate | `python3 scripts/validate_survey.py` |
| PDF | `python3 publish/build_pdf.py` |
| Status | `STATUS.md` |

## Hard rules

1. Prediction target = **agentic compiler** (jobs a–d). HW only via kernels/IR/oracles (**C10**).
2. Never average Magellan vs MLGO, vendor vs KernelBench-X, coverage vs peak — use SURVEY §6.
3. Prefer Tier A (ACCLAIM, Magellan, TritorX, KernelEvolve, Kernel*, CompileIQ, Archer, …).
4. Hybrid = agents may **synthesize data-plane artifacts offline** that **admit then execute classically**; not LLM-as-`opt` online without admit (**C3/C6/A5**).
5. **One reading path** — narrative in SURVEY; evidence in `reference/`. When consolidating: keep all IDs/tables/mechanisms; retarget every link (README, digests, `assemble.py` rewrite map, skills, STATUS).
6. Work on **`main`**, commit, **`git push origin main`** — no PRs unless asked.
7. After narrative batches: `validate` → **PDF** → push.
8. Cite **external primary sources** only — never this survey’s own repo URL/name in digests, covers, or prediction text.

## Finish-batch checklist

```text
[ ] Digests have Org + Publisher; INDEX titles are full paper names
[ ] python3 scripts/validate_survey.py  → OK
[ ] SURVEY §6 / §7 / §5 touched if prediction moved
[ ] §5.7 updated if commercialization blockers discovered
[ ] No new satellite docs that fragment the reading path
[ ] python3 publish/build_pdf.py
[ ] STATUS.md changelog
[ ] git commit && git push origin main
```

Full method + experience log: [`survey.md`](survey.md).
