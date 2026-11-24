# Voyager: An Open-Ended Embodied Agent with Large Language Models

| Field | Value |
|---|---|
| **Year** | 2023 |
| **Org** | NVIDIA · California Institute of Technology · University of Texas at Austin · Stanford University · University of Wisconsin–Madison |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [arXiv 2305.16291](https://arxiv.org/abs/2305.16291) · [project](https://voyager.minedojo.org/) |
| **Evidence tier** | **C** — foundational procedural-memory (skill library) mechanism; Minecraft, no compiler workload |
| **Version / reviewed** | v2, 19 October 2023; HTML full text (first part) reviewed 24 November 2026 |

## Key contributions

An agent that plays Minecraft with GPT-4 as a black box. Three parts: an automatic curriculum that proposes the next task, an iterative prompting loop that uses environment feedback, execution errors and a separate GPT-4 critic for self-verification, and a **skill library** of executable programs. A program enters the library only after the critic judges that it achieved its task; skills are indexed by an embedding of a generated description and the top five are retrieved for each new task.

## Summary

Against prior agents it reports 3.3× more unique items, 2.3× longer distances, and key tech-tree milestones up to 15.3× faster. Without the skill library, progress plateaus: the ablation reaches the iron level (29 ± 11 iterations against 21 ± 7) but never unlocks diamond tools (0 of 3 trials). In new worlds the library helps solve unseen tasks faster (diamond pickaxe in 19 ± 3 iterations, 3 of 3 trials, against 36 in 2 of 3 trials without it).

## Key takeaways

- Admission is gated by an LLM critic (GPT-4 self-verification), not by a ground-truth check; the authors report the critic can misjudge success (it once failed to recognise spider string as evidence of beating a spider), and the curriculum hallucinates items that do not exist.
- GPT-4 cost (about 15× GPT-3.5 at the time) is the authors' first stated limitation.

## Why it matters for this survey

The closest general-agent analogue of a compiler that keeps the kernels, rewrites or schedules its agents discover and reuses them: procedural memory in the [CoALA](coala.md) sense, and the "Experience" stage of the [Storage-to-Experience survey](agent-memory-storage-to-experience.md). Its admission rule (only critic-approved skills enter) is weaker than the survey's rule that acceptance stays outside the optimizer, because the critic is itself an LLM. For a compiler it motivates a test of component reuse; reusing a stored kernel or schedule does not by itself demonstrate a reusable compiler transformation or lowering. The compiler question it cannot answer is staleness: a stored kernel can become slower or wrong when the toolchain or hardware changes.

## Limits / caveats

- A game environment with an API of primitive actions; no performance objective, so "better" means more capability, not faster code.
- Comparisons are to other prompting agents, not to search or planning baselines at equal cost.
