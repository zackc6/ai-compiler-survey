# KCoral: Lightweight Benchmark Server for Agentic GPU Programming

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | MLC community (Carnegie Mellon University · Apache TVM) |
| **Publisher** | MLC blog · GitHub |
| **Type** | company |
| **Group** | Agent control-plane substrate |
| **Link** | [Blog post](https://blog.mlc.ai/2026/10/05/kcoral-lightweight-benchmark-server-for-agentic-gpu-programming) · [mlc-ai/kcoral](https://github.com/mlc-ai/kcoral) · [harness documentation](https://tirxharness.mlc.ai/docs/components/kcoral.html) |
| **Evidence tier** | **B** — evaluation infrastructure; the measured quantity is evaluations per minute and timing fidelity, not kernel speed |
| **Version / reviewed** | Blog 5 October 2026; reviewed 15 October 2026 |

## Key contributions

- **Agent host and GPU worker are separated.** Command-line adapters (Python, Nsight Compute, IKET, Compute Sanitizer, a workload benchmark adapter) upload code and inputs, run on a remote `kcoral server`, and return logs and profiler artifacts. Each request is packaged independently; no local GPU is needed.
- **Isolation:** each request sees a fixed set of system directories plus its own working directory, using bubblewrap (millisecond startup versus second-level Docker startup). Once scheduled, a program has exclusive GPU access. `CUDA_VISIBLE_DEVICES` and the working directory are worker-managed and cannot be overridden; symlinks and overlapping upload paths are rejected; request timeouts default to 300 s (1–3600 s).
- **Throughput experiment (one B200):** 256 workloads—eight fixed TIRx kernel specializations (Kimi Delta Attention, Alpha-MoE, MiniMax Sparse Attention among them) repeated 32 times, each compiling from a cold cache, building GPU inputs, and benchmarking. Local sequential baseline **4.98 per minute** (3,083.61 s batch); KCoral at concurrency 32 **12.86 per minute**, i.e. **2.58×**, which is 99.7% of the 2.59× bound set by 1,190.79 s of exclusive-GPU work. CPU-only compilation overlaps other requests' GPU time.
- **Timing fidelity:** across 500 workload configurations from 82 kernel families, median difference from direct local timing **0.425%**, 95th percentile 3.136%, 497 of 500 within 5%. The three outliers are 1.9–2.2 µs RMSNorm and LayerNorm kernels with 0.13–0.38 µs absolute differences.

## Summary

KCoral turns the GPU into a shared, isolated evaluation service for agent loops. The 2.58× figure is evaluation throughput, not a speedup of any generated kernel, and it excludes agent generation time.

## Key takeaways

- Measure evaluation infrastructure on its own axes: GPU occupancy, timing fidelity, queueing, isolated test time, and failure recovery.
- Timing measurements cover kernel execution only, excluding compilation, input preparation, and request latency.

## Why it matters for this survey

Shared evaluation is part of search cost and of reproducibility. An evaluator that owns the hardware, isolates requests, and reports fidelity against local timing is a reusable design for the candidate/evaluation interface the guide asks teams to build first. Lineage: same community as [TIRx Harness](tirx-harness.md) and [KDA²](kda2.md); the throughput study uses TIRx kernels.

## Limits / caveats

- One hardware setting; the throughput study runs existing kernels, not an agent loop.
- The example server configuration disables worker filesystem isolation (`--sandbox none`) to share weights and compilation caches; isolation strength depends on deployment choices.
- Remote execution of generated code still requires careful contract ownership and resource limits beyond what the post measures.
