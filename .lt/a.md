# Discovery ledger — 2026-11-24

Provenance: script `9eb33aae21fa` (main), run started 2026-11-24 15:00 UTC. OpenAlex: key absent (keyless, about $0.10/day per IP); 0 lists + 0 searches = about $0.0000; 0 per-second 429s; breaker: not tripped.

Frozen corpus: `4336d72f42c2` committed 2026-09-23 UTC; cutoff 2026-09-24 (derived: day after the corpus commit).

Window: since 2026-09-24. Channels: none. Candidates: 0 raw, 0 already indexed, **0 new source leads**, **0 indexed-repo events**.

**Status: all enumerated channels returned candidates.**

Known-positive regression (sources the method once missed; checked before the index dedupe): AccelOpt: NOT TESTED: expected channel venue omitted from this run; Reflexion: NOT TESTED: expected channel refs omitted from this run; Voyager: NOT TESTED: expected channel refs omitted from this run; MemGPT: NOT TESTED: expected channel refs omitted from this run; TASO: NOT TESTED: expected channel refs omitted from this run; Ansor: NOT TESTED: expected channel refs omitted from this run.

Limits of this check: it matches titles only, so a work cut before metadata resolution (refs cap) or on a failed venue page cannot be named, only flagged as possibly truncated; a date-windowed channel cannot recover a source older than its window (out-of-window, not a miss). The CoALA mechanism-checklist control is a sweep-checklist test (§4.6 rows), not a channel test, and is not run here. Same-day ledgers must still be reconciled as a union with channel provenance before discovery is called closed.

Triage source rows as INCLUDE (digest it), EXCLUDE (reason), or PENDING (what is missing). For indexed-repo events use UPDATE-DIGEST, NOTE-IN-REPOS or IGNORE with a reason. Mark every Decision cell on the batch branch; blank means the sweep is unfinished.

## Channel diagnostics

Raw candidates per channel: {}

Fetch log (failures and venue page sizes):


