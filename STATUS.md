# Survey status

Last updated: **2026-07-31**

## Overall progress

| Area | Status | Notes |
|---|---|---|
| Goals (agentic-compiler prediction) | Done (v3) | + roadmap, stack reshape, HW codesign via job (d) |
| Future prediction §5 | Done | Four jobs; codesign feedback plane; §5.5–5.6 pointers |
| **ROADMAP 2027–28 / ~5yr** | Done | `docs/ROADMAP.md` Horizons A/B |
| **STACK reshape** | Done | `docs/STACK.md` layers 1–8 |
| Claims map | Done | `docs/CLAIMS.md` A/P/S/H |
| Conflicts | Done | C1–C10 (+ coverage vs peak, codesign vs EDA) |
| Survey narrative Q1–Q4 | Done (v3) | Gaps as blockers |
| Tiered REPOS/PRODUCTS | Done (v3) | TritorX/KernelEvolve/Helion/AutoKernel |
| Publication digests | Done (v4) | **95** digests (+10 wave) |
| Validate script | Done | `python3 scripts/validate_survey.py` |
| **PDF publish** | Done | `publish/` → en / zh-CN / zh-TW PDFs |
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

## Next actions

1. Watch C1/C2/C9 settlements; update CLAIMS/ROADMAP; rebuild PDF after narrative edits.
2. Prefer new Tier A codesign/agentic-compile sources; skip pure EDA.
3. Deepen Wave E digests; keep `validate_survey.py` green.
