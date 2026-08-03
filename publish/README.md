# Publish survey → PDF + PPTX

English artifacts in `publish/out/`.

## Build

```bash
python3 publish/build_pdf.py     # English PDF
python3 publish/build_pptx.py    # editorial idea deck (not a chart dump)
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.en.pdf` | Full survey PDF |
| `out/next-gen-ai-compiler-survey.pptx` | 15-slide idea exploration deck |

Chinese PDF scripts remain (`--lang zh-CN|zh-TW|all`) but those files are not kept in `out/`.

## PPT design intent

- Explores surveyed **ideas** (thesis, hard limits, four jobs, conflicts, codesign, roadmap)
- Editorial layout (Noto Serif + Inter, paper/ink/copper)
- Few charts, used only where they clarify evidence mix / claim status
- For prettier commercial polish, see [`PPT_TOOLS.md`](PPT_TOOLS.md)

## Requirements

- PDF: `pandoc`, `weasyprint`, `pypdf`
- PPTX: `python-pptx`
- Optional zh PDF: `deep-translator`, `opencc-python-reimplemented`
