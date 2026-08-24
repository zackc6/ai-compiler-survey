# Slide 41: Appendix — publication groups

Digest corpus shape — group counts and usage rules. On-slide: count rows + “how digests are used” footer. Spoken: give scale, then methodology.

**Group counts (read the numbers).**
24 GPU kernels & inference · 14 agentic & RL · 14 source control & review · 10 classic DL compilers · 10 company infra · 10 forums & workshops · 8 surveys & vision · 8 foundation LLMs · 6 MLGO & RL gyms · 6 HW codesign & bring-up · 6 commercial products · 5 control-plane substrate · 1 correctness lineage. Total **122** digests — tiered, not flat. Also mention Cake, Argus, GEAK v4, Zomboss, T-LLM, llvm-harness as the August-wave additions if someone asks what moved the counts.

**How digests are used (footer).**
Mechanism first — what did they build, what oracle, what artifact freezes? Demote generic forge AI — Tier C repos and Copilot-class tooling do not settle C1–C10. Keep both sides of a conflict — Magellan *and* MLGO, free rewrite *and* advisory; do not average opposing evidence into a comfortable middle.

**Update rule.**
Change the prediction only when Tier A products/repos or ★ digests move — public traces, release notes with ACF workflows, llvm patches, serving A/B results. Opinions and single-kernel blogs are pressure, not settlement.

Closing beat: the corpus is organized for falsification. Use group counts to find depth in your subdomain; use ★ and Tier A to decide if the hybrid bet shifted.
