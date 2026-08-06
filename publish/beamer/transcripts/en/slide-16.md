# Slide 16: Checkpoint C1 — heuristics vs neural advisors

**C1** is the highest-signal LLVM-tree bet: evolutionary shippable C++ vs in-tree learned advisors. Two live paths — do not average them into “AI opt wins.”

**Path A — Magellan path (amber, left).**
- Evolve shippable C++ via **`EVOLVE-BLOCK`** markers in LLVM sources — heuristics you can diff, review, and bisect.
- Offline coding agent **is** the control-plane output — not a chat sidebar; the artifact is C++ checked into tree.
- Product shape: evolutionary coding agent + human/oracle **review** before merge. Magellan (Google DeepMind) is Tier A evidence this path ships.

**Path B — MLGO / EmitC path (steel, right).**
- **MLGO** (Machine Learning Guided Optimization) — neural network advisors stay **in-tree** as LLVM pass hooks; agents train/feature the nets rather than replace passes wholesale.
- June 2026 **plan of record** on slide: inliner → Android/Fuchsia → Chrome multi-model rollout — Google-scale deployment signal.
- Agents’ job here is data pipeline + feature engineering for advisors, not unconstrained rewrite.

**Settlement callout (ink, bottom center).**
Watch quarterly through 2027:
- Public Magellan **LLVM patches that displace MLGO** on a hot pass, **or**
- **EmitC-MLGO** becomes customer-default path for major products.

Neither outcome kills hybrid — both keep classical admit. The question is *which shippable artifact shape* wins inside LLVM.

Closing beat: C1 is about artifact type (C++ blocks vs NN advisors), not “agents vs no agents.” Bridge: C2/C5 on slide 17 ask whether any path becomes *default* in build-CI distributions.
