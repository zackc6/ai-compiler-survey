# Slide 20: Blocker 1 — Oracles for money

Blocker 1 unpacked — the oracle **ladder** agents must climb before money moves. Walk bottom-up on the diagram; each layer is necessary, none is sufficient alone.

**Layer 1 — Unit / golden / OpInfo (mute).**
Cheap, fast, CI-friendly — catches obvious crashes and shape errors. **Misses** subtle miscompiles, race bugs, numeric drift on long sequences. Every agent demo stops here; production cannot.

**Layer 2 — Numerical tolerances (mute).**
Reference vs candidate with atol/rtol bands — standard for kernels. **Tolerance games** — agents overfit to test tolerances without true equivalence. Needed but gameable; pair with stricter layers.

**Layer 3 — Alive2 / local honesty (steel).**
**Alive2**-class local formal equivalence on LLVM IR slices — strong for peephole and many scalar transforms; **weak** on **GPU** concurrency, memory models, FP nondeterminism. Use for admit on local rewrites; do not claim serving equivalence.

**Layer 4 — Serving A/B (amber).**
Production **A/B** catches product-level regressions — latency, quality, **$/token**, **SLO** (Service Level Objective) breaches. **Slow** and **hard to attribute** — which band/agent change caused the drift? Still required for **F**-admit (slide 12).

**Layer 5 — Done (green).**
Staged production path: formal/local where cheap → shape-grid diff → statistical serving gates → staged rollout with freeze and rollback. This is what “oracle strong enough for money” means operationally — not one silver bullet.

**Room question (ember footer) — pause for answers.**
Who owns **false negatives** when admit passes and production still miscompiles? Legal, SRE, compiler team, agent vendor — if the room has no owner, blocker 1 is unsolved regardless of model size.

Closing beat: hybrid control plane is only shippable with this ladder + ownership — bridge to blocker 2 (cost/replay) on next slide if time allows.
