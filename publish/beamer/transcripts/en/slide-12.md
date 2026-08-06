# Slide 12: E2E-optimal-seeking — reshape around F

Answer to: “Many bands → local optima; can next-gen target true end-to-end optimum?” Complexity theory says a closed-form global optimum is intractable — **that is not an excuse** to keep siloed per-pass greed.

**Product fitness F (top ember bar).**
**F** bundles latency, energy, **$/token**, quality, cluster utilization — a **Pareto** or constrained front (tradeoffs explicit), **not** the sum of local band costs. Product defines which point on the front they need; compiler+agent stack searches toward it.

**E2E search controller (steel bar).**
Joint or bilevel policy with **credit assignment across bands** — a win at L4 kernel DSL may hurt L6 serving **KV** layout; controller learns coupling. Budget/stop/freeze rules live here, not inside each local pass.

**Band row — L2–L3, L4–L5, L6, L7*.**
Bands remain **legality / lower surfaces** — classical compilers still own correctness. Local cost models (slide 11) are **proposal priors only**; physical measurement and **F**-admit decide what ships.

**Physical F-admit (green bar).**
Serving A/B → pinned traces → energy/fleet measurement. Admit on real **F**, not proxy microbench alone. On failure: **freeze** last good artifact or **classical fallback** — never silent bad codegen in production.

**Claimed vs not claimed (bottom two boxes).**
*Claimed:* **e2e-optimal-*seeking*** control plane — joint search + **F**-admit + freeze. This is the SURVEY lean for Horizon A–B.
*Not claimed:* unique closed-form global optimum or polynomial complexity bound. Bound ≠ stop trying; it means honest architecture with admit and fallback.

Closing beat: seek e2e under **F**; do not pretend you proved optimality. Bridge: slide 13 separates soft **merge** of that controller from hard **replace** of the compiler (**M1≠M3**, **C6-B**).
