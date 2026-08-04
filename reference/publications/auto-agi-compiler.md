# Auto: The AGI Compiler

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | RightNow AI |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2607.04542](https://arxiv.org/abs/2607.04542) |
| **Evidence tier** | **A** — compiles live agent behavior into verified/WASM “cognition binaries”; ★ for §5.7 P23 / freeze-amortize |

## Key contributions

- Frames every frontier agent run as re-deriving behavior token-by-token — expensive, slow, unbounded.
- **Auto** records live agent traces, finds **witnessed-deterministic** spans, extracts verified programs or distilled specialists, emits **WebAssembly cognition binaries** with manifests + sandbox-enforced capabilities.
- Tiered runtime with conformal guards; guard trips **deopt** to reference agent and recompile — “nothing figured out twice.”
- AUTO-BENCH: high fraction of spans witnessed-deterministic; large marginal-cost drop on a shifting stream.

## Summary

Same lab as AutoKernel. Treats the *agent control plane itself* as a compile target: experience → permanent, measured, near-free skill. Directly supports the survey’s commercial path (search with frontier tokens → freeze artifact → serve with zero/low LLM calls).

## Key takeaways

- Sub-agent architectures need a **compile-down** path, not only better prompts.
- Deopt + recompile is the admit/fallback pattern for agent runtimes (parallel to classical compiler fallback).
- Strengthens **P23**: tokens/capability problems are solved by compilation, not hoping prices fall.

## Why it matters for this survey

★ Substrate for future **agentic compiler** control planes: jobs (a)/(b) produce artifacts; Auto-like compilers make multi-agent loops affordable in production. Wire to §5.7 P3/P22/P23 and §4.6 FMware. Pair with [autokernel.md](autokernel.md).

## Limits / caveats

- “AGI compiler” is used in a narrow testable sense (experience → verified skill), not general intelligence.
- Benchmark is author-introduced; reproduce cost/parity claims carefully.
