#!/usr/bin/env python3
"""Validate the survey structure, local links, and source-index consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "reference" / "publications"
INDEX = PUB / "INDEX.md"

REQUIRED_SECTIONS = (
    "Key contributions",
    "Summary",
    "Key takeaways",
    "Why it matters",
)

REQUIRED_FIELDS = (
    "**Org**",
    "**Publisher**",
)

DIGEST_LINK_RE = re.compile(r"\]\(([a-zA-Z0-9_./+-]+\.md)\)")


def validate_narrative_and_links(errors: list[str]) -> None:
    survey = ROOT / "docs" / "SURVEY.md"
    text = survey.read_text(encoding="utf-8")
    sections = re.findall(r"^## (\d+|1b)\. ", text, re.MULTILINE)
    expected = ["0", "1", "1b", *map(str, range(2, 10))]
    if sections != expected:
        errors.append(f"SURVEY.md: expected main section order {expected}, found {sections}")
    for horizon in ("One year", "Three years", "Five years", "Ten years", "Beyond ten years"):
        if not re.search(r"^#### 5\.5\.\d+ " + horizon, text, re.MULTILINE):
            errors.append(f"SURVEY.md: missing forecast horizon {horizon!r}")

    # Old links remain valid through explicit anchors after heading rewrites.
    anchors = set(re.findall(r'<a id="([^"]+)"', text))
    for heading in re.findall(r"^#{1,6} (.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        anchors.add(slug)
    documents = [ROOT / "README.md", *ROOT.glob("docs/*.md"),
                 *ROOT.glob("reference/*.md"), *PUB.glob("*.md")]
    for path in documents:
        body = path.read_text(encoding="utf-8-sig")
        for target in re.findall(r"\]\(([^\s)]+)\)", body):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            relative, _, fragment = target.partition("#")
            destination = (path.parent / relative).resolve() if relative else path.resolve()
            if not destination.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link target {target}")
            elif destination == survey and fragment and fragment not in anchors:
                errors.append(f"{path.relative_to(ROOT)}: missing survey anchor {fragment}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    validate_narrative_and_links(errors)

    index_text = INDEX.read_text(encoding="utf-8")
    indexed = {
        Path(m).name
        for m in DIGEST_LINK_RE.findall(index_text)
        if not m.startswith("../") and Path(m).name != "INDEX.md"
    }
    digests = {
        p.name
        for p in PUB.glob("*.md")
        if p.name not in {"INDEX.md", "_TEMPLATE.md"}
    }

    for name in sorted(indexed - digests):
        errors.append(f"INDEX links missing file: reference/publications/{name}")
    for name in sorted(digests - indexed):
        errors.append(f"digest not in INDEX.md: reference/publications/{name}")

    for name in sorted(digests & indexed):
        text = (PUB / name).read_text(encoding="utf-8")
        for sec in REQUIRED_SECTIONS:
            if sec not in text:
                errors.append(f"{name}: missing section '{sec}'")
        for field in REQUIRED_FIELDS:
            if field not in text:
                errors.append(f"{name}: missing field {field}")

    m = re.search(r"\*\*Total:\*\*\s*(\d+)", index_text)
    if m and int(m.group(1)) != len(digests):
        errors.append(f"INDEX Total={m.group(1)} but found {len(digests)} digests")

    for bad in ("鈥", "\ufffd"):
        if bad in index_text:
            errors.append(f"INDEX.md contains mojibake marker {bad!r}")

    print(f"digests={len(digests)} indexed={len(indexed)}")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
