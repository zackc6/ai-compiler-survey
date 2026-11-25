#!/usr/bin/env python3
"""Emit a discovery ledger's review evidence as GitHub Actions notice annotations.

Read-only test runs keep their ledgers as artifacts, but artifact downloads go through blob
storage that an agent's sandbox may not reach. Check-run annotations are readable through the
public REST API (GET /repos/{o}/{r}/check-runs/{job_id}/annotations), so the review evidence is
published there too, in priority order:

1. header: provenance, frozen-corpus cutoff, window, status with every DEGRADED channel and its
   reason, known-positive regression, raw candidates per channel;
2. the frozen-corpus recovery estimate;
3. the refs seed audit (Codex 14:58: low recovery must be readable as coverage gap, rate limit,
   or unresolved seed);
4. the head of the fetch log (budget, breaker, truncation, HTTP failures).

GitHub cuts an annotation message at about 4 KB (run 45419826954 lost the recovery table
after 4062 characters), so each part is split on line boundaries into chunks whose escaped message
is at most CHUNK UTF-8 bytes (the truncation marker included), leaving room for the title framing. Each part is capped so a long recovery table cannot crowd out the diagnostics; every capped part
says so and points to the artifact. Usage: ledger_notices.py <ledger> <label> [artifact-name].
At most 9 notices per step."""
import pathlib, re, sys

path, label = pathlib.Path(sys.argv[1]), sys.argv[2]
artifact = sys.argv[3] if len(sys.argv) > 3 else "the ledger artifact"
if not path.exists():
    print(f"::warning title={label}::ledger {path} missing")
    sys.exit(0)
text = path.read_text(encoding="utf-8")


def section(start: str, stop: str = r"^#{2,3} ") -> str:
    m = re.search(rf"^{start}.*?(?={stop}|\Z)", text, re.S | re.M)
    return m.group(0).strip() if m else ""


head = "\n".join(l for l in text.splitlines()[:16] if l.strip() and not l.startswith("Triage "))
raw = re.search(r"^Raw candidates per channel:.*$", text, re.M)
diag = section(r"## Channel diagnostics", r"\Z")
audit = section(r"### refs seed audit", r"^Fetch log")
fetch = section(r"Fetch log", r"\Z")
# (text, notices allowed) — 9 in total; the header is never cut.
parts = [(head + ("\n" + raw.group(0) if raw else ""), 2),
         (section(r"## Frozen-corpus recovery estimate", r"^## "), 3),
         (audit or ("refs seed audit: not in this ledger (refs did not run)" if diag else ""), 2),
         (fetch, 1)]


def esc(s: str) -> str:
    return s.replace("%", "%25").replace("\r", "").replace("\n", "%0A")


# Budget = UTF-8 bytes of the *emitted* message, after workflow-command escaping (Codex 16:31:
# a character budget let a non-ASCII table reach ~4.5 KB once "\n" became "%0A" and "%" "%25").
CHUNK = 3500


def cost(s: str) -> int:
    return len(esc(s).encode("utf-8"))


def take(s: str, budget: int) -> int:
    """Longest prefix length of s whose escaped UTF-8 size fits budget (at least 1 char)."""
    lo, hi = 1, len(s)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(s[:mid]) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo


def split_lines(body: str, budget: int = CHUNK):
    buf = ""
    for line in body.splitlines(keepends=True):
        while cost(line) > budget:
            if buf:
                yield buf
                buf = ""
            k = take(line, budget)
            yield line[:k]
            line = line[k:]
        if cost(buf + line) > budget:
            yield buf
            buf = ""
        buf += line
    if buf:
        yield buf


n = 0
for body, allowed in parts:
    if not body:
        continue
    chunks = list(split_lines(body))
    if len(chunks) > allowed:
        marker = f"\n… truncated for the annotation budget; full text in {artifact}"
        chunks = chunks[:allowed]
        last = chunks[-1]
        chunks[-1] = last[:take(last, CHUNK - cost(marker))] + marker
    for c in chunks:
        n += 1
        print(f"::notice title={label} {n}::{esc(c)}")
print(f"::notice title={label} pointer::Complete ledger (all rows, channel diagnostics, fetch log): {artifact}")
