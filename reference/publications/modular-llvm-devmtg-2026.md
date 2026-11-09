# Modular: LLVM Dev Meeting 2026 — Durable Infrastructure in the Agentic Era

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Modular |
| **Publisher** | Modular blog |
| **Type** | company |
| **Group** | Company infra |
| **Link** | [https://www.modular.com/blog/llvm-dev-meeting-2026-durable-infrastructure-in-the-agentic-era](https://www.modular.com/blog/llvm-dev-meeting-2026-durable-infrastructure-in-the-agentic-era) |
| **Evidence tier** | **C** — a vendor design position and meeting account with no measurements; context for the kernel-language and compiler-foundation questions, not decision evidence |
| **Version / reviewed** | Post dated 4 November 2026. Content verified independently by ChatGPT (09:25 HKT, 8 November 2026) and Claude (01:35 UTC, 8 November 2026) in the Review thread; not re-fetched by the 9 November sweep run; **re-fetched 9 November 2026 (~01:25 UTC) by the Claude GitHub Action**: the 4 November date, both BaseDSL quotations ("a platform for building custom Python DSLs on top of MLIR through a series of plugins", "internal to NVIDIA for now") and the absence of any performance or benchmark figure held. |

## Key contributions

The post is Modular's account of the 2026 US LLVM Developers' Meeting. Its argument is that **durable, shared compiler infrastructure** — MLIR-backed Mojo and the MAX stack, plus tooling shared across the LLVM community — reduces the fragmentation of kernel domain-specific languages and the per-accelerator maintenance burden, and that this matters more, not less, when agents write much of the code. It also reports NVIDIA's internal **BaseDSL**, described as "a platform for building custom Python DSLs on top of MLIR through a series of plugins" and "internal to NVIDIA for now".

## Summary

This is a design position, not an evaluation. The post gives **no performance or portability numbers** and does not compare Mojo/MAX against Triton, TileLang, TIRx or vendor libraries on any workload. Its value for the survey is as one pole of a live disagreement about what the foundation for agent-written kernels should be: a unified language and MLIR stack (Modular's position) against a minimal, extensible core with runtime-registered operations and types (Apache TVM's TIRx essay of 3 November 2026, digested in the [TIRx family](tirx.md)). NVIDIA's BaseDSL, as reported here, is a third shape — many small DSLs sharing one MLIR plugin platform — and is reported second-hand with no public artifact.

## Key takeaways

- No measured result; nothing here changes a forecast, a confidence label or a §5.3 row.
- The post is the clearest recent statement of the **"one durable stack" position** in the §6 question "One kernel language or several?". The opposite position (many thin surfaces over a small core) is stated the same week by the TVM community, also without measurements.
- BaseDSL is an industry report of an internal system; it should not be cited as evidence that NVIDIA has adopted or benchmarked a particular approach.

## Why it matters for this survey

The kernel-language question is now argued by three vendors or communities in the same fortnight with no shared measurement. The survey's test for that question stands: measure the same kernels on every deployment target under a declared tuning budget and report the worst-target result with the best. A unified stack and an extensible core are both compatible with agentic or entirely conventional optimization, so neither position bears on whether an agent adds value; they bear on the cost of giving any optimizer a new target. Related Modular material already indexed: [What about the MLIR compiler infrastructure?](modular-mlir-blog.md) and [the Claude C Compiler post](modular-claude-c-compiler.md).

## Limits / caveats

Vendor blog post; no data, no artifact, no comparison. Verified only as to its content and date (two independent reads on 8 November 2026). The claims about BaseDSL are Modular's report of another company's internal work.
