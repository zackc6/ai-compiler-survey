# TASO: Optimizing Deep Learning Computation with Automatic Generation of Graph Substitutions

| Field | Value |
|---|---|
| **Year** | 2019 |
| **Org** | Stanford University and collaborators |
| **Publisher** | ACM SOSP 2019 |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | https://people.eecs.berkeley.edu/~matei/papers/2019/sosp_taso.pdf |
| **Evidence tier** | **A** — non-agent graph-search and formally verified rewrite comparator |
| **Version / reviewed** | SOSP 2019 primary paper, verified 29 October 2026 |

## Key contributions

TASO automatically enumerates tensor-graph substitutions, checks them using operator properties, and performs cost-based graph and data-layout search. This is a strong historical non-agent synthesis, verification and joint-search system.

## Summary

Across five DNNs on a Tesla V100, TASO matches mature frameworks on ResNet-50. On four newer architectures it reports 1.3–2.8× end-to-end inference speedups with the cuDNN backend and 1.1–1.8× with the TVM backend over the compared contemporary frameworks. These are model/backend-specific ranges, not a common mean or a 2026 production comparison.

## Key takeaways

- **Discovery:** 743 candidate substitutions generated in about five minutes and verified using 43 operator properties. Each graph search was under ten minutes.
- **Hidden cost:** the bounded operator-specification validation involved about one million proof obligations and approximately one hour on 128 CPU cores. Rule verification and redundancy checks also have costs. Expert-authored operator properties and implementations are not free.
- **Baselines:** TensorFlow, XLA, TensorRT, MetaFlow and TVM. TVM kernel tuning used 2,000 trials, averaging two hours per operator; TASO reused the cuDNN-selected graph for the TVM backend, rather than doing TVM-specific graph search.
- **Correctness:** verification is relative to supplied properties and validated bounded cases, not an unconditional all-input floating-point guarantee.
- **Limit:** candidate generation for five or more operators was infeasible due to exponential fingerprint-storage growth. New operators require expert specification work.

## Why it matters for this survey

TASO falsifies any categorical claim that agentic methods uniquely enable verified graph-rule synthesis or graph/layout coordination. Compare TASO, Tensat, EqiForge and agentic systems under matched action space, hardware, numerical acceptance, backend, human input and amortized cost. Measure both graph runtime and time/compute to discover it, across unseen graphs and repeat seeds. Ask whether generated components survive as maintained reusable compiler passes.

## Limits / caveats

Historical V100 workloads and baselines do not establish modern LLM-serving performance. Best-case 2.8× is not universal. TASO and Tensat share rewrite-rule lineage, not independent replication. This alone neither establishes nor refutes the 2027 qualifying predicates.
