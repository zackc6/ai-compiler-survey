# Beyond Pass-by-Pass Optimization: Intent-Driven IR Optimization with Large Language Models

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | SKLP, ICT, CAS · UCAS · Jiangnan University · The Chinese University of Hong Kong |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Agentic & RL compilers |
| **Link** | [https://arxiv.org/abs/2602.18511](https://arxiv.org/abs/2602.18511) |
| **Evidence tier** | **B** — intent as an explicit IR *stage* (T1 family-3); headline speedups are C2-class CPU IR |

## Key contributions

- **IntOpt:** three-stage IR optimizer — intent formulation → compiler-grounded refine → intent realization.
- Intent is an ordered sequence of **natural-language transformation actions** (region + transform), distilled from LLVM `-O3` unopt/opt pairs, then used to fine-tune LLM Compiler FTD 13B.
- Realization still goes through compiler analysis / transform; not free SSA rewrite as the product.

## Summary

ICT/CAS et al. argue that both classical pass pipelines and end-to-end LLM IR generators leave *optimization intent* implicit — fragmented across passes, or hidden in a black-box generation. IntOpt makes intent a first-class intermediate: a specialized model proposes a global strategy; analysis refines it (e.g. vector width); a second stage realizes it. On 200 LLVM IR programs they report **90.5%** verified correctness and **2.660×** mean speedup vs other LLM IR optimizers, and beating `-O3` on 37 benches (author max **272.60×**). Mechanism for this survey: **intent/action IR**, not LLM-as-`opt`.

## Key takeaways

- Separating *what to do* from *how `opt` does it* is the same hybrid split as pass-list LLMs and HintPilot, with a richer action language.
- Do **not** average the 2.66× / 272× figures into C2 or serving claims — selected CPU IR, author protocol.
- Fine-tune starts from Meta LLM Compiler FTD: fluency IR (family 1) as a *prior*, intent as the agent-visible contract.

## Why it matters for this survey

T1 / C3 / §4.4: evidence that an **intent IR** can sit between the LLM and classical realization. Strengthens advisory+admit over Translator-only rewrite. Pair with Cake (typed schedule) and HintPilot (validated pragmas). Does **not** move A5 or C6 toward unconstrained IR emission.

## Limits / caveats

- LLVM IR / CPU-style benches; not Triton/Tile/serving.
- Intent distilled by GPT-5 from `-O3` pairs can inherit pass-pipeline bias.
- Mean speedup vs other LLM generators ≠ median CI win vs production `-O3` (**C2**).
