# Next-Generation AI Compiler Survey

Living survey aimed at **predicting the next-generation AI compiler** and **how agents change that future**. Papers, OSS, commercial products, and forums are treated as **evidence** for that prediction (with explicit conflict tracking when sources disagree).

## Goals

1. **Predict next-gen compilation** — What architecture wins (~2027–2028): hybrid agent control plane + classical data plane, new artifacts (ACFs, synthesized heuristics, verified kernels), and what will *not* happen soon.
2. **Explain how agents change the future** — Online specialization, offline heuristic synthesis, and compiler engineering/review — with hard limits (oracles, constrained actions).
3. **Answer four research questions** (plus comparison + conflicts)
   - **Q1 Trends** — Dominant technical directions now
   - **§1b Comparison** — Traditional AI compilation vs LLM/agent trends
   - **Q2 Agents** — How agents help AI compilation
   - **Q3 Reshape** — Control-plane reshape vs data-plane replacement
   - **Q4 Gaps** — What blocks the predicted future (ten gaps)
   - **Conflicts** — Where papers/vendors/forums disagree ([`docs/CONFLICTS.md`](docs/CONFLICTS.md))
4. **Build a reusable bibliography** — Short digests under [`publications/`](publications/).
5. **Track progress** — [`STATUS.md`](STATUS.md).

## Repo layout

```text
README.md                 # Goals and entry point
STATUS.md                 # Living status tracker
docs/
  SURVEY.md               # Narrative: Q1–Q4, §1b, §5 future prediction
  CONFLICTS.md            # Unresolved disagreements (C1–C8)
  COMPARISON.md           # Pointer to traditional vs trends
  REPOS.md                # Tier A/B/C OSS & forge evidence
  PRODUCTS.md             # Commercial offerings as prediction signals
  SYSTEMS.md              # System comparison table
  TAXONOMY.md             # Selector / Translator / Generator
  SETUP_GITHUB.md         # How to auth + push remote
publications/
  INDEX.md                # Catalog of digests
  *.md                    # One digest per source
```

## Quick start

1. Read [`docs/SURVEY.md`](docs/SURVEY.md) — especially **§0.1 North star** and **§5 Future prediction**.
2. When two sources disagree, open [`docs/CONFLICTS.md`](docs/CONFLICTS.md).
3. Skim [`publications/INDEX.md`](publications/INDEX.md); use Tier maps in [`docs/REPOS.md`](docs/REPOS.md) / [`docs/PRODUCTS.md`](docs/PRODUCTS.md).
4. Check [`STATUS.md`](STATUS.md) before contributing.

## How we update

- Prefer **Tier A** evidence (agents reshape compile) over catalog growth (generic review bots, runtime glue).
- Add digests in `publications/` first; update INDEX; bump STATUS.
- If a new source conflicts with an existing claim, add/update a row in `docs/CONFLICTS.md` instead of overwriting the narrative.
- Prefer primary links (arXiv, official docs/blogs, Discourse) over secondary summaries.

## Scope

- **In scope:** DL/AI compilers + AI-for-compilers; kernel agents; verification-in-the-loop; vendor agent/autotune (CompileIQ, GEAK, Magellan/AlphaEvolve); forums with technical signal.
- **Out of scope:** General coding agents unrelated to compilation; exhaustive commercial SKU lists; generic SCM AI review without compiler oracles (Tier C only).

## License

Research/education summaries with links to originals; originals keep their copyrights.
