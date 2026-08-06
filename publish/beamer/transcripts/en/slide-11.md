# Slide 11: One universal cost model? — No (Horizon A)

Direct answer to the room’s question: “Can one cost model cover all passes — including ones we have not invented yet?” **No** for Horizon A. Two columns plus a size callout at the bottom.

**Left — Why not one model (amber box).**
- **Different legality / oracles per band** — Alive2 certifies LLVM IR slices; it does not certify **GPU** race freedom or serving-time equivalence. A single cost tensor cannot share labels across L3 vs L6.
- **Choosing the level *is* the product** — ACCLAIM’s guide agent decides *which band* to spend search budget on; that meta-decision is not reducible to one local cost.
- **Cost models stay local** — **MLGO**, Ansor, MetaSchedule transfer inside a family (e.g., LLVM inliner features), not from fusion → Triton → regalloc → serving A/B in one weight file.
- **Future passes need new measured labels** — every new ISA SKU and pass needs fresh (program, action, HW) tuples; frozen weights cannot invent unmeasured hardware behavior.

**Right — If bands do not consolidate (steel box).**
Do not wait for the one true IR. Ship **pluggable interfaces** now:
- Agent compile schema with admit hash — reproducible agent outputs.
- Typed tools / **MCP**-class servers (Model Context Protocol — typed tool servers agents call).
- Dialect + oracle + objective plugins per band.
- Placement / fleet plugins for **L7**.

**Size callout (bottom ink box).**
Parameter count is **not** the bottleneck. Local advisors: often **KB–MB**. Cross-band *proposer*: ~**7B–70B+** IR LLM — still only a **prior**, not ground truth. Hard part: labeled (program, action, HW, energy, **SLO**) tuples, refreshed every SKU.

**Bet line — say it.**
Small per-band costs + optional large orchestrator — **not** one mega-cost-model eating L1–L7.

Bridge to slide 12: local costs are proposal priors only; architecture must still seek **e2e** (end-to-end) optimum under product fitness **F**.
