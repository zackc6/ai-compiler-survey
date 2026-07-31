# Next-Generation AI Compiler Survey

Living survey aimed at **predicting the next-generation agentic compiler** (~2027–28 and ~5 years): how agents reshape the **software stack** and **HW–SW codesign**, without drifting into general EDA. Papers, OSS, products, forums, and ASIC bring-up studies are **evidence** (with explicit conflict tracking).

## Goals

1. **Predict the agentic compiler** — Hybrid agent control plane + classical data plane; four jobs (online specialize, offline heuristic synthesis, oracle engineering, bring-up/codesign).
2. **Roadmap** — Near (2027–28) and ~5-year horizons in [`docs/ROADMAP.md`](docs/ROADMAP.md).
3. **Stack reshape** — Layer map (framework → DSL → IR → oracles → silicon feedback) in [`docs/STACK.md`](docs/STACK.md).
4. **Answer Q1–Q4** plus comparison + conflicts ([`docs/CONFLICTS.md`](docs/CONFLICTS.md) C1–C10).
5. **Reusable bibliography** — Digests under [`publications/`](publications/).
6. **Track progress** — [`STATUS.md`](STATUS.md).

## Repo layout

```text
README.md                 # Goals and entry point
STATUS.md                 # Living status tracker
docs/
  SURVEY.md               # Narrative: Q1–Q4, §5 prediction
  ROADMAP.md              # 2027–28 + ~5-year milestones
  STACK.md                # SW + HW-codesign reshape
  CLAIMS.md               # Falsifiable claims ↔ digests
  CONFLICTS.md            # C1–C10 disagreements
  WORKFLOW.md             # How to add evidence
  REPOS.md / PRODUCTS.md  # Tier A/B/C evidence maps
  SYSTEMS.md / TAXONOMY.md
publications/
  INDEX.md / _TEMPLATE.md / *.md
scripts/validate_survey.py
```

## Quick start

1. [`docs/SURVEY.md`](docs/SURVEY.md) §0.1 + §5, then [`docs/ROADMAP.md`](docs/ROADMAP.md) and [`docs/STACK.md`](docs/STACK.md).
2. [`docs/CLAIMS.md`](docs/CLAIMS.md) / [`docs/CONFLICTS.md`](docs/CONFLICTS.md) when sources disagree.
3. ★ digests in [`publications/INDEX.md`](publications/INDEX.md) (TritorX, KernelEvolve, ACCLAIM, Magellan, …).
4. Contribute via [`docs/WORKFLOW.md`](docs/WORKFLOW.md); `python3 scripts/validate_survey.py`.

## How we update

- Prefer **Tier A** (agents reshape compile / ASIC bring-up with oracles) over Tier C catalog growth.
- Digest → INDEX → CONFLICTS/CLAIMS → ROADMAP/STACK/SURVEY (if prediction moves) → STATUS.
- HW is in scope only when it closes the loop through **kernels, IR, tests, or profilers** (not autonomous tape-out — conflict **C10**).
- Prefer primary links.

## Scope

- **In scope:** DL/AI compilers + AI-for-compilers; kernel agents; verification-in-the-loop; vendor agent/autotune; **agentic ASIC/NPU bring-up and codesign feedback**.
- **Out of scope:** General coding agents; exhaustive SKUs; generic SCM AI without compiler oracles; pure EDA/RTL LLM without compiler admit loops.

## License

Research/education summaries with links to originals; originals keep their copyrights.
