# Helion: A High-Level DSL for Performant and Portable ML Kernels

| Field | Value |
|---|---|
| **Year** | 2025 |
| **Org** | Meta (PyTorch) |
| **Publisher** | PyTorch blog |
| **Type** | company |
| **Group** | Classic DL compilers |
| **Link** | [Launch article](https://pytorch.org/blog/helion/) |
| **Evidence tier** | **B** — kernel programming and tuning infrastructure |

## Key contributions

Helion provides a domain-specific language close to PyTorch, with tile-oriented programming and automatic tuning over generated Triton implementations.

## Summary

The launch article describes a higher-level interface for writing kernels while retaining a substantial optimization space below it.

## Key takeaways

Compare both developer effort and per-target runtime performance. A higher-level interface can expose a useful search space without asking a programmer or agent to specify every low-level detail.

## Why it matters for this survey

Helion is a concrete option for the optimizer’s programming interface. The later [language-model-guided tuning report](helion-llm-autotuning.md) adds evidence about search efficiency.

## Limits / caveats

This digest covers the launch article. It must not be used to claim that Helion has no language-model tuner: that conclusion became outdated in June 2026. The later report distinguishes tuning time from final kernel speed.
