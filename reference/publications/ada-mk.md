# Ada-MK: Adaptive MegaKernel Optimization via Automated DAG-based Search for LLM Inference

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Baidu |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [arXiv 2605.11581](https://arxiv.org/abs/2605.11581) |
| **Evidence tier** | **B** — industrial deployment of an offline-searched megakernel; non-agent, narrow hardware and model scope |
| **Version / reviewed** | v1, 12 May 2026; reviewed 15 October 2026 |

## Key contributions

For millisecond-budget decoding in online advertising, where kernel launch overhead reaches 14.6% of end-to-end time, Ada-MK fuses the decode step into a megakernel whose execution path is fixed at compile time by an MLIR-based offline DAG search, removing the runtime branching that auto-compiled megakernels otherwise carry. A three-dimensional shared-memory constraint model with K-dimension splitting halves peak shared-memory use. The megakernel runs as a TensorRT-LLM plugin for decode; prefill stays on the standard path. The authors describe it as the first industrial megakernel deployment in a commercial advertising system.

## Summary

On one NVIDIA L20 with GPTQ-W4A16 Qwen3-1.7B and Qwen2.5-1.5B, batch 1–16: fixed short sequences (64 in, 12 out) give **up to 23.6% higher single-batch throughput than TensorRT-LLM** (above 10% at every batch size for Qwen3-1.7B; 6.7–15.6% for Qwen2.5-1.5B) and up to 50.2% over vLLM and 71.9% over SGLang at the smallest batches. On real datasets the gain over TensorRT-LLM is 4.0–19.5%; at batch 16 on long-context CSL, vLLM is 3.5% ahead.

## Key takeaways

- The premise is that under a fixed deployment configuration the optimal execution path is unique, so search can be offline and the runtime can be branch-free; the paper does not report the offline search time.
- Gains concentrate at small batch and short sequence, which is the advertising operating point; they narrow at large batch and long context.

## Why it matters for this survey

Production evidence for the per-workload-versus-offline question: when the deployment configuration is fixed and reuse is high, offline search amortizes and a conventional compiler pipeline captures the launch-overhead headroom without an agent. Read with [MPK](mpk.md) (research megakernel compiler with a runtime scheduler) as two designs for the same boundary expansion—compile-time fixed path versus in-kernel dynamic scheduling.

## Limits / caveats

- One GPU model (L20, Ada), two similar 1.5–1.7B models, one quantization scheme, offline batch mode; Blackwell and larger models are stated future work.
- First-party industrial report; the deployment's own serving metrics are not disclosed beyond the benchmark comparisons.
- "Up to" figures are peaks; per-scenario numbers above are the ones to cite.
