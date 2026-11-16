# AgentKernelArena: an RL-ready environment for GPU kernel agents with independently evaluated rewards and end-to-end serving tasks

| Field | Value |
|---|---|
| **Year** | 2026 (repository created January 2026; paper arXiv 2605.16819, May 2026) |
| **Org** | AMD (AMD-AGI organization on GitHub; the citation lists Sharareh Younesian, Wenwen Ouyang, Sina Rafati, … Emad Barsoum) |
| **Publisher** | GitHub repository (`README.md`, `docs/reference/benchmark-methodology.md`); arXiv for the paper |
| **Type** | code |
| **Group** | MLGO & RL gyms |
| **Link** | [AMD-AGI/AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena) · [paper (arXiv 2605.16819, not read)](https://arxiv.org/abs/2605.16819) |
| **Evidence tier** | **A** — defines a benchmark and reward protocol (cold-cache graph timing, interleaved baseline remeasurement, evaluator-owned verdicts, end-to-end serving-throughput tasks with a read-only verifier) that directly informs the comparable-benchmark and contract-evasion guidance; it is evaluation machinery, not a measured optimization result |
| **Version / reviewed** | Repository head `ace3ee5fa41dedf299095528f59a7354546984fc` (10 November 2026), read by shallow clone on 16 November 2026: README, benchmark-methodology reference, task tree (380 `task.yaml` files: 278 `triton`, 56 `flydsl`, 38 `hip`, 7 `gluon`, 1 `tilelang`, plus `e2e/`). The paper's own results (which agents, which scores) were not read because arXiv is refused on this runner. |

## Key contributions

AgentKernelArena ("Arena") is AMD's environment for developing and evaluating kernel-optimization *policies* with real GPU feedback. It separates three things that most kernel benchmarks fold together: the **task contract** (interface, high-precision PyTorch reference, vendored baseline implementation, production-derived workload shapes, correctness bounds), the **agent** (Codex, Claude Code, Cursor and DeepSeek Harness integrations; GEAK and KernelForge with separate setup), and the **evaluator**, which "independently compiles, checks and benchmarks the delivered implementation. The evaluator writes the result; an agent's completion message is not an acceptance verdict."

Two task scopes exist. **Kernel tasks** ask the agent to implement one operator for one scenario in a language the run selects (Triton, Gluon, HIP or FlyDSL); the same task can be run in any supported language and scored against the same vendored baseline. **End-to-end tasks** let the agent rewrite kernels and fuse computation across a model's declared source trees while weights, precision, parallelism, serving flags and workload stay fixed; the measure is model correctness and serving throughput under a fixed workload, "rather than substituting kernel-only timing". The end-to-end catalogue (the Magpie workload catalogue) includes text, multimodal and AgentX workloads.

## Summary

**Timing protocol (schema-v3 kernel tasks).** Each call is captured into a CUDA/HIP graph and timed per replay after a 1 GiB cache flush: 10 warm-ups, 100 samples, median; two input draws alternate between samples and every timed sample's outputs are checked. There is no event-timing fallback for these tasks: a baseline that cannot be graph-captured fails the task's QA audit, and every performance case must take the baseline at least 10 µs. The final evaluation remeasures the baseline interleaved with the candidate; the task's speedup is the geometric mean of per-case speedups. A paired utility keeps raw samples and reports a 95% percentile-bootstrap interval as a diagnostic.

**Reward.** A correct implementation can receive zero reward. For candidates eligible for performance credit, `reward = score = max(0, 1 − 1.05 / s)` with `s` the evaluator-reported speedup, so the score is positive only above 1.05× and compilation and correctness are prerequisites with no separate bonus. Correctness, acceptance and reward are separate fields; "a failed correctness case scores zero". Arena supplies environment and reward; training and policy updates are owned by an external system, and the evaluator's original result must be retained beside any trainer transformation.

**Comparisons.** Inside a task, the delivered implementation is compared with the preserved baseline; across runs, two configurations that differ in one setting (model, prompt, tool) are compared on the same task set and hardware with `compare_runs.py`. The README asks for repeated matched runs for stochastic agents and for gains to be read "alongside measurement variation".

**Task quality.** A `qa_auditor` agent runs deterministic checks, a control suite of known-wrong implementations and an optional model review, and writes an itemized report; blocking findings fail the task. New or materially changed tasks need a fresh GPU `qa_report.yaml` with `status: PASS`; "a schema-valid task or CPU test pass does not establish GPU qualification".

**Hardware.** Triton, Gluon, HIP and FlyDSL are verified on MI355X (`gfx950`); MI300X, MI325X and RDNA4 configurations exist but are "implemented but unverified".

## Key takeaways

- **The evaluator, not the agent, decides.** Independent recompilation, hidden-draw correctness on every timed sample, interleaved baseline remeasurement and cold-cache graph replay are the contract-evasion rows of this guide's validation table implemented as a benchmark, with a declared floor (10 µs) and a declared reward threshold (1.05×).
- **Application denominator exists but is a separate task class.** End-to-end tasks report model throughput from fresh paired baseline/candidate serving runs with a read-only verifier for scope, computation and measurement evidence; the README states that "numerical checks and semantic review have finite coverage; passing them is not a proof against every possible invalid implementation".
- **No results in the repository.** The README reports no agent scores, no speedups and no cost figures; those are in the unread paper. The repository is the protocol and the task set.
- **Language-agnostic tasks.** Scoring the same task in four languages against one vendored baseline is a way to separate the language from the agent, which the §6 kernel-language question needs.
- **Costs are recorded but may be null.** `agent_costs/` holds usage records; "unavailable values are null".

## Why it matters for this survey

For §4.10 (comparable benchmarks) and §4.2's contract-evasion row, Arena is the most complete public statement of *how* a kernel-agent result should be measured: graph-captured cold-cache timing with a stated flush size, paired interleaved remeasurement, correctness on every timed sample, a reward that is zero below a declared threshold, and an audit that fails tasks whose baselines cannot be timed honestly. It should be cited beside [Measuring the Checker](measuring-the-checker.md) (what an oracle misses), [HPCAgent-Bench](hpcagent-bench.md) (paired-run intervention efficacy) and [KCoral](kcoral.md) (remote-evaluation fidelity) as evaluation machinery that both agent and non-agent arms can share.

For the thesis it moves nothing by itself: there is no measured result in the repository, and the reward design is as usable for a conventional tuner as for an agent. Its value is that AMD's own agent results (AKLR, GEAK, Hyperloom) now have a declared protocol under which they could be compared with a non-agent arm; a future AMD result that reports Arena end-to-end throughput against a vendored baseline, with the evaluator's verdicts and costs, would be a candidate for the 2027 predicate. The same organization's [AKLR](aklr.md), [GEAK](geak-v4-github.md), [Hyperloom](hyperloom.md), [AMDKernelVault](amdkernelvault.md), Magpie (the workload catalogue, repository only) and ProfileLens form one AMD evidence family; Arena is its evaluation layer.

**Experiment:** run a strong non-agent tuner (hipBLASLt tuning, a Magnitude-class search, or EqiForge where the task class fits) through the same Arena tasks and reward, at the same wall-clock budget as the agent integrations, and publish both sides' evaluator verdicts, costs and variance.

## Limits / caveats

- The paper (arXiv 2605.16819) was not read; agent scores, task-set statistics beyond the file count, and any reported variance are unknown here.
- Verified on MI355X only; other AMD architectures are unverified and NVIDIA is out of scope, so cross-vendor comparison needs another harness.
- The baseline is the task's *vendored* implementation (and for end-to-end tasks the serving system as configured), not necessarily the best available one; a speedup over it is not a speedup over an expert-tuned library unless the task says so.
- The `qa_auditor` and the end-to-end verifier are themselves model-assisted; their detection rates are not reported.
- Worker containers "are not security sandboxes", which matters for any claim that the evaluator is isolated from the agent.
