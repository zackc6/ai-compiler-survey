# MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs (Mirage Persistent Kernel)

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | Carnegie Mellon University · Tsinghua University · NVIDIA · University of Michigan · Peking University |
| **Publisher** | USENIX OSDI 2026 · arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [arXiv 2512.22219](https://arxiv.org/abs/2512.22219) · [OSDI '26](https://www.usenix.org/conference/osdi26/presentation/cheng) |
| **Evidence tier** | **A** — compiler-level expansion of the optimization boundary to a whole multi-GPU inference step, without agentic control |
| **Version / reviewed** | v1 22 December 2025, v2 10 June 2026; reviewed 15 October 2026 |

## Key contributions

MPK compiles a model's inference step into a single persistent mega-kernel. The compiler lowers tensor programs into a streaming-multiprocessor-level task graph with explicit data dependencies and generates CUDA for each task; an in-kernel runtime schedules those tasks across SMs with decentralized scheduling. This enables cross-operator software pipelining and fine-grained overlap of computation with communication that a kernel-per-operator design cannot express. Kernel launches per token drop from 293 to one.

## Summary

Offline batched inference (batch 1–16, 64-token prompts, 1,024 output tokens; median of five runs) on A100, H100, and B200 with Qwen3-0.6B/1.7B/8B, Llama-3.2-1B, and Qwen3-30B-A3B: **1.0–1.7× over SGLang and vLLM**, largest for small models and newer GPUs. Qwen3-8B on A100: per-token decode latency 14.5 ms (vLLM/SGLang) to 12.5 ms (MPK), against an estimated 10 ms memory-bandwidth bound. Multi-GPU Qwen3-1.7B on up to eight H100s with tensor parallelism: 1.1–1.4× over SGLang and vLLM, up to 10× over PyTorch.

## Key takeaways

- Ablations attribute the gains: cross-task pipelining cuts the final linear layer 1.2–1.3× on B200; compute–communication overlap cuts per-iteration latency 1.1×; launch cost is about 1.1 ms per token eager and 0.2 ms with CUDA Graphs on B200.
- The abstract reports "up to 1.7× lower latency" while the evaluation section describes the same range as throughput; the paper does not reconcile the two metrics.
- Costs of the design: register usage is fixed at the maximum any task needs; batch-size-specialized graphs are precompiled for powers of two; scheduling is decentralized, with globally coordinated policies left as future work.

## Why it matters for this survey

A measured example of the "optimization is expanding beyond isolated kernels" trend at the compiler level: the object of compilation is the whole inference step across GPUs, and the gains come from overlap and launch elimination rather than from faster individual kernels. It is non-agentic, so it belongs with DITRON and Triton-distributed as evidence that scope expansion does not by itself require an agent, and as a comparison arm for the coupling hypothesis. **Lineage:** same Carnegie Mellon group (Zhihao Jia) as [Mirage](mirage.md) and [Prism](prism.md); count together. Related industrial result: [Ada-MK](ada-mk.md) deploys a megakernel through offline search in production.

## Limits / caveats

- Offline batched inference only; no online serving with variable arrivals, which is where launch overhead and scheduling behave differently.
- Gains shrink for larger models and older GPUs; the largest numbers are small models on B200.
- First-party evaluation; TensorRT-LLM is not compared.
