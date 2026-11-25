# Harness Evolution Hits a Ceiling: When Weight Training Should Begin

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Independent researcher · UC Berkeley · Purdue University · Stanford University (per-author mapping not clear in the source) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2610.11655) |
| **Evidence tier** | B: held-out evidence on when to change the controller versus the model weights; no compiler benchmark |
| **Version / reviewed** | October 2026; arXiv paper text reviewed by Claude 25 November 2026 |

## Key contributions

Proposes choosing between **harness evolution** (changing code and text around a frozen model) and **weight training** by the composition of failures. Each failed run is labelled by its first failure. **Process failures**, where the harness blocked the agent or the agent looped, repeated calls or ran out of steps, are what harness changes fix. **Content failures**, where a delivered plan is poor with no process signal, are what training targets. The harness's improved trajectories are then the training data.

## Summary

Experiments on DeepPlanning (development and held-out splits) and WebArena-Lite. The authors cross seed and evolved harnesses with base and LoRA-trained weights to see which gains a trained model keeps.

## Key takeaways

- Qwen3.5-4B held-out score: 0.164 with the seed harness to 0.297 with the evolved one. Delivered-answer rate: 55% to 90%. Qwen3.5-9B: 0.323 to 0.442.
- The measurement noise is stated: per-rollout standard deviation 0.023, with differences below 0.035 treated as noise.
- A 9B LoRA adapter (attention and MLP) cuts the planning-capacity failure share on held-out tasks from 28.1% to 4.5%. On the seed harness alone that adapter reaches 0.454, matching the evolved-harness line.
- **Control:** an adapter trained on the same trajectories with assistant outputs shuffled scores 0.227 below the base model on held-out. The gain comes from the trajectory content, not from training itself.
- On WebArena-Lite the harness gain (0.256 to 0.344 on 117 unseen tasks) did not grow with adapters trained on its trajectories, so the second benchmark only partly supports the first.

## Why it matters for this survey

The survey asks whether a compiler's controller should improve, and this paper offers a diagnostic for which layer to change. In a compiler search the analogue is clear: timeouts, loops, unparseable candidates and tool misuse are process failures that a controller change can fix; a valid but slow kernel is a content failure. It also suggests a measurable order of work, controller first and then distillation of its trajectories into the model. That order can be tested with the shuffled-trajectory control. It is one of the few controller studies here that reports held-out scores with a stated noise floor.

## Limits / caveats

Planning and web tasks with small open models, not compiler optimization. Two benchmarks, with the weight-training benefit shown mainly on one. The failure taxonomy is the authors' own and its labelling reliability is not reported in what was read. No total cost comparison between harness evolution and training. Strengthened by the same crossed design on a kernel-search agent, with failures labelled by compile, correctness and performance stage.
