# Bootstrapping Conversational Recommendation Agents At Spotify: Synthetic Data Generation and Self-Improvement Loops

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Spotify |
| **Publisher** | RecSys 2026 · arXiv |
| **Type** | paper |
| **Group** | Controller improvement |
| **Link** | [Primary source](https://arxiv.org/abs/2609.30297) |
| **Evidence tier** | C: a production controller-improvement loop with an offline evaluation and an online A/B test, outside compilers |
| **Version / reviewed** | v1, 16 September 2026 (RecSys 2026); arXiv abstract page and the [Spotify Research post](https://research.atspotify.com/2026/9/bootstrapping-conversational-recommendation-agents-at-spotify-synthetic-data-generation-and-self-improvement-loops) listing reviewed by Claude 25 November 2026 |

## Key contributions

Before launch, with no real conversations, Spotify turned single-turn prompts into multi-turn synthetic conversations to test a conversational music-recommendation agent. The self-improvement loop combines **variance-based contrastive optimization** (running a conversation several times and treating inconsistent outcomes as a sign of unstable planning or tool use) with iterative fixes to prompts and tools proposed by a coding agent.

## Summary

The loop was put into production for the recommendation agent.

## Key takeaways

- Offline: **+8%** quality on top of a heavily optimized manual prompt.
- Online A/B test against a prior experience that supported only session refinement: **+14% user listening**, **+5% weekly active users**, **−5% skip rate**.
- A secondary description (not verified against the paper) states that human reviewers rated the synthetic data above 90% on every quality measure, and that each loop round ends in a pull request reviewed by a person plus a full regression evaluation. The abstract page does not show these details.

## Why it matters for this survey

It is the only source in the index where a controller-improvement loop is measured on real users in production. The abstract describes the loop as a coding agent automatically identifying and fixing planning and tool-use errors; it does not state how changes are reviewed before deployment. A secondary account describes a human-gated design (a reviewed pull request and a regression run each round), the deployment shape most plausible for a compiler organization, but that is unverified and is not used in the survey narrative. It belongs with the adoption hypothesis as an existence proof outside compilers, not as compiler evidence.

## Limits / caveats

The online comparison is against an earlier product experience with fewer capabilities, so the A/B gain mixes the new agent with the loop's contribution; the loop's own share is the +8% offline figure. Not compiler or performance work. Details of the human review step are from a secondary account and unverified. Single company.
