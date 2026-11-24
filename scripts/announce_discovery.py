#!/usr/bin/env python3
"""Prepend a discovery-ledger notice to the Review thread in STATUS.md.

Arguments: ledger, new-lead count, event count, branch, date, and optionally the
ref@sha that ran. A run from a branch other than main is a live test of unmerged
discovery code and is labelled so: its ledger is evidence about the script, not a sweep."""
import os, pathlib, re, subprocess, sys
f, n, events, br, d = sys.argv[1:6]
prov = sys.argv[6] if len(sys.argv) > 6 else ""
p = pathlib.Path("STATUS.md"); s = p.read_text(encoding="utf-8")
a = "## Review thread\n\n"
# The workflow announces from a checkout of main, where the ledger (committed on the discovery
# branch `br`) is absent. Read it from LEDGER_FILE if given, else the working tree, else the
# branch itself. `f` stays the path named in the notice.
src = pathlib.Path(os.environ.get("LEDGER_FILE") or f)
ledger = src.read_text(encoding="utf-8") if src.exists() else ""
if not ledger and not os.environ.get("LEDGER_FILE"):
    for ref in (br, f"origin/{br}"):
        r = subprocess.run(["git", "show", f"{ref}:{f}"], capture_output=True, text=True)
        if r.returncode == 0:
            ledger = r.stdout
            break
if prov and not ledger:
    sys.exit(f"announce_discovery: ledger {f} not readable from {src} or branch {br}; "
             "refusing to publish an unlabelled notice")
status = re.search(r"^\*\*Status: [^\n]*", ledger, re.M)
regress = re.search(r"^Known-positive regression[^\n]*", ledger, re.M)
test = bool(prov) and not prov.startswith("main@")
entry = (f"**{d} — Claude (discovery job{', LIVE TEST of ' + prov if test else ''})** — mechanical ledger `{f}` on branch `{br}`"
         + (f" (script {prov})" if prov and not test else "") + ": "
         f"**{n} new source leads**, **{events} indexed-repo events**; these are candidates, not vetted evidence. "
         + (f"{status.group(0)} " if status else "")
         + (f"{regress.group(0)} " if regress else "")
         + ("This test ledger checks the unmerged discovery code; it is not a merge candidate and its rows need no triage."
            if test else
            "Whichever agent sweeps next triages every row as INCLUDE / EXCLUDE / PENDING in the ledger's Decision "
            "column and copies INCLUDEs into its Open batch scope; a ledger with blank rows means the sweep is not complete.")
         + "\n\n")
assert a in s
p.write_text(s.replace(a, a + entry, 1), encoding="utf-8")
