# Measuring the Checker: Mutation Analysis for GPU-Kernel Benchmark Oracles

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | National University of Singapore · Nanyang Technological University · VinUniversity (CAIR) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Validation and approximate hardware |
| **Link** | [arXiv 2609.22220](https://arxiv.org/abs/2609.22220) |
| **Evidence tier** | **A** — makes the benchmark oracle a measured component; directly affects how any reported speedup should be read |
| **Version / reviewed** | v1, 2 September 2026; reviewed 15 October 2026 |

## Key contributions

Injects 10,303 compilable faults into verified CUDA implementations of 188 KernelBench problems and establishes an independent kill witness for 7,384 of them. The official KernelBench check (five inputs, `allclose` tolerance) **misses 16.9%** of witnessed faults.

## Summary

Misses are concentrated by fault class: precision faults 78.6% missed (of 271), synchronization 27.8% (of 400), boundary 22.9% (of 1,735), semantic 14.9%, indexing 14.4%, arithmetic 8.7% (of 3,349). The tolerance forgives precision faults by construction.

## Key takeaways

- Test suites chosen by set cover over the kill matrix detect 98.0% of witnessed faults with two inputs per problem (94.8% on held-out mutants), versus 83.1% for the official five-input protocol.
- [KernelBench-Verified](kernelbench-verified.md), audited in the paper, improves detection by 8.5 points over the official protocol on a unified denominator. A reconstructed fuzzing baseline reaches 86.2% but falsely rejects correct kernels 107 times, so it is not a sound fix.
- The 16.9% figure is a miss rate on this synthetic fault population, not a real-world error rate for generated kernels.

## Why it matters for this survey

Every kernel-level number in the evidence register passes through a checker; this is the first measurement of how much the common one lets through, and the precision result explains why agent-found "speedups" that trade accuracy survive. Combine with the rejected-candidate list in [KDA²](kda2.md): injected faults, held-out inputs, and false-rejection tests should be reported for the acceptance machinery before an agent's speedup is trusted.

## Limits / caveats

- Synthetic mutants in CUDA on KernelBench problems; other benchmarks and Triton or TIRx kernels are not covered.
- Set-cover suites are tuned to the observed mutants; the held-out figure is the one to use.
- Oracle strength and false-rejection rate trade off; the paper quantifies one side more than the other.
