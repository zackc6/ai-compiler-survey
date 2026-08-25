# Can Large Language Models Understand Intermediate Representations in Compilers?

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Kent State University · Huazhong University of Science and Technology · Pacific Northwest National Laboratory · Chongqing University |
| **Publisher** | ICML 2025 · PMLR · arXiv |
| **Type** | paper |
| **Group** | Foundation LLMs for compilers |
| **Link** | [https://arxiv.org/abs/2502.06854](https://arxiv.org/abs/2502.06854) |
| **Evidence tier** | **A** — negative probe: fluency on LLVM IR ≠ CFG / execution skill; bounds free-rewrite (C3) |

## Key contributions

- First systematic eval of six LLMs (GPT-4, GPT-3, DeepSeek, Gemma 2, Llama 3, Code Llama) on **compiler IR understanding**, not only source code.
- Four tasks on HumanEval-C++ compiled to LLVM IR at `-O0`–`-O3`: CFG reconstruction (DOT), decompilation, summarization, execution-reasoning assertions.
- Public harness: [hjiang13/LLM4IR](https://github.com/hjiang13/LLM4IR) (LaMIR).

## Summary

ICML 2025 study asking whether frontier and open code models *understand* LLVM IR the way compilers do. Models parse syntax and recover high-level structure, but fail instruction-level reasoning: wrong CFG edges on branches/loops, skipped ops in decompile/summaries, and heuristic “what this function probably does” instead of simulating SSA. Authors recommend IR-specific fine-tuning **and** control-flow-sensitive architectures — not dumping more `.ll` into the prompt.

## Key takeaways

- Surface IR fluency is not a compiler skill: CFG and execution are the failure modes that matter for Translator-role agents.
- Matches mlirAgent (below-identity free rewrite) and Fast Feedback (metrics beat full compiled IR in the prompt).
- Does **not** justify a new data-plane band; it justifies **summaries / fingerprints / typed mutation surfaces** (T1) instead of paste-the-IR.

## Why it matters for this survey

★ for **C3-B / A5 / T1**: the missing *understanding* bound on family-1 fluency IRs. Cite with [mlirAgent](mliragent.md) (transform skill) and [compiler-feedback](compiler-feedback-llms.md) (Fast Feedback). Supports hybrid: agents should not treat classical LLVM IR as a chat language.

## Limits / caveats

- HumanEval-C++ scale (164 programs × four opt levels), not GPU kernels or serving graphs.
- 2025 model set; later IR-pretrained models (Meta LLM Compiler FTD) are not the eval subjects.
- Probe of *understanding*, not of pass-list or kernel-search product loops.
