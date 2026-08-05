# Sharing Deck — Slide Transcripts

Per-slide speaking scripts for [`../expert-briefing.tex`](../expert-briefing.tex).
Numbering matches the Beamer source comments (`% 1` … `% 39`).

## Languages

| Locale | Path | Notes |
|---|---|---|
| **English** | [`en/slide-NN.md`](en/) | Source of truth for wording |
| **Traditional Chinese** | [`zh-TW/slide-NN.md`](zh-TW/) | Presenter script; regenerate after English edits |

```bash
# After editing English transcripts (or when slides change):
python3 publish/translate_transcripts.py           # all slides
python3 publish/translate_transcripts.py --slides 12 24 25   # subset
```

Pipeline: English → MT (zh-CN via `publish/translate.py` + glossary) → OpenCC `s2twp` → `zh-TW/`.
Polish spoken phrasing in `zh-TW/` when a slide is presentation-critical.

## Maintainer rules

(See `.cursor/skills/survey/SKILL.md`.)

1. Whenever `expert-briefing.tex` changes, update matching **`en/slide-NN.md` and `zh-TW/slide-NN.md`** (and this index if titles/order change) **in the same commit**.
2. Prefer: edit English first → `python3 publish/translate_transcripts.py --slides …` → polish zh-TW if needed.
3. Layout: **no overlapping boxes/arrows**; content must **fit one 16:9 slide**; **refine** (build → inspect PDF → fix) until clean before push.

Presenter notes that are **intentionally spoken but not shown** on slides:
- **Slide 2 (Agenda):** Weight prediction → blockers → technical techniques → trends; contract = diagrams/checkpoints first.

