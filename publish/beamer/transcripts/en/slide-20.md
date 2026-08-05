# Slide 20: Blocker 1 — Oracles for money

Climb the oracle stack: unit and golden and OpInfo are cheap but miss subtle bugs; numerical tolerances invite games; Alive2-style local honesty is strong locally but weak on GPU concurrency; serving A/B catches product issues but is slow and hard to attribute.

Done looks like: formal, then shape-grid diff, then statistical serving, then staged rollout.

Room question: who owns false negatives when admit passes and production still miscompiles?
