# Publish survey → PDF

English PDF in `publish/out/`.

## Build

```bash
python3 publish/build_pdf.py     # English PDF
```

| Output | Role |
|---|---|
| `out/next-gen-ai-compiler-survey.pdf` | Full survey PDF (English only in out/) |

Chinese PDF scripts remain (`--lang zh-CN|zh-TW|all`) but those files are not kept in `out/`.

## Requirements

- PDF: `pandoc`, `weasyprint`, `pypdf`
- Optional zh PDF: `deep-translator`, `opencc-python-reimplemented`
