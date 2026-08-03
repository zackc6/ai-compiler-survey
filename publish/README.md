# Publish survey → PDF (en / zh-CN / zh-TW)

Build PDFs of the living survey in **English**, **Simplified Chinese**, and **Traditional Chinese**.

## Quick build (all languages)

```bash
# from repo root
python3 publish/build_pdf.py
```

Outputs under `publish/out/`:

| File | Language |
|---|---|
| `next-gen-ai-compiler-survey.en.pdf` | English |
| `next-gen-ai-compiler-survey.zh-CN.pdf` | 简体中文 |
| `next-gen-ai-compiler-survey.zh-TW.pdf` | 繁體中文 |
| `next-gen-ai-compiler-survey.pdf` | English (legacy alias) |

## One language only

```bash
python3 publish/build_pdf.py --lang en
python3 publish/build_pdf.py --lang zh-CN
python3 publish/build_pdf.py --lang zh-TW
```

## Requirements

- Python 3.10+
- `pandoc`
- `weasyprint` (`pip install weasyprint`) — default PDF engine
- `deep-translator`, `opencc-python-reimplemented` — for Chinese builds
- CJK-capable font (e.g. WenQuanYi Micro Hei / Noto CJK)

Fallback engine:

```bash
python3 publish/build_pdf.py --engine wkhtmltopdf
```

## How Chinese is produced

1. Assemble English manuscript from `docs/*` + `publications/INDEX.md`.
2. Machine-translate body EN → **zh-CN** (glossary-protected domain terms).
3. Convert **zh-CN → zh-TW** with OpenCC (`s2twp`).
4. Attach hand-written Chinese covers (not machine-translated).
5. Render each locale to PDF with CJK fonts.

English docs remain the source of truth. Re-run after narrative edits.

## What is included

Cover + SURVEY + ROADMAP + STACK + CLAIMS + CONFLICTS + SYSTEMS + TAXONOMY + INDEX.

Digests stay in `publications/` (not inlined).
