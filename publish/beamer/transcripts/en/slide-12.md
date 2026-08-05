# Slide 12: E2E-optimal-seeking — reshape around F

This is the answer to “many bands → local optima; can next-gen target e2e optimum?”

Complexity bound first, without using it as an excuse: a unique closed-form global optimum over all bands and future hardware is intractable. That does *not* mean we keep siloed greeds because classical compilers never proved optimality.

Survey lean: yes — an e2e-optimal-*seeking* architecture. Product fitness F — latency, energy, dollars-per-token, quality, cluster util — as a Pareto or constrained front, not the sum of local costs.

Walk the stack: F on top; e2e search controller with joint or bilevel policy and credit across bands; L2–L7 remain legality and lower surfaces — local cost models are proposal priors only; physical F-admit via serving A/B, pinned traces, energy and fleet; freeze or classical fallback.

Claimed: joint search plus F-admit plus freeze. Not claimed: unique mathematical global optimum. Complexity bound is not a reason to stop reshaping.

Bridge: next slide separates soft merge of that e2e controller from hard replace of the compiler.
