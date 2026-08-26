# Gluon: Triton's lower-level GPU programming model

| Field | Value |
|---|---|
| **Year** | 2025/26 |
| **Org** | Triton project (OpenAI / community) |
| **Publisher** | Triton docs |
| **Type** | company |
| **Group** | GPU kernels & inference compilers |
| **Link** | [https://triton-lang.org/main/gluon/index.html](https://triton-lang.org/main/gluon/index.html) |
| **Evidence tier** | **B** — explicit-layout / warp-specialize face of Triton; Helion raises, Gluon lowers; not a published agent product |

## Key contributions

- **Gluon** (`triton.experimental.gluon`, `@gluon.jit`) is a Python frontend to Triton **GPU (`ttg`) IR**: layouts, shared-memory descriptors, and warp specialization are *arguments*, not compiler secrets.
- `warp_specialize` forks a default partition plus worker partitions (distinct warp counts / register budgets) — the control Triton’s block-uniform model hid.
- Same backend as Triton below `ttg`; skips the middle that guessed layouts. Trade: less portable across vendors/generations; more peak on Blackwell-class async MMA.
- [Helion](helion-blog.md) raises Triton; Gluon lowers it. [TLX](tlx.md) is Meta’s *embedded extension* of Triton (MIMW), not the same frontend.

## Summary

When FlashAttention-class Blackwell kernels broke Triton’s “compiler picks the schedule” promise, the Triton stack added a lower face instead of abandoning the compiler. Gluon is that face: explicit layouts and warp roles, still classically lowered. Same search-scope class as TIRx — a docs/code launch, not an “LLM-oriented IR” title.

## Key takeaways

- **L4** Triton-family *lower* surface (**C4**), not a new band. Agents that only emit `tl.dot` Triton miss the Gluon/TLX rungs KernelEvolve already uses.
- Explicit layouts are T1-adjacent mutation knobs; they do not replace serving oracles (T6).
- Do not collapse Gluon, TLX, and Helion: raise / extend / lower are three Triton faces.

## Why it matters for this survey

Tier B for **C4** and T1 “what face does the LLM see?”. Cite with [Helion](helion-blog.md), [TLX](tlx.md), [Cake](cake.md) (typed schedule, no layout algebra).

## Limits / caveats

- Docs + in-tree tutorials (`python/tutorials/gluon`); experimental API.
- No public Gluon agent-loop benchmark; production FA kernels may be hand-written Gluon (**C2**).
- PyTorch autoWS / warp-specialization roadmap is a *compiler* path on top of OSS Triton — complementary, not Gluon-the-language.
