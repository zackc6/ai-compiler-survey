# TIRx Harness: An Open Compiler Harness for Agentic GPU Programming

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | MLC community (Carnegie Mellon University · Apache TVM) with NVIDIA's Kernel Design Agent team |
| **Publisher** | MLC blog · GitHub |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Blog post](https://blog.mlc.ai/2026/09/29/tirx-harness-an-open-compiler-harness-for-agentic-gpu-programming) · [mlc-ai/TIRx-harness](https://github.com/mlc-ai/TIRx-harness) · [documentation](https://tirxharness.mlc.ai/) |
| **Evidence tier** | **A** for harness design; **B** for the reported speedups (author-measured, references differ per family, no component ablation) |
| **Version / reviewed** | Blog 29 September 2026; reviewed 15 October 2026 |

## Key contributions

A compiler harness built around the [TIRx](tirx.md) kernel language, with four parts:

- **TIRx Foundation:** a thin PTX-level programming surface that adds little semantics beyond the hardware interface, so the PTX ISA stays the source of truth; new PTX capabilities need only lightweight additions. Loops and conditionals are kept so the harness can analyze programs.
- **Tools:** synchronization and data-race analyses, numerical simulation that runs without a GPU, and integration with the Nsight Compute and IKET profilers.
- **Knowledge base:** a kernel zoo of more than 60 TIRx kernels plus PTX and ISA documentation. The authors chose concrete implementations over agent-written summaries, which they found overfit to the debugged case.
- **Evaluation service:** [KCoral](kcoral.md) owns the GPUs and schedules correctness tests, benchmarks, and profiles centrally so concurrent jobs do not distort each other's timings. Agents never run GPU work locally; new hardware (an edge device such as Thor) attaches to KCoral rather than to every agent host.

Experiments used the Humanize 2 "flame chase" workflow from Humanfia with web access disabled during optimization.

## Summary

On NVIDIA Blackwell, geometric-mean GPU kernel time improvements per family against that family's own reference, from the 25–26 September 2026 curated sweep: KDA forward **2.94×** over FlashKDA; KDA backward **6.84×** over Flash Linear Attention; MSA prefill 2.59×; MSA decode 3.99×; KDA decode 1.33×; MLA 1.71×; VSA 1.68×. The authors say the speedups should be read within each family and may change within days as agents, workflows, compilers, and references improve.

## Key takeaways

- Concrete mechanisms behind the gains: `tcgen05.mma` output-lane masking raised observed GPU frequency for 2–3% on sparse MSA prefill without reducing MMA work; moving a row-wise dot product onto tensor cores (full 64×64 product, keep the diagonal) improved KDA backward latency about 15%; adapting FlashAttention-4's mixed native/software exponential improved MSA about 2.9%; transferring Gated DeltaNet's hierarchical inverse decomposition improved KDA forward about 17%.
- The synchronization analysis found a latent `mbarrier` generation bug in a KDA candidate that had already passed correctness tests—an example of a static check catching what sampled tests missed.
- Stated gaps: the zoo only covers ideas present in existing kernels; correctness tooling for megakernels is future work; the team wants to measure how fast the harness adapts to new GPU architectures and instructions.

## Why it matters for this survey

The harness separates the compiler representation from everything an agent needs around it: analyses, simulation, references, profiling, and an evaluation service with a stable contract. That decomposition is directly usable as an experiment plan—compare a plain compiler interface, tools alone, tools with references, and the full harness at fixed models, workloads, and budgets. It also shows an evaluation-ownership choice (the service owns the GPU, the agent only submits) that the design guide's isolation and reproducibility sections can adopt.

**Lineage:** TIRx, TIRx Harness, KCoral, [KDA²](kda2.md), [MetaKernelBench](metakernelbench.md) (built on TIRx), and [CAKE](cake.md) come from one Carnegie Mellon / MLC / NVIDIA research community with overlapping authors. Count them as one evidence family when assessing corroboration.

## Limits / caveats

- Author-measured kernel results on one GPU generation; the contribution of each harness component is not isolated, and the Humanize workflow is not ablated.
- Each family has a different reference implementation, so the 1.33–6.84× range is not a single comparison.
- No application-level or serving measurement; no search-cost report in the post (see KDA² for a partial ablation).
- The harness was published days after the KDA² post it supports; treat both as one evolving first-party report.
