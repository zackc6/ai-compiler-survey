# Survey status

Last updated: **2026-08-04**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals (agentic-compiler prediction) | Done (v3) | + roadmap, stack reshape, HW codesign via job (d) |
| Future prediction §5 | Done | Four jobs; codesign; §5.5–5.6; **§5.7 commercialization** |
| **Roadmap 2027–28 / ~5yr** | Done | folded into `docs/SURVEY.md` §5.5 |
| **STACK reshape** | Done | folded into `docs/SURVEY.md` §5.6 |
| Claims map | Done | `docs/SURVEY.md` §7 (A/P/S/H) |
| Conflicts | Done | `docs/SURVEY.md` §6 C1–C10 |
| Survey narrative §0–§9 | Done (v3) | Single reading path; gaps as blockers |
| **Reference store** | Done | `reference/` guide → publications / products / repos |
| Publication digests | Done (v7) | **108** digests under `reference/publications/` |
| Validate script | Done | `python3 scripts/validate_survey.py` |
| **PDF publish** | Done | Survey PDF + expert Beamer deck in `publish/out/` |
| **Survey skill** | Done | `.cursor/skills/survey/` (+ personal `~/.cursor/skills/survey/`) |
| GitHub remote | Available | work on `main` and push |

## Coverage checklist

### Prediction / roadmap / codesign

- [x] §0.1 + §5 architecture with job (d) bring-up/codesign
- [x] SURVEY §5.5 Horizon A (2027–28) + B (~5 years)
- [x] SURVEY §5.6 SW+HW layer map focused on agentic compiler
- [x] TritorX, KernelEvolve, Ascend diagnosis, KForge, AutoKernel, Helion digests
- [x] Conflicts C9 (coverage vs peak), C10 (codesign vs autonomous chip)
- [ ] Second-vendor public TritorX-class reproduction
- [ ] Revisit after Magellan/MLGO or KernelBench-X settlement

### Publications

- [x] Waves A–D + SCM + prediction wave
- [x] Codesign/roadmap wave: TritorX, KernelEvolve, Ascend diagnosis, KForge, AutoKernel(+gh), Kernel Forge, KernelBlaster, Helion(+gh)
- [x] Agent control-plane substrate: Auto, FlowCompile, AgentFlow, Heterogeneous agentic AI
- [ ] Wave E — deepen thin digests from full PDFs

## Change log

| Date | Change |
|---|---|
| 2026-08-04 | Add LaTeX Beamer expert briefing (~28 slides, diagram-first; §5→§4→§1) → `publish/out/next-gen-ai-compiler-expert-briefing.pdf` |
| 2026-08-04 | Remove visual posters, PPTX decks, and `build_visual.py` / `build_pptx.py` — PDF-only publish |
| 2026-08-04 | Refresh §5.1 + architecture-evolution visuals; add 2-slide share deck `architecture-51-and-evolution.pptx` |
| 2026-08-04 | Rescan: EmitC-MLGO June 2026 PoR checkpoint (C1 not settled); +CuTeGen ★, CompileIQ agent-skills ★, Hexagon-MLIR; INDEX **108** |
| 2026-08-04 | Distill docs-consolidation + prediction lessons into `.cursor/skills/survey` (SKILL.md architecture rules + survey.md experience log) |
| 2026-08-04 | Consolidate docs into one reading path: fold TAXONOMY/SYSTEMS/CLAIMS/CONFLICTS/WORKFLOW (+ COMPARISON stub) into `docs/SURVEY.md` §0 / §1b / §6–§9; `docs/` = SURVEY + SETUP_GITHUB only |
| 2026-08-04 | Fold STACK into SURVEY §5.6; drop circular SURVEY↔STACK pointers |
| 2026-08-04 | Collect evidence under `reference/` (guide → publications / products / repos) |
| 2026-08-04 | Fold ROADMAP into SURVEY §5.5; drop circular SURVEY↔ROADMAP pointers; remove self-repo name from PDF cover / setup notes |
| 2026-08-04 | Redraw §5.1 architecture + §5.5 architecture-evolution diagrams; add visual posters (architecture stack, Today→A→B evolution) |
| 2026-08-04 | Add agent control-plane substrate digests (Auto, FlowCompile, AgentFlow, Hetero); wire §0.1, Trend B, §4.6, §5.1, §5.7 P3/P22/P23; INDEX **104** |
| 2026-07-31 | Initial scaffold through prediction refocus (C1–C8, §5, tiers) |
| 2026-07-31 | Roadmap + stack reshape + HW codesign (job d); C9–C10; +10 digests; CLAIMS/WORKFLOW/validate |
| 2026-07-31 | Add `publish/` PDF pipeline; export `next-gen-ai-compiler-survey.pdf` |
| 2026-07-31 | Distill methodology into `.cursor/skills/survey` skill |
| 2026-08-03 | PDF publish builds en + zh-CN + zh-TW |
| 2026-08-03 | Keep only English PDF in out/; add graph-heavy PPTX builder |
| 2026-08-03 | Redesign PPTX as editorial idea deck; add PPT_TOOLS.md suggestions |
| 2026-08-03 | Add Compiler 2.0 Ken Kennedy plenary + lineage + MOCHA; SURVEY §1.5 vision map |
| 2026-08-03 | Fix KernelEvolve INDEX title (full paper name); add Meta Engineering blog digest |
| 2026-08-03 | Add Org + Publisher to all digests and INDEX; validate requires fields |
| 2026-08-03 | Visual survey pack: 10 diagram posters + visual PPTX in publish/out |
| 2026-08-03 | SURVEY §5.7: commercialization critical problems (contract, memory, sub-agents, …) |
| 2026-08-03 | Expand §5.7 → P1–P22 (eval, economics, tenancy, IP, versioning, DR, A/B, compliance, …) |
| 2026-08-03 | §5.7 P23: tokens / inference / model capability survey + conclusion |
| 2026-08-03 | Rebuild PDF + visuals (+ commercial/P23 posters) + editorial PPTX |
| 2026-08-03 | Update `.cursor/skills/survey` with §5.7/P23, visuals, Org, hybrid lessons |

## Next actions

1. Watch C1 customer uptake (Android/Fuchsia EmitC; Chrome multi-model) and Magellan OSS recipes; C2 p50/p90; C9 second-vendor TritorX-class.
2. Prefer new Tier A codesign/agentic-compile sources; skip pure EDA.
3. Deepen Wave E digests; keep `validate_survey.py` green.
