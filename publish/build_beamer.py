#!/usr/bin/env python3
"""Build the sharing Beamer deck PDF into publish/out/."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path(__file__).resolve().parent / "beamer"
TEX = SRC_DIR / "expert-briefing.tex"
OUT = Path(__file__).resolve().parent / "out"
PDF_NAME = "next-gen-ai-compiler-sharing.pdf"


def main() -> int:
    if not TEX.exists():
        print(f"ERROR: missing {TEX}", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    build = SRC_DIR / "_build"
    build.mkdir(exist_ok=True)

    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={build}",
        TEX.name,
    ]
    # two passes for overlays / page refs
    for i in range(2):
        print(f"+ {' '.join(cmd)}  (pass {i+1})")
        r = subprocess.run(cmd, cwd=SRC_DIR, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-4000:] if r.stdout else "", file=sys.stderr)
            print(r.stderr[-2000:] if r.stderr else "", file=sys.stderr)
            print("FAILED: pdflatex", file=sys.stderr)
            return r.returncode

    pdf = build / "expert-briefing.pdf"
    dest = OUT / PDF_NAME
    shutil.copy2(pdf, dest)
    print(f"Built: {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
