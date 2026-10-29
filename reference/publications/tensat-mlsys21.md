# Equality Saturation for Tensor Graph Superoptimization (Tensat)

| Field | Value |
|---|---|
| **Year** | 2021 |
| **Org** | MIT, Google, University of Washington, OctoML (author affiliations) |
| **Publisher** | MLSys 2021; arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [arXiv 2101.01332v2](https://arxiv.org/abs/2101.01332v2) |
| **Evidence tier** | **A** — non-agent tensor-graph joint search and search-efficiency comparator |
| **Version / reviewed** | arXiv v2, 17 March 2021; full primary text reviewed 22 October 2026 |

## Key contributions

Tensat applies equality saturation and e-graphs to explore many equivalent tensor-graph rewrites without committing to sequential rewrite order. It uses the **same rewrite rules as TASO** and extracts a joint solution using integer linear programming (ILP), including multi-pattern rewrites. The decision method is symbolic, not agentic.

## Summary

Across **seven inference graphs** on a **single NVIDIA Tesla T4**, the authors report **up to 16% better graph runtime than TASO** and an average **48 times less search time**. NasRNN search takes **177.3 seconds** for TASO versus **0.5 seconds** for Tensat, while graph-runtime speedup relative to the original graph improves from **45.4%** to **68.9%**. Execution uses TASO's cuDNN backend; this is graph runtime, not serving throughput.

## Key takeaways

- **Baseline and actions:** TASO with the same rewrite rules, default 100 backtracking iterations. Increasing TASO to 1,000 iterations gives less than 1% extra speedup on average at more than 11 times the search time.
- **Hardware and coverage:** one T4, 16-core CPU and 60 GB RAM; BERT, ResNeXt-50, NasNet-A, NasRNN, Inception-v3, VGG-19, SqueezeNet. The shared rewrite rules did not improve ResNet-50 on T4.
- **Budget:** e-graph cap **50,000 nodes**, at most **15** exploration iterations, and a **one-hour ILP timeout**. Default searches take roughly 0.3–10.6 seconds; extra multi-pattern passes can explode the graph and time out.
- **Validation:** shape-checked semantics-preserving rewrite rules, but no independent bitwise floating-point equivalence proof. TASO's shared cost model sums operator times and can misrank actual whole-graph runtime.
- **Negative cases:** default Tensat underperforms TASO on Inception-v3 until more multi-pattern search; additional search can worsen SqueezeNet runtime due to model error.

## Why it matters for this survey

This is direct historical evidence that non-agent joint search can handle interdependent graph decisions. Compare a modern agent on the same seven graphs and rewrites, with matched feedback and compute budgets, five seeds, graph throughput, numerical acceptance and search cost. EqiForge (2026) extends the non-agent equality-saturation design space; it is not an independent replication of Tensat's exact T4 experiment.

## Limits / caveats

One older GPU and seven graphs do not establish production serving, cross-hardware portability or runtime/communication joint search. E-graph memory growth, ILP timeouts and model/runtime mismatch limit scalability. The paper does not establish a modern agent would lose a matched comparison.
