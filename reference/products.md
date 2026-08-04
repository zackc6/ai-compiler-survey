# Commercial products as prediction signals

**Purpose:** Company offerings that inform **what next-gen compile will ship** and **how agents enter production** — not a full SKU catalog.

Companion: [`../docs/SURVEY.md`](../docs/SURVEY.md) §5 · [`../docs/SURVEY.md`](../docs/SURVEY.md) §6 · [`repos.md`](repos.md) · [guide](README.md)

---

## Role tags

| Tag | Meaning |
|---|---|
| **DataPlane-Compile / Serve** | Graph→device or inference engine (baseline agents must plug into) |
| **ControlPlane-Autotune** | Searches knobs/schedules (classic or evolutionary) |
| **ControlPlane-Agent** | Explicit LLM/agent in the loop |
| **Kernel-Platform** | Tile/DSL/IR agents target |
| **Cloud-Agent** | Sold as cloud agent service |
| **Research-release** | Important, not a full SKU |

---

## Tier A — shapes the agent future

| Company | Offering | Roles | Prediction signal | Conflicts |
|---|---|---|---|---|
| **Google Cloud / DeepMind** | [AlphaEvolve on Cloud (GA)](https://cloud.google.com/blog/products/ai-machine-learning/alphaevolve-is-available-for-everyone) | Cloud-Agent, ControlPlane-Agent | Evolutionary coding agent as a sold product; Magellan lineage | C5, C1 |
| **Google** | Magellan (prod inlining narrative) + MLGO | ControlPlane-Agent / Autotune | Offline heuristic synthesis *and* neural advisors in production | **C1** |
| **NVIDIA** | [CompileIQ](https://developer.nvidia.com/cuda/compileiq) (+ [agent-skills](https://nvidia.github.io/CompileIQ/stable/install.html)) | ControlPlane-Autotune / ControlPlane-Agent | Workload-specialized compiler controls; versioned ACFs; AGENTS.md skill pack drives search+Welch validate | **C2** (blog vs docs) |
| **NVIDIA** | [CUDA Tile / Tile IR](https://developer.nvidia.com/blog/focus-on-your-algorithm-nvidia-cuda-tile-handles-the-hardware/) | Kernel-Platform | Next agent IR vs Triton | **C4** |
| **AMD** | [GEAK](https://rocm.blogs.amd.com/artificial-intelligence/kernel-optimization-agent/README.html) (v3) | ControlPlane-Agent, Kernel-Platform | Repo-level multi-DSL kernel agents on Instinct | **C2**, **C4** |
| **Meta** | [LLM Compiler](https://ai.meta.com/research/publications/meta-large-language-model-compiler-foundation-models-of-compiler-optimization/) / [KernelLLM](https://huggingface.co/facebook/KernelLLM) | Research-release | Open foundation / specialist models | — |
| **NVIDIA** | TensorRT-LLM + [Claude agents/skills PR](https://github.com/NVIDIA/TensorRT-LLM/pull/12831) | DataPlane-Serve + ControlPlane-Agent | Agents wired into flagship serve compiler (multi-DSL) | **C4** |
| **Meta** | TritorX + KernelEvolve (MTIA + hetero GPUs) | ControlPlane-Agent + Kernel-Platform | Agentic ASIC bring-up + production ranking kernels | **C9**, C2 |
| **Meta / LF** | [Helion](https://pytorch.org/projects/helion/) | Kernel-Platform | Higher-level agent/autotune surface over Triton | **C4** |

---

## Tier B — data-plane baselines (agents must integrate)

Brief on purpose: these are **defaults**, not proof that agents win.

| Company | Offering | Roles | Why keep |
|---|---|---|---|
| **NVIDIA** | TensorRT-LLM / CUDA libs | DataPlane-Serve/Compile | Peak production path |
| **Meta** | `torch.compile` / Inductor | DataPlane-Compile | De-facto app compile entry |
| **Google / OpenXLA** | XLA + StableHLO | DataPlane-Compile | Portable HLO; Magellan XLA experiments |
| **Modular** | MAX + Mojo | DataPlane-Serve/Compile | MLIR-rooted alternative stack |
| **Intel** | OpenVINO | DataPlane-Compile | Edge/CPU deploy toolkit |
| **AWS** | Neuron (+ NKI) | DataPlane-Compile, Kernel-Platform | Cloud-custom silicon; NKI as agent surface |
| **Qualcomm** | AI Hub / QNN | Edge compile | On-device compile-as-a-service |
| **Qualcomm** | [Hexagon-MLIR](https://github.com/qualcomm/hexagon-mlir) | DataPlane-Compile, Kernel-Platform | Open Triton/PyTorch→Hexagon NPU MLIR stack |

---

## Demoted / footnote (misaligned with prediction goal)

| Item | Why demoted |
|---|---|
| Olive / ORT / HF Optimum glue | Cross-runtime packaging; little agent-compile signal |
| OctoML (historical TVM SaaS) | Cite only as **lineage** for commercial autotune appetite that later products (CompileIQ, AlphaEvolve Cloud) still sell — not an active next-gen agent compiler |
| Generic “AI code review” SKUs | Conflict **C7** — HITL UX, not compiler oracles |
| Anthropic CCC | Process signal (agents-as-engineers), **not** a sold compiler SKU |

---

## Architecture placement

```text
Control plane (emerging SKUs)
  AlphaEvolve Cloud · GEAK · CompileIQ · Magellan/MLGO · TRT-LLM agent skills
        │
Data plane (mature defaults)
  TRT-LLM · Inductor · XLA · MAX · OpenVINO · Neuron
        │
Kernel / tile platforms
  Triton · CUDA Tile · CuTe · NKI · HIP / FlyDSL
```

**Commercial reality:** revenue still sits on the data plane. Explicit agent control-plane SKUs are newer and often opt-in for hot kernels — consistent with §5 prediction (defaults classical first).

---

## Mapping to survey questions

| Question | Commercial signal |
|---|---|
| Q1 Trends — hybrid control plane | CompileIQ, GEAK, AlphaEvolve Cloud, Magellan/MLGO |
| §1b Traditional still wins defaults | TRT-LLM, Inductor, XLA, OpenVINO |
| Q2 How agents help | Evolve code, kernel loops, knob search, specialist models |
| Q3 Reshape process | ACF-in-VCS; heuristic synthesis; agent skills in TRT-LLM |
| §5 Future | Tier A rows above + conflicts C1–C5 |

Commercial digests for Tier A/B prediction-relevant items live under [`publications/`](publications/) (CompileIQ, GEAK, AlphaEvolve, Magellan/MLGO, TRT-LLM agents). Skip Olive/OctoML churn.

Update when a vendor ships a **named agent-compile default**, not when another runtime EP appears.
