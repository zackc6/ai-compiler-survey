# Traditional AI compilation vs following trends

Canonical write-up lives in [`SURVEY.md` §1b](SURVEY.md#1b-traditional-ai-compilation-vs-following-trends).

This file is a short pointer for navigation and status tracking.

## One-line synthesis

Keep traditional compilers as the **data plane** (deterministic lowering, library kernels, CI). Adopt LLM/agent methods as an optional **control plane** (search, orchestration, heuristic synthesis) with admit/fallback—not as a replacement for `opt` / Inductor.

## See also

- Full dimension table and pros/cons: [`SURVEY.md` §1b](SURVEY.md#1b-traditional-ai-compilation-vs-following-trends)
- Future prediction sketch: [`SURVEY.md` §5](SURVEY.md#5-future-prediction-what-next-gen-looks-like)
- Unresolved disagreements: [`CONFLICTS.md`](CONFLICTS.md)
- Gaps that explain why hybrids are not yet default: [`SURVEY.md` §4](SURVEY.md#4-whats-missing--under-covered-q4)
- System gallery: [`SYSTEMS.md`](SYSTEMS.md)
