# AI as a Compiler: Compiling Triton kernels without the Triton compiler

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Stanford University · EPFL |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [arXiv 2609.36800](https://arxiv.org/abs/2609.36800) · [HTML](https://arxiv.org/html/2609.36800) · [triton_ai_compiler](https://github.com/francois141/triton_ai_compiler) · [ptx_gym](https://github.com/francois141/ptx_gym) |
| **Evidence tier** | **A** — first direct test of replacing a compiler's optimization and lowering pipeline with an agent; same Stanford lineage as KernelBench (Mirhoseini) |
| **Version / reviewed** | v1, 29 September 2026; reviewed 15 October 2026 |

## Key contributions

- **AI lowering:** an LLM agent translates Triton kernels directly into PTX, bypassing the Triton compiler's optimization and lowering passes. The harness (TAIC) has three skills—interpreting Nsight Compute metrics, retrieving PTX ISA documentation, and applying GPU optimization principles. The environment (TCENV) assembles, sanitizes, tests numerically, benchmarks, and profiles each candidate.
- **Loop:** generate an initial PTX implementation, diagnose the bottleneck, plan an optimization, have subagents produce candidate patches; only candidates that assemble, pass the safety and correctness gates, and improve the measured objective seed the next round, until the budget is spent.
- **Verification:** the Volta PTX verifier is extended to Blackwell's `tcgen05` tensor-core interface (tensor memory, descriptor-based operand layouts, asynchronous commits, waits, barriers, and proxy fences). With Volta in the loop a candidate must be proven equivalent to the Triton reference, not just pass sampled tests.
- **Compiler model:** GPT-6 Astra. A model ladder on FP16 GEMM shows the environment is not the only variable: GPT-5.4 0.73×, GPT-5.5 and GPT-5.6 Terra 0.87×, GPT-5.6 Luna no accepted kernel, GPT-5.6 Sol 0.97×, GPT-6 Astra 1.00×.

## Summary

Twelve common kernels and ten kernels from recent papers, on NVIDIA L40S (Ada), H100 (Hopper), and B200 (Blackwell), against autotuned Triton 3.6.0 from TritonBench and the OpenAI tutorials. Reported range: **0.83× to 3.34×** of autotuned Triton. Gains concentrate where Triton's abstraction hides a hardware capability; mature dense kernels land at parity or below.

## Key takeaways

- **Common kernels:** elementwise (sigmoid, ReLU, SiLU, SwiGLU) within about 1%; RMSNorm at most 4%; RoPE at most 5%; GEMV 0.98–1.15×; softmax 1.08–1.29×; convolution 1.17–2.23×; FP16 GEMM 1.00× on B200 and L40S but **0.83× on H100**; FP8 GEMM 1.61× on H100, 1.15× on L40S, parity on B200.
- **Recent-paper kernels (B200, $15 budget each):** BitDelta 3.34× (packed binary weights decoded directly into tensor-core operands), batched BitDelta 2.51×, FlashSinkhorn 1.55×, SageAttention 1.41×, FlashAttention 1.37× (one thread per softmax row in tensor memory), Forgetting Attention 1.01×, Lion 1.00×, Dion 0.97×, Mamba-2 primitives 1.07× and 1.10×.
- **Repeatability (B200, five runs):** convolution FP8 2.00 ± 0.20 (best 2.23×), FP16 GEMM 1.02 ± 0.01, SwiGLU 1.00 ± 0.00, FlashAttention forward 1.24 ± 0.11 (best 1.37×). The main results grid is single-run.
- **Verified vs numerical speedup:** when provable equivalence is required under the original Volta, GEMM falls to **0.24×** (1.03× numerically), FlashAttention to **0.78×** (1.37×), 2-D convolution to **0.77×** (1.35×). The extended Volta verifies every common kernel except reduction-sum and softmax, and six of the ten recent kernels. Unsupported patterns: atomics, input-dependent control flow, bit-level value manipulation.
- **Search cost:** per-run budgets of $15 (convolution, GEMM, FlashAttention) and $1 (SwiGLU); elementwise candidates under about $1.50, convolution and GEMM candidates roughly $5–12. Tokens, wall-clock, and iteration counts are not reported. The authors describe generation as "orders of magnitude more expensive than millisecond-scale Triton compilation," paid once per kernel.

## Why it matters for this survey

This is the first measured point for the question of how much of the compiler agents should replace: lowering itself can be synthesized, and the win is largest where the fixed pipeline cannot express a hardware feature. Two conditions bound the result. The reuse condition from the per-workload-versus-offline question applies in full—each kernel costs dollars, not milliseconds. The verification condition is new: the deployable speedup is the one measured at the verification level the deployment requires, and the checker's coverage, not the model, currently sets that level. Read with [PTXBench](ptxbench.md), where model-written PTX does not consistently match expert libraries, and with [ACT](act-backend.md), a non-agent backend generator, before concluding that direct synthesis is the cheaper path. Related lineage: KernelBench and [KernelBench-Verified](kernelbench-verified.md) share Stanford authorship.

## Limits / caveats

- The Volta extensions are a proof of concept: "We do not claim our extensions to be sound or complete." The trusted computing base grew from 42 to 60 kLoC, and floating point is modeled as real arithmetic.
- Kernel latency only; no application, serving, or maintenance evidence. No comparison with cuBLAS, library FlashAttention, or hand-written PTX.
- Single-run main grid with moderate variance on the kernels with the largest gains; one frontier model family.
- Experiment that would settle more: the same kernels under a matched dollar budget against a structured PTX search without an LLM, reported at both numerical and verified acceptance levels.
