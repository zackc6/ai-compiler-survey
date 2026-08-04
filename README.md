# Next-Generation AI Compiler Survey

Living survey aimed at **predicting the next-generation agentic compiler** (~2027–28 and ~5 years): how agents reshape the **software stack** and **HW–SW codesign**, without drifting into general EDA. Papers, OSS, products, forums, and ASIC bring-up studies are **evidence** (with explicit conflict tracking).

## Goals

1. **Predict the agentic compiler** — Hybrid agent control plane + classical data plane; four jobs (online specialize, offline heuristic synthesis, oracle engineering, bring-up/codesign).
2. **Roadmap inside the narrative** — Near (2027–28) and ~5-year horizons live in [`docs/SURVEY.md`](docs/SURVEY.md) §5.5 (with architecture in §5.1).
3. **Stack reshape** — Layer map (framework → DSL → IR → oracles → silicon feedback) in [`docs/SURVEY.md`](docs/SURVEY.md) §5.6.
4. **Answer Q1–Q4** plus comparison (§1b) and conflicts ([`docs/SURVEY.md`](docs/SURVEY.md) §6, C1–C10).
5. **Reference evidence** — [`reference/`](reference/) guide → publications / products / repos.
6. **Publish** — English PDF via [`publish/`](publish/): [`PDF`](publish/out/next-gen-ai-compiler-survey.pdf) (`python3 publish/build_pdf.py`).
7. **Track progress** — [`STATUS.md`](STATUS.md).

## Repo layout

```text
README.md                 # Goals and entry point
STATUS.md                 # Living status tracker
docs/
  SURVEY.md               # Single reading path §0–§9
  SETUP_GITHUB.md         # Maintainer git/GitHub notes
reference/
  README.md               # Entry guide → publications / products / repos
  publications/           # Digests + INDEX + template
  products.md             # Commercial prediction signals
  repos.md                # Forge / OSS evidence map
publish/
  build_pdf.py
  out/*.pdf
scripts/validate_survey.py
.cursor/skills/survey/
```

## Quick start

1. Read [`docs/SURVEY.md`](docs/SURVEY.md) end-to-end (§0 → §9).
2. Open [`reference/README.md`](reference/README.md) → ★ digests in [`reference/publications/INDEX.md`](reference/publications/INDEX.md) when you need to stress-test a claim.
3. Contribute via [`docs/SURVEY.md`](docs/SURVEY.md) §9; `python3 scripts/validate_survey.py`.
4. Export: `python3 publish/build_pdf.py`.

## How we update

- Prefer **Tier A** (agents reshape compile / ASIC bring-up with oracles) over Tier C catalog growth.
- Digest → INDEX → SURVEY §6/§7 → SURVEY §5 (if prediction moves) → reference maps → STATUS.
- HW is in scope only when it closes the loop through **kernels, IR, tests, or profilers** (not autonomous tape-out — conflict **C10**).
- Prefer primary external links; do not cite this survey repository as a source.

## Scope

- **In scope:** DL/AI compilers + AI-for-compilers; kernel agents; verification-in-the-loop; vendor agent/autotune; **agentic ASIC/NPU bring-up and codesign feedback**.
- **Out of scope:** General coding agents; exhaustive SKUs; generic SCM AI without compiler oracles; pure EDA/RTL LLM without compiler admit loops.

## License

Research/education summaries with links to originals; originals keep their copyrights.
