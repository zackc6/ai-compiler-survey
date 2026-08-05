# Publish survey → PDF + sharing Beamer deck

English artifacts in `publish/out/`.

## Build

```bash
python3 publish/build_pdf.py       # full survey PDF
python3 publish/build_beamer.py    # sharing deck (Beamer + TikZ)
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.pdf` | Full survey manuscript |
| `out/next-gen-ai-compiler-sharing.pdf` | Sharing deck (diagram-first, §5→§4→§1) |

Source for the deck: [`beamer/expert-briefing.tex`](beamer/expert-briefing.tex).

Per-slide presentation transcripts: [`beamer/transcripts/`](beamer/transcripts/) (`slide-01.md` … `slide-37.md`).

Appendix slides summarize the `reference/` evidence store (products, repos, ★ digests).

## Requirements

- Survey PDF: `pandoc`, `weasyprint`, `pypdf`
- Beamer deck: `pdflatex` + TeX Live (`beamer`, `tikz`, `pgfplots`, Fira, EB Garamond)
- Optional zh survey PDF: `deep-translator`, `opencc-python-reimplemented`
