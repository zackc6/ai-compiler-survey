# AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | Stanford University · Amazon Web Services · University of Toronto |
| **Publisher** | MLSys 2026 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2511.15915](https://arxiv.org/abs/2511.15915) · [MLSys 2026 proceedings](https://proceedings.mlsys.org/paper_files/paper/2026/hash/0f8426558905746fc38da5e335700aec-Abstract-Conference.html) |
| **Evidence tier** | **A** — the only kernel study in the index that ablates accumulated optimization memory against the same search without it, on non-GPU accelerators |
| **Version / reviewed** | v1, 19 November 2025; v2, 15 April 2026; MLSys 2026 camera-ready (28 pp.). v1 HTML reviewed 24 November 2026; camera-ready §4.4 (pp. 9–11, Figures 13–14) and v2 §4.4 compared the same day. The headline figures (49% → 61%, 45% → 59%, 26×, 13 against 16 iterations, 16–17%, and the "does not significantly improve" statement) are unchanged in the camera-ready. v2 and the camera-ready add two §4.4 controls ("Validate the Diversity Design", "Reflexion-style Baseline") that WebFetch did not find in v1's HTML; those figures are cited from the camera-ready. An earlier draft of this digest called v1 "the only arXiv version"; that was wrong. |

## Key contributions

AccelOpt optimizes kernels written in the Neuron Kernel Interface (NKI), the Python-embedded kernel language for AWS Trainium. A planner proposes optimization plans for each candidate kernel, an executor writes several rewrites per plan, and a beam search keeps the fastest correct kernel per plan group, then the best few by latency. A summarizer turns selected rewrites into **optimization memory**: a bounded queue of slow–fast kernel pairs (both faster rewrites and slower ones, filtered by speedup thresholds) with a natural-language strategy and the changed code segment as pseudocode. The memory is fed to later iterations, so the system can reuse what worked without a human writing hardware notes. The authors also release NKIBench, 14 NKI kernels from LLM workloads (single operators such as Matmul and BatchMatmul up to Group Query Attention and a Mamba block), scored as a percentage of a roofline-estimated peak.

## Summary

Within the study's coverage of Trainium 1 and Trainium 2 (separate campaigns; no test carries memory from one generation to the other), the mean percentage of estimated peak over NKIBench rises **from 49% to 61%** and **from 45% to 59%**. With open models (Qwen3-Coder-480B as executor, gpt-oss-120b for the other roles), the Trainium 1 result is reported as matching Claude Sonnet 4 in thinking mode with repeated sampling, at about **26× lower token cost**. Cost is computed from visible input and output tokens, because Claude's internal reasoning tokens are unavailable. Correctness follows KernelBench: several random seeds and a per-task norm tolerance against a CPU reference. Compilation time is excluded from latency, and wall-clock search time is not reported.

## Key takeaways

- **Similar best observed speedup at lower reported cost, in this campaign.** Beam search plus memory reaches a similar best speedup (Figure 13: geometric mean "across all tasks"; §4.4 does not restate a kernel count) in 13 iterations against 16 for beam search alone, "saving 16-17% cost" (v1 §4.4). The authors state that with enough sampled kernels, memory "does not significantly improve" the best kernel. What the ablation does not establish: an unchanged attainable optimum (only best observed speedup at a 16-iteration budget is compared); what the 16–17% includes (§4.4 does not define it; §4.1 defines cost, for the comparison with Claude Sonnet 4, as input plus output tokens times the per-token price, and Figure 13's caption speaks of "inference cost", so applying that definition here is the digest's conjecture, not a statement in the passage); the number of repeats (not stated); and the hardware and models for this arm (not stated; the appendix default is Trainium 1 with Qwen3-Coder-480B / gpt-oss-120b).
- **Negative control: no memory benefit at beam width 1.** With B=1 and the number of profiled kernels matched to the main gpt-oss-120b run (N=72, K=2, T=16), memory reached a best speedup of 1.204× ($143.58), against 1.229× ($116.35) without memory. Both are below the main configuration's 1.235× ($139.00). The authors conclude that "the memory might limit optimization if the candidates are not diverse enough" (camera-ready §4.4, p. 10). No repeat count or uncertainty is reported, so this is one comparison, not a measured effect size. The result suggests a diversity-dependent benefit; one unreplicated comparison cannot establish that, and the ~2% gap may be within run-to-run noise.
- **Reflexion-style baseline (workflow comparison, not an isolated memory-format effect).** A reflector writes insights after every generated kernel, following [Reflexion](reflexion.md). With generated kernels matched (144 trajectories × T=16), it reached 1.137× ($178.37) against AccelOpt's 1.235× ($139.00). This arm changes the selection, reflection frequency and memory format together, so it does not isolate which component carries the difference. The authors give reasons for not running a non-LLM search baseline (manual input reformatting and search-space specification, as in Wu et al. 2025) but do not run one (§4.4, p. 11).
- Doubling the memory capacity from 8 to 16 items changes the best speedup by +0.6% to +4.6% depending on the executor model, at about $12–18 more per run. Swapping planner models changes cost by up to 2.7× ($116.87 to $316.21) with no substantial speedup difference.
- Beam search beats repeated sampling at equal inference cost. That is a search-method result, separable from the memory result.
- Denominator: kernel latency as a fraction of a best-case roofline peak, on the 14 NKIBench kernels. No application or model-level throughput is reported.

## Why it matters for this survey

The "adapt through persistent experience" row of the controller section previously rested on an abstract-only lead (KOPE) and a supplied-knowledge study (AKLR). AccelOpt is a learned-memory ablation with a matched search arm, and its answer is the distinction the survey insists on: accumulated experience reached a similar best observed kernel at lower reported cost in one campaign; it did not test whether the attainable kernel changes. It is also hardware-portability evidence outside NVIDIA and AMD. In the memory taxonomy of [CoALA](coala.md), the memory is episodic (selected trajectories) abstracted into reusable strategies, the "Experience" stage of the [Storage-to-Experience survey](agent-memory-storage-to-experience.md), which cites AccelOpt. Comparable mechanisms: [Reflexion](reflexion.md) (lessons in text) and [Voyager](voyager.md) (reusable code skills).

## Limits / caveats

- Fourteen kernels; the authors plan more diverse starting kernels. Saturation may mean either near-peak or an initial kernel that is hard to improve.
- The non-agent comparator is missing: no NKI autotuner or compiler-search arm with the same measurement budget (the authors explain why they did not run one; they do not run it). The Claude comparison is repeated sampling, not a tuned search.
- Peak estimates assume best-case scheduling of the vector and scalar engines; the paper is internally inconsistent on one beam parameter (N versus K = 12).
- Memory is evaluated within one benchmark campaign. Transfer to unseen kernels, to new Neuron compiler versions, or across Trainium generations, and how stale memory is detected, are untested.
