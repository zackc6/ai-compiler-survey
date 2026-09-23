# MaxKernel: Agentic Kernel Generation for TPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google · Google DeepMind |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://arxiv.org/abs/2609.04523](https://arxiv.org/abs/2609.04523) |
| **Evidence tier** | **A** — multi-agent Pallas/TPU search with compiler feedback and XProf; peak on a mature stack, not ASIC coverage |

## Key contributions

- Three orchestration modes over one sub-agent pool (plan, implement, fix, test, autotune, profile): human-in-the-loop, a closed autonomous loop, and graph search (parallel vs beam).
- The editable artifact is **[Pallas](pallas.md)** (JAX → Mosaic on TPU). Compile errors and **XProf** traces close the loop. RAG is docs/handbooks only — hand-tuned kernels are excluded from retrieval.
- On [JAXBench](jaxbench.md) (50 tasks): **1.58×** geometric-mean speedup over XLA (author). On the eight tasks with hand-tuned Pallas, parallel search **2.32×** vs XLA vs **2.02×** for the hand-tuned geomean (floor at 1×). Ragged paged attention still favors the hand kernel (4.65× vs 1.42×).
- Code: [AI-Hypercomputer/accelerator-agents](https://github.com/AI-Hypercomputer/accelerator-agents/tree/main/MaxKernel) (posted 2026-09-03).

## Summary

Google’s September 2026 TPU kernel agent. It does not replace XLA. It proposes Pallas kernels, lets the compiler and a numerical harness reject them, and uses hardware traces to hill-climb. Parallel search (longer horizon per candidate) beats beam search on this brittle DSL (2.32× vs 1.78× geomean on the eight-kernel slice). OSS case studies (MLA, Qwen3-Next, DeepSeek-V4 sparse attention) are author-reported latency cuts against JAX or a human Pallas baseline, including crash fixes, not a serving A/B.

## Key takeaways

- Strongest public **peak** agent on Google TPU. Job (a) on a shipping accelerator with a classical lower (Mosaic), not job (d) coverage bring-up.
- **Does not settle C9.** TritorX-class “any correct ATen op, sim + silicon” is a different objective from beating XLA on 50 JAXBench tasks.
- Docs-only RAG matches the JAXBench finding that target context moves Pallas correctness more than a bigger model. Hybrid lean holds (**C3-B / C6-B**).
- Per-kernel wins are uneven. Do not quote 2.32× as “beats experts on attention.”

## Why it matters for this survey

★ for **T1** (Pallas as the TPU agent face), **T2** (compile + numerical admit before timing), and **C4** (another sink beside Triton/Tile). Pair with [JAXBench](jaxbench.md). P23: search structure (parallel vs beam) changes token horizon; it does not license LLM-as-`opt`.

## Limits / caveats

- Author speedups vs XLA; tolerances are per-workload and loose on some attention tasks (appendix rtol/atol).
- No public multi-month serving p50/p90 (**C2** open).
- TPU-only eval. The intro lists NKI and MTIA as related surfaces; this paper does not measure them.
