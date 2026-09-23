# Product and deployment evidence

These offerings and first-party reports inform the [design guide](../docs/SURVEY.md). Research prototypes are included when they expose useful implementation choices; their inclusion does not imply a supported commercial product. See also the [implementation map](repos.md).

## Optimization services and integrations

| Offering | Reported role | Design implication or limitation |
|---|---|---|
| [AlphaEvolve on Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/alphaevolve-is-available-for-everyone) | Evolutionary optimization offered as a service. | A deployment model for expensive search; service availability does not establish compiler superiority. |
| Google Magellan and MLGO | Generated compiler heuristics and learned decision policies. | Compare both ways to amortize optimization into a compiler. |
| [NVIDIA CompileIQ](https://developer.nvidia.com/cuda/compileiq) and [agent skills](https://nvidia.github.io/CompileIQ/stable/install.html) | Workload-specific compiler configuration and optimization workflows. | Preserve reusable configuration artifacts and validate actual application benefit. |
| [AMD GEAK](https://github.com/AMD-AGI/GEAK) | Kernel optimization and application profiling/measurement workflows. | Let application bottlenecks select kernel work; check the version and protocol. |
| [AMD Hyperloom](publications/hyperloom.md) | Application optimization with kernel work delegated to GEAK or KernelForge. | Evaluate the complete serving path and separate framework from kernel gains. |
| NVIDIA TensorRT-LLM [agent integration proposal](https://github.com/NVIDIA/TensorRT-LLM/pull/12831) | Compiler and kernel workflows inside a serving stack. | A proposed integration is a signal, not evidence of universal default deployment. |
| [Helion](https://pytorch.org/projects/helion/) and its [model-guided tuner](publications/helion-llm-autotuning.md) | Higher-level kernel programming and automated configuration search. | Measure tuning time separately from final kernel latency. |
| [FlashInfer-Bench](https://github.com/flashinfer-ai/flashinfer-bench) | Evaluation and substitution of kernels in serving workloads. | Connect a kernel experiment to application measurements. |

## Research systems that affect product design

| System | Useful capability | Scope of evidence |
|---|---|---|
| [MaxKernel](publications/maxkernel.md), [Pallas](publications/pallas.md), [JAXBench](publications/jaxbench.md) | Kernel optimization and evaluation on tensor processing units. | Performance on a supported platform; not proof of coverage on a new chip. |
| Meta LLM Compiler and [KernelLLM](https://huggingface.co/facebook/KernelLLM) | Models specialized for compiler or kernel tasks. | Model releases are ingredients for a system, not complete deployment evidence. |
| Meta TritorX and KernelEvolve | Hardware enablement and performance optimization across accelerator targets. | Separate coverage results, kernel measurements, and industry deployment reports. |
| [CAKE](publications/cake.md) | Schedule representation and compiler feedback developed with agents. | Author evaluation; compares complete programming environments. |
| [Ave, formerly Argus](publications/argus.md) | Compile-time data-flow assertions and useful failure feedback. | Revised September 2026 MI300X results; do not reuse older Argus metrics. |
| [CUDA Tile](https://developer.nvidia.com/blog/focus-on-your-algorithm-nvidia-cuda-tile-handles-the-hardware/) | Tile-oriented programming and compiler representation. | An interface candidate; its existence does not establish the best agent architecture. |

## Existing compiler and runtime choices

These are baselines and possible components. Their maturity is a reason to evaluate reuse, not a permanent requirement to preserve their boundaries.

| Platform | Role in a design experiment |
|---|---|
| NVIDIA TensorRT-LLM and CUDA libraries | Established serving and kernel baselines. |
| [FlashInfer](https://github.com/flashinfer-ai/flashinfer) | Attention and related kernels used by serving systems. |
| PyTorch `torch.compile` and Inductor | Application capture, compilation, and integration. |
| OpenXLA XLA, StableHLO, and [Shardy](publications/shardy.md) | Model representation, compilation, and distributed tensor partitioning. |
| JAX [Pallas](publications/pallas.md) and Mosaic | Kernel programming and compilation on supported accelerators. |
| Modular MAX and Mojo | An alternative compiler and runtime stack. |
| Intel OpenVINO | Deployment toolkit for supported processors and devices. |
| AWS Neuron and its kernel interface | Compilation and kernel control for AWS accelerators. |
| Qualcomm AI Hub, Qualcomm Neural Network tools, and [Hexagon-MLIR](https://github.com/qualcomm/hexagon-mlir) | Device deployment and an open compiler path for Hexagon. |

## Adjacent infrastructure and historical context

| Item | Why it is included cautiously |
|---|---|
| Olive, ONNX Runtime, Hugging Face Optimum | Deployment and packaging context; assess separately from agent optimization. |
| OctoML | Historical commercial context for automated tuning; avoid assuming a current offering. |
| Generic AI code-review products | Workflow evidence until connected to compiler-specific checks. |
| Anthropic’s C compiler experiment | Evidence about agents constructing compiler software; not a general commercial compiler result. |
| [DeepSeek Harness](publications/deepseek-harness.md) | General agent runtime; compiler-specific evaluation must be added. |
| [Agent Skills specification](publications/agent-skills-spec.md) | A packaging format, not a compiler optimization method. |
| SIGIL, SkCC, SkVM, SkillSmith, and SKILL.state | Skill compilation and workflow-state research; compiler-task transfer needs measurement. |

Update this map when a source changes an interface, deployment fact, or design decision. A paper, product page, and code release about one system remain one evidence family.
