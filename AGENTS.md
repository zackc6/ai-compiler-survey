# Instructions for coding agents (ChatGPT/Codex, Claude, Cursor)

This file is the briefing for any agent working in this repository. Read it fully, then read `.cursor/skills/survey/SKILL.md`, which is the detailed rulebook. Both apply to every agent.

## What we are trying to do

The maintainer (Zack) keeps a living survey and design guide for next-generation AI compilers, in `docs/SURVEY.md`, with one source digest per publication in `reference/publications/`. The guide tests one thesis: **the compiler increasingly becomes an agentic optimization system** that chooses strategies, synthesizes implementations and compiler components, evaluates results, and adapts from feedback. The job is to test that thesis against the public record, not to confirm it. That means strong non-agentic alternatives (symbolic search, learned policies, generated backends such as ACT, vendor libraries) must be covered as carefully as agentic systems.

The guide commits to dated, checkable forecasts (2027, 2029, 2031, 2036, beyond) with observable predicates, a running tally under the 2027 predicate, a controller-research checkpoint in September 2027, and decision checkpoints in section 5.8.3. Every evidence batch must say what it does to those: usually nothing, and "nothing" must be stated.

Two agents maintain the repository together: Claude (scheduled: daily review-thread check 08:52 HKT, weekly evidence sweep Mondays 08:47 HKT) and ChatGPT/Codex. The maintainer wants the survey kept current and wants the two agents to **agree** on each change, with the maintainer deciding ties.

## Priority order (set by the maintainer)

1. **Does the thesis still hold?** Every batch leads with a verdict: for each row of the section 5.3 table (what would weaken or strengthen the thesis), each horizon predicate in section 5.5 with the running 2027 tally, each decision checkpoint in 5.8.3, and each unresolved question in section 6 — moved or untouched, naming the evidence — and an explicit line "Direction / timing / architecture confidence: unchanged" or the proposed change with its reason. The two agents must **agree** on this verdict in the Review thread before it is written into `docs/SURVEY.md`; a change to a forecast call, confidence label, predicate status, or checkpoint rule applied without prior agreement is reverted by the reviewer. Record misses as misses; keep original calls.
2. **New evidence.** Digests and narrative for new sources, to the quality bar below. Important, but second: a batch that adds ten sources and omits the verdict is incomplete.

## How the two agents work together

1. **Claim before editing.** Add one row to the "Open batch" table at the top of `STATUS.md` (agent, scope, start date, status) and push it, or include it in your batch commit. If the other agent has an open row on overlapping scope, do not edit the same files; review its pushed work instead.
2. **Talk in the Review thread** in `STATUS.md`, newest entry first, one dated entry per reply. Each entry: verdict on the other agent's last batch (agree / object, naming file and line), open points, and what you will do next. Mark a point "resolved" with the commit hash that resolves it. Do not argue in commit messages or in prose inside `docs/SURVEY.md`.
3. **Debate, then merge.** (Maintainer's rule, 15 October 2026.) An evidence or thesis batch goes on a branch named `claude/<topic>-<date>` or `chatgpt/<topic>-<date>`, validated and with the PDF rebuilt on that branch. The author posts its argument in the Review thread on `main`: what the new evidence means for the thesis, which §5.3 rows, predicates, checkpoints, or unresolved questions it touches, and the proposed wording. The other agent replies with agree / object per point, with reasons and evidence. The branch merges to `main` (fast-forward or merge commit, never force) only after both agents have written "agree" on every disputed point, or the maintainer has ruled. Review-thread entries, Open-batch rows, and pure fact fixes (a wrong number, a broken index, a missing rebuild) may go to `main` directly. If the other agent has not replied within two daily checks, the author may ask the maintainer to rule; it does not merge unilaterally.
4. **Sign commits** with your agent name (for example `Co-Authored-By: ChatGPT` or `Co-Authored-By: Claude`) so the change log shows who did what.
5. **Sweep on different days.** Claude sweeps Mondays. ChatGPT should sweep mid-week (Thursday) and otherwise review. Check the thread once a day.

## The quality bar every batch must meet

These are the points the two agents converged on in October 2026; see the Review thread for the record.

- **Digest depth.** Every digest carries the organization (never "research authors"), publisher, type, group, primary link, evidence tier with the reason, and the numbers a designer would act on: baseline, hardware, denominator (kernel time vs application throughput vs search cost), budget or cost, validation scope, and the strongest caveat the source itself states. Follow `reference/publications/_TEMPLATE.md`; `ai-as-compiler.md` and `kda2.md` show the expected level. Boilerplate "Key takeaways" copied across digests are not acceptable.
- **Evidence families, not papers.** A paper, blog, repository, and talk about one system are one family. Shared organizations or lineages (for example TIRx / TIRx Harness / KCoral / KDA² / MetaKernelBench / CAKE) must be named in the digest and in the narrative wherever they are cited together.
- **Batch completeness.** Digest + index row + index total + narrative + evidence register + `STATUS.md` change log, then `python3 scripts/build_blueprint.py`, `python3 scripts/validate_survey.py`, and `python3 publish/build_pdf.py` in the same batch. A pushed batch with a stale PDF is incomplete.
- **Argue, do not just tally.** Each thesis entry is a position: say what the evidence implies for the thesis, name the strongest objection to your own reading, and say what experiment would settle it. A list of "unchanged" rows without reasons is not a verdict.
- **Milestone bookkeeping.** Update the running tally under the 2027 predicate for any post-23-September-2026 candidate and state in the change log whether any horizon call, confidence label, checkpoint rule, or Figure 1 changed. Never move a forecast date or confidence silently; record misses as misses.
- **Write for a compiler engineer** reading start to finish: full terms at first use, no private symbol chains, recommendations labeled as recommendations, observed capability separated from author evaluation, industry report, corroborated direction, and forecast.
- **Verify before writing.** Read the primary source. Do not paraphrase a secondary summary into numbers. Record the version and date reviewed.

## What not to do

- Do not create parallel roadmap, claims, or architecture documents; the single narrative is `docs/SURVEY.md`.
- Do not rewrite contrary evidence to fit the thesis, and do not drop an alternative because it is inconvenient.
- Do not re-edit the other agent's stylistic choices; object in the thread, fix only facts, broken indexes, or missing rebuilds.
- Do not edit `docs/architecture-overview.svg` by hand; change `scripts/build_blueprint.py` and re-render.
- Do not touch the Beamer slides unless the maintainer asks; they are an earlier snapshot.
