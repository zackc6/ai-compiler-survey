# Architecting for Hardware Diversity: Meta's End-to-End Co-Design for High-Performance AI Training on AMD GPUs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Meta (Infrastructure; about sixty authors, first author Haoyu Zhang, last author Chunqiang Tang) |
| **Publisher** | arXiv; to appear at IEEE/ACM MICRO 2026 |
| **Type** | paper |
| **Group** | Company infra |
| **Link** | [arXiv 2610.22230](https://arxiv.org/abs/2610.22230) · [HTML](https://arxiv.org/html/2610.22230) |
| **Evidence tier** | **A** — first hyperscaler report of production AMD training that names agentic kernel optimization as one of three methods behind an end-to-end training-throughput gain; it is the first post-23-September-2026 candidate for the 2027 predicate that carries an application denominator. The full v1 text has been read and reports no validation protocol, search cost, or failure count for the agent work. The tier records decision relevance, not replication quality or predicate qualification; "provisional" was dropped on 20 October 2026 after both agents agreed in the Review thread, and the report remains a nonqualifying 2027 candidate |
| **Version / reviewed** | v1, 15 October 2026 (16 pages, 21 figures, 6 tables). Three passes on 19 October 2026: (1) abstract and arXiv metadata only, after rate-limited full-text attempts failed; (2) Claude GitHub Action, HTML body, about 100k of 134k characters (see "Body findings"); (3) Claude GitHub Action, the remaining 34k characters, which hold only the tail of the reference list and arXiv page boilerplate. The "Key contributions", "Summary", and "Key takeaways" sections come from the first pass; their unread-body statements were replaced on 20 October 2026 with the full-text findings. The paper reports no validation protocol, search cost or budget, failure counts, or expert-versus-agent comparison for the agent-generated kernels |

## Key contributions

Three "reusable principles" for making a non-NVIDIA accelerator competitive for large-scale training, stated by the authors as follows:

1. **Hardware–model co-design.** "Rather than directly porting models from NVIDIA GPUs, revising model structures and software recipes allows full exploitation of accelerator-specific strengths (e.g., MI350X's 1.6x HBM capacity relative to B200)."
2. **Analytical kernel selection.** "Our analytical performance model enables zero-warmup optimal kernel selection across diverse datatypes and matrix shapes in production models, drastically simplifying tuning." This is a conventional, non-agent mechanism: a model predicts which kernel wins for a shape and datatype instead of measuring candidates at startup.
3. **Agentic kernel workflows.** "Increasingly mature agentic workflows have lowered the barrier to porting from the CUDA ecosystem; we extend these workflows for microarchitecture-aware kernel optimizations and custom shim generation."

## Summary

Case study: AMD Instinct MI350X versus NVIDIA B200 for recommendation-model training, inside a fleet that also runs Meta's MTIA accelerators. "Compared to the directly ported baseline, these methods deliver up to 1.5x improvement in end-to-end training throughput." The authors describe this as "the first hyperscaler report on productionizing AMD GPUs for large-scale training," and state that their contributions "have been upstreamed to the open-source PyTorch, Triton, and ROCm ecosystems."

## Key takeaways

- **Denominator:** end-to-end training throughput, relative to a *directly ported* recipe on the same AMD hardware — not relative to B200, and not relative to an expert-tuned AMD recipe. "Up to 1.5×" is a maximum; the distribution across models is not in the abstract.
- **Attribution is the open question.** The 1.5× is the joint effect of model restructuring, analytical kernel selection, and agent-optimized kernels. The full v1 text does not apportion it either (see "Body findings"); the agent-derived share is isolated for one kernel only.
- **Agent role, as stated:** porting from the CUDA ecosystem, microarchitecture-aware kernel optimization, and generating "custom shims" (adapter code between frameworks and kernels). The full v1 text reports no validation protocol, search cost or budget, human effort, or failure cases for the agent work.
- **Lineage:** same organization as [KernelEvolve](kernelevolve.md) and its [engineering blog](kernelevolve-blog.md), which reported production agentic kernels across NVIDIA, AMD, and MTIA; the body names KernelEvolve as the agent architecture its workflow builds on (see "Body findings"). Count the two as one organization's evidence, not independent confirmation.

## Body findings (HTML v1, read 19 October 2026)

- **No apportionment of the 1.5×.** No table or figure splits it among co-design, analytical kernel selection (Origami), and agentic kernels. For one feed ranking model, §V-A and Fig. 15(b) report 1.26× from co-design alone (larger batch, activation checkpointing removed, embedding placement), reaching 1.5× over the initial baseline "together with kernel optimizations." The implied ~1.19× from kernels is our arithmetic, not the paper's, and it mixes agent and non-agent kernel work.
- **One agent-attributable application number (§IV-C).** The jagged flash attention (JFA) backward kernel in the ranking models was about 2× slower on MI350X than on B200 because grouped-query heads raced on `tl.atomic_add`. Following a tuning skill, the agent rewrote it to accumulate dK/dV in registers per KV-head group: "a 2.3× speedup (32 ms→14 ms)," "delivering a 25% improvement in end-to-end model training throughput." The comparator is the directly ported kernel, not an expert rewrite; the authors say agent output reaches "near-expert performance while reducing development time by an order of magnitude," and v1 contains no table of expert-versus-agent results.
- **Origami** is reported as 93% average selection efficiency against exhaustive autotuning, a selection metric, not an end-to-end share.
- **Agents also do porting:** hipification fixes ("iteratively compile code, interpret error messages, and apply fixes until the build succeeds") and generated shims. The paper names [KernelEvolve](kernelevolve.md) as the general agent architecture its workflow builds on, confirming the same lineage.
- **Venue confirmed:** arXiv comments field, "To appear in the 59th IEEE/ACM International Symposium on Microarchitecture (MICRO 2026)."

## Why it matters for this survey

This is the first candidate for the 2027 predicate with the right shape: an integration into a production training stack, published after 23 September 2026, with an application-level throughput evaluation. The headline 1.5× does not isolate the agent's share, because it mixes three mechanisms, one of which (analytical kernel selection) is explicitly non-agent, and the body does not apportion it. The body does, however, report one agent-derived application gain: the agent-rewritten jagged flash attention backward kernel, credited with +25% end-to-end training throughput for one ranking model. On the attribution condition, then, that one case meets the letter of the predicate. What still keeps it from being a *qualifying* evaluation, in the full v1 text, is the rest of the predicate's rule. There is no strong non-agent baseline: the comparator is the directly ported atomic-add kernel, not an expert rewrite or an expert-tuned AMD recipe. There is no search or model-call budget for the case, and no validation protocol or failure count. Both Meta reports also count as one organization with [KernelEvolve](kernelevolve.md). The paper is therefore recorded under the running tally as a **candidate, not qualifying**, and as the first entry in the trail the September 2027 review will consult. Separately, the analytical kernel-selection result, if accurate, is a data point for the generated-heuristics-versus-learned-policies question and for the "Expand to another accelerator" checkpoint: a predictive model replacing warm-up autotuning is the kind of conventional component that competes with agent-driven tuning. Read with [KernelEvolve](kernelevolve.md) (same organization, earlier agent system) and [Hyperloom](hyperloom.md) (AMD's own agentic inference-optimization harness) before treating AMD results as corroborated across organizations.

## Limits / caveats

- First pass was abstract-only; the body pass (above) covered about three quarters of the HTML, and the third pass confirmed the rest is references and page boilerplate. The paper does not report validation, cost, failures, or an expert-versus-agent comparison for the agent work: these are absent from v1, not unread.
- Private workloads and organization-specific baselines, as with KernelEvolve; the "directly ported" comparator is the authors' own starting point.
- One hardware pair (MI350X versus B200), one workload class (recommendation training), one organization.
- Experiment that would settle more: the paper's own ablation, if it exists, separating the three principles on the same model; failing that, a public reproduction on an open recommendation model with the upstreamed PyTorch/Triton/ROCm changes, reporting directly-ported, expert-tuned, and agent-tuned recipes under one budget.
