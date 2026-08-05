# VibeServe: Can AI Agents Build Bespoke LLM Serving Systems?

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of Washington (SyFI Lab) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2605.06068](https://arxiv.org/abs/2605.06068) |
| **Evidence tier** | **B** — end-to-end serving synthesis (T6/T10-adjacent); research, not money-grade A/B product |

## Key contributions

- Multi-agent outer planner + inner Implementer / Accuracy Judge / Performance Evaluator loop
- Generates **entire** LLM serving stacks specialized to model × hardware × workload
- User contract: reference impl, accuracy checker, workload benchmark, HW notes; skills library for serving knowledge
- Near-parity with vLLM/SGLang on mainstream Llama-3.1-8B/H100; larger gains on long-tail scenarios
- Code: [uw-syfi/vibe-serve](https://github.com/uw-syfi/vibe-serve)

## Summary

Extends agentic optimization from kernels/heuristics to **generation-time specialization of serving runtimes**. Outer loop keeps git/issues/memory outside any single context window; only correct candidates proceed. Positions bespoke stacks as an alternative to one general-purpose engine — relevant when agents own control-plane search and classical checkers admit.

## Key takeaways

- Accuracy Judge + Performance Evaluator = serving-level admit pattern (T2/T6 shape)
- Freeze/provenance via git checkpoints (weak T9/T10 signal)
- Orthogonal to FlashInfer-Bench (kernel substitution into existing engines vs rewrite the engine)

## Why it matters for this survey

Evidence for **§5.8 T6** (serving oracles/benchmarks as admit gates) and **T10** (agent-workflow compile of large systems). Complements FlowCompile/Auto (workflow freeze) with **runtime synthesis**. Keep out of Tier A products until multi-month production A/B exists.

## Limits / caveats

- Research harness; not a commercial default-path A/B SKU
- Correctness delegated to user checkers — whole-program/GPU-race contracts still missing
