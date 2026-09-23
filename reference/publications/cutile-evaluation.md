# Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Wisconsin–Milwaukee · Illinois Institute of Technology |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | GPU kernels & inference compilers |
| **Link** | [Primary source](https://arxiv.org/abs/2604.23466v2) |
| **Evidence tier** | **A** — relevance to the guide’s design choices, not a quality rating |
| **Version / reviewed** | Version 2 (3 June 2026; results unchanged from version 1); reviewed 2026-09-23 |

## Key contributions

Measures CUDA Tile (cuTile) Python kernels against cuBLAS, Triton, FlashAttention-2, cuDNN attention, and hand-written CUDA on H100 NVL, B200, and RTX PRO 6000 Blackwell Server Edition in BF16 and FP16. Reports kernel lines of code alongside throughput.

## Summary

The study is independent of NVIDIA. For matrix multiplication, a 22-line cuTile kernel reaches 52–79% of cuBLAS on the two Blackwell GPUs, but is slower than autotuned Triton on every tested square and LLaMA-7B feed-forward shape. Triton reaches 62–101% of cuBLAS on all three GPUs without source changes. For causal attention (batch 8, 32 heads, head dimension 128), the same 60-line cuTile kernel is 2.51 times FlashAttention-2 and 1.92 times Triton on B200 at sequence length 4,096, yet 53% of FlashAttention-2 and 62% of Triton on the RTX PRO 6000. cuTile 1.1.0 does not run on Hopper.

## Key takeaways

One source file does not imply portable performance: the attention kernel is the fastest tested implementation on one Blackwell part and behind both FlashAttention-2 and Triton on another. (The paper calls it worst among fused kernels there, but its own table shows cuDNN attention slower at sequence lengths of 1,024 and above.) The authors attribute the gap to compiler maturity for that target and to its smaller 48 KB shared-memory limit, and report up to fourfold slowdowns from a wrong thread-block cluster setting. Code size favors cuTile for matrix multiplication (22 versus 53 kernel lines for Triton) but not for attention (60 versus 62).

## Why it matters for this survey

Supplies measured evidence for the kernel-language question: source reuse and per-target performance must be judged separately, and the ranking can reverse within one vendor’s architecture generation. It evaluates no agent or generated kernel. Related NVIDIA work lets Triton code target the same Tile IR, which is a different route from choosing one language; see the [Triton-to-TileIR backend](triton-tileir-backend.md). [Artifacts](https://github.com/uwm-se/CuTile) support further checking.

## Limits / caveats

- Tuning effort is not matched or fully described. Triton searched 18 matrix-multiplication configurations per GPU and its attention kernel was also autotuned; cuTile uses per-target cluster settings, but its tile-size selection is not stated. “Without architecture-specific tuning” for Triton means no target-specific source changes, not no tuning.
- The attention baselines are FlashAttention-2 2.8.3, cuDNN through PyTorch, and a Triton kernel. No attention implementation written specifically for Blackwell is compared, so the B200 result is not a comparison with the fastest available attention.
- One device per GPU type; means reported without distributions; no hardware profiling. Correctness is described as numerical equivalence with references, without stated tolerances.
- Different PyTorch, CUDA, and Triton versions on H100 and Blackwell systems. cuTile 1.1.0 with CUDA 13.1; later compilers may change the RTX PRO 6000 result.
- The end-to-end inference section uses no cuTile kernels; it gives no application evidence for cuTile. Lines of code are a partial productivity measure.
- An online machine review ([Pith](https://pith.science/paper/2604.23466)) read only the abstract; its simulated author rebuttal contradicts the paper’s stated versions and must not be cited as author evidence.
