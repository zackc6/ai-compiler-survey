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

## Sweep discovery coverage and omission regression

Every sweep starts from the newest mechanical discovery ledger in `reference/discovery/`, produced by `scripts/discover.py` (see "Discovery" in `AGENTS.md`). It triages every row as INCLUDE, EXCLUDE (with a one-line reason) or PENDING (with what is missing) in the ledger's Decision column, and commits the ledger with the batch. Only after that does the sweep search for leads the enumerated channels cannot see: (1) compiler-specific agent and strong non-agent methods, (2) adjacent harness/controller evolution, multi-objective evolutionary search, program synthesis, intermediate representations and system/runtime research. Web search verifies candidates and finds those extra leads; it is not the primary discovery channel. Follow related work and competing systems from primary papers such as Meta-Harness, Darwin Gödel Machine, and GEPA. Inspect Hacker News submissions and comments as a supplementary lead source only, for new sources, practitioner objections, and potential counterexamples; follow each useful lead to a primary publication or repository, label the discussion itself as anecdotal, retain the thread link, count the discussion and the linked system as one evidence family, and do not count votes or multiple posts as independent evidence.

Before declaring a sweep complete, reconcile newly found titles and arXiv/DOI IDs against the publication index and existing digests. Record INCLUDE, EXCLUDE, or PENDING with a reason in the ledger's Decision column; a lead found outside the ledger gets its own row added there. Never leave a source as an unindexed digest. Treat one system's paper, repository, blog and talk as one evidence family. Regression check: explicitly search for **Harmony Harness**, **2610.15150**, and known related families; if a known source is missing, explain its disposition. Review coverage omissions, not only the sources already discovered. Record search date, scope, primary-source verification and unresolved full-text or budget gaps.


**Updates to already-indexed repositories are not new evidence families.** The `repoevent` discovery channel lists dated GitHub commits and published releases even when a repository name, title, star count, or agent vocabulary has not changed. Revisit substantive design specifications, public API/IR changes, releases, benchmarks, corrective reversals, and correctness limitations. Decide **UPDATE-DIGEST** (edit its existing family digest after primary verification), **NOTE-IN-REPOS** (a narrow implementation note) or **IGNORE** (reason stated). Record organization, commit SHA or release tag, event/published date, first-seen date, changed behavior, protected validation contract and the strongest caveat. Different artifacts of one system are not independent confirmations. The channel is bounded, and an access failure or truncated history is reported as **pending coverage**, never as evidence that there were no updates. A commit message is a lead, not an independently validated measurement.

## Adding or refining a source

1. Use the [digest template](publications/_TEMPLATE.md), including organization, publisher, primary link, and limitations.
2. Update the publication index and its total. Keep related sources visibly connected.
3. Explain which design decision changes, or why the evidence leaves the choice unresolved.
4. Update product and implementation maps when the source adds a useful interface or deployment fact.
5. Follow the repository Survey skill, run `python3 scripts/validate_survey.py`, and rebuild the PDF after narrative edits.

Use descriptive links and plain language. Detailed evidence belongs here; the main guide should remain readable from beginning to end.
