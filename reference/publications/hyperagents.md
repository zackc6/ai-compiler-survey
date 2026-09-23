# Hyperagents

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | University of British Columbia · Meta · Vector Institute · University of Edinburgh (among listed affiliations) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2603.19461v1) |
| **Evidence tier** | B: editable improvement procedure outside compiler workloads |
| **Version / reviewed** | v1, submitted 19 March 2026; retrieved HTML also carries an August 2026 document date; reviewed 23 September 2026 |

## Key contributions

Hyperagents place a task agent and an agent that modifies it in one editable program. The modification procedure can itself change. Official code is [facebookresearch/HyperAgents](https://github.com/facebookresearch/HyperAgents).

## Summary

Experiments cover coding, paper review, robotics reward design, and mathematics grading. Transfer experiments hold the learned modifier fixed and measure its ability to generate better task agents over 50 iterations.

## Key takeaways

This is closer to recursive controller improvement than a fixed optimizer rewriting prompts. However, the main experimental process still fixes components such as parent selection and evaluation protocols. Do not describe it as unrestricted self-modification.

## Why it matters for this survey

Provides an experiment design for separating a better task solver from a better improvement procedure. It extends [Darwin Gödel Machine](darwin-godel-machine.md), with shared authors, and is not independent replication of that line.

## Limits / caveats

No compiler-controller result is established. Transfer to compiler search, stable long-run gains, and total evaluation economics remain open. The claim that improvement could continue indefinitely is a hypothesis, not a measured outcome.
