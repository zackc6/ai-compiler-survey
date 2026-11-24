# MemGPT: Towards LLMs as Operating Systems (with Sleep-time Compute)

| Field | Value |
|---|---|
| **Year** | 2023/25 |
| **Org** | University of California, Berkeley · Letta |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [MemGPT, arXiv 2310.08560](https://arxiv.org/abs/2310.08560) · [Sleep-time Compute, arXiv 2504.13171](https://arxiv.org/abs/2504.13171) · [Letta](https://github.com/letta-ai/letta) |
| **Evidence tier** | **C** — memory-management and background-consolidation mechanisms; chat and math workloads only |
| **Version / reviewed** | MemGPT v2, 12 February 2024 (PDF); Sleep-time Compute v1, 17 April 2025 (abstract and affiliations); reviewed 24 November 2026 |

## Key contributions

**MemGPT** (all authors UC Berkeley) treats the context window like main memory in an operating system. The prompt holds read-only system instructions, a writable working context and a FIFO queue of recent messages; evicted messages go to recall storage and arbitrary text to archival storage, and the model pages between them with function calls. **Sleep-time Compute** (Letta and UC Berkeley, same family) lets an agent spend compute while idle, rewriting its stored context into a form that anticipates likely queries.

## Summary

MemGPT on Deep Memory Retrieval: accuracy rises from 32.1% to 92.5% with GPT-4 and from 35.3% to 93.4% with GPT-4 Turbo; on nested key–value retrieval, GPT-4 alone fails by three nesting levels while MemGPT with GPT-4 stays stable. Sleep-time Compute reports about 5× less test-time compute for the same accuracy on Stateful GSM-Symbolic and Stateful AIME, up to 13% and 18% higher accuracy when sleep-time compute is scaled, and 2.5× lower cost per query when amortized over related queries; the benefit correlates with how predictable the queries are.

## Key takeaways

- MemGPT's weaker models struggle with the function calls that manage memory; document QA is limited by the retriever, and the agent often stops paging early.
- Sleep-time compute is amortization: it pays when many later queries share the prepared context.

## Why it matters for this survey

Two mechanisms map onto a compiler optimizer that runs many jobs. Paging is how a long optimization campaign keeps profiles and earlier attempts available without filling the context. Sleep-time consolidation is the between-jobs step the survey's continual-adaptation experiment must control: reorganizing memory between tasks is allowed, but task order must be disclosed and future evaluation data must not leak backward. The amortization condition mirrors the survey's search-economics rule that search cost is justified by reuse.

## Limits / caveats

- No code-optimization workload; Deep Memory Retrieval is a small, single-fact benchmark (a weakness the [Zep](zep.md) authors also note).
- Letta is a company product built on this line of work; benchmark results are first-party.
