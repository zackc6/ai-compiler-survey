# Slide 23: Blocker 4 — Distributional production evidence

Blocker four: evidence that survives contact with production. On-slide: funnel graphic — wide top, narrow bottom. Spoken: walk each band, then name the marketing bar the survey actually trusts.

**Top — curated kernels and opt-in flags.**
Vendor headline blogs, KernelBench hot runs, GEAK best-of demos. Easy to publish; easy to cherry-pick. C2 (median/p90 on pinned traces) exists precisely because headline peaks lie — the slide-17 bar chart tension: ~15% vendor headline vs ~2.5% on docs hot kernels. Magellan and CompileIQ can each show stunning single-kernel wins; neither settles C2 until the distribution moves. Say out loud: opt-in flags are not default-path evidence.

**Middle — attribution gets hard.**
CUDA Graphs, KV-cache layouts, GEMV micro-kernels, serving runtimes — gains blur across bands. FlashInfer-Bench and VibeServe-class serving traces help, but multi-month stability on *default* builds is still rare. This is where T6 (serving-level oracles) and T8 (benchmark ladder) must connect IR → kernel → fused → serving.

**Bottom — default-path A/B plus multi-month stability.**
What C2 settlement needs: pinned public traces, p50 and p90 (50th / 90th percentile) gains across the build distribution, cost-to-compile, persistent serving throughput — MLGO-style QPS under load, not single-kernel speedups. Money-grade oracles from blocker one must gate entry to this band.

Closing beat: the marketing bar is median + 90th-percentile + dollars-to-compile + serving stability. Anything less is pressure, not settlement. Do not average disagreements — wait for distributional wins on the path customers actually run.
