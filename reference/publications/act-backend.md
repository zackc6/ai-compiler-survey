# Automatically Generating ML Compiler Backends from Tensor Accelerator ISA Descriptions (ACT)

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | University of Illinois Urbana-Champaign (Charith Mendis's group; affiliations not listed on the arXiv abstract page) |
| **Publisher** | ACM OOPSLA 2026 · arXiv |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [arXiv 2510.09932](https://arxiv.org/abs/2510.09932) · [DOI 10.1145/3839457](https://doi.org/10.1145/3839457) · [act-compiler/act](https://github.com/act-compiler/act) |
| **Evidence tier** | **A** — a strong non-agent alternative for backend generation; required by the survey's rule to test the thesis against conventional methods |
| **Version / reviewed** | v1 11 October 2025, v2 18 August 2026; reviewed 15 October 2026 |

## Key contributions

ACT generates an ML compiler backend from an accelerator's instruction-set description alone. Instruction selection uses equality saturation parameterized by the ISA; memory allocation uses constraint programming. Generated backends plug into XLA. Six accelerator platforms are targeted, from industry (AWS Trainium, Intel AMX) and academia (Gemmini).

## Summary

The authors report that generated backends match or outperform commercial compiler backends and expert-written kernel libraries while keeping compilation overhead low, and that the generated backend for the AWS NKI ISA improved code-generation **coverage** for Trainium by **2.3×** over AWS's production compiler. The abstract gives no speedup figures; consult the paper for per-target numbers.

## Key takeaways

- The result is primarily coverage and retargeting cost, not peak speed; keep those axes separate.
- No LLM anywhere in the pipeline: the search is symbolic, so the artifact is deterministic and inspectable.

## Why it matters for this survey

The thesis must be tested against strong conventional alternatives. ACT shows that generating a backend from a hardware description is achievable with symbolic methods, which is the comparison arm for agent-generated lowering ([AI as a Compiler](ai-as-compiler.md)) and for the bring-up question: coverage on a new accelerator is exactly what agentic bring-up work such as TritorX claims. A controlled comparison would hold the ISA and workloads fixed and measure coverage, speed, validation effort, and engineering time for an ACT backend, an agent-written backend, and the vendor compiler.

## Limits / caveats

- Author evaluation; the peer-reviewed version should be consulted for per-platform numbers and the baselines used.
- ISA descriptions must exist and be accurate; writing them is a cost the abstract does not quantify.
- Coverage improvement on Trainium is relative to one production compiler version.
