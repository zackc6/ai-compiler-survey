# DeepSeek Harness (`dsh`)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | DeepSeek AI |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Agent control-plane substrate |
| **Link** | [https://github.com/deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) |
| **Also** | [https://deepseek.com/harness/en/](https://deepseek.com/harness/en/) · Cordis design note [A Programming Paradigm for Spatiotemporal Composability](https://github.com/cordiverse/paper) |
| **Evidence tier** | **B** — shipping-ish open agent *runtime* (plugin kernel + session log); not a compiler harness |

## Key contributions

- Open-source agent harness (`dsh`, MIT, developer preview 2026-08-13): **everything is a plugin** — models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and UI.
- **Cordis** kernel: plugins mount/unmount with services, typed events, and reversible effects on a shared context. Profiles stack **bundles** + `cordis.patch.yml`; no privileged core to fork.
- **Append-only session log** is the source of model-visible context (`deriveMessages()`). Resume, fork, search, replay, and Trajectory view operate on the same event stream. Invariant: anything the model sees must be reconstructable from the log.
- Runtime modes: Standard (full coding agent), Code (TypeScript orchestration of multi-step tools), Minimal (bash + `str_replace_editor` for model benches), Creator (inspect/compose plugins in memory).
- Capability **seams** (service definition / provider / consumer): swap filesystem or subprocess provider and Bash/PTY/LSP move with it. Sandbox and approval policy are independent of the loop.

## Summary

August 2026 DeepSeek AI release of the *runtime* half of an agent stack: model + harness, not a new LLM and not an AI compiler. Architecturally it is a composable control-plane host (plugin graph, durable session events, sandbox/approval) in the same *family* as Claude-class coding agents. For this survey it is **substrate**, not job (a)–(d) evidence: there is no LLVM/Triton/Alive2 admit path, no kernel ladder, and no compiled/frozen agent-graph IR. Complements [FlowCompile](flowcompile.md) / [Auto](auto-agi-compiler.md) / [AgentFlow](agentflow.md) (those *compile or analyze* the graph); DeepSeek Harness *runs* a live plugin tree. Contrast [llvm-harness](llvm-harness.md) (compiler-specific tools + llvm-bench).

## Key takeaways

- **T10 color only:** composable harness + traceable runs exist as a vendor product. Missing cell is unchanged — shared agent-graph IR, fail-closed quality gates, CI that regresses *compiler* multi-agent products.
- **C7:** generic coding-agent harness. Do not treat star counts or “open Claude Code” headlines as compiler-oracle review.
- Plugin/seam design is how a future compiler control plane *could* swap oracles and tool servers without forking the loop — still a hypothesis until someone mounts Alive2 / KernelBench / admit as first-class seams.

## Why it matters for this survey

In-scope as **control-plane substrate** (§0.1 / §4.6 / T10), same bucket as Auto / FlowCompile / AgentFlow / VibeServe. **Not ★** — does not move the hybrid prediction, C2, or C6. Pair with llvm-harness so “harness” is not overloaded: DeepSeek = agent runtime; llvm-harness = job (c) compiler tools.

## Limits / caveats

- Developer preview; maintainers warn of compatibility-breaking changes.
- No public compiler/kernel oracle plugins at digest time.
- Cordis paper is a design note for the plugin kernel, not an AI-compiler evaluation.
