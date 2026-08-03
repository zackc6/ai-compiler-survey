# Stronger AI PowerPoint tools (if python-pptx still feels thin)

`publish/build_pptx.py` is good for **reproducible, survey-synced** decks in-repo. For **design polish**, these tools are usually stronger:

| Tool | Strength | Best for |
|---|---|---|
| **[Gamma](https://gamma.app)** | Fast, modern layouts from a prompt/outline | Narrative decks from SURVEY §0.1 + §5 + ROADMAP |
| **[Beautiful.ai](https://www.beautiful.ai)** | Smart templates that reflow as you edit | Exec readout of four jobs + roadmap |
| **[Tome](https://tome.app)** | Story-first generative slides | Vision / north-star storytelling |
| **[Plus AI](https://plusai.com)** (Google Slides / PPT add-on) | Works inside existing corporate slide stacks | Editing our `.pptx` further |
| **[Pitch](https://pitch.com)** | Team design system + AI assist | Polished stakeholder versions |
| **[Decktopus](https://www.decktopus.com)** | One-shot AI decks | Quick external share |
| **[SlideSpeak](https://slidespeak.co)** | Doc → slides | Drop in `survey-bundle.md` / PDF |
| **[NotebookLM](https://notebooklm.google.com) → slide / briefing** | Grounded on uploaded survey PDFs | Source-faithful briefings (then restyle) |

## Recommended workflow for this survey

1. Keep generating the **outline + facts** here: `python3 publish/build_pptx.py`
2. Paste the **one-page check + four jobs + C1/C2/C9/C10** into **Gamma** or **Beautiful.ai** for visual polish
3. Or upload `publish/out/next-gen-ai-compiler-survey.en.pdf` to **SlideSpeak / NotebookLM** and restyle
4. Re-sync numbers from `CLAIMS.md` / `INDEX.md` whenever evidence moves

## Prompt starter (Gamma / Beautiful.ai)

```text
Create a 12–14 slide editorial presentation (not a dashboard) titled
"The next compiler is agentic — not replaced."

Use a paper background, deep ink typography, one copper accent. No purple gradients.

Slides:
1. Title + north star quote
2. Thesis: agents search / compilers decide
3. Hard limit: free IR rewrite fails (mlirAgent)
4. Architecture: control / data / codesign planes
5. Four agent jobs (a–d) with example systems
6. Era timeline 2018→2026
7. Six stealable ideas
8. Stack pressure layers
9. Conflicts C1, C2, C3, C9, C10 as productive tension
10. Codesign ladder coverage→perf→feedback
11. 2027–28 ships vs will-not
12. Org adoption questions
13. Closing one-page check

Tone: technical, calm, prediction-first. Prefer mechanisms over speedup charts.
```
