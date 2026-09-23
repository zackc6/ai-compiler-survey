# Implementation and evaluation evidence

Use these projects to investigate interfaces, baselines, and experiments for the [design guide](../docs/SURVEY.md). A repository shows inspectable artifacts; it does not by itself establish measured benefit, current maintenance, or independent reproduction. Check the relevant source digest and version before relying on it.

## Optimization and compiler engineering

| Project | What to inspect | Question to test |
|---|---|---|
| [Archer](https://github.com/cuhk-s3/Archer) and [llvm-harness](https://github.com/dtcxzyw/llvm-harness) | Review and repair workflows using compiler-specific tools. | Does feedback improve defect detection and reviewer effort? |
| [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve) and [HeuriGym](https://github.com/cornell-zhang/heurigym) | Evolutionary search and heuristic evaluation. | Do generated heuristics generalize to held-out applications? |
| [ACCLAIM](https://github.com/amazon-science/acclaim) | Cooperation between a language model and compiler at several levels. | Which interactions contribute measurable gains? |
| [mlirAgent](https://github.com/ucb-bar/mlirAgent) | Compiler tools and experiments with representation edits. | Which feedback or action-space changes address observed failures? |
| [LLM4IR](https://github.com/hjiang13/LLM4IR) | Evaluation of models’ understanding of compiler representations. | Does better understanding translate into better optimization? |
| [Compiler-R1](https://github.com/Mind4Compiler/Compiler-R1) | Reinforcement learning with compiler tools. | How does learned tool use compare with conventional search? |
| [HintPilot](https://github.com/ZJU-PL/hintpilot) | Restricted compiler hints and pragmas. | What performance is lost or gained by restricting actions? |
| [CompileIQ](https://github.com/NVIDIA/CompileIQ) | Compiler configuration search and reusable artifacts. | Does the selected configuration improve the intended workload? |
| [Claude’s C compiler](https://github.com/anthropics/claudes-c-compiler) | An agent-built compiler implementation. | How much workload and target coverage survives independent testing? |
| [MLGO training tools](https://github.com/google/ml-compiler-opt) | Learned compiler policies. | When is a learned policy preferable to generated heuristic code? |
| [CompilerGym](https://github.com/facebookresearch/CompilerGym) | Compiler optimization environments. | Are the action space and reward representative of deployment? |

Magellan’s papers and [LLVM presentation](publications/magellan-llvm-slides.md) provide the research account. OpenEvolve and HeuriGym offer related public experimentation routes; they should not be represented as independent reproductions of Magellan’s production results.

## Kernel and application optimization

| Project | What to inspect | Evaluation boundary |
|---|---|---|
| [KernelBench](https://github.com/ScalingIntelligence/KernelBench) and [KernelBench-X digest](publications/kernelbench-x.md) | Kernel generation, correctness, and performance protocols. | Passing a test does not establish a speedup or full numerical coverage. |
| [KernelAgent](https://github.com/meta-pytorch/KernelAgent) | Generation and validation of Triton kernels. | Separate kernel outcomes from application outcomes. |
| [GEAK](https://github.com/AMD-AGI/GEAK) and [GEAK-agent](https://github.com/AMD-AGI/GEAK-agent) | AMD kernel workflows and application-level evaluation. | Match versions, workloads, and baseline configurations. |
| [Hyperloom](https://github.com/AMD-AGI/Hyperloom) | Serving optimization and delegation to kernel tools. | Attribute runtime/framework gains separately from kernel gains. |
| [Accelerator agents](https://github.com/AI-Hypercomputer/accelerator-agents) | MaxKernel and JAXBench on supported targets. | Target-specific peak results do not establish new-chip coverage. |
| [KernelGenBench](https://github.com/flagos-ai/KernelGenBench) | Tasks across sources and devices, including search-cost measurements. | Compare success and regression distributions under declared budgets. |
| [AutoKernel](https://github.com/RightNow-AI/autokernel) | Profiling-directed application and kernel work. | Measure whether optimizing the selected bottleneck helps the application. |
| [FlashInfer-Bench](https://github.com/flashinfer-ai/flashinfer-bench) | Workload traces, kernel evaluation, and serving integration. | Keep kernel validation and application validation distinct. |
| [VibeServe](https://github.com/uw-syfi/vibe-serve) | Research on serving-stack synthesis. | Evaluate the whole generated execution path and deployment assumptions. |
| [Helion](https://github.com/pytorch/helion) | Tile programming, configuration spaces, and tuning. | Consult the [2026 tuning report](publications/helion-llm-autotuning.md) for model-guided search evidence. |
| [Kernel-headroom artifacts](https://github.com/gauravapiscean/kernel-headroom) | Workload profiles, numerical checks, and DLRM-Bench. | Inspect the classification and projection assumptions before generalizing. |
| [Kernel generation bibliography](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) | Discovery of further primary sources. | A bibliography is not an evaluation. |

TritorX and KernelEvolve have important paper and industry-report evidence. Do not assume full public implementations or reproducibility merely because related libraries are public.

## Compiler interfaces and reusable components

| Project | Why it belongs in an experiment |
|---|---|
| [LLVM](https://github.com/llvm/llvm-project) | Existing analyses, transformations, code generation, and learned-policy integration. |
| [TVM](https://github.com/apache/tvm) and [TIRx kernels](https://github.com/mlc-ai/tirx-kernels) | Tensor representations, schedule controls, and example kernels. |
| [TileLang](https://github.com/tile-ai/tilelang) and [language tools](https://github.com/tile-ai/tilelang-lsp) | Tile programming, layout inference, and editor/tool feedback. |
| [Triton](https://github.com/triton-lang/triton), [Gluon digest](publications/triton-gluon.md), and [Triton extensions](https://github.com/facebookexperimental/triton) | Different levels of layout and scheduling control. |
| [Triton-distributed](https://github.com/ByteDance-Seed/Triton-distributed), also the [DITRON](publications/ditron.md) project | Related implementations of joint computation, memory movement, and communication; one research lineage. |
| [FlyDSL](https://github.com/ROCm/FlyDSL) | Python-based control for AMD kernel programming. |
| [CUTLASS and CuTe](https://github.com/NVIDIA/cutlass) | NVIDIA kernel components and layout/scheduling interfaces. |
| [ThunderKittens](https://github.com/hazyresearch/thunderkittens) | Tile abstractions embedded in CUDA. |
| [OpenXLA](https://github.com/openxla/xla), StableHLO, and [Shardy](publications/shardy.md) | Model compilation and distributed tensor decisions. |
| PyTorch `torch.compile` and Inductor | Application-facing compilation and integration. |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) and [FlashInfer](https://github.com/flashinfer-ai/flashinfer) | Serving execution and kernel integration targets. |
| [KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) | Paired PyTorch and Triton training examples; inspect coverage and leakage. |
| [Mirage](publications/mirage.md) and [Prism](publications/prism.md) | Structured superoptimization baselines and possible search components. |

[IBM’s analog hardware toolkit](https://github.com/IBM/aihwkit) supplies executable noise and drift models for [statistical evaluation](publications/analog-validation.md); simulation and measured hardware evidence must remain distinct.

## Workflow infrastructure

| Project | Scope |
|---|---|
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | General agent runtime and session state. |
| [Agent Skills](https://github.com/agentskills/agentskills) | Skill packaging and discovery. |
| [SIGIL](https://github.com/sigilagent/sigil) | Skill compilation into executable workflows. |
| [SkCC](https://github.com/Nexa-Language/Skill-Compiler) | Skill representations and code generation. |
| [SkillSmith](https://github.com/AetherHeart-AI/Aeloon) | Research on skill boundaries and compilation. |
| Gerrit [AI review](https://gerrit.googlesource.com/plugins/ai-code-review/), [ReviewAI](https://github.com/amarula/reviewai-gerrit-plugin), and [GerritForge provider](https://github.com/GerritForge/ai-review-agent-provider) | General review interfaces; add and evaluate compiler checks before claiming compiler-specific benefit. |

Infrastructure can support a future optimizer without proving that optimizer’s performance. Negative results are useful evidence for choosing the next experiment; they do not establish permanent limits on the architecture. Detailed accounts are in the [publication index](publications/INDEX.md).
