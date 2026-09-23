# Experience notes for the survey and design guide

## Keep a single reading path

Separate roadmap, stack, claims, conflicts, and comparison files previously forced readers to jump among competing narratives. Keep these topics in `docs/SURVEY.md` and keep evidence in `reference/`. Preserve the section sequence and historical link targets when reorganizing.

The PDF should assemble the narrative and thin reference appendices, not every digest body. Keep the publishing link-rewrite logic aligned with the actual structure. Update the narrative before making presentation changes.

## Test a thesis without turning it into a source-selection rule

The September 2026 review clarified the goal: survey AI compilation broadly and test whether the compiler becomes an agentic optimization system. Earlier guidance treated a hybrid agent/control-plane architecture as the required conclusion. That stance could make new evidence confirm the architecture by construction.

Use conventional and symbolic optimization as serious alternatives. Compare learned policies, agent proposals, synthesis, and compiler co-evolution. A non-agent system can be a high-priority source when it challenges a design assumption.

Separate the function a compiler must perform from today's implementation. Generating a heuristic or replacing a lowering component counts as architectural progress even if a checker or assembler remains. A fixed number of layers or agent jobs is a useful organizing map, not an established law.

## Turn observations into usable design guidance

A bibliography tells readers what exists. A design guide also explains which choice to start with, why it helps, its cost, when another option is preferable, and how to evaluate the choice.

For this project, runtime performance is primary. Developer productivity and portability have similar secondary importance. Record search cost immediately. For highly reusable artifacts, prioritize cost reduction after a useful performance advantage is demonstrated; for short-lived deployment, impose payback and latency constraints immediately. Per-deployment search does not imply one useful execution, and fleet-wide reuse does not eliminate maintenance. On new hardware, coverage can enable the first application-performance experiment.

Use representative application metrics and strong baselines. Keep kernel speed, application throughput, search efficiency, compilation time, and coverage separate. Define numerical tolerances and model-quality constraints before the optimizer runs.

## Make the prose readable without losing substance

Long chains of abbreviated concepts and record codes made the previous narrative difficult to follow. Expanding every abbreviation into an even longer sentence is not enough: rewrite the sentence around a concrete decision.

| Earlier style | Preferred style |
|---|---|
| “T1 + T2 + T6 enable F-admit across L1-L7.” | “Expose candidate actions, validate them, and measure their effect on the application.” |
| “M1 by Horizon A; M3 excluded through B.” | “Near-term systems are likely to reuse existing backends; component replacement remains open over longer horizons.” |
| “Supported (lean).” | “Design recommendation informed by several systems; comparative evidence remains limited.” |
| “See section symbols and claim codes for the argument.” | Explain the point locally and offer a descriptive link for detail. |

Keep identifiers in the evidence register or invisible compatibility anchors. Use short tables for actual choices and source catalogs for detailed measurements. Preserve alternatives and caveats when condensing repeated content.

## Keep evidence quality distinct from relevance

Relevance tiers tell the reader why a source is included. They do not certify correctness, production use, replication, or general superiority.

Record source families. A company blog and its paper are one family; related systems may share authors, infrastructure, or organizational assumptions. Count those dependencies when judging corroboration.

Check versions. Argus became Ave in September 2026 with revised metrics. Helion's original language announcement does not describe all later tuning methods. Keep the historical digest filename when needed for links and label the current version clearly.

For representation comparisons, distinguish the full environment from the representation alone. A matched model and budget can still leave compiler support, diagnostics, and search spaces different. For performance results, state the measured object and denominator before interpreting the number.

## Forecast capability, timing, and architecture separately

Use one-, three-, five-, and ten-year horizons and a longer-term scenario. For each, state the central path, a more ambitious possibility, required advances, and separate confidence in direction, timing, and architectural form. Make the dated claim checkable: define a predicate, evidence rules, review date, and what would change the conclusion. Keep original predictions when recording misses. An undated long-term scenario can have a dated precursor test without claiming a deadline for universal capability.

Failures in current models are research challenges, not permanent ceilings. Avoid both “cannot happen” conclusions based on present limitations and claims of inevitable success without mechanisms or evidence. Use bounded experiments and dated review checkpoints rather than unfalsifiable “forever” criteria.

## Search lessons to preserve

| Past coverage gap | Better search practice |
|---|---|
| TIRx was missed by searches for “LLM + compiler IR.” | Walk vendor languages, documentation launches, interfaces, and stale compiler stacks. |
| Agents were cited without the languages they use. | Maintain a source digest for the representation or language when it supports the argument. |
| Skills meant only vendor optimization packs. | Distinguish instruction packaging, skill compilers, workflow compilation, and runtime state. |
| Similar names were conflated. | Disambiguate TritorX, TIRx, Triton extensions, different KernelForge projects, and different SkillSmith papers. |
| Conventional alternatives were secondary to agent papers. | Include structured search and compiler/runtime advances that can challenge the thesis. |
| Company speedups were treated as one common metric. | Separate application, kernel, tuning-time, and coverage results before comparing. |

Keep workflow and skill infrastructure adjacent until there is evidence from a compiler setting. Hardware work belongs when it connects to executable workloads or compiler feedback; general chip-design automation is a separate survey.

## Publication and maintenance lessons

- Validate digest/index consistency, organization/publisher fields, local links, and historical anchors.
- Keep source URLs usable in the standalone PDF.
- Rebuild the survey PDF whenever its narrative changes and inspect the rendered output.
- Update cover text when objectives or horizons change.
- Keep current status separate from historical changelog wording.
- Defer presentation changes unless requested or the narrative is explicitly settled; identify an older deck as an earlier snapshot when needed.
- Any Beamer content edit requires matching English and Traditional Chinese transcript updates.
- Inspect changed slides for overlap, text clipping, and unreadable density. Keep titles and explanatory cards in separate areas.
- Work on main. An explicit no-push instruction overrides the normal publish-after-batch workflow.

## Success check

A reader should be able to explain the central hypothesis, objective order, main architectural choices, strongest evidence, uncertain forecasts, and next experiments without opening another narrative or decoding record identifiers. The source catalog should support deeper verification when needed.

## Lessons from the scope and economics review

- Scope expansion changes the decisions available to an optimizer; it does not establish which search method wins. DITRON is a useful non-agent comparison and shares the Triton-distributed lineage.
- An addressable-runtime profile is local to its workload, shape, action space, and classification. A library-heavy profile does not imply an invariant performance ceiling, and cannot be assigned to another organization’s private workload.
- Read tables and methods as well as abstracts. The kernel-headroom study’s transformer projections span 1.32–2.49%; its full recommender addressable fraction is different from a single embedding kernel’s share.
- Search cost measurement, search cost optimization, and deployment payback answer different questions. Cheaper tuning at comparable runtime can be valuable even without a speedup.
- Nondeterminism changes the acceptance contract, not the existence of a mathematical specification. Repeated evaluation, drift, and tail requirements belong in the validation framework.
