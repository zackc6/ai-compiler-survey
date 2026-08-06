# Slide 32: Org Adoption Questions

Discussion prompts — not a quiz. On-slide: five amber question rows. Spoken: pause after each; let the room answer against their own roadmap.

**1. Online (CompileIQ) vs offline (Magellan) — which matches your release model?**
Job (a) online propose→measure→admit vs job (b) offline evolve heuristics→C++/MLGO. Product CI cadence, freeze artifacts, and reviewer capacity differ. If you ship weekly kernels but evolve heuristics quarterly, you may need both — but which is *default*? C5 settlement is release notes, not lab demos.

**2. Oracle stack: Alive2 / golden / serving A/B — who owns false negatives?**
Blocker one’s room question returns. When admit passes and production miscompiles, is it compiler team, agent platform, or serving SRE? Without named ownership, oracle ladders stall at “someone else’s problem.”

**3. Agent contract surface: LLVM / MLIR / Triton / StableHLO / Tile?**
Where will you invest T1 typed interfaces first? LLVM/heuristics (C1), MLIR mid-IR, Triton kernel DSL, StableHLO portable graph, or vendor Tile IR? Multi-substrate fleets cannot wait for one mega-schema — but you need *a* chosen surface per product line.

**4. How do you cache/regress traces across compiler *and* model upgrades?**
T3 replay contract in practice. Cache key: IR hash, hardware, compiler version, agent policy. What breaks your golden replay — and who reruns the agent vs pins the old artifact?

**5. Max $/build for a median X% win? Named maintainer per admitted artifact?**
Commercial blocker two in one question. Token budget per percent gain; CODEOWNER per ACF, kernel, or heuristic class. If you cannot name both numbers and owners, Horizon A economics are undefined.

Closing line: use silence. These five questions expose whether the hybrid bet is actionable in *this* org — not whether the survey is interesting.
