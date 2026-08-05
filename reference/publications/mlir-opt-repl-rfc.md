# LLVM Discourse RFC: mlir-opt-repl interactive MLIR explorer and MCP server

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | LLVM / MLIR community (makslevental et al.) |
| **Publisher** | LLVM Discourse |
| **Type** | forum |
| **Group** | Forums & workshops |
| **Link** | [https://discourse.llvm.org/t/rfc-mlir-opt-repl-interactive-mlir-pass-pipeline-explorer-and-mcp-server/91068](https://discourse.llvm.org/t/rfc-mlir-opt-repl-interactive-mlir-pass-pipeline-explorer-and-mcp-server/91068) |
| **Evidence tier** | **B** — compiler-native typed tool surface for agents (T1), not yet a portable cross-IR standard |

## Key contributions

- Pip-installable `mlir-opt-repl`: stateful REPL over `mlir-opt` (load, run/chain passes, diff, rewind, bookmarks, verify, save)
- **MCP server** exposing the same tools (`run_pipeline`, `chain_pipeline`, `rewind`, `list_passes`, …) for coding agents
- In-tree / PyPI distribution intent; companion LLVM PRs (#203796 / #203803)

## Summary

Community RFC for a first-class **agent↔MLIR** interface: enumerated pass actions, persistent IR history, and structured MCP tools rather than prompting agents to shell `mlir-opt` with ad-hoc flags. Complements mlirAgent’s research MCP stack with a lighter, mlir-opt-centric surface aimed at Claude Code–class assistants.

## Key takeaways

- Typed, stateful pass-pipeline tools are landing in the MLIR tooling conversation (not only research demos)
- Debate remains: MCP server vs agent “skills” that dump `--mlir-print-ir-before-all` into context
- Still MLIR-only — does not solve portable schemas across Triton/Tile/StableHLO

## Why it matters for this survey

Moves **§5.8 T1** “what exists” beyond mlirAgent/CompileIQ toward **in-tree-adjacent MLIR MCP**. Keeps **C3** lean: agents drive enumerated pass actions, not free IR rewrite. Does not close the portable multi-IR conformance gap.

## Limits / caveats

- RFC/PR status; not yet a vendor-neutral conformance suite
- No admit/oracle policy product surface (T2) by itself
