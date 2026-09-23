# Reference guide

This directory stores the evidence behind the [survey and design guide](../docs/SURVEY.md). The narrative explains the design choices; these sources let readers examine their basis.

| Collection | What to use it for |
|---|---|
| [Publication index](publications/INDEX.md) | Find a digest and its primary source, organization, publisher, and date. |
| [Product evidence](products.md) | Understand reported integrations, commercial offerings, and research prototypes. |
| [Implementation evidence](repos.md) | Find code, evaluation tools, and compiler interfaces for experiments. |

## Reading evidence

A paper, blog, repository, and talk about one system are one evidence family. Several systems can support a direction without independently reproducing the same result. Related research such as Mirage and Prism, or DITRON and Triton-distributed, also shares a lineage.

Relevance tiers describe how a source informs a design decision: direct evidence, supporting infrastructure, or background. They are not quality ratings. A star in the index indicates reading priority. Read the evaluation conditions and limitations before using a numerical result.

Distinguish runtime speed from tuning time, kernel gains from application gains, and workload coverage from peak performance. Record the hardware, baseline, budget, source version, and validation scope. Label projected application gains separately from measured gains; a runtime profile does not automatically transfer to another workload or organization. The current Ave digest retains its historical `argus.md` filename for compatibility.

Controller-improvement sources distinguish reusable instructions, persistent experience, workflow code, and recursive changes to the improvement procedure. Begin with [GEPA](publications/gepa.md) for limited kernel-specific evidence, then [Meta-Harness](publications/meta-harness.md) and [Hyperagents](publications/hyperagents.md) for broader mechanisms. [KOPE](publications/kope.md) remains an abstract-only lead. General agent benchmarks do not establish compiler-performance gains.

## Adding or refining a source

1. Use the [digest template](publications/_TEMPLATE.md), including organization, publisher, primary link, and limitations.
2. Update the publication index and its total. Keep related sources visibly connected.
3. Explain which design decision changes, or why the evidence leaves the choice unresolved.
4. Update product and implementation maps when the source adds a useful interface or deployment fact.
5. Follow the repository Survey skill, run `python3 scripts/validate_survey.py`, and rebuild the PDF after narrative edits.

Use descriptive links and plain language. Detailed evidence belongs here; the main guide should remain readable from beginning to end.
