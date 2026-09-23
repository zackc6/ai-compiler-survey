# Publish survey → PDF + sharing Beamer deck

English artifacts in `publish/out/`.

## Build

```bash
python3 scripts/build_blueprint.py # refresh both architecture figures
python3 publish/build_pdf.py       # full survey PDF
python3 publish/build_beamer.py    # sharing deck (Beamer + TikZ)
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.pdf` | Full survey manuscript |
| `out/next-gen-ai-compiler-sharing.pdf` | Sharing deck (diagram-first, §5→§4→§1) |

Source for the deck: [`beamer/expert-briefing.tex`](beamer/expert-briefing.tex).

The architecture overview and controller-development detail are generated from
`scripts/build_blueprint.py`. Keep each image followed by its numbered `*Figure`
caption in `docs/SURVEY.md`; the PDF assembler groups them on one landscape page.
Inspect both pages at normal reading size after a rebuild. The figure check verifies
that the SVGs match their generator; agreement with the narrative requires review.

Per-slide presentation transcripts (English + Traditional Chinese): [`beamer/transcripts/en/`](beamer/transcripts/en/) and [`beamer/transcripts/zh-TW/`](beamer/transcripts/zh-TW/). Regenerate zh-TW with `python3 publish/translate_transcripts.py`.

Appendix slides summarize the `reference/` evidence store (products, repos, ★ digests).

## Requirements

- Survey PDF: `pandoc`, `weasyprint`, `pypdf`
- Beamer deck: `pdflatex` + TeX Live (`beamer`, `tikz`, `pgfplots`, Fira, EB Garamond)
- Optional zh survey PDF: `deep-translator`, `opencc-python-reimplemented`
