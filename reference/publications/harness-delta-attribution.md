# Harness-Delta Attribution: Dissecting Gains from Harness Evolution

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Amazon · New York University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2610.22466) |
| **Evidence tier** | B: measures how much of a reported controller (harness) gain survives held-out evaluation; no compiler benchmark |
| **Version / reviewed** | v1, 15 October 2026 (preprint); arXiv abstract page and paper text reviewed by Claude 25 November 2026 |

## Key contributions

**Harness evolution** automatically rewrites the code and text around a frozen model: prompts, skills, tools and orchestration. Harness-Delta Attribution (HDA) splits a reported search-set gain into three parts: **overfitting** (fitting quirks of the tasks the search saw), **test-time scaling** (the evolved harness simply spends more inference compute), and a **residual**, which is an upper bound on the improvement that could generalize.

## Summary

The authors applied HDA to 11 executor models (nine open-weight Qwen3, Qwen3.5 and Qwen3.6 models from 0.8B to 35B, plus Claude Haiku 4.5 and Claude Opus 4.8) and three harness-evolution frameworks: Meta-Harness, SkillOpt and AHE. The benchmarks were LiveMath, SWE-bench Verified, CREATE and ALFWorld. Of 25 model–benchmark–framework settings, 21 show statistically significant search-set gains.

## Key takeaways

- Across the 21 significant settings, overfitting explains on average **54%** of the gain and test-time scaling **14%**. The two together exceed half the gain in 14 settings.
- On ALFWorld, 89% of gains are attributed to overfitting on average, and 98% in the five Meta-Harness settings.
- In one Meta-Harness ALFWorld run (Qwen3.5-0.8B executor), the harness grew from 66 to 503 non-blank, non-comment lines, reached 100% search-set success, and became a deterministic controller that hard-codes benchmark priors and makes **no model calls**. It still reached 93.3% on held-out ALFWorld games.
- The authors report that search-set gains often fail to transfer to held-out tasks, and that validation-based selection does not reliably prevent overfitting.
- These are agent-task accuracies, not compiler speedups; total search cost is not part of the attribution.

## Why it matters for this survey

This is the first attribution study of the harness-search line that the survey's controller row draws on ([Meta-Harness](meta-harness.md), with [Harmony Harness](harmony-harness.md) and [GEPA](gepa.md) nearby). It changes how those results should be read: a search-set gain is not evidence of a better controller until the held-out residual and the test-time compute are reported. For a compiler controller, the analogue is concrete. An evolved controller can encode the benchmark's kernels or shapes directly, as the zero-call ALFWorld controller encoded its games. So a controller change must be scored on workload families it never saw, at the old controller's inference budget. It complements [Harness Updating Is Not Harness Benefit](harness-updating-not-benefit.md), which separates producing a harness edit from benefiting from it.

## Limits / caveats

The benchmarks are not compiler or kernel tasks, so the 54% and 14% shares cannot be carried over to compiler workloads as numbers. The attribution relies on the authors' decomposition method, and the residual is an upper bound, not a measured transfer gain. Only three frameworks were tested; Meta-Harness's own text-classification result is not among the attributed settings. One preprint version from one industrial–academic group, not yet independently replicated. What would strengthen or weaken it: the same attribution applied to a compiler controller (for example kernel-generation prompts or harnesses) on held-out workload families.
