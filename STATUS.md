# Survey status

Last updated: **2026-08-03**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals (agentic-compiler prediction) | Done (v3) | + roadmap, stack reshape, HW codesign via job (d) |
| Future prediction §5 | Done | Four jobs; codesign; §5.5–5.6; **§5.7 commercialization** |
| **ROADMAP 2027–28 / ~5yr** | Done | `docs/ROADMAP.md` Horizons A/B |
| **STACK reshape** | Done | `docs/STACK.md` layers 1–8 |
| Claims map | Done | `docs/CLAIMS.md` A/P/S/H |
| Conflicts | Done | C1–C10 (+ coverage vs peak, codesign vs EDA) |
| Survey narrative Q1–Q4 | Done (v3) | Gaps as blockers |
| Tiered REPOS/PRODUCTS | Done (v3) | TritorX/KernelEvolve/Helion/AutoKernel |
| Publication digests | Done (v5) | **100** digests (+ Compiler 2.0 / MOCHA; KernelEvolve blog) |
| Validate script | Done | `python3 scripts/validate_survey.py` |
| **PDF + PPTX publish** | Done | English PDF + editorial PPTX in `publish/out/` |
| **Visual posters** | Done | Diagram-first PNGs + visual PPTX via `publish/build_visual.py` |
| **Survey skill** | Done | `.cursor/skills/survey/` (+ personal `~/.cursor/skills/survey/`) |
| GitHub remote | Available | work on `main` and push |

## Coverage checklist

### Prediction / roadmap / codesign

- [x] §0.1 + §5 architecture with job (d) bring-up/codesign
- [x] ROADMAP Horizon A (2027–28) + B (~5 years)
- [x] STACK SW+HW layer map focused on agentic compiler
- [x] TritorX, KernelEvolve, Ascend diagnosis, KForge, AutoKernel, Helion digests
- [x] Conflicts C9 (coverage vs peak), C10 (codesign vs autonomous chip)
- [ ] Second-vendor public TritorX-class reproduction
- [ ] Revisit after Magellan/MLGO or KernelBench-X settlement

### Publications

- [x] Waves A–D + SCM + prediction wave
- [x] Codesign/roadmap wave: TritorX, KernelEvolve, Ascend diagnosis, KForge, AutoKernel(+gh), Kernel Forge, KernelBlaster, Helion(+gh)
- [ ] Wave E — deepen thin digests from full PDFs

## Change log

| Date | Change |
|---|---|
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

## Next actions

1. Watch C1/C2/C9 settlements; update CLAIMS/ROADMAP; rebuild PDF after narrative edits.
2. Prefer new Tier A codesign/agentic-compile sources; skip pure EDA.
3. Deepen Wave E digests; keep `validate_survey.py` green.
