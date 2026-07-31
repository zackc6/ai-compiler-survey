#!/usr/bin/env python3
"""Assemble living-survey markdown into one publishable bundle."""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "out"

# Narrative-first order for the PDF manuscript.
SECTIONS: list[tuple[str, Path]] = [
    ("Survey narrative", ROOT / "docs" / "SURVEY.md"),
    ("Roadmap", ROOT / "docs" / "ROADMAP.md"),
    ("Software stack & HW codesign reshape", ROOT / "docs" / "STACK.md"),
    ("Claims map", ROOT / "docs" / "CLAIMS.md"),
    ("Conflicts register", ROOT / "docs" / "CONFLICTS.md"),
    ("Systems comparison", ROOT / "docs" / "SYSTEMS.md"),
    ("Taxonomy", ROOT / "docs" / "TAXONOMY.md"),
    ("Publications index", ROOT / "publications" / "INDEX.md"),
]


def cover_md(today: str) -> str:
    return f"""<div class="cover">

# Next-Generation AI Compiler Survey

<p class="subtitle">Predicting the agentic compiler (~2027–28 and ~5 years): software-stack reshape and HW–SW codesign</p>

<p class="meta">
<strong>Living survey export</strong><br/>
Generated: {today}<br/>
Source repository: ai-compiler-survey<br/>
Primary narrative: docs/SURVEY.md · Roadmap: docs/ROADMAP.md · Stack: docs/STACK.md
</p>

<div class="verdict">

**North star.** Agents own semantic search, orchestration, and artifact synthesis. Compilers own lowering, legality, measurement, and fallback. Hardware codesign enters only through kernels, IR, tests, and profilers — not autonomous tape-out.

</div>

</div>
"""


def rewrite_links(text: str) -> str:
    """Best-effort link rewrite so PDF-relative paths stay meaningful."""
    replacements = {
        "](../publications/": "](publications/",
        "](../STATUS.md)": "](STATUS.md)",
        "](CONFLICTS.md)": "](#conflicts-register)",
        "](ROADMAP.md)": "](#roadmap)",
        "](STACK.md)": "](#software-stack--hw-codesign-reshape)",
        "](CLAIMS.md)": "](#claims-map)",
        "](REPOS.md)": "](docs/REPOS.md)",
        "](PRODUCTS.md)": "](docs/PRODUCTS.md)",
        "](SYSTEMS.md)": "](#systems-comparison)",
        "](TAXONOMY.md)": "](#taxonomy)",
        "](WORKFLOW.md)": "](docs/WORKFLOW.md)",
        "](../docs/SURVEY.md)": "](#survey-narrative)",
        "](../docs/ROADMAP.md)": "](#roadmap)",
        "](../docs/STACK.md)": "](#software-stack--hw-codesign-reshape)",
        "](../docs/CONFLICTS.md)": "](#conflicts-register)",
        "](../docs/REPOS.md)": "](docs/REPOS.md)",
        "](../docs/PRODUCTS.md)": "](docs/PRODUCTS.md)",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text


def strip_first_h1(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and lines[0].strip() == "":
            lines = lines[1:]
    return "\n".join(lines).strip() + "\n"


def assemble() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    parts: list[str] = [cover_md(today)]

    for title, path in SECTIONS:
        if not path.is_file():
            raise FileNotFoundError(path)
        body = strip_first_h1(path.read_text(encoding="utf-8"))
        body = rewrite_links(body)
        anchor = title.lower().replace(" ", "-").replace("&", "").replace("--", "-")
        parts.append(
            f'<div class="section-break"></div>\n\n'
            f'## {title} {{#{anchor}}}\n\n'
            f"{body}\n"
        )

    parts.append(
        "\n---\n\n"
        "## Export notes\n\n"
        "- Full digests remain in `publications/*.md` (not inlined).\n"
        "- Tier maps: `docs/REPOS.md`, `docs/PRODUCTS.md`.\n"
        "- Rebuild: `python3 publish/build_pdf.py`.\n"
    )

    bundle = OUT / "survey-bundle.md"
    bundle.write_text("\n".join(parts), encoding="utf-8")
    return bundle


if __name__ == "__main__":
    path = assemble()
    print(f"Wrote {path}")
