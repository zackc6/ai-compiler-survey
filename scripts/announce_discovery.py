#!/usr/bin/env python3
"""Prepend a discovery-ledger notice to the Review thread in STATUS.md."""
import pathlib, sys
f, n, br, d = sys.argv[1:5]
p = pathlib.Path("STATUS.md"); s = p.read_text(encoding="utf-8")
a = "## Review thread\n\n"
entry = (f"**{d} — Claude (discovery job)** — mechanical ledger `{f}` on branch `{br}`: **{n} new candidates** "
         f"not in the index (arXiv listings, venue TOCs, cited-by of Tier A digests, tracked GitHub orgs, PyPI). "
         f"Whichever agent sweeps next triages every row as INCLUDE / EXCLUDE / PENDING in the ledger's Decision "
         f"column and copies INCLUDEs into its Open batch scope; a ledger with blank rows means the sweep is not complete.\n\n")
assert a in s
p.write_text(s.replace(a, a + entry, 1), encoding="utf-8")
