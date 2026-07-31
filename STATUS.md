# Survey status

Last updated: **2026-07-31**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals & repo scaffold | Done | README, STATUS, docs skeleton |
| Expanded survey narrative (Q1–Q4) | Done (v1) | `docs/SURVEY.md` — broaden continuously |
| System comparison table | Done (v1) | `docs/SYSTEMS.md` |
| Taxonomy / stack diagram | Done (v1) | `docs/TAXONOMY.md` |
| Publication digests | Done (Wave A–D v1) | **65** digests under `publications/` |
| Publication INDEX | Done | `publications/INDEX.md` |
| GitHub remote + progressive pushes | Blocked on auth | Local commit ready; see `docs/SETUP_GITHUB.md` |
| Interactive canvas sync | Optional | Mirror of chat canvas; not required for GitHub |

## Coverage checklist

### Q1 — Trends

- [x] Hybrid LLM–compiler control plane
- [x] From CompilerGym/MLGO → foundation LLMs → agents
- [x] MLIR / Triton / StableHLO substrate
- [x] Industrial kernel agents (GEAK, KernelBench, KernelLLM)
- [x] Verification-in-the-loop (Alive2 / LLM-VeriOpt)
- [x] Broadening of compile object (generative compilation, FMware)
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

### Q4 — Gaps

- [x] Initial gap list (10 items)
- [ ] Prioritized research agenda with owners/questions
- [ ] Benchmark unification proposal draft

### Publications digests

- [x] Wave A — surveys, foundation LLM compilers, Magellan/AlphaEvolve, KernelBench/GEAK
- [x] Wave B — agent papers (AwareCompiler, AutoPass, HintPilot, ACCLAIM, Generative Compilation, …)
- [x] Wave C — classic DL compilers + MLGO lineage
- [x] Wave D — NVIDIA/AMD/Modular/Anthropic posts + HN/Discourse
- [ ] Wave E — deepen digests with quotes/numbers from full PDFs where thin

## Change log

| Date | Change |
|---|---|
| 2026-07-31 | Initial repository scaffold; goals; status tracker; expanded survey docs; 65 publication digests |

## Next actions

1. Authenticate GitHub CLI (`gh auth login`) and create/push remote repo.
2. Optionally deepen Wave E digests from full PDFs.
3. Expand OpenXLA/IREE/Mojo sections in `docs/SURVEY.md`.
4. Use PRs/issues on GitHub for progressive survey updates.
