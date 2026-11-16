# Xe-Forge: Multi-Stage LLM-Powered Kernel Optimization for Intel GPU

| Field | Value |
|---|---|
| **Year** | 2026 (repository March 2026; paper arXiv 2605.26118, May 2026; README results as of commit of 1 November 2026) |
| **Org** | Intel Labs (Spoczynski, Fleischer, Berchansky, Stan, Guskin, Xu, Siemieniuk, Heinecke) |
| **Publisher** | GitHub repository (IntelLabs); arXiv for the paper |
| **Type** | code (first-party README with roofline plots; the paper itself not read) |
| **Group** | GPU kernels & inference compilers |
| **Link** | [IntelLabs/Xe-Forge](https://github.com/IntelLabs/Xe-Forge) · [paper (arXiv 2605.26118, not read)](https://arxiv.org/abs/2605.26118) |
| **Evidence tier** | **B** — the first indexed agentic kernel optimizer on a third GPU vendor (Intel), with a staged pipeline, a verification loop and a supplied-knowledge base; its README numbers are first-party roofline figures against unoptimized or framework baselines, so it is adjacent evidence for the vendor-stack and supplied-knowledge questions until the paper's controlled evaluation is read |
| **Version / reviewed** | Repository head `ad3bd0076cf7d656635f23bbe39e9bebc6c2eb44` (1 November 2026), README and `docs/CORRECTNESS.md` read by shallow clone on 16 November 2026. arXiv refused on this runner; upgrade to Tier A is possible once arXiv 2605.26118 is read (evaluation on KernelBench Level 2 and FlashAttention on Intel Arc Pro B70). |

## Key contributions

Xe-Forge is a multi-stage LLM pipeline that analyzes a Triton (or Gluon, SYCL, CUDA) kernel, produces a structured issue list (`dtype_float64`, `suboptimal_tile_size`, `missing_autotune`, …), maps each issue to an optimization stage, and runs the stages in a fixed order: algorithmic rewrites, data-type fixes, fusion, memory access, tensor descriptors, persistent kernel, Intel-XPU-specific settings (256×256 tiles, `num_warps=32`, swizzling) and autotuning. Each stage runs a **Chain-of-Verification-and-Refinement** loop: compile, execute, compare with the original; if incorrect or slower, feed the result back and retry up to `AGENT_MAX_ITERATIONS` (default 5). After each stage the kernel is re-analyzed. Defaults: `rtol = 0.01`, `atol = 1e-5`, `TARGET_SPEEDUP = 2.0`, `LLM_MODEL = openai/gpt-4o` (the README's quick start uses `gpt-5.2`; any litellm provider works).

Two engines exist: a DSPy pipeline (fully automated) and a Claude Code engine that generates a workspace (`CLAUDE.md`, config, knowledge base, skill commands) which Claude Code then drives, interactively or headless (`--max-turns 80`). A separate **tile-search** mode tunes CUTLASS SYCL tile configurations by propose–validate–benchmark against Intel Xe DPAS constraints. An optional **knowledge base** supplies validated patterns per stage and 19 reference kernels; the analyzer receives its constraints and the optimizer its before/after examples.

`docs/CORRECTNESS.md` states the oracle rules: every run has exactly one oracle (a PyTorch reference, or, when none is given, the input kernel itself); "a trial that disagrees with it is wrong, however fast"; the oracle is read-only; a host result with no correctness verdict is never a pass; `--no-correctness` disables checking only for the DSPy engine, and results from it "are timings, not correctness claims"; "a regression is never finalized; parity is". The document also warns that a baseline-kernel oracle "proves 'the same as before', never 'correct'".

## Summary

The README reports three result sets on one **Intel Arc Pro B70** (roofline plots; the numbers below are the README's text):

- **FlashAttention forward:** up to **13.3×** over "unoptimized Triton kernels" across skinny, non-square and irregular shapes, with optimized kernels above 80 TFLOP/s.
- **vLLM attention variants** (`BatchedMoE`, `FusedMoE`, `UnifiedAttention`) across 24 production configurations (Gemma2/3-27B, gpt-oss 20B, Llama 3.1-8B, 3.3-70B, Llama 4 Scout, Qwen 2.5/3; prefill, decode, chunked prefill, sliding window, fp8/int8 caches): **geometric-mean 2.8×** over each configuration's original kernel; up to 35× on memory-bound configurations "lifted off near-zero baselines"; the compute-bound Gemma3-27B prefill kernel reaches the 160 TFLOP/s peak.
- **KernelBench Level 2 GEMM/matmul:** optimized Triton kernels "surpass both PyTorch eager and `torch.compile` baselines" and exceed the 160 TFLOP/s roofline ceiling for compute-bound configurations (no aggregate ratio in the text).

## Key takeaways

- **Baselines are weak or framework-level.** "Unoptimized Triton kernels" and vLLM's existing XPU kernels are the starting points; the vLLM set is the more meaningful one because those kernels are what the serving stack ships on Intel, but the README does not say how tuned they were. Neither is a matched-budget non-agent tuner.
- **Denominator is kernel throughput (TFLOP/s and per-kernel speedup)**, not application throughput; no serving-level result is reported in the README.
- **Cost is not reported**: no tokens, dollars, wall-clock per kernel or number of iterations; the loop's cap is 5 iterations per stage and 10 trials per run by default.
- **Validation is tolerance-based with defaults `rtol 0.01 / atol 1e-5`** against the original kernel or a PyTorch reference; the correctness document is candid that a baseline oracle inherits the baseline's bugs.
- **Supplied knowledge is a switchable component** (`KNOWLEDGE_BASE_ENABLED`), which makes a knowledge-on/off ablation easy to run, but no such ablation is reported in the README.
- **Portability of the harness:** the same CLI targets `xpu`, `cuda` and `cpu` devices and four kernel languages, with a documented path for adding a language.

## Why it matters for this survey

Xe-Forge closes a coverage gap this guide named: Intel was the one vendor stack with no indexed agentic kernel work. It is the Intel counterpart of AMD's [GEAK](geak-v4-github.md)/[AKLR](aklr.md) line and NVIDIA's [KDA²](kda2.md): a vendor research group packaging hardware knowledge (tile sizes, warp counts, GRF modes, DPAS constraints) into a staged agent with a verification loop. For the §5.3 adoption row, it is one more organization deploying the same pattern, which is evidence of *spread*, not of a measured advantage over conventional search. For the §6 controller question, it is a third public knowledge-bundle design (after AKLR and D2K-Bench) whose on/off effect could be measured but has not been reported. For the §6 kernel-language question, its vLLM result is a vendor-specific restatement of the CUDA Tile lesson: the same Triton source needed Intel-specific tiles, warp counts and descriptors to reach the roofline.

Record it in the 2027 trail as **not a candidate**: kernel-level, no application evaluation, baselines unmatched. The paper may contain the controlled evaluation the README summarizes; until it is read, the digest stays at the README's level.

Lineage: Intel Labs; built on the Intel XPU backend for Triton; uses KernelBench tasks and vLLM kernels as task sources; the Claude Code engine and skill commands are the same packaging pattern as NVIDIA's skills catalogue and AKLR's skills.

**Experiment:** knowledge base on/off and DSPy-versus-Claude-engine arms on the 24 vLLM configurations at a fixed wall-clock and token budget, against Intel's own hand-tuned kernels and an autotuned Triton configuration search, reporting per-configuration cost, rejected candidates and an end-to-end vLLM throughput number on the B70.

## Limits / caveats

- Paper not read; README figures are from plots and prose and may be best-of-run; no variance, seeds or failure counts.
- Single GPU (Arc Pro B70, a workstation part), single vendor; the CUDA device path is supported but no CUDA result is reported.
- "Up to 13.3×" and "up to 35×" are maxima over weak starting points; the geometric-mean 2.8× over vLLM's kernels is the number to carry, with the unknown tuning state of those kernels as its caveat.
- The project states it is "not stable and not intended for production"; interfaces change without notice.
- Default tolerance `rtol 0.01` is loose for some kernels (compare the derived bounds in [TileFoundry](tilefoundry.md) and the proven bounds in [ptxv](ptxv.md)).
