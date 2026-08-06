# Slide 21: Blocker 2 — Cost, replay, when may the agent run?

This is blocker two from the top-five list. On-slide: three phases left to right with arrows; footer gives the cache key and budget formula. Spoken: walk the lifecycle, then name what makes it commercially real.

**Lab — explore, do not ship.**
Interactive chat and tools. GEAK-style generate–eval–reflect loops, CompileIQ experiments, Magellan recipe drafts. Nondeterministic spend is acceptable here. Say out loud: lab is where you learn the action space — not where you bill customers per compile.

**Product build CI — batch optimize under budget.**
Agents run in batch on pinned traces with explicit targets: dollars per build, latency ceiling, Welch or canary gates before merge. This is where SLO (Service Level Objective — measurable target) meets SLA (Service Level Agreement — contracted promise): you need a named budget for median percent gain, not “run the LLM whenever.” ACCLAIM and CompileIQ-class online specialize belong here — admitted outputs only.

**Freeze — zero LLM at serve time.**
Control files (ACF — Advanced Control File, portable compiler knobs), specialized kernels, evolved heuristics land in version control. Serving replays artifacts; no agent on the hot path. FlowCompile / AgentFlow freeze is the pattern: compile the workflow once, place the frozen graph. Horizon A success = build-CI gated specialize + oracles + freeze artifacts.

**Cache key and budget line.**
Read the footer: cache key is (IR hash, hardware, compiler version, agent policy). Budget is dollars per percent gain. Without both, CI cannot regress agent decisions across upgrades — model swap, compiler bump, policy change all invalidate silently.

Closing beat: this commercially falsifies “chat with the compiler on every build” without spend and latency SLOs. If your roadmap cannot name when the agent runs and what gets frozen, you are still in demo mode.
