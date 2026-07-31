# Next-Generation AI Compiler Survey

Living survey of **AI/ML compilers** (systems that compile neural models) and **AI-for-compilers** (LLMs/agents that guide, rewrite, or evolve compilation). Maintained as a progressive research notebook with per-publication digests.

## Goals

1. **Map the landscape** — What is “next-gen” AI compilation in 2024–2026: hybrid LLM–compiler loops, agentic tuners, MLIR/Triton stacks, and SE 3.0 intent compilers.
2. **Answer four research questions** (plus a comparison section)
   - **Q1 Trends** — What are the dominant technical directions now?
   - **§1b Comparison** — Traditional AI compilation pros/cons vs following LLM/agent trends
   - **Q2 Agents** — How do agents help the AI compilation process?
   - **Q3 Reshape** — Can agents reshape (rearchitect) compilation processes, or only assist them?
   - **Q4 Gaps** — What is missing / under-covered (ten gaps, fully spelled out)?
3. **Build a reusable bibliography** — Every searched publication gets a short digest under [`publications/`](publications/) so others can learn quickly without reading full papers first.
4. **Track progress openly** — Status, open tasks, and coverage live in [`STATUS.md`](STATUS.md).

## Repo layout

```text
README.md                 # This file — goals and entry point
STATUS.md                 # Living status tracker
docs/
  SURVEY.md               # Expanded survey narrative (Q1–Q4 + §1b comparison)
  COMPARISON.md           # Pointer to traditional vs trends section
  SYSTEMS.md              # System comparison table
  TAXONOMY.md             # Selector / Translator / Generator + stack layers
  SETUP_GITHUB.md         # How to auth + push remote
publications/
  INDEX.md                # Catalog of all digests + links
  *.md                    # One digest per publication
```

## Quick start

1. Read [`docs/SURVEY.md`](docs/SURVEY.md) for the full narrative.
2. Skim [`publications/INDEX.md`](publications/INDEX.md) for the bibliography.
3. Open individual digests under [`publications/`](publications/) for contributions + takeaways.
4. Check [`STATUS.md`](STATUS.md) before contributing an update.

## How we update this survey

- Add or revise digests in `publications/` first (one file per source).
- Update `publications/INDEX.md` and, if needed, `docs/SURVEY.md` / `docs/SYSTEMS.md`.
- Bump the relevant checklist in `STATUS.md` and note the date.
- Prefer primary links (arXiv, conference pages, official blogs) over secondary summaries.

## Scope notes

- **In scope:** DL/AI compilers (TVM, XLA, MLIR, Inductor/Triton, IREE), LLM/agent compiler optimization, kernel agents, verification-in-the-loop, vendor compiler AI (CompileIQ, GEAK, Magellan/AlphaEvolve), community forums when they carry technical signal.
- **Out of scope (for now):** General coding agents unrelated to compilation; pure frontend LLM codegen without a compiler/runtime loop (except generative compilation, which couples compilers into decoding).

## License

Content in this repository is for research and education. Individual papers and blog posts remain under their original copyrights; digests are fair-use style summaries with links to originals.
