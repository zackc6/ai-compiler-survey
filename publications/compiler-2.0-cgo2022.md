# CGO 2022 Keynote: Compiler 2.0

| Field | Value |
|---|---|
| **Year** | 2022 |
| **Type** | talk |
| **Group** | Surveys & vision |
| **Link** | [https://www.youtube.com/watch?v=w_sX9aZoZxg](https://www.youtube.com/watch?v=w_sX9aZoZxg) |
| **Evidence tier** | **B** — public lineage for Compiler 2.0 agenda (pre-LLM-agent wave) |
| **Also** | Program: [CGO 2022](https://conf.researchr.org/program/cgo-2022/program-cgo-2022/); successor: [2026 Ken Kennedy plenary](compiler-2.0-cgo2026.md) |

## Key contributions

- Argues the compiler community has been slow to import 21st-century program structures, algorithms, and systems used elsewhere in CS.
- Calls for **radically rethinking how compilers are built**, not only adding another pass.
- Positions ML and modern search/cost models as ways out of sticky, irreversible multi-pass pipelines with weak joint optimization.

## Summary

Saman Amarasinghe’s CGO 2022 keynote (“Why We Need to Modernize Our Compiler Stack…”). Public YouTube recording (~44 min). Sets the **Compiler 2.0** brand that later becomes the Ken Kennedy Award plenary (2026) and the DARPA MOCHA project title. Content is agenda-setting: critique of stagnant construction methods and inspiration via examples, not a single shipped artifact.

## Key takeaways

- “Compiler 2.0” predates the 2024–26 LLM-agent literature; treat 2026 talk as evolution, not a one-off.
- Focus is **modernizing compiler construction** (cost models, search, learned components), which maps to jobs (b)/(d) more than unconstrained IR rewrite.
- Use as historical pointer when citing the 2026 plenary.

## Why it matters for this survey

Lineage evidence for the Compiler 2.0 thread in Surveys & vision. Supports the claim that ML-for-compilers vision work has a multi-year academic through-line (not only vendor blogs).

## Limits / caveats

- Pre-ChatGPT framing; does not discuss tool-using LLM agents or FMware compile objects.
- Video talk — quote carefully; prefer later abstract/MOCHA pages for concrete claims.
