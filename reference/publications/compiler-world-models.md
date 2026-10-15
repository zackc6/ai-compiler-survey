# Toward Compiler World Models: Learning Latent Dynamics for Efficient Tensor Program Search

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Institute of Software, Chinese Academy of Sciences · University of Chinese Academy of Sciences (Hangzhou Institute for Advanced Study) |
| **Publisher** | arXiv |
| **Type** | paper |
| **Group** | MLGO & RL gyms |
| **Link** | [arXiv 2606.09312](https://arxiv.org/abs/2606.09312) |
| **Evidence tier** | **B** — a learned evaluator that cuts measurement count in conventional schedule search; no agent, no new search space |
| **Version / reviewed** | v1, 8 June 2026; reviewed 15 October 2026 |

## Key contributions

Schedule search is modeled as action-conditioned latent dynamics: a state encoder maps the initial program to a latent, a lightweight transition model rolls scheduling actions forward in that space, and a ranking model scores the terminal latent with action and hardware features. This avoids repeated AST mutation and code encoding when evaluating candidates. Training data: 10,000 encoder samples, about 391k (CPU) and 396k (GPU) state–action transitions, and 500k (CPU) / 140k (GPU) ranking samples; the paper does not report training compute.

## Summary

On an RTX 4090 and a Xeon Gold 6430 with TVM 0.8, over 103 subgraphs grouped into 22 representative ones from seven models (ResNet-50, BERT-base, MobileNetV2, GPT-2, ResNet18-3D, OPT-1.3B and GPT-Neo-2.7B self-attention): at the same 64-trial budget, **1.37× (GPU) and 1.54× (CPU) lower latency than Ansor**; matches Ansor with 10,000 trials within 2.2% geometric mean using **10× fewer measurements**. Full-model inference: 4.61× over PyTorch and 3.67× over PyTorch with cuDNN, geometric mean.

## Key takeaways

- The gain is search efficiency—fewer hardware measurements for the same result—not a better attainable optimum; the authors state the method improves candidate evaluation, not candidate generation or search-space design.
- Stated limits: latent rollouts accumulate error on long scheduling trajectories; the ranker is trained for within-workload ranking, not calibrated latency.

## Why it matters for this survey

A learned-policy entry for the "several search methods remain competitive" trend and for search economics: a cheaper evaluator inside a conventional autotuner is the same kind of outcome as Helion's cheaper tuning, and should be compared with agent proposals under the same measurement budget. The authors' own caveat—an evaluator cannot find what the search never proposes—is exactly the division of labor the survey's coupling hypothesis asks about.

## Limits / caveats

- Older TVM version and consumer GPU; PyTorch baselines are weaker than library-backed serving stacks.
- Training data volume is substantial and its compute cost is not reported; reuse across hardware generations is untested.
