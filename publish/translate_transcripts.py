#!/usr/bin/env python3
"""Translate Beamer slide transcripts: en → zh-TW (via survey MT + OpenCC)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRANS = ROOT / "beamer" / "transcripts"
EN = TRANS / "en"
ZHTW = TRANS / "zh-TW"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--slides",
        nargs="*",
        help="Optional slide numbers like 01 12 24 (default: all en/slide-*.md)",
    )
    args = parser.parse_args()

    # Import after path setup so glossary/translate resolve.
    sys.path.insert(0, str(ROOT))
    from translate import translate_markdown

    EN.mkdir(parents=True, exist_ok=True)
    ZHTW.mkdir(parents=True, exist_ok=True)

    if args.slides:
        sources = [EN / f"slide-{n.zfill(2)}.md" for n in args.slides]
    else:
        sources = sorted(EN.glob("slide-*.md"))

    if not sources:
        print("ERROR: no English transcripts found under", EN, file=sys.stderr)
        return 1

    for src in sources:
        if not src.exists():
            print(f"ERROR: missing {src}", file=sys.stderr)
            return 1
        dest = ZHTW / src.name
        print(f"Translate {src.relative_to(ROOT)} → {dest.relative_to(ROOT)}")
        text = src.read_text(encoding="utf-8")
        zh = translate_markdown(text, target="zh-TW")
        # Keep English product / checkpoint IDs readable in headings.
        dest.write_text(zh.rstrip() + "\n", encoding="utf-8")

    print(f"Done: {len(sources)} zh-TW transcript(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
