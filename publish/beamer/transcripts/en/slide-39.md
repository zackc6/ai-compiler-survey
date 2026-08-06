# Slide 39: Appendix — Tier A open repositories

Tier A open repos by job type. On-slide: two bands + tier gloss. Spoken: map repos to jobs (a)–(d) and tier semantics.

**Offline / review / heuristics.**
OpenEvolve, HeuriGym — evolutionary heuristic search. Archer — oracle-gated pull-request review. Compiler-R1 — tool-calling pass search (SFT+RL). HintPilot — compiler-validated pragmas. mlirAgent — IR transform baseline (fragile; useful as negative pressure for C3). Job (b) offline and job (c) engineering review.

**Online / kernels / bring-up.**
ACCLAIM, CompileIQ — online propose→measure→admit. GEAK, KernelAgent — kernel generation loops. KernelBench(-X) — correctness and speed ladder. FlashInfer-Bench — serving traces. AutoKernel, Helion — kernel DSL surfaces. TritorX / KernelEvolve — sim/silicon→dialect feedback (job d). Jobs (a) online and (d) bring-up.

**Tier definitions.**
A = agents + domain oracles change heuristics, kernels, knobs, or review — prediction-relevant. B = data-plane hosts agents attach to. C = generic forge AI only — useful tooling, demoted for checkpoint settlement (C7).

**How to use in discussion.**
When someone cites a repo, ask: Tier A mechanism or Tier C demo? Point to job letter — does it freeze artifacts, admit with oracles, or just chat?

Closing line: this is a curated forge map for the hybrid prediction — not every GitHub repo tagged “compiler AI.”
