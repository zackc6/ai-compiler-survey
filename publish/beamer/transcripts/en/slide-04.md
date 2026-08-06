# Slide 4: Six active trends

This is the §1 backdrop. On-slide: claim lines dominate; org tags are the tiny mute foot line only. Spoken: claim first, then name examples with organization.

**A — Hybrid guidance, not LLM-as-compiler.**
Free **IR** (Intermediate Representation) rewrite is fragile: mlirAgent from UC Berkeley shows frontier models scoring below identity on IR transforms. Winners constrain the action space. AgentCompile (City University of Hong Kong) emits advisory metadata; templates plus checks admit CUDA. HintPilot (Zhejiang University, with Purdue) inserts compiler-validated pragmas, not arbitrary rewrites. Meta’s LLM Compiler proposes pass lists that `opt` applies. Say out loud: constrain actions; keep the classical applicator.

**B — From RL gyms to LLM agents.**
Leave CompilerGym-style opaque neural policies in the gym era. Move to tool-using and multi-agent loops. Compiler-R1 (ISCAS / UCAS) trains tool-calling pass search with **SFT** (supervised fine-tuning) + **RL** (reinforcement learning). Magellan (Google DeepMind / Google) synthesizes shippable C++ heuristics inside LLVM/XLA. FlowCompile (UMass Amherst, MIT, MIT-IBM Watson) compiles structured LLM workflows offline — control-plane substrate, not only chat. Also nod to Auto / AgentFlow for freeze and **ADG** (Agent Dependency Graph) if time allows.

**C — MLIR + Triton as default substrate.**
The production AI path is still classical stacks with org fingerprints: Meta PyTorch → TorchInductor → Triton (OpenAI-origin, community); parallel **StableHLO** / **HLO** (High Level Operations) → OpenXLA/Google XLA and IREE. Peak performance often still sits in NVIDIA vendor libraries, CUDA Tile, CUTLASS, FlashAttention-class kernels. **MLIR** (Multi-Level IR) is the shared mid-IR; product lowering paths diverge by vendor.

**D — Kernel agents go industrial.**
KernelBench (Stanford / Princeton Scaling Intelligence) asks for correct *and* faster kernels; one-shot success is often under 20%, fusion remains hard. GEAK (AMD) runs generate–eval–reflect–optimize for Triton on Instinct. KernelLLM (Meta) specializes PyTorch→Triton at smaller model size. AgentCompile (CityU) bounds CUDA specialization for transformer graphs. Closing beat: refinement raises correctness more reliably than speed — the portability bottleneck for new models and non-NVIDIA **GPU** (graphics processing unit) hardware.

**E — Verification enters the loop.**
Stack the oracles: unit and golden tests, numerical checks versus reference (AgentCompile-style), then Alive2-class local formal equivalence (Alive2 from the UIUC / formal-IR lineage; used in LLM-VeriOpt-style rewards). Strong locally; weak on **GPU** races and floating-point nondeterminism. Admit for money needs this ladder, not a single check.

**F — Compilers broaden their object.**
Beyond graph→binary: mid-decode diagnosis in generative compilation loops; FMware — prompts, agents, free parameters — as a compile object in Compiler.next (Queen’s University). Magellan (Google) treats agents as in-tree heuristic engineers. Anthropic’s Claude C Compiler shows agent teams *building* a compiler (~100kLoC Rust) — adjacent evidence for agents as compiler engineers, not only compile-time optimizers.

Closing line for the slide: six trends, one pattern — hybrid control plane over classical substrates, with named orgs behind each example.
