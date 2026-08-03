# Publish survey → PDF + PPTX

English artifacts in `publish/out/`. Scripts can still build Chinese PDFs on demand.

## Quick build (tracked outputs)

```bash
# from repo root
python3 publish/build_pdf.py          # English PDF only (default)
python3 publish/build_pptx.py         # graph-heavy PowerPoint
```

Outputs:

| File | What |
|---|---|
| `out/next-gen-ai-compiler-survey.en.pdf` | English survey PDF |
| `out/next-gen-ai-compiler-survey.pdf` | Legacy alias of English PDF |
| `out/next-gen-ai-compiler-survey.pptx` | Slide deck with charts |

## Optional Chinese PDFs (not kept in out/)

Scripts remain; build then discard or keep locally:

```bash
python3 publish/build_pdf.py --lang zh-CN
python3 publish/build_pdf.py --lang zh-TW
python3 publish/build_pdf.py --lang all
```

## Requirements

- `pandoc`, `weasyprint`, `pypdf` — PDF
- `python-pptx` — PowerPoint
- `deep-translator`, `opencc-python-reimplemented` — Chinese PDF only

## PPT contents (graphs)

Era timeline, agent-job doughnut, evidence tiers, claims status stack, conflicts urgency, stack-layer pressure, roadmap confidence, bibliography group/kind/year charts, author-reported speedup bars (with C2 caveat), online/offline radar, codesign ladder, falsifiers, takeaways.
