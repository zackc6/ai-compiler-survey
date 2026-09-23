# Pallas: JAX kernel language for GPUs and TPUs

| Field | Value |
|---|---|
| **Year** | 2024+ |
| **Org** | Google (JAX) |
| **Publisher** | JAX documentation |
| **Type** | company |
| **Group** | Classic DL compilers |
| **Link** | [https://docs.jax.dev/en/latest/pallas/design/design.html](https://docs.jax.dev/en/latest/pallas/design/design.html) |
| **Evidence tier** | **B** — typed kernel sink under MaxKernel / JAXBench; Mosaic still lowers |

## Key contributions

- JAX extension for custom kernels in a Triton-like blocked model: `pallas_call` / `pl.kernel`, `BlockSpec` index maps, and explicit refs.
- **Two lowers, one front door.** GPUs lower to Mosaic GPU (formerly Triton). TPUs lower to **Mosaic**, which consumes mostly standard MLIR (`vector`, `arith`) and emits LLO. `BlockSpec`s become Mosaic pipeline schedules.
- TPU memory is part of the language: HBM vs VMEM vs SMEM vs semaphore, `dimension_semantics` (`parallel` vs `arbitrary`) for megacore, and `pltpu.emit_pipeline` for software pipelining. TPU interpret mode can check races off-device.
- Not an agent. [MaxKernel](maxkernel.md) and [JAXBench](jaxbench.md) treat Pallas as the program the agent is allowed to edit.

## Summary

Pallas is the agent-visible kernel face on the JAX/TPU path, the way Triton/Gluon/TLX are faces on NVIDIA/AMD GPUs and TIRx is the face on TVM. The agent authors blocked Python; Mosaic owns pipelining, legality, and device code. Docs stress that the TPU backend is experimental and that patterns the hardware does not support fall back to slow emulation — a sharp compiler error is the useful signal, not a fluent kernel that “runs.”

## Key takeaways

- **C4** gains a TPU sink. It does not collapse Triton vs Tile, and it is not an L-llm band (survey L4-class kernel DSL, classical lower).
- **T1** example: block specs, memory spaces, and compiler params are a narrower contract than pasted Mosaic IR. Still no portable schema across Pallas · Triton · Tile · Cake.
- Name collisions: Pallas ≠ PLENA (Zomboss research accelerator) ≠ a new survey L-band.

## Why it matters for this survey

Substrate digest required once MaxKernel names Pallas as the sink (same rule as CuTe DSL under CuTeGen). Job (a) artifact. Mosaic remains the data plane.

## Limits / caveats

- Living docs, not a measured paper. Performance claims belong to MaxKernel / JAXBench / Tokamax, not this page.
- GPU and TPU backends do not expose the same control. An agent trained on one does not automatically transfer.
