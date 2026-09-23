---
name: survey
description: >-
  Maintain this AI compiler survey and design guide. Use for any edit in this
  repository: read and refine SURVEY.md first, evaluate primary evidence,
  preserve the single narrative and source catalog, update claims and forecasts,
  validate, and rebuild the survey PDF. Work on main; never create a branch or
  pull request unless requested. Respect explicit instructions not to push.
---

# AI compiler survey and design guide

## Follow the repository structure

Keep one narrative in `docs/SURVEY.md`. Preserve the main section order and place detailed evidence in `reference/`. Do not create separate roadmap, architecture, claims, conflicts, comparison, or design-guide documents that compete with the narrative.

| Location | Purpose |
|---|---|
| `docs/SURVEY.md` | Purpose, trends, alternatives, mechanisms, gaps, design guidance, forecasts, unresolved choices, evidence register, systems, and maintenance method. |
| `docs/SETUP_GITHUB.md` | Repository maintenance instructions. |
| `reference/publications/` | Source digests, publication index, and digest template. |
| `reference/products.md` and `reference/repos.md` | Product and implementation evidence maps. |
| `STATUS.md` | Current coverage, change history, and next research actions. |
| `publish/` | Survey PDF generation and downstream presentation sources. |

Keep the narrative's established section numbers from 0 through 9, including the alternatives section numbered 1b. Preserve material decisions, caveats, source coverage, and historical record identities when reorganizing. Preserve old heading links with invisible compatibility anchors where useful; do not make readers navigate through identifiers.

## Test the thesis instead of requiring evidence to support it

Use the central hypothesis that the compiler increasingly becomes an agentic optimization system. Survey the broader compiler field to test it. Include strong conventional optimizers, symbolic search, learned policies, compiler/runtime integration, and hardware-aware programming models. Separate optimization scope from the decision method. A larger coupled space motivates comparison; it does not prove agents necessary. Test causal claims with comparable headroom, actions, feedback, and resources.

Treat the division between agents and conventional compiler components as an architectural choice that can evolve. Do not require permanent layers, a fixed number of agent roles, a particular agent topology, or a universal representation. Evaluate retaining, generating, merging, or replacing components according to their results.

Distinguish necessary functions from current implementations. Executable realization and validation remain relevant, but they do not require today's fixed passes or lowering sequence. A generated component can execute deterministically. Retaining a checker or assembler does not disqualify a meaningful compiler replacement.

Treat current failures as challenges with possible solutions, not permanent ceilings. Separate confidence in direction, timeline, and architecture. Forecast at **1, 3, 5, and 10 years, plus beyond**, anchored to the survey date. For each horizon, state the central prediction, a more ambitious possibility, needed progress, and evidence that would change confidence. Assign separate qualitative confidence to direction, timing, and architectural form. Add a dated observable predicate, qualifying-evidence rules, and a review date; for an undated long-term scenario, use a dated precursor test. Treat numerical thresholds as declared assessment choices rather than calibrated forecasts. Preserve original calls and record misses explicitly.

## Apply the agreed objective order

Use runtime performance as the primary objective. Treat developer productivity and portability as secondary objectives of similar importance, while naming coverage constraints that prevent meaningful application evaluation. Measure search cost immediately. Prioritize cost reduction after demonstrating performance value when expected artifact reuse justifies that ordering; apply payback and deployment-latency constraints immediately when reuse is limited. Cheaper search at comparable runtime is a separate useful outcome. Count useful executions before invalidation, not merely search jobs, and separate campaign totals from per-artifact costs.

Define correctness, numerical or statistical acceptance criteria, model quality, supported inputs, and deployment constraints before comparing candidates. Stochastic execution can retain a deterministic mathematical reference; specify repeated sampling, confidence and tail requirements, noise assumptions, and drift conditions where relevant. Use application performance where possible; distinguish kernel speed, application throughput, tuning time, compilation time, and operator coverage.

Compare strong baselines. Include matched-budget experiments and a larger declared budget to distinguish search efficiency from attainable performance. Do not equate source reuse with performance portability. On new hardware, treat required workload coverage as an enabling condition for application-performance work.

## Write for human understanding and design use

1. Lead each major section with its decision, conclusion, or purpose. Explain enough locally that the reader does not need to jump elsewhere to understand the paragraph.
2. For substantial design guidance, state the **recommended starting point, reason, benefit, tradeoff, conditions for choosing differently, and validation experiment**. Label recommendations as recommendations.
3. Use full terms at first use for necessary abbreviations. Keep familiar system names, but avoid strings such as `e2e F-admit / T1+T6 / C6-B / M1` in running prose. Prefer “measure application performance and validate the candidate” where that is the intended meaning.
4. Use descriptive links such as “the forecast” or “the evidence register.” Avoid symbol-led section references, arrow chains, and bare record codes as explanations. Place old identifiers only in the evidence register, source-maintenance metadata, or invisible anchors.
5. Use complete sentences, short paragraphs, and concrete examples. Replace slogans such as “money-grade,” “hard replace,” and “production truth” with the actual requirement or decision.
6. Keep tables readable: generally three or four columns, short cells, one comparison per table. Split long tables by topic. Move source catalogs and detailed results into digests rather than packing them into every recommendation.
7. Preserve technical substance when simplifying. Keep decision alternatives, measurements, conditions, disagreements, and caveats. Condense repeated explanation rather than deleting an inconvenient alternative.
8. Separate observed capability, author evaluation, industry report, corroborated direction, design recommendation, and forecast. Never label a future prediction “Supported” without identifying its evidence scope and uncertainty.
9. Count evidence families rather than papers. A paper, blog, repository, and talk about the same system are not independent confirmations. Shared organizations or research lineages must be visible when they affect confidence.
10. Read the result from beginning to end. A compiler engineer should be able to explain the recommended choices, tradeoffs, and next experiments without decoding a private vocabulary.

