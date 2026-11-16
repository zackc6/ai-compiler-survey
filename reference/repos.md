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
| [GEAK](https://github.com/AMD-AGI/GEAK) (`AMD-AGI/GEAK-agent` is the renamed alias of the same repository, ID 1028816796, resolved 15 November 2026) | AMD kernel workflows and application-level evaluation; PR #539 (14 November 2026) adds a `mega_fusion` expert workflow in which an `expert_skill_id` pins a MegaMoE skill behind a skill-contract checker (skills packaging, no new measurement). | Match versions, workloads, and baseline configurations. |
| [Hyperloom](https://github.com/AMD-AGI/Hyperloom) | Serving optimization and delegation to kernel tools. | Attribute runtime/framework gains separately from kernel gains. |
| [Accelerator agents](https://github.com/AI-Hypercomputer/accelerator-agents) | MaxKernel and JAXBench on supported targets; `auto_search` gains continuous hill-climbing from an initial kernel with frontier resumption and a forward/backward-pass contract re-check (#138–#139, 6 November 2026; no new result in the messages). | Target-specific peak results do not establish new-chip coverage. |
| [KernelGenBench](https://github.com/flagos-ai/KernelGenBench) | Tasks across sources and devices, including search-cost measurements. | Compare success and regression distributions under declared budgets. |
| [AutoKernel](https://github.com/RightNow-AI/autokernel) | Profiling-directed application and kernel work; PRs #22–#23 (8–9 November 2026) add long-context prefill (paged KV, `gqa_prefill_attention`), attention %-of-peak calibration against FlashInfer and SDPA backends, cold/warm time-to-first-token tooling and `decode_step` gates that refuse truncated streams — a lead for a digest update once the numbers are read. | Measure whether optimizing the selected bottleneck helps the application. |
| [FlashInfer-Bench](https://github.com/flashinfer-ai/flashinfer-bench) | Workload traces, kernel evaluation, and serving integration. | Keep kernel validation and application validation distinct. |
| [VibeServe](https://github.com/uw-syfi/vibe-serve) | Research on serving-stack synthesis. | Evaluate the whole generated execution path and deployment assumptions. |
| [Helion](https://github.com/pytorch/helion) | Tile programming, configuration spaces, and tuning; a `[cutedsl]` tcgen05 (Blackwell) backend stream landed 14 November 2026 (epilogue, split-K and batched-GEMM defaults), and the 12 November PyTorch post *Fast by Default: Compile-Time Heuristics for Helion Kernels* is pending primary reading. | Consult the [2026 tuning report](publications/helion-llm-autotuning.md) for model-guided search evidence. |
| [Kernel-headroom artifacts](https://github.com/gauravapiscean/kernel-headroom) | Workload profiles, numerical checks, and DLRM-Bench. | Inspect the classification and projection assumptions before generalizing. |
| [KernelBench-Verified](https://github.com/facebookresearch/kernel_bench_verified) | TF32 baseline, hidden input transformations, and peak-memory measurement for KernelBench. | Fixed hidden transformations can be anticipated; keep the baseline precision explicit. |
| [CUDA Tile evaluation artifacts](https://github.com/uwm-se/CuTile) | Matrix-multiplication and attention kernels across cuTile, Triton, and CUDA baselines. | Check tuning parity and baseline versions before comparing languages. |
| [Triton AI Compiler](https://github.com/francois141/triton_ai_compiler) and [PTX Gym](https://github.com/francois141/ptx_gym) | Direct PTX candidates, checking and optimization traces; commits of 4–7 November 2026 add "GPT-6 compiler results" and after-GPT-6-cutoff Liger selective-logprob benchmarks (unread; a lead for updating the [AI as a Compiler](publications/ai-as-compiler.md) digest). | Does direct synthesis beat Triton after counting all failed trials and GPU time? |
| [TIRx Harness](https://github.com/mlc-ai/TIRx-harness) | Compiler analysis, references, experiments and candidate frontiers. | Which harness components make an independent contribution? |
| [Kernel generation bibliography](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) | Discovery of further primary sources. | A bibliography is not an evaluation. |
| [VOLTA](https://github.com/willtunnels/volta) | PTX-level equivalence and race checking over the reals; 39 paper benchmarks ([digest](publications/volta-gpu-equivalence.md)). | A proof covers CTA 0 and the nominated outputs in real arithmetic, not IEEE results or application speed. |
| [lean_kernel_verify](https://github.com/facebookresearch/lean_kernel_verify) | Lean-checked bounds, write coverage and barrier contracts from TLX/Triton and CuTe DSL IR ([digest](publications/lean-kernel-verify.md)). | Concrete case inputs only; UNDECIDED is not PASS; no production detection rate. |
| [ptxv](https://github.com/meta-pytorch/ptxv) | Binary-level (SASS/PTX) verifier for Blackwell kernels: race, deadlock and protocol checks over hardware-allowed schedules, proven per-output bounds against a reference kernel, error distributions under an input distribution; assumptions registry and 87-pair mutant suite ([digest](publications/ptxv.md)). | Verdicts hold for the captured inputs and launch shape; equivalence is to a reference kernel, not a specification; Blackwell only; no detection rate over generated kernels published. |
| [HPCAgent-Bench](https://github.com/spcl/hpcagent-bench) | Matched-intervention benchmark harness ([digest](publications/hpcagent-bench.md)); releases v0.3.0–v0.5.0 (25 October – 3 November 2026) and 14 November grading commits (fixed held-out case set on a golden store; mismatch-fraction thresholds tied to measured FP-contraction flips). | Release notes unread; the per-comparison efficacy table behind "two of 40" is still not in the indexed v1 text. |
| [ProfileLens](https://github.com/AMD-AGI/ProfileLens) | Trace, counter and empirical-roofline opportunity ranking on ROCm 7.x ([digest](publications/profilelens.md)). | Ranked headroom is an optimistic upper bound, not an achieved speedup. |
| [LLVM GPU Backend Benchmarks](https://github.com/facebookexperimental/llvm_gpu_backend_benchmarks) | DSL-produced LLVM IR cases for AMDGPU/NVPTX backend comparisons ([digest](publications/llvm-gpu-backend-benchmarks.md)). | No aggregate result published; hold backend revision, inputs and measurement protocol fixed. |
| [Magnitude](https://github.com/magnitudedev/magnitude) | Non-agent on-device kernel-parameter tuning inside a local inference engine ([digest](publications/magnitude.md)). | Whole-engine ratios against Ollama do not isolate the tuner; test tuner on versus off. |
| [AKLR](https://github.com/AMD-AGI/AKLR) | Knowledge base, skills and example kernels for an optimization agent on ROCm; the `docs/kernel_rosetta_stone.md` knowledge-on/off study ([digest](publications/aklr.md)). Through 15 November 2026 the library keeps adding FlyDSL fused-MoE and paged-MQA kernels with automated MI355X measurement commits; the study at `a12866b` is unchanged. | A same-agent knowledge-bundle ablation measures memory assistance, not a controller-procedure change; which bundle component carries the effect, and what a fixed non-agent tuner reaches at the same budget, are untested. |
| [AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena) | AMD's RL-ready evaluation environment: 380 schema-v3 kernel tasks (Triton, FlyDSL, HIP, Gluon, TileLang) with vendored baselines, cold-cache graph timing, interleaved remeasurement, an independent evaluator, a `max(0, 1 − 1.05/s)` reward and end-to-end serving-throughput tasks ([digest](publications/agentkernelarena.md)). | The repository holds the protocol, not results; vendored baselines are not necessarily expert-tuned; MI355X verified only. |
| [Xe-Forge](https://github.com/IntelLabs/Xe-Forge) | Intel Labs staged LLM pipeline for Triton/SYCL kernels on Intel GPUs with a Chain-of-Verification loop, a switchable knowledge base and DSPy or Claude Code engines ([digest](publications/xe-forge.md)); adds the IntelLabs organization to the discovery watch. | README results are kernel-level roofline figures against unoptimized or framework baselines on one Arc Pro B70; no cost or variance; paper unread. |
| [TileFoundry](https://github.com/tile-ai/TileFoundry) | Agentic program-generation platform over TileLang, CuTeDSL, CUDA C and Apple AMX; worked examples with whole-model prefill/decode tables against SGLang, derived tolerances and agent budgets ([digest](publications/tilefoundry.md)). | One organization, one H200, batch 1, one run per example; SGLang is a default-configured system baseline, not a budget-matched non-agent optimizer; rejected-candidate logs not published. |
| [ModelBlaster](https://github.com/ucb-bar/ModelBlaster) | The RISC-V side of the [ModelBlaster](publications/modelblaster.md) flow: PyTorch → quantized → Zephyr with LLM kernel generation, verify-then-beam-search over spike/FireSim cycles, a persistent verified-kernel cache, Gemmini and Saturn outer-product targets and a multi-model scheduler (README read 16 November 2026; no measurements in the repository). | Spike cycle counts are blind to cache locality; the README does not cite the paper, so the match is by platform. |

TritorX and KernelEvolve have important paper and industry-report evidence. Do not assume full public implementations or reproducibility merely because related libraries are public.

## Compiler interfaces and reusable components

| Project | Why it belongs in an experiment |
|---|---|
| [LLVM](https://github.com/llvm/llvm-project) | Existing analyses, transformations, code generation, and learned-policy integration. |
| [ACT backend generation](https://github.com/act-compiler/act) | Non-LLM synthesis of compiler backends from accelerator instructions; compare coverage, performance and engineering costs. |
| [Mirage Persistent Kernel](https://github.com/mirage-project/mirage) | Mega-kernel compiler and in-kernel runtime; a non-agent arm for whole-step optimization. |
| [TVM](https://github.com/apache/tvm), [TIRx kernels](https://github.com/mlc-ai/tirx-kernels) and the [`apache/tvm-tirx` foundation](https://github.com/apache/tvm-tirx) (created October 2026; [family digest](publications/tirx.md)) | Tensor representations, schedule controls, example kernels, and a runtime-extensible core (registered operations and types, Z3-backed symbolic analysis, `structural_map`) meant for agent rewriting; no measured result in the November 2026 essay. `v0.1.0` released 13 November 2026 (Apache vote #234 closed, after rc0–rc3 on 9–12 November); the tag points at commit `f43b3030`, which apache/tvm `30fd3017` pins as its `3rdparty/tvm-tirx` submodule while threading explicit targets through Relax, TOPI, DLight and MetaSchedule; `tirx-harness` 0.1.3rc0 and `kcoral` 0.1.2rc1 (12 November) align with it; no performance claim in any of them. |
| [TileLang](https://github.com/tile-ai/tilelang) and [language tools](https://github.com/tile-ai/tilelang-lsp) | Tile programming, layout inference, and editor/tool feedback. |
| [Triton](https://github.com/triton-lang/triton), [Gluon digest](publications/triton-gluon.md), and [Triton extensions](https://github.com/facebookexperimental/triton) | Different levels of layout and scheduling control. |
| [Triton-distributed](https://github.com/ByteDance-Seed/Triton-distributed), also the [DITRON](publications/ditron.md) project | Related implementations of joint computation, memory movement, and communication; one research lineage. |
| [FlyDSL](https://github.com/ROCm/FlyDSL) | Python-based control for AMD kernel programming; v0.5.0 released 11 November 2026 (release notes unread), the language AKLR's newest fused-MoE kernels and AgentKernelArena's `flydsl` tasks target. |
| [CUTLASS and CuTe](https://github.com/NVIDIA/cutlass) | NVIDIA kernel components and layout/scheduling interfaces. |
| [ThunderKittens](https://github.com/hazyresearch/thunderkittens) | Tile abstractions embedded in CUDA. |
| [OpenXLA](https://github.com/openxla/xla), StableHLO, and [Shardy](publications/shardy.md) | Model compilation and distributed tensor decisions. |
| PyTorch `torch.compile` and Inductor | Application-facing compilation and integration. |
| [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) and [FlashInfer](https://github.com/flashinfer-ai/flashinfer) | Serving execution and kernel integration targets. |
| [KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) | Paired PyTorch and Triton training examples; inspect coverage and leakage. |
| [Mirage](publications/mirage.md) and [Prism](publications/prism.md) | Structured superoptimization baselines and possible search components. |

[IBM’s analog hardware toolkit](https://github.com/IBM/aihwkit) supplies executable noise and drift models for [statistical evaluation](publications/analog-validation.md); simulation and measured hardware evidence must remain distinct.

## Controller improvement experiments

| Project | What to inspect | Evaluation boundary |
|---|---|---|
| [GEPA](https://github.com/gepa-ai/gepa) | Reflective optimization of reusable instructions. | Reproduce kernel results with strong baselines and fresh workloads. |
| [Automated Design of Agentic Systems](https://github.com/ShengranHu/ADAS) and [AFlow](https://github.com/FoundationAgents/AFlow) | Agent-code and workflow search. | Generated task agents do not imply an evolving outer optimizer. |
| [MetaKernelBench](https://arxiv.org/abs/2610.05014) | Same-problem cross-DSL skill-transfer evaluation. | Which reused instructions help, and how often does negative transfer occur? |
| [Meta-Harness](https://github.com/stanford-iris-lab/meta-harness) | Harness-code search using prior source and execution traces. | General-task evidence; compiler adaptation requires measurement. |
| [Hyperagents](https://github.com/facebookresearch/HyperAgents) | Editable task and modification agents. | Some outer selection and evaluation components remain fixed. |

These are experiment starting points, not demonstrations that a complete compiler controller evolves autonomously. See the [controller source summaries](publications/INDEX.md) for versions, evaluation scope, and research-family dependencies.

## Workflow infrastructure

| Project | Scope |
|---|---|
| [Auto Ontology](https://github.com/NVIDIA/auto-ontology) | Enterprise semantic context; [reviewed applicability and lifecycle limits](publications/auto-ontology.md). No compiler-memory evaluation. |
| [KCoral](https://kcoral.mlc.ai/) | Isolated shared GPU evaluation and remote diagnostics. |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) | General agent runtime and session state. |
| [Agent Skills](https://github.com/agentskills/agentskills) | Skill packaging and discovery. |
| [SIGIL](https://github.com/sigilagent/sigil) | Skill compilation into executable workflows. |
| [SkCC](https://github.com/Nexa-Language/Skill-Compiler) | Skill representations and code generation. |
| [SkillSmith](https://github.com/AetherHeart-AI/Aeloon) | Research on skill boundaries and compilation. |
| Gerrit [AI review](https://gerrit.googlesource.com/plugins/ai-code-review/), [ReviewAI](https://github.com/amarula/reviewai-gerrit-plugin), and [GerritForge provider](https://github.com/GerritForge/ai-review-agent-provider) | General review interfaces; add and evaluate compiler checks before claiming compiler-specific benefit. |

Infrastructure can support a future optimizer without proving that optimizer’s performance. Negative results are useful evidence for choosing the next experiment; they do not establish permanent limits on the architecture. Detailed accounts are in the [publication index](publications/INDEX.md).
