# LLVM-Bench: Benchmarking and Advancing Large Language Models for LLVM Compiler Issue Resolution

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Tianjin University (School of Computer Software: Zhao Tian, Chenyao Suo, Junjie Chen; School of Cybersecurity: Yingquan Zhao) · University of Bristol (Meng Wang) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [arXiv 2607.00700v1](https://arxiv.org/abs/2607.00700) · [full HTML](https://arxiv.org/html/2607.00700v1) · [lead-author publications](https://tianzhaotju.github.io/) |
| **Evidence tier** | **A for evaluating agentic compiler engineering**, not for runtime optimization gains: real compiler repository repairs, feature work, and optimization issues, with full-build and test gates |
| **Version / reviewed** | v1, 1 July 2026; full primary HTML read by ChatGPT (draft) and re-verified by Claude, 15 October 2026 |

## Key contributions

LLVM-Bench contains **423** executable, manually screened issue-resolution tasks collected from LLVM versions 18–21. Tasks come from issue-linked, merged pull requests with a reproducible failing test and a known fix. The sample contains **319 bug fixes, 82 optimization issues, and 22 new features**. In LLVM-Gym, candidates are applied to the target repository version, the compiler is rebuilt, and LLVM tests are run (including task-specific new tests). The full-build gate separates patch applicability from functional correctness.

The authors compare four models (DeepSeek V3.2, Qwen3-Coder-Plus, Gemini 3 Flash, Grok Code Fast 1) under sparse retrieval and **oracle retrieval of gold-patch files** at three context budgets, and with SWE-agent, Trae-agent, and Live-SWE-agent. Agents are allowed at most **50 interaction turns**. Their LLVM-Ens method collects patches from multiple candidate generators, rejects unappliable or unbuildable patches, deduplicates with unidiff normalization, and has an LLM ensemble agent (DeepSeek or Grok as base model) reason over the issue and the surviving candidates to choose one; it is not a learned ranker.

## Summary

Across the study's retrieval and agent settings on 423 issues, **mean resolved-issue rate is 1.91% for retrieval-only LLM approaches versus 6.21% for agents**. This is an observed result for two **different resource budgets**: agents average **293,366 input tokens and $0.188 model-inference cost per attempt**, versus **29,931 input tokens and $0.023** for retrieval-based attempts. Those costs exclude the LLVM compiler rebuild/test infrastructure and other non-inference expense. The best individual agent-model combination in Table IV is **SWE-agent + Grok, 10.87% resolved**; the paper's Section VI-A text instead calls SWE-agent + Gemini-3-Flash (4.26%) "the best configuration", an internal inconsistency to note when citing. As a separate upper-bound design, the 12-agent-output pool with LLVM-Ens (Grok selector) reaches **21.99% resolved at $2.302 average inference cost** across combined patch generation and selection, versus **7.33%** when choosing a random candidate from the *same 12-agent-output pool* (the authors' table). Using all 36 model/agent candidates actually lowers the best selection score to **20.80%** and costs about **$2.85** per issue.

## Key takeaways

- **Measured denominator and contract:** issue resolution across 423 historical LLVM changes; this is *not* kernel latency, application throughput, or proven independent performance benefit from generated optimization passes. The actual optimization-relevant subset is **82/423 (19.39%)**; bugs dominate at **319/423 (75.41%)**. Compiler rebuilding and tests measure functional issue resolution but do not separately establish runtime performance or maintenance robustness of an accepted compiler component.
- **Agent benefit is resource-confounded:** 6.21% vs 1.91% reflects greater interaction and access to tools along with roughly **9.8× input tokens and 8.2× model-inference dollars**. No matched-cost non-agent search arm with identical actions, diagnostics, candidate sampling and feedback is evaluated. The stronger claim that *agent reasoning itself* caused the improvement is unproven.
- **Ensemble improvement is partly attributable to selection:** at a common pool of 12 agent candidates and roughly equal cost, 21.99% model-selected vs 7.33% randomly selected shows that model-based selection over a fixed candidate pool beats random selection about threefold; a strong non-LLM selector (deterministic or learned ranking with the same build and test feedback) was not tested, so this supports a narrow selector hypothesis, not the adaptive-reasoning row of the thesis tests. Increasing pool size from 12 to 36 did not monotonically improve resolved rate (20.80%).
- **Failure stages:** of *incorrect generated patches*, 35.77% can be applied; of the applicable incorrect patches, only 17.88% build. These are conditional failure-stage rates, **not percentages of all tasks or all agent outputs**. Patch integration and builds, rather than late-stage semantic bugs, dominate failures.
- **Evaluation cost and hardware:** the paper reports model-inference dollar estimates and token counts, but not a reproducible total GPU/CPU hardware cost for building, testing and maintaining LLVM per task. Do not convert these dollar figures into all-in evaluation cost. The held-out LLVM version mixes are described, but no prospective production rollout is evaluated.

## Why it matters for this survey

This is a compiler-development **negative-control and positive-mechanism** case for §5.3 (compiler co-evolution and controller procedure), §5.8.3 (replace a compiler component; increase autonomy), and §6 (general code review vs compiler-specific validation). It shows both that interactive workflows have useful *observed* lift over retrieval-only single patches, and that the lifted score could result from more attempts, repository navigation, static/build feedback and stronger selection. The selection ablation (same candidates, random vs model-picked) is particularly useful for specifying a matched candidate-pool experiment. Read alongside [PeepholeBench](peepholebench.md) for the distinction between valid/compiler-building patches and **profitable** LLVM optimization, and alongside [ACT](act-backend.md) for conventional generated backend alternatives. No known directly shared research-system lineage with those two studies; their workload and metrics differ.

## Limits / caveats

- **Not a runtime-gain result:** 82 tasks are labelled optimizations, but the headline denominator is 423 issue resolutions; this cannot qualify for any application-gain horizon or generated-component deployed-across-releases predicate.
- One LLVM repository family (versions 18–21), author-collected historic issues, and evaluation by test suites rather than long-term deployment; version and model snapshot effects may change the absolute scores.
- **Oracle retrieval knows gold-patch files** and is deliberately not a deployable baseline; its higher resolution rates must not be conflated with practical retrieval.
- 50-turn agents and much smaller retrieval-only attempts are not a fair causal test of agent reasoning at equal resources. Report per-task compute/build cost and full budget-normalized curves in any follow-up.
- **Next decisive experiment:** compare a fixed agent, a fixed sampling-plus-structured-test loop, and a conventional/rule/learned selector on *the same* LLVM optimization subset with equivalent candidate pools, expert information, rebuild/test access and total computational budget. Report applied/built/issue-resolved/profitable/application-speed outcomes separately and repeat on genuinely held-out LLVM versions and patches.

**Provenance:** digest drafted by ChatGPT from the full arXiv HTML; affiliations, selector description, and every quoted number re-verified by Claude against the same HTML on 15 October 2026. Minor internal inconsistencies in the paper (average codebase file counts 145.49K vs 149.49K; context lengths 20K vs 27K) do not affect the figures used here.
