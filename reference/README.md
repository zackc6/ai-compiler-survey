# Reference

Evidence store for the living survey. Digests, product signals, and repo/forge maps live here; the **prediction narrative** stays in [`../docs/SURVEY.md`](../docs/SURVEY.md).

## Start here

| Category | Path | What it is |
|---|---|---|
| **Publications** | [`publications/`](publications/) · [`INDEX.md`](publications/INDEX.md) | One digest per searched source (papers, blogs, talks, code pages). ★ = prediction-critical. |
| **Products** | [`products.md`](products.md) | Commercial SKUs / offerings as **prediction signals** (Tier A/B/C) — not a full catalog. |
| **Repos** | [`repos.md`](repos.md) | GitHub / Gerrit / forge artifacts tiered for the agentic-compiler prediction — not an exhaustive forge list. |

## How to use

1. Read [`../docs/SURVEY.md`](../docs/SURVEY.md) §0.1 + §5 for the prediction.
2. Open ★ digests from [`publications/INDEX.md`](publications/INDEX.md) when you need mechanism detail.
3. Use [`products.md`](products.md) / [`repos.md`](repos.md) for Tier A/B/C shipping surfaces (CompileIQ, GEAK, ACCLAIM, Archer, …).
4. When sources disagree → [`../docs/CONFLICTS.md`](../docs/CONFLICTS.md). Claim IDs → [`../docs/CLAIMS.md`](../docs/CLAIMS.md).

## Add a source

1. Create a digest from [`publications/_TEMPLATE.md`](publications/_TEMPLATE.md) (**Org** + **Publisher** required).
2. Add an INDEX row (★ only if it moves the prediction).
3. Update `products.md` / `repos.md` only if the mechanism is a new shipping surface.
4. Thin-touch SURVEY §5 / STACK if the prediction moves.
5. `python3 scripts/validate_survey.py`

## Related narrative docs

- [`../docs/SURVEY.md`](../docs/SURVEY.md) — Q1–Q4 + §5 prediction / roadmap / commercialization  
- [`../docs/STACK.md`](../docs/STACK.md) — SW + HW-codesign layer map  
- [`../docs/SYSTEMS.md`](../docs/SYSTEMS.md) · [`../docs/TAXONOMY.md`](../docs/TAXONOMY.md)  
- [`../docs/WORKFLOW.md`](../docs/WORKFLOW.md) — add-source loop  
