# Slide 17: Checkpoints C2 + C5 — gains & default path

Two checkpoints on one slide — left is illustrative tension chart; right is the settlement prose. Emphasize: chart is **not** a meta-analysis; it shows the metric mismatch to avoid.

**Chart — illustrative tension (left).**
Bar one: **vendor headline ~15%** — best-case kernel or pass-order win on cherry-picked benchmark. Bar two: **docs hot kernels ~2.5%** — median-ish gains on documentation-style representative kernels. The gap is the whole point: marketing peak ≠ build-CI distribution. Do not let the room anchor on the tall bar.

**Define percentiles in the room (C2).**
- **p50** — 50th percentile: **median** gain across pinned builds/traces. Typical compile, not hero kernel.
- **p90** — 90th percentile: near-tail wins; still not single best blog post.

**C2 — agents become default.**
“Agents are default” requires **median (p50) build-CI wins** on **pinned public traces** — reproducible, distributional evidence. One KernelBench hero or one LLVM inliner win is necessary but not sufficient. Settlement: published trace suite + reported p50/p90, not headline only.

**C5 — online specialize vs offline eng.**
Two coexistence modes — both may live:
- **Online specialize** — control files, hints, **ACF**s at compile/serve time (job **a)**.
- **Offline eng** — Magellan/**MLGO** heuristics evolved offline (job **b)**).

The product question: **which is the default flag?** Release notes and compiler driver defaults reveal true path — not keynote slides.

**Settlement (bottom of right box).**
Pinned public traces + release notes listing agent / control-file workflows. If their vendor cannot point to both, treat “default agent compiler” as aspirational.

Closing beat: C2 is distribution; C5 is default flag — together they test whether hybrid left the lab.
