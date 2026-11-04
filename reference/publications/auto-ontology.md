# NVIDIA Auto Ontology

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | NVIDIA |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Company infra |
| **Link** | [NVIDIA Auto Ontology](https://github.com/NVIDIA/auto-ontology) |
| **Evidence tier** | B: adjacent semantic-context and evidence-management mechanisms, without compiler evaluation |
| **Version / reviewed** | Commit `cdaf61e1bd0cf3820d11d72b43bb460816aebbd3`; reviewed 3 November 2026 |

## Key contributions

Auto Ontology builds semantic context over enterprise metadata for agents that query structured data. Its documented interfaces separate discovering definitions, answering questions, and publishing reviewed semantic changes. This is a possible source of ideas for optimizer memory, rather than an executable compiler intermediate representation.

## Summary

The repository describes a semantic catalog backed by Postgres, natural-language-to-SQL services and interfaces through the Model Context Protocol (MCP), command line and API. The top-level README identifies an Apache-2.0 public project that is not accepting external contributions. An internal-only statement in the MCP README is stale relative to that availability; contribution eligibility and public access are distinct.

The [query-validation guide](https://github.com/NVIDIA/auto-ontology/blob/cdaf61e1bd0cf3820d11d72b43bb460816aebbd3/skills/nvidia-ontology-query/references/query-validation.md) asks users to verify the question, SQL, returned rows and final answer separately. It requires units, population, denominator, source identity, validity and supersession to survive interpretation. These are documented workflow requirements; this review did not execute the system or establish that every API enforces them.

The [publication guide](https://github.com/NVIDIA/auto-ontology/blob/cdaf61e1bd0cf3820d11d72b43bb460816aebbd3/skills/nvidia-ontology-management/references/publication.md) requires durable writes followed by exact readback, preserves the original artifact for recovery, and distinguishes a recommendation from approval or execution. It explicitly warns that certification fields do not implement an atomic promotion, supersession or rollback lifecycle. The MCP interface is read-only; arbitrary result-row publication requires an external governed destination.

## Key takeaways

No compiler baseline, accelerator workload, kernel latency, application gain, search budget or compiler-specific validation result is reported in these reviewed materials. The README links to ontology-sql-eval for SQL benchmarking; no SQL score is imported into this survey. Treat that evaluation and the repository as one system family if used together.

For a compiler optimizer, the transferable idea is to record what a claim means, where it came from, when it applies, and whether it remains valid. Numerical acceptance still needs an executable checker and measurement. A semantic label alone cannot certify a kernel or authorize deployment.

## Why it matters for this survey

Primary placement is optimizer workflow/memory and evaluation infrastructure. Updating stored knowledge is memory adaptation. Only a versioned change to the retrieval decision procedure, independently tested on new compiler tasks, belongs to controller improvement. This distinction preserves the existing three-loop experiment rather than implying a new architecture.

**Recommended experiment, not an observed result:** use held-out CuTe DSL/TIRx task pairs from [MetaKernelBench](metakernelbench.md). Compare flat retrieval, typed records with deterministic applicability filters, and ontology-guided retrieval with the same proposer, actions, feedback and total budget. Inject stale, contradictory and superseded records. Report invalid reuse, negative transfer, admitted application performance and total context-construction/query cost. Predeclare whether each arm changes stored knowledge or retrieval policy, and keep evaluation answers outside the context corpus.

## Limits / caveats

The enterprise SQL stack has not been evaluated as compiler memory, and its integration cost may outweigh any benefit. Typed records may achieve equivalent grounding without a graph or autonomous ontology construction. If reusable mechanisms cannot be separated from the enterprise stack, downgrade relevance to background rather than advocating adoption. No thesis predicate, confidence label or decision checkpoint moves from this source alone.

The [Hacker News submission](https://news.ycombinator.com/item?id=50348962) was found in the 3 November sweep. A retrieved excerpt raises skepticism about grounding reliability, but the full thread could not be opened in this run. This is a discovery lead, not a validation result or an independent evidence family. No popularity count is used as evidence.
