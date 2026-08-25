# ucb-bar/mlirAgent

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | UC Berkeley (ucb-bar) |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://github.com/ucb-bar/mlirAgent](https://github.com/ucb-bar/mlirAgent) |

## Key contributions

- MCP tool layer for MLIR/LLVM agents
- Structural IR fingerprinting
- Empirical finding: LLMs weak at direct IR transforms

## Summary

Research framework for AI-guided MLIR/LLVM development via tools, knowledge graphs, and evolutionary heuristic optimization.

## Key takeaways

- Negative result on direct IR rewrite is important
- MCP-style tool APIs as agent contracts
- Inlining heuristic evolution results

## Why it matters for this survey

Negative **C3/A5** result: free IR transform loses to identity. Pair with [LLM4IR](llm4ir.md) (understanding probe) and Cake/Argus (typed agent IR). MCP + fingerprints are T1 family-2, not a data-plane replacement.
