# Prism: Symbolic Superoptimization of Tensor Programs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Carnegie Mellon University · Tsinghua University · Weizmann Institute of Science |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Structured and distributed compilation |
| **Link** | [Primary source](https://arxiv.org/abs/2604.15272v1) |
| **Evidence tier** | **A** — relevance to the design decisions, not a quality score |
| **Reviewed** | 2026-09-23 |

## Key contributions

Symbolic hierarchical graphs describe families of implementations. Outer search explores graph structures; inner search selects concrete parameters, with semantic pruning.

## Summary

Prism extends structured superoptimization by searching over symbolic program families rather than enumerating every concrete implementation independently.

## Key takeaways

Representation and pruning can improve search without requiring agent reasoning.

## Why it matters for this survey

Use it as a strong alternative, or a component within a broader optimizer. Compare action spaces, feedback, and budgets before attributing gains to the agent.

## Limits / caveats

The preprint evaluates selected language-model workloads. It does not establish general application superiority. Mirage and Prism share authors and research lineage.
