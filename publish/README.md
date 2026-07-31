# Publish survey → PDF

Build a single PDF of the living survey (narrative + roadmap + stack + claims + conflicts + systems).

## Quick build

```bash
# from repo root
python3 publish/build_pdf.py
```

Outputs:

- `publish/out/survey-bundle.md` — assembled Markdown
- `publish/out/survey.html` — intermediate HTML
- `publish/out/next-gen-ai-compiler-survey.pdf` — **publish artifact**

## Requirements

- Python 3.10+
- `pandoc` (assemble/optional)
- `weasyprint` (`pip install weasyprint`) — default PDF engine

Fallback if WeasyPrint fails:

```bash
python3 publish/build_pdf.py --engine wkhtmltopdf
```

## What is included

| Order | Source | Role |
|---|---|---|
| 1 | cover (generated) | Title / north star |
| 2 | `docs/SURVEY.md` | Q1–Q4 + §5 prediction |
| 3 | `docs/ROADMAP.md` | 2027–28 / ~5yr |
| 4 | `docs/STACK.md` | SW + HW-codesign reshape |
| 5 | `docs/CLAIMS.md` | Claim ↔ evidence map |
| 6 | `docs/CONFLICTS.md` | C1–C10 |
| 7 | `docs/SYSTEMS.md` | System table |
| 8 | `docs/TAXONOMY.md` | Roles / layers |
| 9 | `publications/INDEX.md` | Bibliography |

Digests stay in `publications/` (linked from INDEX); they are not inlined into the PDF.

## Re-publish after survey edits

1. Update docs / digests on `main` as usual.
2. `python3 publish/build_pdf.py`
3. Commit `publish/out/next-gen-ai-compiler-survey.pdf` if you want the artifact on the remote.
