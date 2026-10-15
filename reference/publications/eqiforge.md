# Unleashing the Power of Equality Saturation for Tensor Program Superoptimization (EqiForge)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Zhejiang University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [arXiv 2609.12330](https://arxiv.org/abs/2609.12330) |
| **Evidence tier** | **A** — a non-agent superoptimizer that derives fused attention-style kernels from tensor expressions; a required comparison arm for the thesis |
| **Version / reviewed** | v1, 11 September 2026; reviewed 15 October 2026 |

## Key contributions

EqiForge is a tensor-program superoptimizer built on equality saturation. One expression language represents both high-level tensor expressions and tiled computations, so algebraic rewrite rules can compose into fused implementations—the paper derives FlashAttention-style kernels from the attention expression. Two scaling devices make this tractable: early compaction prunes redundant partial programs before they are complete, and subgraph composition extends the search to larger graphs. No language model is involved.

## Summary

On NVIDIA A100 80GB and RTX 5090, across 21 tensor-program configurations (normalization, MLP, LoRA, causal attention in decode and prefill; batch 1, 8, 16), EqiForge beats the fastest available baseline in 18, with a **1.32× geometric mean and 2.74× maximum**. Baselines: PyTorch eager, `torch.compile`, TVM MetaSchedule (1,000 trials per shape), Mirage, Trinity for non-attention; Trinity, Neptune, FlashAttention, FlashInfer for attention. Decode attention is up to 1.87× FlashAttention; prefill attention trails FlashAttention by 3–6%. On five Transformer layers versus `torch.compile`: 3.16× on QK-normalized MLA and 5.84× on mHC.

## Key takeaways

- Search budget up to four hours per configuration; at batch 16, saturation takes 0.02–1,742 s and extraction 0.5–911 s, with attention prefill the largest e-graph (about 5,300 e-classes, 65,000 e-nodes).
- Losses are reported: LayerNorm–GEMM is 6–12% slower than the best baseline.
- Correctness is a relative L2 tolerance of 0.01 against PyTorch; rewrites assume real arithmetic, so reassociation can change floating-point results.
- Prism was not compared because its implementation was not public at evaluation time.

## Why it matters for this survey

The thesis must be tested against strong conventional search. EqiForge discovers the same class of fused kernels that agent systems are credited with, by exhaustive algebraic rewriting under a declared budget, and reports the configurations it loses. It is the natural non-agent arm for the "several search methods remain competitive" trend and for the coupling hypothesis: a matched-budget comparison of EqiForge against an agent loop on the same 21 configurations would be one of the cleanest tests available. Lineage: Mirage and Prism (Carnegie Mellon) are the closest prior systems and are compared or discussed; EqiForge's authors are a separate group.

## Limits / caveats

- Two GPUs, single-token Transformer-layer shapes, and author-chosen configurations; no application-level or serving measurement.
- Four-hour search budgets place this on the offline, high-reuse side of the per-workload-versus-offline question; per-program cost matters for low-reuse deployment.
- Tolerance-based correctness, not equivalence; the floating-point caveat is the same one that affects agent-generated kernels.
