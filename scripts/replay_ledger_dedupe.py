#!/usr/bin/env python3
"""Replay the indexed-repo event URL dedupe over a stored discovery ledger.

    python3 scripts/replay_ledger_dedupe.py reference/discovery/2026-11-15.md

Parses the "Events in indexed repositories" table of a ledger, runs
``discover.dedupe_repo_events`` over its rows and prints the before/after counts,
every canonical URL that occurred more than once with the families it was listed
under, and the ledger's per-repository truncation lines grouped by canonical URL
host path. This is arithmetic over the stored ledger: it shows which rows the
URL guard would have merged. It is NOT a rerun of discovery, so it cannot show
events that a run with canonical-repository resolution would fetch in addition.
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import discover as d  # noqa: E402

ROW = re.compile(r"\| (\S+) \| \[(.*?)\]\((\S+)\) \| (.*?) \| *(.*?) *\|$")


def parse_events(text: str) -> list[dict]:
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("## Events in indexed repositories"))
    end = next(i for i, l in enumerate(lines) if l.startswith("## ") and i > start)
    rows = []
    for line in lines[start:end]:
        m = ROW.match(line)
        if not m:
            continue
        date, title, url, why, _decision = m.groups()
        fam = re.search(r"family ([^\s;]+)", why)
        family = fam.group(1) if fam else title.split(":", 1)[0]
        rows.append({"channel": "repoevent", "id": f"{family}@{url.rsplit('/', 1)[1]}",
                     "title": title, "date": date, "url": url, "why": why})
    return rows


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    rows = parse_events(text)
    d.DIAG.clear()
    out = d.dedupe_repo_events(rows)
    print(f"{path}: {len(rows)} event rows before URL dedupe, {len(out)} after")
    families = defaultdict(set)
    for r in rows:
        families[d.canonical_event_url(r["url"])].add(re.search(r"family ([^\s;]+)", r["why"]).group(1))
    dups = {u: f for u, f in families.items() if Counter(d.canonical_event_url(r["url"]) for r in rows)[u] > 1}
    print(f"canonical URLs listed more than once: {len(dups)}")
    for u in sorted(dups):
        print(f"  {u}  <- {', '.join(sorted(dups[u]))}")
    trunc = [l for l in text.splitlines() if l.startswith("- repoevent truncated:")]
    cap = [l for l in trunc if "only " in l]
    print(f"truncation lines: {len(trunc)} (cap lines: {len(cap)})")
    for l in cap:
        print(f"  {l}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "reference/discovery/2026-11-15.md"))
