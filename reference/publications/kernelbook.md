# GPUMODE/KernelBook (Hugging Face dataset)

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | GPU MODE (Paliskara · Saroufim) |
| **Publisher** | Hugging Face |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://huggingface.co/datasets/GPUMODE/KernelBook](https://huggingface.co/datasets/GPUMODE/KernelBook) |
| **Evidence tier** | **A** — primary open PyTorch↔Triton corpus fueling KernelLLM / TritonRL / related RL |

## Key contributions

- ~18k paired PyTorch `nn.Module` ↔ Triton kernels (Inductor/`torch.compile` generated, PyTorch 2.5.0)
- Pipeline: Stack-v1 repos → module extract → unit tests → Inductor Triton → KernelBench-like format + license/star metadata
- Permissive JSON/Parquet releases for SFT

## Summary

Open multi-repo corpus that made Triton specialization practical at 8B scale. KernelLLM SFT, TritonRL distillation/RL, and many community finetunes cite KernelBook as the seed set. Complements KernelBench (eval) with **training pairs**.

## Key takeaways

- Concrete open T7 fuel for Triton — still Inductor-shaped positives, not miscompile/slow-correct negatives
- Version pin (torch 2.5.0) matters for replay

## Why it matters for this survey

Fills the missing digest behind SURVEY’s KernelBook mentions (**§4.7**, **§5.8 T7**). Pair with [KernelLLM](kernelllm.md), [TritonRL](tritonrl.md), [DRTriton](drtriton.md).

## Limits / caveats

- Triton side is compiler-emitted, not expert-tuned peak kernels; teachers often re-synthesize for RL
- No MLIR / Tile / StableHLO coverage; negative data sparse