| Slide | EN | ZH-TW | Title |
| --- | --- | --- | --- |
| 1 | [`en/slide-01.md`](en/slide-01.md) | [`zh-TW/slide-01.md`](zh-TW/slide-01.md) | plain / 開場 |
| 2 | [`en/slide-02.md`](en/slide-02.md) | [`zh-TW/slide-02.md`](zh-TW/slide-02.md) | Agenda |
| 3 | [`en/slide-03.md`](en/slide-03.md) | [`zh-TW/slide-03.md`](zh-TW/slide-03.md) | Trend backdrop --- two stacks converging |
| 4 | [`en/slide-04.md`](en/slide-04.md) | [`zh-TW/slide-04.md`](zh-TW/slide-04.md) | Six active trends |
| 5 | [`en/slide-05.md`](en/slide-05.md) | [`zh-TW/slide-05.md`](zh-TW/slide-05.md) | Keep substrate, change control plane |
| 6 | [`en/slide-06.md`](en/slide-06.md) | [`zh-TW/slide-06.md`](zh-TW/slide-06.md) | Executive verdict |
| 7 | [`en/slide-07.md`](en/slide-07.md) | [`zh-TW/slide-07.md`](zh-TW/slide-07.md) | Four agent jobs --- architecture spine |
| 8 | [`en/slide-08.md`](en/slide-08.md) | [`zh-TW/slide-08.md`](zh-TW/slide-08.md) | Architecture --- Target Stack |
| 9 | [`en/slide-09.md`](en/slide-09.md) | [`zh-TW/slide-09.md`](zh-TW/slide-09.md) | Architecture evolution --- component changes |
| 10 | [`en/slide-10.md`](en/slide-10.md) | [`zh-TW/slide-10.md`](zh-TW/slide-10.md) | Data plane --- ~6--7 abstraction bands (not one) |
| 11 | [`en/slide-11.md`](en/slide-11.md) | [`zh-TW/slide-11.md`](zh-TW/slide-11.md) | One universal cost model? --- No (Horizon A) |
| 12 | [`en/slide-12.md`](en/slide-12.md) | [`zh-TW/slide-12.md`](zh-TW/slide-12.md) | What ships / does not by 2028 |
| 13 | [`en/slide-13.md`](en/slide-13.md) | [`zh-TW/slide-13.md`](zh-TW/slide-13.md) | Roadmap Checkpoints --- when the prediction changes |
| 14 | [`en/slide-14.md`](en/slide-14.md) | [`zh-TW/slide-14.md`](zh-TW/slide-14.md) | Checkpoint C1 --- heuristics vs neural advisors |
| 15 | [`en/slide-15.md`](en/slide-15.md) | [`zh-TW/slide-15.md`](zh-TW/slide-15.md) | Checkpoints C2 + C5 --- gains \& default path |
| 16 | [`en/slide-16.md`](en/slide-16.md) | [`zh-TW/slide-16.md`](zh-TW/slide-16.md) | Checkpoints C3 / C6 / C9 / C10 --- interface width \& scope |
| 17 | [`en/slide-17.md`](en/slide-17.md) | [`zh-TW/slide-17.md`](zh-TW/slide-17.md) | Commercial blockers --- top 5 |
| 18 | [`en/slide-18.md`](en/slide-18.md) | [`zh-TW/slide-18.md`](zh-TW/slide-18.md) | Blocker 1 --- Oracles for money |
| 19 | [`en/slide-19.md`](en/slide-19.md) | [`zh-TW/slide-19.md`](zh-TW/slide-19.md) | Blocker 2 --- Cost, replay, when may the agent run? |
| 20 | [`en/slide-20.md`](en/slide-20.md) | [`zh-TW/slide-20.md`](zh-TW/slide-20.md) | Blocker 3 --- Agent$\leftrightarrow$compiler contract |
| 21 | [`en/slide-21.md`](en/slide-21.md) | [`zh-TW/slide-21.md`](zh-TW/slide-21.md) | Blocker 4 --- Distributional production evidence |
| 22 | [`en/slide-22.md`](en/slide-22.md) | [`zh-TW/slide-22.md`](zh-TW/slide-22.md) | Blocker 5 --- Ownership, security, human review |
| 23 | [`en/slide-23.md`](en/slide-23.md) | [`zh-TW/slide-23.md`](zh-TW/slide-23.md) | Gap map --- what blocks the prediction, not a wishlist |
| 24 | [`en/slide-24.md`](en/slide-24.md) | [`zh-TW/slide-24.md`](zh-TW/slide-24.md) | Cross-Cutting Research Agenda |
| 25 | [`en/slide-25.md`](en/slide-25.md) | [`zh-TW/slide-25.md`](zh-TW/slide-25.md) | Technical Prediction --- Accelerate The Roadmap (T1--T10) |
| 26 | [`en/slide-26.md`](en/slide-26.md) | [`zh-TW/slide-26.md`](zh-TW/slide-26.md) | Technical Prediction --- Within The Compiler (T1--T5) |
| 27 | [`en/slide-27.md`](en/slide-27.md) | [`zh-TW/slide-27.md`](zh-TW/slide-27.md) | Technical Prediction --- Outside The Compiler (T6--T10) |
| 28 | [`en/slide-28.md`](en/slide-28.md) | [`zh-TW/slide-28.md`](zh-TW/slide-28.md) | Technical Prediction --- What Each Checkpoint Needs |
| 29 | [`en/slide-29.md`](en/slide-29.md) | [`zh-TW/slide-29.md`](zh-TW/slide-29.md) | Technical Prediction --- Critical Missing Parts Now |
| 30 | [`en/slide-30.md`](en/slide-30.md) | [`zh-TW/slide-30.md`](zh-TW/slide-30.md) | Org Adoption Questions |
| 31 | [`en/slide-31.md`](en/slide-31.md) | [`zh-TW/slide-31.md`](zh-TW/slide-31.md) | Working stance until conflicts settle |
| 32 | [`en/slide-32.md`](en/slide-32.md) | [`zh-TW/slide-32.md`](zh-TW/slide-32.md) | Commercial checklist --- handout |
| 33 | [`en/slide-33.md`](en/slide-33.md) | [`zh-TW/slide-33.md`](zh-TW/slide-33.md) | Discussion |
| 34 | [`en/slide-34.md`](en/slide-34.md) | [`zh-TW/slide-34.md`](zh-TW/slide-34.md) | Appendix divider |
| 35 | [`en/slide-35.md`](en/slide-35.md) | [`zh-TW/slide-35.md`](zh-TW/slide-35.md) | Appendix --- evidence map |
| 36 | [`en/slide-36.md`](en/slide-36.md) | [`zh-TW/slide-36.md`](zh-TW/slide-36.md) | Appendix --- Tier A commercial signals |
| 37 | [`en/slide-37.md`](en/slide-37.md) | [`zh-TW/slide-37.md`](zh-TW/slide-37.md) | Appendix --- Tier A open repositories |
| 38 | [`en/slide-38.md`](en/slide-38.md) | [`zh-TW/slide-38.md`](zh-TW/slide-38.md) | Appendix --- prediction-critical digests ($\bigstar$) |
| 39 | [`en/slide-39.md`](en/slide-39.md) | [`zh-TW/slide-39.md`](zh-TW/slide-39.md) | Appendix --- publication groups |
