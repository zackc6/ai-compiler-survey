# Slide 38: Appendix — Tier A commercial signals

Tier A products that shape what ships. On-slide: company bands + Tier B footer. Spoken: walk each vendor as a *signal*, not an endorsement — what mechanism they expose.

**Google / DeepMind.**
AlphaEvolve Cloud — evolutionary coding in cloud. Magellan + MLGO in parallel (C1). **MaxKernel** — Pallas/TPU peak agent with compiler and XProf admit; not ASIC coverage (C9 still open). Signal: offline heuristics, in-tree advisors, and a TPU kernel agent coexist.

**NVIDIA.**
CompileIQ with agent-skills — online specialize, ACF-class control files, following the Agent Skills `SKILL.md` spec (packaging, not T1). CUDA Tile / Tile IR — hardware-native kernel surface. **Cake IR** (research, with CMU) — typed schedule IR plus evolving verifier; serving-validated KDA. TensorRT-LLM agent skills — serving-stack integration. Signal: typed tools + kernel DSL + serving, not chat-only.

**AMD.**
**GEAK v4** — e2e Amdahl triage on warm sglang/vLLM. **Hyperloom** (21 Sep 2026) sits above that: framework pass first, then one kernel backend (GEAK or KernelForge), critic keep/revert, mission in a state file. Author median 1.73× on 16 workloads. Signal: serving \(F\), not only kernel microbench. Still not a public p50 default path (**C2**).

**CausalFlow et al.**
**Argus** — data-flow invariants + SMT on MI300X; 99–104% of assembly TFLOPS on selected families. Research paper, **not** an AMD SKU. Signal: compile-time kernel admit exists on Instinct-class hardware; peak on three families is C2 *color*, not settlement.

**Meta.**
LLM Compiler / KernelLLM — IR and PyTorch→Triton specialization. TritorX + KernelEvolve — bring-up / codesign feedback (job d). Helion / **TLX** — raise vs extend Triton (KernelEvolve already searches Triton+TLX). Signal: full stack from portable graph to silicon feedback, still hybrid.

**FlashInfer.**
FlashInfer-Bench — serving-trace ladder with `apply()` into SGLang/vLLM. Signal: T6/T8 serving-kernel rung exists; settlement still needs default-path A/B (C2).

**Tier B baselines (footer).**
TensorRT-LLM, Inductor, XLA/StableHLO, FlashInfer runtime, Modular MAX, OpenVINO, Neuron, Hexagon-MLIR — data-plane defaults agents must interoperate with, not replace (C6-B).

Closing beat: Tier A tells you where vendors bet agent control plane; Tier B is what must still admit and lower.
