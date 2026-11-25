# Exo: An Architecture for Self-Improving Systems at Runtime

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | UC Berkeley · Andreessen Horowitz · Braintrust |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2611.00463) |
| **Evidence tier** | B: a controller that edits itself during use, with a protected layer and held-out cost evaluation; no compiler benchmark |
| **Version / reviewed** | arXiv v1, 30 October 2026 (title corrected to the arXiv v1 title 25 November 2026); arXiv paper text reviewed by Claude 25 November 2026; Table 1 and §§5.2.1–5.4.3 figures checked against the v1 PDF independently by ChatGPT and by Claude, 25 November 2026; [open-source release](https://github.com/exoharness/exo/tree/c5c1963a3445417e64938c139da88edd9154075d) at commit c5c1963 not inspected |

## Key contributions

Exo lets an agent edit its own harness (tools, skills, memory, context handling) while it works, instead of tuning the harness in a separate search before deployment. A minimal **protected layer** holds what the agent may not edit: an append-only, queryable execution history annotated with costs, a versioned artifact store, credentials, the sandbox API, and an independent **guardian** that decides whether a candidate executor is activated. The default guardian check is that the new version builds.

## Summary

The authors compare Exo with the same starting policy with editing disabled, and with the Codex and Pi agents on long RuneScape objectives.

## Key takeaways

Figures are from arXiv v1 (printed pp. 8–9, Table 1, §§5.2.1 and 5.4). The Table 1 caption states that SREGym reports median time and rounds and **mean** cost.

- **AppWorld:** Exo learns on one variant of each of 50 scenarios, then runs 100 held-out variants **of those same scenarios** without feedback, three seeds; the holdout is new variants, not new scenarios. Mean held-out model cost per task falls from $0.359 to $0.141 (−61%), with a 96.9% pass rate in both arms. Total mean cost including learning and reflection falls from $57.36 to $32.70 (−43%).
- **SREGym:** 21 learning incidents and 20 held-out incidents from the same fault families on different applications. **Mean** held-out model cost per incident falls from $0.892 to $0.584 (−35%); diagnosis time and rounds are reported as medians. The paper states only that correctness is comparable, with no figure.
- **CLB coding tasks:** 19 fixed issues, five runs per arm, no separate held-out split. Both arms resolve every issue; model cost per issue including reflection falls from $0.507 to $0.436 (−14%).
- **RuneScape:** 12–53% lower model cost than Codex and Pi in standalone runs, for example $3.71 against $7.26 and $7.95 for one combat objective.
- **Negative result when reuse is low (§5.2.1):** on a quest objective, over three runs per arm, Exo averages $0.28 per quest point against $0.24 for Codex and $0.21 for Pi. Self-editing costs more than it saves when little of the learned harness is reused.
- **Weak model (§5.4.3):** with gpt-5-mini on AppWorld, three seeds, Exo made few harness edits and did not reuse its tools on held-out tasks; total cost and pass rate were similar ($6.63 and 59% for Exo against $6.73 and 55% for the control). The authors conclude that there is "an intelligence floor" for the savings.
- The gains are **lower cost**, not higher task success: AppWorld pass rates are identical (96.9% in both arms), and SREGym correctness is described only as "comparable". Edit-only cost is not isolated, but campaign costs including learning and reflection are reported for AppWorld and CLB.

## Why it matters for this survey

The survey's controller rows so far describe offline search over a controller ([Meta-Harness](meta-harness.md)) or editable improvement procedures ([Hyperagents](hyperagents.md)). Exo is the runtime version, and its protected layer is a concrete answer to a design question a self-improving compiler must settle: what the controller may never rewrite. For a compiler, that set is the measurement service, the correctness oracle, the toolchain and the run log. The guardian is where a compiler's acceptance test (correctness plus measured speed on held-out workloads) would sit. Exo's own guardian only checks that the build succeeds, which is far weaker.

## Limits / caveats

No compiler workloads. The reported benefit is lower inference spend, with AppWorld pass rates reported as identical and SREGym correctness described only as comparable, which matters for search cost but is not better optimization results. The saving reverses when reuse is low (the quest experiment) and disappears with a weak model. The guardian's default build check would not catch a regression in what the agent produces. Held-out splits are the authors' own (CLB has none, and AppWorld's are variants of the learning scenarios, so they test reuse within known scenarios more than transfer to new ones), and correctness for SREGym is not quantified. Industry-affiliated authors, one of whom is from an investment firm. Do not extrapolate these adjacent cost results to compiler optimization quality. Strengthened by a compiler-search run in which runtime self-edits lower the cost of reaching a fixed kernel or application target on unseen workloads, with a correctness-and-performance guardian.
