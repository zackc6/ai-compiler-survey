# Slide 6: Executive verdict

Lead with the headline, then the gloss chips, then the body columns. Do not let chips cover the headline on the PDF — they sit *below* it.

**Headline — hybrid punchline.**
Agents reshape the **control plane** (search, orchestrate, synthesize) more than they replace the **data plane** (lower, legality, measure, fallback). This is the executive verdict the rest of the deck defends. If they remember one sentence, it is this.

**Gloss chips — define the planes in the room.**
Left chip: **Control plane** = search / orchestrate / synthesize — where LLM agents and offline eng live. Right chip: **Data plane** = lower / legality / measure / fallback — Inductor, XLA, MLIR passes, Triton, Tile, classical `opt`. Agents sit *above* via typed tools and admit; they do not silently become the lowering path.

**Left column — three stacked claims (walk top to bottom).**
1. **Compilers for AI × AI for compilers** — the two stacks from slide 3 are merging, not one eating the other.
2. **Hybrid LLM–compiler loops** — propose → measure → admit; classical applicator always runs; agent output is advisory until gated.
3. **4th job Tier A: bring-up / codesign** — job (d): coverage → performance on new **GPU** / **NPU** (neural processing unit) / **ASIC** (application-specific integrated circuit) silicon; TritorX / KernelEvolve-class evidence. Hardware only via kernels/IR/oracles — not autonomous tape-out.

**Right box — what will *not* happen soon.**
Bullet one: unconstrained LLM replaces Inductor/`opt` — no typed admit, no CI regressability. Bullet two: autonomous chip tape-out via compiler agents — that is **C10** scope creep; humans and EDA own tape-out; agents stress kernels and IR proposals.

Closing line: hybrid is the bet; replacement is the anti-pattern. Bridge to slide 7: the four jobs (a–d) are how that hybrid decomposes in product.
