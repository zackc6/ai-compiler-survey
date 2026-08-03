#!/usr/bin/env python3
"""Validate digest ↔ INDEX consistency for this survey repo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications"
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


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

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
        errors.append(f"INDEX links missing file: publications/{name}")
    for name in sorted(digests - indexed):
        errors.append(f"digest not in INDEX.md: publications/{name}")

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
