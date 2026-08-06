# Slide 19: Commercial blockers — top 5

Before technique deep dives, rank **productization gaps** — why hybrid is not default in production yet. Lean from SURVEY §5.7 and §4. Each blocker gets one following slide; this is the menu.

**1 — Oracles strong enough for money (ember).**
Fast-but-wrong specialize creates **liability** — admit passed, production miscompiled, dollars and reputation burn. Without stacked oracles, agents stay demo-tier. Deep dive: slide 20.

**2 — Cost / replay / when agents run (amber).**
**Nondeterministic $N compiles** — agent search is stochastic; without freeze, admit hash, and budget caps, cloud compile bills explode and CI becomes irreproducible. Product needs policy: when may the agent run, what gets cached, what is replayed from **VCS** artifacts.

**3 — Agent↔compiler contract (steel).**
**Natural-language-only** interface is a demo — no typed tools, no schema, no legality surface. Production needs **MCP**-class servers, compile schema, per-band plugin contracts. Without contract, every agent hop is a bespoke integration.

**4 — Distributional production evidence (ink).**
No **default-path A/B** yet in most orgs — wins are lab traces, not pinned production distributions. Ties directly to **C2** checkpoint: p50/p90 on real builds, not vendor headlines.

**5 — Ownership · supply chain · human review (mute).**
Unowned agent code in **TCB** (trusted computing base) — who maintains evolved heuristics? License on generated kernels? **PR** review ownership when Archer-class merges agent patches? Governance blocker, not FLOPs.

**Footer line.**
Each blocker is a product gap, not a research wishlist — if they cannot name an owner for oracle failures (blocker 1) and compile cost (blocker 2), hybrid stays pilot forever.

Closing beat: oracles first — slide 20 opens the ladder.
