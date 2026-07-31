# Survey status

Last updated: **2026-07-31**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals (prediction-first) | Done (v2) | README leads with next-gen prediction + agent future |
| **Future prediction section** | Done | `docs/SURVEY.md` §0.1 North star + §5 (incl. §5.4 Magellan/ACCLAIM) |
| Survey narrative (Q1–Q4) | Done (v3) | Gaps framed as blockers to §5 future |
| Traditional vs trends | Done | §1b + `docs/COMPARISON.md` |
| Gaps (10 items) | Done | Blockers to the predicted future |
| **Conflicts (C1–C8)** | Done | `docs/CONFLICTS.md` — Magellan vs MLGO, vendor vs benches, IR rewrite, DSL, … |
| **Evidence-tiered REPOS/PRODUCTS** | Done (v2) | Tier A/B/C; Gerrit/glue demoted |
| Systems / taxonomy | Done (v1) | `docs/SYSTEMS.md`, `docs/TAXONOMY.md` |
| Publication digests | Done (v3) | 85 digests; ACCLAIM paper+code ★; Magellan paper+slides ★ |
| GitHub remote | Blocked on auth | `docs/SETUP_GITHUB.md` |

## Coverage checklist

### Prediction / agent future

- [x] §0.1 North star + §5 future architecture sketch
- [x] Three agent jobs (online / offline / engineering)
- [x] Conflicts register (do not false-consensus)
- [x] Evidence tiers on REPOS/PRODUCTS
- [x] ACCLAIM (2604.04238) + Magellan slides future signals in §5.4 / digests
- [ ] Revisit §5 after next Magellan/MLGO or KernelBench-X public settlement

### Q1 — Trends

- [x] Hybrid LLM–compiler control plane
- [x] CompilerGym/MLGO → foundation LLMs → agents
- [x] MLIR / Triton / StableHLO (+ Tile tension)
- [x] Industrial kernel agents (GEAK, KernelBench, KernelLLM)
- [x] Verification-in-the-loop
- [x] Broadened compile object (FMware, generative compilation)
- [x] §1b traditional vs trends
- [ ] Deeper OpenXLA / IREE production paths
- [ ] Quantization / sparse / speculative-decode compile paths

### Q2 — How agents help

- [x] Selector / Translator / Generator
- [x] Closed-loop propose → check → measure → feedback
- [x] Multi-agent orchestration (ACCLAIM, AutoPass, GEAK)
- [x] Heuristic synthesis (Magellan)
- [ ] Cost models + agent interaction patterns (deeper)

### Q3 — Process reshape

- [x] Control-plane vs data-plane
- [x] Old → new process table + §5.2
- [x] Hard limits (mlirAgent, KernelBench-X)
- [ ] Case study write-ups (Chrome inlining / Magellan production)

### Q4 — Gaps

- [x] 4.1–4.10 detailed write-ups
- [ ] GitHub issues from agenda (needs remote)

### Publications

- [x] Waves A–D + SCM
- [x] Prediction wave: kernel survey, awesome list, GEAK v3, EmitC-MLGO RFC, TRT-LLM agents PR, CompileIQ docs
- [x] ACCLAIM (2604.04238) + Magellan slides future signals → INDEX ★ + SURVEY §5.4
- [ ] Wave E — deepen remaining thin digests from full PDFs

## Change log

| Date | Change |
|---|---|
| 2026-07-31 | Initial scaffold; goals; status; survey; 65 digests |
| 2026-07-31 | §1b comparison; expanded §4 ten gaps |
| 2026-07-31 | REPOS.md + SCM digests |
| 2026-07-31 | Refocus on prediction: CONFLICTS.md (C1–C8), SURVEY §5, tiered REPOS/PRODUCTS, new digests |
| 2026-07-31 | Prediction refocus: §0.1 North star + §5/§5.4; tiered REPOS/PRODUCTS; Q3/Q4→§5 blockers; ACCLAIM+Magellan digests; amazon-science/acclaim Tier A |

## Next actions

1. Authenticate GitHub CLI and push (`docs/SETUP_GITHUB.md`).
2. Watch settlements for conflicts C1 (Magellan vs MLGO EmitC; OpenEvolve OSS path) and C2 (CompileIQ/GEAK vs KernelBench-X).
3. Deepen Wave E digests; expand OpenXLA/IREE only as Tier B substrate.
4. Prefer new Tier A sources over Tier C catalog growth.
