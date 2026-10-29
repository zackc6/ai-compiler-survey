# OpenTuner: An Extensible Framework for Program Autotuning

| Field | Value |
|---|---|
| **Year** | 2014 |
| **Org** | Massachusetts Institute of Technology, Computer Science and Artificial Intelligence Laboratory |
| **Publisher** | ACM PACT 2014; MIT author manuscript |
| **Type** | paper |
| **Group** | Classic DL compilers |
| **Link** | [MIT primary PDF](https://commit.csail.mit.edu/papers/2014/ansel-pact14-opentuner.pdf) |
| **Evidence tier** | **A** — non-agent adaptive search controller and matched-budget baseline |
| **Version / reviewed** | PACT 2014 full paper; reviewed 22 October 2026 |

## Key contributions

OpenTuner exposes domain-specific configuration spaces, measurement interfaces and an ensemble of optimization methods. A bandit-style allocator gives more tests to techniques that find improvements; techniques share results in a common database. Adaptive controller behavior and experiment memory therefore predate language-model agent systems.

## Summary

The authors build autotuners for **seven projects and sixteen benchmarks**, reporting **up to 2.8 times** improvement against each project's own earlier technique. These are different projects and denominators, not one matched benchmark or a common geometric mean. Compiler-relevant cases include GCC optimization flags and Halide pipeline schedules; other cases are not compilers.

## Key takeaways

- **Baseline:** each project's prior tuner or hand-optimized setting, rather than a shared modern compiler or agent. The maximum 2.8-times result must not be described as a GPU kernel or application-wide gain.
- **Actions:** user-specified flags, schedules and configuration constraints; no automatic invention of arbitrary compiler analyses or lowering backends.
- **Search cost:** measured candidate evaluations allocated dynamically. Time-to-result is reported per project, but the mixed suite has no single GPU-hour, token or dollar budget; a modern comparison needs the same measurement service and total wall/compute cost.
- **Validation:** domain-specific execution and constraints, not universal formal equivalence. Some GCC floating-point flags can change numerical contracts; enforce the same acceptance rules.
- **Lineage:** the Halide experiment in OpenTuner and the 2019 Halide autoscheduler belong to one broad Halide research ecosystem, not independent replication.

## Why it matters for this survey

Agentic compiler orchestration must beat a strong *non-agent adaptive controller*, not just a fixed random or Bayesian baseline. Compare OpenTuner's ensemble, a fixed search method, and an agent on the same actions, feedback, knowledge and resources. Separate final performance from search efficiency and amortized development cost.

## Limits / caveats

Hardware and benchmarks date to 2014, and the 2.8-times maximum spans heterogeneous workloads. Adaptive test allocation is not recursive self-modification, nor does it qualify the 2027 controller research checkpoint or the 2031 component-generation predicate.