Use the same style in the README, current status, source-guide introductions, PDF cover, and future presentation updates. Historical changelog entries can retain their original wording.

## Read and record primary evidence

Prefer papers, official documentation, repositories, and first-party engineering reports. Use secondary discussion for context and source discovery; identify it as secondary. Check the version and publication date before updating numerical claims or forecasting from a source.

For each result, record the baseline, measured object, hardware, workload coverage, search budget when available, and validation scope. State what the result cannot establish. Distinguish measured application results from projections based on runtime fractions and assumed local gains. Addressable runtime depends on workload, actions, and classification; do not transfer a profile to a different organization’s private workloads or turn a library share into a universal performance ceiling. Distinguish the effect of a whole environment from an isolated representation or model effect. Avoid comparing unrelated headline speedups.

Keep relevance separate from evidence quality:

- **Tier A:** directly informs or challenges a design decision, including non-agent alternatives.
- **Tier B:** infrastructure or adjacent mechanisms that could support an implementation.
- **Tier C:** background or discussion without direct decision evidence.

A star in the publication index marks a decision-relevant reading priority, not independent replication or peer-review quality. Every digest needs organization, publisher, type, group, primary link, relevance, and limitations. Use the full source title in the index. Keep original filenames when a paper is renamed, but clearly identify the new title and version.

## Search broadly enough to avoid biased coverage

Search vendor kernel languages, compiler interfaces, documentation launches, distributed execution, runtime behavior, and mature stacks with stale coverage. Do not restrict searches to titles containing “LLM” and “compiler.” If the narrative uses a language as evidence, maintain its own digest as well as the agent paper built on it.

Disambiguate TritorX, TVM TIRx, and Triton Low-level Language Extensions. Likewise distinguish ForgeMegakernel from AMD KernelForge and different papers sharing the SkillSmith name.

For agent skills, distinguish vendor optimization packs, the Agent Skills packaging specification, skill compilation, and explicit runtime-state systems. These are adjacent infrastructure until evaluated in a compiler context. Do not promote generic coding, customer-service, or security-challenge benchmarks into evidence of compiler optimization.

Include hardware research when executable workloads, representations, simulation, or compiler feedback connect it to co-design. Keep general chip-design automation outside the main survey unless that connection is demonstrated.

## Update the narrative before the presentation

1. Read the current narrative and affected digests.
2. Update evidence and the publication index first when facts or sources change.
3. Refine the relevant narrative sections, unresolved questions, and evidence records together.
4. Check whole-document consistency: objectives, architectural choices, evidence labels, terminology, dates, and forecast confidence.
5. Run `python3 scripts/validate_survey.py`.
6. Rebuild the survey PDF with `python3 publish/build_pdf.py` in the same batch as a narrative edit. Inspect the rendered output and repair unreadable tables, broken links, overlap, and clipping.
7. Update `README.md`, source guides, publishing metadata, and `STATUS.md` where the change affects them.
8. Update Beamer only when the narrative is settled and slides are requested or explicitly part of the batch. Otherwise identify the existing presentation as an earlier snapshot if its conclusions differ.
9. Review the diff and save a coherent commit on main. Publish only when authorized.

A consistency check may require changing the goal or architecture recommendation. Never rewrite contrary evidence to make it agree with a preferred thesis.

## Maintain the publication pipeline

Keep `publish/assemble.py` aligned with the single narrative and reference appendices. Update cover text when the objective or forecast horizons change. Preserve meaningful legacy links. Keep source links usable in the standalone PDF.

When adding digests, update the index total and the organization/publisher metadata helper when applicable. Validate source links and historical anchors without depending on network availability for every build.

### When slides change

Every content edit to `publish/beamer/expert-briefing.tex` must update the affected transcripts in both `publish/beamer/transcripts/en/` and `publish/beamer/transcripts/zh-TW/` in the same batch. Refresh their README index when titles or ordering change. Draft the English script first; use `publish/translate_transcripts.py --slides NN` if appropriate and review the Traditional Chinese result.

Make scripts explain the claim, evidence, and spoken transition instead of pasting slide text. Expand central abbreviations in context. Keep a content-slide level of detail comparable to the existing slide-04 transcript.

Build with `python3 publish/build_beamer.py`, rasterize changed pages, and inspect them. Keep titles, cards, glosses, and timelines in separate clear areas. Route connectors around text. Split overloaded slides rather than shrinking them into unreadability. Never leave overlap, clipped content, or mismatched transcripts.

## Work on main and honor publication instructions

Use the existing main branch; do not create feature branches or pull requests unless explicitly requested. Fetch and fast-forward a clean stale checkout before editing. Preserve unrelated user changes.

Commit coherent batches. When publishing is authorized, push main directly using the available authenticated route. Never force-push or overwrite concurrent remote work. If the user says “do not push,” prepare and validate local changes, commit if appropriate, and clearly state that publishing is pending. Skill defaults do not override that instruction.

## Finish-batch checklist

- Preserve the single narrative and existing section responsibilities.
- Verify facts against the appropriate primary versions; update digests and index together.
- Keep all five forecast horizons and distinguish observations from predictions.
- Make performance priorities and validation contracts explicit.
- Explain design alternatives, tradeoffs, and experiments in ordinary language.
- Remove unexplained abbreviations and symbol-heavy cross-references from the revised narrative.
- Preserve historical record identities and usable links.
- Run repository validation; rebuild and visually inspect the survey PDF.
- Refresh both transcript languages whenever slides change.
- Update current status and the change log.
- Review and commit the intended files on main; publish only when authorized.

See [experience notes](survey.md) for the reasons behind this workflow.
