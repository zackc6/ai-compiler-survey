# KForge: LLM-Driven Cross-Platform Kernel Generation for AI Accelerators

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Gimlet Labs |
| **Publisher** | MLArchSys @ ISCA 2026 · arXiv |
| **Type** | paper |
| **Group** | HW codesign & accelerator bring-up |
| **Link** | [https://arxiv.org/abs/2606.02963](https://arxiv.org/abs/2606.02963) |
| **Evidence tier** | **A** — multi-vendor / multi-DSL agent forge |

## Key contributions

- Two-agent loop: generation (compile+correctness) ↔ performance-analysis (profiler/GUI metrics → rewrite guidance).
- Uniform interface across **four vendors** and **six programming models** (CUDA, Triton, CuTe, HIP, SYCL, Metal).
- NVIDIA B200: +2.12% e2e vs TensorRT-LLM on gpt-oss-20b; Intel Arc B580: 5.13× geomean vs better of eager/`torch.compile` on 37 KernelBench-L2 GEMM+tail ops (fusion + mixed precision).

## Summary

Gimlet Labs framework treating cross-platform kernel synthesis as the agentic compiler’s job when production pipelines span heterogeneous accelerators. Contrasts vendor-saturated NVIDIA baselines with bring-up-like Intel Arc setting.

## Key takeaways

- Agentic compilers must be **multi-ISA by default** by ~2027–28 (**C4**).
- Functional-pass vs optimization-pass separation is a reusable control-plane pattern.
- Small % vs TRT-LLM on NVIDIA vs large× on Arc illustrates **C2** baseline dependence.

## Why it matters for this survey

Tier A for software-stack reshape *and* HW diversity: agents as portability layer when classical compilers lag new devices.

## Limits / caveats

- End-to-end % gains on NVIDIA are modest; don’t overclaim vs library stacks.
- Multi-DSL support breadth ≠ equal maturity per backend.
