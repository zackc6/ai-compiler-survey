# Slide 7: Four agent jobs — architecture spine

These four jobs are the architecture spine from SURVEY §5.1. Every product claim should map to one of them. They sit **above** classical lowering — not instead of it. Footer line on slide says exactly that; repeat it.

**(a) Online — propose → measure → admit.**
Runtime or near-runtime specialize: agent proposes a kernel variant, pass order, or pragma set; compiler measures; oracle stack admits or falls back to classical. Examples on slide: **CompileIQ** (ACF-class control artifacts), **GEAK** (AMD kernel agent loop), **ACCLAIM** (guide agent over bands), **HintPilot** (compiler-validated pragmas). Spoken beat: this is hot-path specialize with explicit admit — not silent default-all.

**(b) Offline — evolve heuristics → C++ / MLGO.**
Agents search offline; output is shippable artifacts checked into **VCS** (version control system): C++ heuristics (Magellan **EVOLVE-BLOCK**), or features for in-tree neural advisors. **MLGO** (Machine Learning Guided Optimization — LLVM’s learned pass advisors) is the in-tree path; Magellan is the evolutionary C++ path. Both may coexist — C1 checkpoint. Examples: Magellan, AlphaEvolve.

**(c) Engineering — oracle-gated PR / change.**
Agents propose compiler patches, dialect additions, or heuristic updates; humans plus oracles review before merge. **Archer**-class: oracle-gated pull request (**PR**) workflow — the agent is a junior engineer with a strict linter and test suite, not an unsupervised committer.

**(d) Bring-up — coverage → performance, sim + silicon.**
New hardware SKU: first win is *coverage* (correct kernels across op surface), then *performance*. Sim ↔ silicon feedback loops propose ISA/dialect tweaks — **TritorX**, **KernelEvolve** as Tier A references. This is codesign feedback without autonomous EDA (**C10**).

**Diagnostic for the room.**
If a vendor pitch does not map to (a)–(d), ask which job it is actually doing. “We replace your compiler” is usually mispackaged (b) or unconstrained (a) without admit — flag it.

Closing beat: four jobs, one invariant — classical lowering stays; agents own search and synthesis around it.
