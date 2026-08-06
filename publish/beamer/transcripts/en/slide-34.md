# Slide 34: Commercial checklist — handout

Leave-behind slide — three columns. On-slide: Architecture, Trust, Business. Spoken: slow down; let people photograph or copy. This is the operational contract for hybrid agentic compilers.

**Architecture (steel column).**
Typed tools + admit traces — not chat as source of truth (T1, blocker three). Version control ≫ dense memory ≫ scratchpad — freeze artifacts (ACF, kernels, heuristics) in VCS. FSM (finite-state machine) or explicit plan for service targets — know which phase: lab, CI, freeze. Freeze before default-on — zero LLM on serving hot path until oracles and replay pass.

**Trust (amber column).**
Layered oracles — unit/golden → numerical → Alive2-class local → serving A/B (blocker one). CODEOWNERS + signed provenance on every admitted artifact (blocker five). Joint version pins across compiler, model, agent policy. A/B before calling anything “production default” — C2 distributional evidence, not opt-in flags.

**Business (ember column).**
Sell regressable artifacts + build-CI quota — customers buy kernels and control files they can replay, not opaque agent sessions. Customer owns outputs — no “our cloud agent retains your heuristics” surprises. Coverage then performance service target — C9 SKU ordering: coverage SLA (contracted coverage promise) before performance SLA. Token budget per percent gain — name max $/build for median X% win (blocker two). Hybrid economics only work when compile spend is capped and gains are distributional.

**Handout moment.**
Pause. Let people photograph or copy. This triad is the minimum commercial contract for agentic compilers through Horizon A — architecture without trust is unsafe; trust without business model is unreproducible.

Closing line: if your vendor pitch cannot tick every row, you are selling demos — not the hybrid prediction the survey bets on for ~2027–31.
