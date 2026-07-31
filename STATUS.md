# Survey status

Last updated: **2026-07-31**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals & repo scaffold | Done | README, STATUS, docs skeleton |
| Expanded survey narrative (Q1–Q4) | Done (v2) | `docs/SURVEY.md` includes §1b + full §4 gaps |
| Traditional vs trends comparison | Done | `docs/SURVEY.md` §1b + `docs/COMPARISON.md` |
| Gaps (10 items, detailed) | Done | Production, correctness, cost, interop, interfaces, FMware, data, HITL, security, benchmarks |
| System comparison table | Done (v1) | `docs/SYSTEMS.md` |
| Taxonomy / stack diagram | Done (v1) | `docs/TAXONOMY.md` |
| Publication digests | Done (Wave A–D v1) | **65** digests under `publications/` |
| Publication INDEX | Done | `publications/INDEX.md` |
| GitHub remote + progressive pushes | Blocked on auth | Local commits ready; see `docs/SETUP_GITHUB.md` |
| Interactive canvas sync | Optional | Mirror of chat canvas; not required for GitHub |

## Coverage checklist

### Q1 — Trends

- [x] Hybrid LLM–compiler control plane
- [x] From CompilerGym/MLGO → foundation LLMs → agents
- [x] MLIR / Triton / StableHLO substrate
- [x] Industrial kernel agents (GEAK, KernelBench, KernelLLM)
- [x] Verification-in-the-loop (Alive2 / LLM-VeriOpt)
- [x] Broadening of compile object (generative compilation, FMware)
- [x] Traditional vs trends pros/cons (§1b)
- [ ] Deeper coverage of OpenXLA / IREE production paths
- [ ] Mojo / Modular stack detail
- [ ] Quantization / sparse / speculative-decode compile paths

### Q2 — How agents help

- [x] Selector / Translator / Generator roles
- [x] Closed-loop propose → check → measure → feedback
- [x] Multi-agent orchestration (ACCLAIM, AutoPass, GEAK)
- [x] Heuristic synthesis (Magellan)
- [ ] Cost models + agent interaction patterns (deeper)
- [ ] Tool-calling failure modes catalog

### Q3 — Process reshape

- [x] Control-plane vs data-plane distinction
- [x] Old → new process table
- [x] Hard limits (mlirAgent IR rewrite, KernelBench-X)
- [ ] Case study write-ups (Chrome inlining / Magellan production)

### Q4 — Gaps (detailed write-ups)

- [x] 4.1 End-to-end production evidence
- [x] 4.2 Correctness at scale (whole-program / FP / GPU races)
- [x] 4.3 Cost & reproducibility of agent compile loops
- [x] 4.4 Cross-stack interoperability
- [x] 4.5 Hardware-native agent interfaces
- [x] 4.6 FMware / agent-app compilation
- [x] 4.7 Training data for compilers
- [x] 4.8 Human-in-the-loop compiler engineering
- [x] 4.9 Security / supply chain
- [x] 4.10 Unified benchmarks
- [x] Cross-cutting research agenda + org questions
- [ ] Optional: turn agenda into GitHub issues once remote exists

### Publications digests

- [x] Wave A — surveys, foundation LLM compilers, Magellan/AlphaEvolve, KernelBench/GEAK
- [x] Wave B — agent papers (AwareCompiler, AutoPass, HintPilot, ACCLAIM, Generative Compilation, …)
- [x] Wave C — classic DL compilers + MLGO lineage
- [x] Wave D — NVIDIA/AMD/Modular/Anthropic posts + HN/Discourse
- [ ] Wave E — deepen digests with quotes/numbers from full PDFs where thin

## Change log

| Date | Change |
|---|---|
| 2026-07-31 | Initial repository scaffold; goals; status; survey docs; 65 publication digests |
| 2026-07-31 | Added §1b traditional vs trends comparison; fully expanded §4 ten gaps |

## Next actions

1. Authenticate GitHub CLI and create/push remote (`docs/SETUP_GITHUB.md`).
2. Optionally deepen Wave E digests from full PDFs.
3. Expand OpenXLA/IREE/Mojo sections in `docs/SURVEY.md`.
4. Open GitHub issues from the §4 research agenda for progressive work.
