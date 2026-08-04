# Hexagon-MLIR: An AI Compilation Stack For Qualcomm’s Neural Processing Units (NPUs)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Qualcomm |
| **Publisher** | arXiv · GitHub |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [https://arxiv.org/abs/2602.19762](https://arxiv.org/abs/2602.19762) |
| **Evidence tier** | **B** — open Triton/PyTorch→Hexagon NPU data-plane substrate agents can later address |

## Key contributions

- Open-source MLIR stack compiling **Triton kernels** and PyTorch models to Qualcomm Hexagon NPU
- Generative fusion / mega-kernel approach targeting TCM locality, HVX/HMX, DMA overlap
- Public repo [`qualcomm/hexagon-mlir`](https://github.com/qualcomm/hexagon-mlir) complements commercial Hexagon toolchains

## Summary

Hexagon-MLIR is not an LLM agent paper; it is a **vendor-opened data-plane** that makes Triton a portable surface onto Hexagon NPUs. That matters for the agentic-compiler prediction because multi-backend kernel agents (GEAK, KForge, Ascend diagnosis, KernelEvolve) need real non-CUDA compilers and oracles—not only CUDA-pretrained guess loops.

## Key takeaways

- Triton remains the cross-vendor agent training surface even as CuTe/Tile deepen the NVIDIA lane (**C4** still open)
- Agent-addressable compilers need open IR/tooling on NPUs (gap **4.4** / **4.5**)
- SDK/device access still gates full reproduction — substrate is open, silicon loop may not be

## Why it matters for this survey

Tier **B** substrate for §5.6 layers 1–4 and multi-vendor Horizon A. Not a C9 TritorX-class bring-up reproduction (no coverage-first agent claims here). Prefer arXiv + GitHub primaries.

## Limits / caveats

- Work-in-progress; Hexagon SDK / HexKL access required for on-device runs
- No agent control plane in this source — do not over-read as TritorX/KernelEvolve
- Not a settlement of any C1–C10 conflict by itself
