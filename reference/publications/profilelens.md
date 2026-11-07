# AMD ProfileLens: trace-to-roofline profiling and opportunity ranking

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | AMD Advanced Graphics and Inference (AMD-AGI) |
| **Publisher** | GitHub |
| **Type** | code |
| **Group** | Company infra |
| **Link** | [AMD-AGI/ProfileLens](https://github.com/AMD-AGI/ProfileLens) |
| **Evidence tier** | **B** — deterministic feedback/diagnostics infrastructure, without demonstrated recovered application gains |
| **Version / reviewed** | `README.md` content blob `aaec36366d7455dc4598a5569a4c4f210f7cfbaa`, reviewed 5 November 2026 |

## Key contributions

ProfileLens combines a Perfetto/PyTorch timeline, dynamic kernel datatype information, a `rocprofv3` counter pass and empirically measured, datatype-specific roofline ceilings into a ranked list of optimization opportunities. A `full-analysis` command executes a workload, reads the trace, profiles the top-K kernels and emits Markdown/JSON reports. This is *structured performance feedback*, not an optimizer that itself generates new programs.

## Summary

The documented flow targets AMD GPUs with ROCm 7.x and PyTorch profiling enabled. It identifies the hottest kernels from the trace, resolves each kernel's compute datatype using PyTorch, Triton, graph-capture and MLIR-DSL launch hooks, then gathers compatible hardware counters in a single `rocprofv3` pass. It can omit lower-priority counters if they cannot fit in one pass, and reports the omissions. It fetches a microbenchmark to measure local per-datatype peaks rather than relying on specification-sheet maxima. The report includes kernel time share, arithmetic intensity, occupancy, HBM traffic, cache statistics and compute-versus-memory classification.

## Key takeaways

- **Reported metric, not achieved speedup:** `Max E2E Gain = (1 − %Roofline/100) × E2E Time%` ranks opportunities by an optimistic recoverable fraction. It assumes a kernel can reach the empirical ceiling without affecting other kernels, launch cost or the runtime; this is neither an independently observed gain nor a forecast of the final application improvement.
- **Baselines and budgets:** it produces a per-workload profile of the starting implementation; there is no published before/after optimization benchmark, stronger serving comparator, agent baseline, GPU-hour budget, false-attribution rate or application benefit in the README. The authors explicitly omit measured example results from the public source tree.
- **Hardware and implementation:** ROCm 7.x `rocprofv3` and `rocprofv3-avail`, a compatible AMD GPU, profiler trace and repeated workload execution. A temporary patched `librocprofiler-sdk-tool.so` is included, with source/licence/checksum/rebuild notes and a removal plan; this increases the environmental and maintenance assumptions.
- **Independent implementation possibility:** most analysis is rule-based and structured. An LLM that merely reads the report cannot be credited with discovering those hotspots; compare its decisions against a deterministic hotspot/roofline ranking with the same data.

## Why it matters for this survey

The thesis' adaptive-reasoning and controller-improvement tests require distinguishing the agent's decision from better supplied measurements. ProfileLens may improve a search agent's information quality, but until there are controlled downstream measurements it is an enabling tool, not causal evidence of agent superiority. The trace-analysis family is related to AMD [GEAK's end-to-end agent](geak-v4-github.md) and [ATTUNE](attune.md) only in general optimization workflow, **not** the same evaluated study or independent replication.

**Proposed experiment:** hold workload, profiler trace, kernels, hardware, fixed optimization actions and total run budget constant. Compare deterministic roofline/top-K heuristics, a conventional tuning/search procedure with the same profiler output, and an agent with/without that output. Check actual admitted application throughput, regression tails, profiler overhead and number of accurately diagnosed bottlenecks. Include serving prefill/decode and multi-GPU communications separately when available.

## Limits / caveats

The formula upper-bounds a simplified kernel-only opportunity; memory traffic, synchronization and run-to-run variability make it easy to overestimate. The documented workflow is not a proof that all launch hooks or hardware-counter mappings are reliable. No reproduction or quantitative gain is claimed here. Do not conflate this new ProfileLens repository with AMD's older [TraceLens](https://github.com/AMD-AGI/TraceLens) library, which also analyzes traces but has a separately described agent.
