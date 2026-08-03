# amazon-science/acclaim (GitHub)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Amazon Science / AWS AI |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Agentic & RL compilers |
| **Link** | [https://github.com/amazon-science/acclaim](https://github.com/amazon-science/acclaim) |
| **Evidence tier** | **A** — OSS realization of ACCLAIM (Q2/Q3) |

## Key contributions

- Public multi-agent implementation of **compiler–LLM cooperation** for C → x86 assembly optimization.
- Five-agent shape: planning/guiding agent + source / IR / assembly level agents + testing agent.
- Planner can call clang frontend / middle-end / backend as tools, and allocate budget across levels.
- Optional single-level mode for ablation; default is multi-level interleaving.

## Summary

AWS Science open-source companion to [ACCLAIM](acclaim.md) ([arXiv:2604.04238](https://arxiv.org/abs/2604.04238)). Focuses on CPU C programs; demonstrates that the hybrid control-plane design (orchestrate compilers + LLM rewrites + test admit) is reproducible outside a paper PDF.

## Key takeaways

- Concrete **online** propose–measure–admit loop across abstraction levels.
- Tool-calling + test agent are first-class — matches survey hard limits when open models fail tool calls.
- Complements Magellan/OpenEvolve (**offline** heuristics) without replacing `clang`/`opt`.

## Why it matters for this survey

Tier A code evidence for §5.4 / Q2/Q3. Prefer the [paper digest](acclaim.md) for claims; prefer this repo to reproduce or extend the loop.
