# AgentFlow: Building Agent Dependency Graphs for Static Analysis of Agent Programs

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Huazhong University of Science and Technology · Macquarie University |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agent control-plane substrate |
| **Link** | [https://arxiv.org/abs/2607.01640](https://arxiv.org/abs/2607.01640) |
| **Evidence tier** | **B** — static analysis / ADG for agent programs; enables typed contracts |

## Key contributions

- Agent programs mix host-language code with framework semantics (models, prompts, tools, memory, handoffs) → new **agent dependencies** invisible to classical CFG/DFG tools.
- **AgentFlow** recovers an **Agent Dependency Graph (ADG)**: typed nodes (agents, prompts, models, capabilities, memory, policies) and typed edges (component / control / data dependencies).
- Framework-agnostic representation for static analysis of agent programs.

## Summary

If the future agentic compiler’s control plane is a multi-agent program, it needs compiler-style **IRs and analysis**—not only chat traces. ADGs are a candidate IR for P1 (structured contract), P22 (FSM/plan bounds), and security/ownership review of agent topologies.

## Key takeaways

- “Agent-addressable” applies to the agent graph itself.
- Static ADG enables audit, blast-radius analysis, and safer auto-merge of agent-config changes (P6/P19).
- Complements FlowCompile (optimize workflows) and Auto (compile spans down).

## Why it matters for this survey

Substrate for analyzing and governing sub-agent architectures that *implement* agentic compilers. Wire to §5.7 P1/P3/P22 and §4.4–4.5 tool/IR contracts.

## Limits / caveats

- Analysis framework paper; not a shipping AI-compiler product.
- Recovery quality depends on framework adapters.
