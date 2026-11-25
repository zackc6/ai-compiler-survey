# The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Shanghai Jiao Tong University · Theseus Labs · Tsinghua University · ByteDance · ModelBest · Xiaohongshu · Humanlaya · Agent-Native Research Lab · Shanghai AI Lab (39 authors; per-author mapping not shown) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Surveys & vision |
| **Link** | [Primary source](https://arxiv.org/abs/2609.11873) |
| **Evidence tier** | C: taxonomy and roadmap for recursive self-improvement; background, not compiler evidence |
| **Version / reviewed** | v3, 22 September 2026; abstract page reviewed by Claude 25 November 2026 (alphaxiv mirror; the arXiv page was not reachable from the review session) |

## Key contributions

Defines **recursive self-improvement** (RSI) as a persistent closed loop in which an AI diagnoses its limitations, then selects, validates and retains changes. A retained change used in a later round is **structural recursion**. **Effective** recursion requires that the mechanism also produce stronger successors under comparable resources and independent assessment. The survey sorts systems into five levels of delegated responsibility:
- **L1:** executes human-prescribed improvements.
- **L2:** chooses interventions, with objectives and acceptance criteria external.
- **L3:** helps decide what experience to acquire next.
- **L4:** adapts persistent state from deployment feedback.
- **L5:** changes a mechanism that governs later improvement.

## Summary

A broad survey and roadmap across scientific discovery, embodied intelligence and software engineering. It also introduces a Headroom-Closed Index for current models. Human objectives, evaluation and governance can remain at every level; the levels describe persistence and delegation, not capability.

## Key takeaways

The useful part for this survey is the vocabulary: retained versus one-off improvement, and *who sets the acceptance criterion*. Revising one answer inside one task is not RSI under its definition, because nothing carries over. The detailed case it discusses (A-Evolve-Training on a 30B model, four autonomous rounds) is described by the authors as a revised research policy guiding a later round, not autonomous goal-setting.

## Why it matters for this survey

The survey's controller row asks whether *accepted* controller changes improve later compiler searches. This taxonomy gives a precise way to state what a compiler system claims. Kernel-prompt evolution with fixed tests is about L2. A controller that picks which workloads to profile next is L3. A procedure that rewrites its own acceptance rule is L5, the level the [Hyperagents](hyperagents.md) row describes. Its effective-recursion condition, stronger successors under comparable resources and independent assessment, matches the survey's demand for held-out, budget-matched evaluation. The 2026-11-08 and 2026-11-15 discovery ledgers surfaced this paper and excluded it as general agent work; that exclusion was a triage error, now corrected.

## Limits / caveats

The levels and roadmap are the authors' framework, not measurements. Only the abstract page was read, so the number of papers covered and how specific systems are placed are not verified. It does not discuss compiler or kernel systems on the page read. Many co-authoring organizations build agent products, so the roadmap may lean toward optimism about RSI timelines.
