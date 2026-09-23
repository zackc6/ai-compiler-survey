# Publish survey → PDF + sharing Beamer deck

English artifacts in `publish/out/`.

## Build

```bash
python3 scripts/build_blueprint.py # refresh Figure 1
python3 publish/build_pdf.py       # full survey PDF
python3 publish/build_beamer.py    # sharing deck (Beamer + TikZ)
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.pdf` | Full survey manuscript |
| `out/next-gen-ai-compiler-sharing.pdf` | Sharing deck (diagram-first, §5→§4→§1) |

Source for the deck: [`beamer/expert-briefing.tex`](beamer/expert-briefing.tex).

Figure 1 (`docs/architecture-overview.svg`) is generated from `scripts/build_blueprint.py`
as one SVG with four parts: where the agent acts, who does what, controller development,
and forecast horizons. Keep the image followed by its numbered `*Figure` caption in
`docs/SURVEY.md`. The PDF assembler prints each part on its own landscape page, rendering
them into `publish/out/figures/` from the same generator. Inspect all four pages at normal
reading size after a rebuild. The figure check verifies
that the SVGs match their generator; agreement with the narrative requires review.

Per-slide presentation transcripts (English + Traditional Chinese): [`beamer/transcripts/en/`](beamer/transcripts/en/) and [`beamer/transcripts/zh-TW/`](beamer/transcripts/zh-TW/). Regenerate zh-TW with `python3 publish/translate_transcripts.py`.

Appendix slides summarize the `reference/` evidence store (products, repos, ★ digests).

## Requirements

- Survey PDF: `pandoc`, `weasyprint`, `pypdf`
- Beamer deck: `pdflatex` + TeX Live (`beamer`, `tikz`, `pgfplots`, Fira, EB Garamond)
- Optional zh survey PDF: `deep-translator`, `opencc-python-reimplemented`
