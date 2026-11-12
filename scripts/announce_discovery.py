#!/usr/bin/env python3
"""Prepend a discovery-ledger notice to the Review thread in STATUS.md."""
import pathlib, sys
f, n, events, br, d = sys.argv[1:6]
p = pathlib.Path("STATUS.md"); s = p.read_text(encoding="utf-8")
a = "## Review thread\n\n"
entry = (f"**{d} — Claude (discovery job)** — mechanical ledger `{f}` on branch `{br}`: "
         f"**{n} new source leads**, **{events} indexed-repo events**; these are candidates, not vetted evidence. "
         f"Whichever agent sweeps next triages every row as INCLUDE / EXCLUDE / PENDING in the ledger's Decision "
         f"column and copies INCLUDEs into its Open batch scope; a ledger with blank rows means the sweep is not complete.\n\n")
assert a in s
p.write_text(s.replace(a, a + entry, 1), encoding="utf-8")
