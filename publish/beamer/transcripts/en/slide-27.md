# Slide 27: Technical Prediction — Accelerate The Roadmap

Open §5.8 technical prediction. On-slide: headline band, then two columns (within / outside compiler), footer. Spoken: lead with the ask, then walk T1–T10 at category level — detail on slides 28–29.

**Headline — settle checkpoints, ship Horizon A.**
To falsify or confirm C1, C2, C5, C3/C6, C9, C10, you enhance techniques *inside and outside* the classical compiler — not one silver bullet in `opt`. The prediction is hybrid: agents on the control plane, classical lowering on the data plane, soft merge M1 not hard replace M3.

**Within the compiler (T1–T5).**
T1 typed agent↔compiler interfaces — constrain the action space (C3, C5, C6). T2 admit/fallback machinery — hybrid advisory path, not unconstrained rewrite (C6-B). T3 control files, hints, fingerprints + replay — ACF freeze artifacts (C2, C5). T4 heuristic hooks and in-tree advisors — Magellan vs MLGO race (C1). T5 dialect/ISA feedback sinks — coverage→performance bring-up, proposals not tape-out (C9, C10).

**Outside the compiler (T6–T10).**
T6 serving-level oracles and production A/B — distributional evidence (C2). T7 open multi-IR corpora with negatives — training selectors, not monolithic IR LLMs. T8 unified benchmark ladder — IR→kernel→fused→serving + cost-to-compile (C2, C9). T9 provenance, ownership, HITL — demote generic forge AI (C7). T10 agent-workflow compile/freeze/place — ADG, freeze artifacts, Horizon B substrate.

**Footer beat.**
Enhancing only `opt`/Inductor/Triton internals is not enough — PGO (profile-guided optimization) and MLGO advisors help the data plane; they do not supply serving A/B, corpora, or workflow freeze. Next slides: exists · missing · unlocks per technique. Survey lean: T1–T5 ship as product surfaces; T6–T10 are equally first-class — mostly outside classical lowering. E2E-optimal-seeking under F ties all ten together via soft merge M1.
