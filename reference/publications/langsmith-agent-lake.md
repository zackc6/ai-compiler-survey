# The Agent Lake (LangChain / LangSmith)

| Field | Value |
|---|---|
| **Year** | 2026 (24 November 2026) |
| **Org** | LangChain (LangSmith product line); author Sam Crowder |
| **Publisher** | LangChain blog |
| **Type** | company |
| **Group** | Agent control-plane substrate |
| **Link** | [The Agent Lake](https://www.langchain.com/blog/the-agent-lake) |
| **Also** | [Introducing SmithDB](https://www.langchain.com/blog/introducing-smithdb) · [Introducing LangSmith Engine](https://www.langchain.com/blog/introducing-langsmith-engine) · [SmithTune fine-tuning](https://www.langchain.com/blog/langsmith-fine-tuning) · [Insights docs](https://docs.langchain.com/langsmith/insights) · [decision models docs](https://docs.langchain.com/langsmith/llm-gateway-decision-models) (linked, not read) |
| **Evidence tier** | **B** — a shipping vendor platform for the *data side* of an agent improvement loop (trace and outcome store, trace classification, scheduled failure clustering, fix proposals checked against an eval set, fine-tuning on selected trajectories); adjacent infrastructure for the controller-improvement loop, not evaluated on compiler or kernel work, and its one benchmark is internal and unspecified |
| **Version / reviewed** | Blog post dated 24 November 2026, read 26 November 2026 (single fetch of the post; the linked SmithDB, Engine and SmithTune posts were not read). No repository: SmithDB, Engine, SmithTune and Insights are closed LangSmith features. |

## Key contributions

The post names a product category, an **agent lake**: a store built for agent *traces* (every step of a run, from user input through model and tool calls to output; multi-turn runs grouped as *threads*) and *outcomes*, with "intelligent compute" running over that corpus. Outcomes are attached to traces one-to-one (a thumbs-down, a low conversation score) or many-to-many (for coding agents, a merged pull request), and come from direct user feedback, observed system events, LLM-as-a-judge proxies, and hand labels in annotation queues. The argument is that general data lakes (the post names Snowflake and Databricks) lack storage and compute shaped for this data.

The compute layer has two jobs: finding the traces that matter, and automating the improvement loop. The named pieces are online evaluators (stock prompts for hallucination, toxicity and satisfaction), cheaper *decision models* for trace classification instead of full LLM-as-a-judge, natural-language trace search, Insights (clustering traces into categories and assigning new ones as they arrive), **LangSmith Engine** (scans traces on a schedule, groups recurring failures into issues, uses evaluator scores and feedback to choose where to look, diagnoses a root cause and, with a repository connected, proposes a fix as a pull request; since Engine v2 it can test that fix against an eval set before a human sees it), and **SmithTune** (fine-tunes a model on the agent's best trajectories and compares it with the base model, offered for when "an agent keeps making the same mistakes after its harness has been tuned").

## Summary

Demonstrated, per the vendor: a production trace store and the features above, at volume. Claimed, not measured in the post: that SmithDB is "the industry's most performant database" for real-time workloads on trace data, that the loop should and can be automated, and that the value lies in the compute over traces rather than in the traces. The post is a product announcement ending in a call to try LangSmith.

## Key takeaways

- **Volumes (vendor-reported, no exact figures):** traces "from billions of agent runs per month"; one customer (Clay) sends "hundreds of millions of events per day"; Engine "has analyzed more than 60 million production traces".
- **The one benchmark:** on "a subset of IssueBench", LangChain's internal benchmark for detecting and grouping issues in traces, a Kimi K3 model fine-tuned with SmithTune on trajectories from one of Engine's agents scored 96, base Kimi K3 90, GPT-5.6 Sol 87. The subset size, task count, scoring rule, number of runs and variance are not given. The measured object is *trace triage quality*, not the improvement of any agent's task outcome.
- **No performance, cost or before/after outcome numbers** for any customer agent improved by Engine fixes or SmithTune. Decision models are called "affordable" with no price; LLM-as-a-judge evaluation is called "expensive", and low-cost online evaluation "an active area of research".
- **Nothing about compilers, kernels or performance optimization.** Code appears only as coding agents scored by merged pull requests and as Engine's proposed fixes.

## Why it matters for this survey

It is the clearest shipping example of the data plane that the survey's controller-improvement loop assumes: retained trajectories with outcomes attached, failure clustering, proposed controller changes, a pre-review eval check, and fine-tuning on selected runs. For an agentic compiler the analogous corpus would be optimization campaigns (candidates, compile and validation verdicts, measured runtimes, rejected attempts) with outcomes such as accepted kernels or end-to-end regressions. It therefore informs two design questions: how trajectories are retained and labelled for reuse (the trajectory-reuse row of the design checklist), and how a proposed controller change is checked before promotion.

It also makes a specific risk concrete. Engine tests a fix "against an eval set" built from the same production traces it mined for the failure, and SmithTune selects "best trajectories" by the same evaluators that score the result. That is the selection-set reuse the 2026 attribution study measured for Meta-Harness, SkillOpt and AHE (about half of significant search-set gains attributable to task-set fitting), and the reason the survey keeps final tasks and detailed results outside proposer access. An agentic-compiler controller built on such a store needs a held-out evaluation the proposer never reads.

Placement: same category as [DeepSeek Harness](deepseek-harness.md) and [SKILL.state](skill-state.md) (runtime and state infrastructure), and adjacent to [GEPA](gepa.md) (trace-driven prompt evolution) on the improvement side. No shared lineage with those systems. It does not count toward any forecast predicate: it is neither a compiler integration nor a controller-improvement measurement on compiler work.

## Limits / caveats

- Vendor blog; the only quantitative result is an internal benchmark subset with no protocol, and it measures trace triage, not agent improvement.
- No evidence that Engine's fixes or SmithTune's fine-tunes improve the agents they target, under any matched comparison, or how often proposed fixes are rejected or regress.
- Pre-review eval checks drawn from the mined traces are not held-out evaluation; treat them as development-set results.
- Closed platform; the linked SmithDB, Engine and SmithTune posts and documentation were not read for this digest.
- **Experiment that would make it Tier A for this survey:** store a kernel-optimization campaign's trajectories in such a system, let the automated loop propose controller changes, and compare the changed and fixed controllers on held-out kernels at a matched budget, reporting runtime, cost, rejected proposals and regressions.
