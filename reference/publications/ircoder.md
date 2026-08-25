# IRCoder: Intermediate Representations Make Language Models Robust Multilingual Code Generators

| Field | Value |
|---|---|
| **Year** | 2024 |
| **Org** | Technical University of Darmstadt (UKP / hessian.AI) · University of Würzburg (CAIDAS) |
| **Publisher** | ACL 2024 · arXiv |
| **Type** | paper |
| **Group** | Foundation LLMs for compilers |
| **Link** | [https://arxiv.org/abs/2403.03894](https://arxiv.org/abs/2403.03894) |
| **Evidence tier** | **C** — IR as *code-LM interlingua* (source↔IR), not an agentic-compiler product loop |

## Key contributions

- **SLTrans:** ~4M parallel source↔IR pairs (self-contained units; `-Oz` and `-O3` IR flavors).
- Continued causal LM on Code-LMs (1.1B–7.3B) so models learn IR *and* align it with many source languages.
- Gains on multilingual completion, prompt robustness, understanding, instruction following — a **code generation** eval, not `opt` / kernels.

## Summary

UKP/CAIDAS paper treating LLVM-class IR as a multilingual *interlingua* so Code-LMs transfer from high- to low-resource languages. Relevant here only as evidence that IR grounding helps *source* models. It does not show that emitting IR is a safe compiler action, and it is not a Selector/Generator compiler agent.

## Key takeaways

- Fluency/alignment on IR can improve **source** codegen — different job from agentic compile.
- Parallel source↔IR data is cheaper than a new data-plane IR.
- Demote for prediction: adjacent to T7, not a checkpoint mover.

## Why it matters for this survey

§4.7 completeness: IR pretrain is not only Meta LLM Compiler. Keep **Tier C** so catalogs do not confuse Code-LM robustness with hybrid compiler architecture (**C8**). Do not cite as C3 settlement.

## Limits / caveats

- Contest-style self-contained files; IR truncated (<2500 lines).
- No admit/oracle/kernel loop.
- Success on MultiPL-E-class tasks ≠ legal IR rewrite.
