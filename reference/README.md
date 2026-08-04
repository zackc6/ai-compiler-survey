# Reference

Evidence store for the living survey. Digests, product signals, and repo/forge maps live here; the **prediction narrative** stays in [`../docs/SURVEY.md`](../docs/SURVEY.md) (§0–§9).

## Start here

| Category | Path | What it is |
|---|---|---|
| **Publications** | [`publications/`](publications/) · [`INDEX.md`](publications/INDEX.md) | One digest per searched source (papers, blogs, talks, code pages). ★ = prediction-critical. |
| **Products** | [`products.md`](products.md) | Commercial SKUs / offerings as **prediction signals** (Tier A/B/C) — not a full catalog. |
| **Repos** | [`repos.md`](repos.md) | GitHub / Gerrit / forge artifacts tiered for the agentic-compiler prediction — not an exhaustive forge list. |

## How to use

1. Read [`../docs/SURVEY.md`](../docs/SURVEY.md) §0 → §5 for the prediction (roadmap §5.5, stack §5.6, commercial §5.7).
2. Open ★ digests from [`publications/INDEX.md`](publications/INDEX.md) when you need mechanism detail.
3. Use [`products.md`](products.md) / [`repos.md`](repos.md) for Tier A/B/C shipping surfaces (CompileIQ, GEAK, ACCLAIM, Archer, …).
4. When sources disagree → [`../docs/SURVEY.md`](../docs/SURVEY.md) **§6**. Claim IDs → **§7**. Systems snapshot → **§8**.

## Add a source

1. Create a digest from [`publications/_TEMPLATE.md`](publications/_TEMPLATE.md) (**Org** + **Publisher** required).
2. Add an INDEX row (★ only if it moves the prediction).
3. Update `products.md` / `repos.md` only if the mechanism is a new shipping surface.
4. Update SURVEY **§6 / §7** if a durable claim or disagreement moved; thin-touch §5 if the prediction moves.
5. Follow [`../docs/SURVEY.md`](../docs/SURVEY.md) **§9** (How to update this survey).
6. `python3 scripts/validate_survey.py`

Do **not** paste long digests into `docs/SURVEY.md`. Keep the narrative thin; park evidence here. The survey points into this tree.

## Related narrative

- [`../docs/SURVEY.md`](../docs/SURVEY.md) — single reading path: vocabulary (§0), Q1–Q4, prediction (§5), conflicts (§6), claims (§7), systems (§8), update loop (§9)
