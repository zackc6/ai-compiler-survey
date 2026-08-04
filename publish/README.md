# Publish survey → PDF + PPTX + visual posters

English artifacts in `publish/out/`.

## Build

```bash
python3 publish/build_pdf.py     # English PDF
python3 publish/build_pptx.py    # editorial idea deck
python3 publish/build_visual.py  # diagram-first PNG posters + visual PPTX
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.pdf` | Full survey PDF (English only in out/) |
| `out/next-gen-ai-compiler-survey.pptx` | 15-slide idea exploration deck |
| `out/next-gen-ai-compiler-survey-visual.pptx` | Full-bleed diagram slides (no tables) |
| `out/visual/*.png` | 13× 1920×1080 posters (hybrid, jobs, stack, codesign, commercial, P23, …) |

Chinese PDF scripts remain (`--lang zh-CN|zh-TW|all`) but those files are not kept in `out/`.

## Visual pack intent

- One composition per image — architecture, orbit, path, ladder, constellation
- Night-forge palette (charcoal / steel / amber); soft radial wash, **no grid** (readability)
- Regenerate whenever SURVEY §5 / four jobs / conflicts move

## PPT design intent

- Explores surveyed **ideas** (thesis, hard limits, four jobs, conflicts, codesign, roadmap)
- Editorial layout (Noto Serif + Inter, paper/ink/copper)
- Few charts, used only where they clarify evidence mix / claim status
- For prettier commercial polish, see [`PPT_TOOLS.md`](PPT_TOOLS.md)

## Requirements

- PDF: `pandoc`, `weasyprint`, `pypdf`
- PPTX: `python-pptx`
- Visuals: `Pillow`
- Optional zh PDF: `deep-translator`, `opencc-python-reimplemented`
