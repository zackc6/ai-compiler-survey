# Slide 38: Appendix — Tier A commercial signals

Tier A products that shape what ships. On-slide: company bands + Tier B footer. Spoken: walk each vendor as a *signal*, not an endorsement — what mechanism they expose.

**Google / DeepMind.**
AlphaEvolve Cloud (GA) — evolutionary coding in cloud. Magellan + MLGO in parallel — heuristic synthesis *and* in-tree learned advisors (C1 live in production). Signal: offline agent-as-output and in-tree NN advisors coexist.

**NVIDIA.**
CompileIQ with agent-skills — online specialize, ACF-class control files. CUDA Tile / Tile IR — hardware-native kernel surface agents must address. TensorRT-LLM agent skills — serving-stack integration. Signal: typed tools + kernel DSL + serving, not chat-only.

**AMD.**
GEAK — multi-agent generate–eval–reflect–optimize for Triton on Instinct. Signal: kernel agents go industrial on second-vendor hardware (C9 pressure).

**Meta.**
LLM Compiler / KernelLLM — IR and PyTorch→Triton specialization. TritorX + KernelEvolve — bring-up / codesign feedback (job d). Helion — kernel DSL path. Signal: full stack from portable graph to silicon feedback, still hybrid.

**FlashInfer.**
FlashInfer-Bench — serving-trace ladder with `apply()` into SGLang/vLLM. Signal: T6/T8 serving-kernel rung exists; settlement still needs default-path A/B (C2).

**Tier B baselines (footer).**
TensorRT-LLM, Inductor, XLA/StableHLO, FlashInfer runtime, Modular MAX, OpenVINO, Neuron, Hexagon-MLIR — data-plane defaults agents must interoperate with, not replace (C6-B).

Closing beat: Tier A tells you where vendors bet agent control plane; Tier B is what must still admit and lower.
