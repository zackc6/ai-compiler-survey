# Better visualization & PPT tools (beyond in-repo generators)

Honest take: `publish/build_pptx.py` and `publish/build_visual.py` are for **reproducible, survey-synced** drafts in git. They will not beat dedicated design tools. Use this repo for **facts + outline**; use the tools below for **looks**.

---

## Recommended split for this survey

| Job | Prefer | Why |
|---|---|---|
| Facts / conflicts / claims stay correct | This repo PDF + digests | Source of truth |
| Stakeholder / pretty deck | **Gamma** (first draft) → polish | Fastest good-looking narrative |
| Must ship editable PPTX in corp brand | **Plus AI** (PowerPoint / Google Slides) or **Beautiful.ai** | Native templates, no broken export |
| Grounded on our PDF | **NotebookLM** → briefing/slides, then restyle in Gamma/Plus | Less hallucination of numbers |
| Architecture / orbit / ladder diagrams | **Napkin.ai**, **Eraser.io**, **Whimsical**, **tldraw** / FigJam | Built for diagrams, not bullet slides |
| Publish as scrollable web story | **Gamma** cards / web export | Better than 16:9 grid posters |

**Do not** expect PIL posters or python-pptx to be the final visual language.

---

## AI presentation tools (2026)

| Tool | Best for | Notes |
|---|---|---|
| **[Gamma](https://gamma.app)** | Fast web-first decks; Agent edits | Current default pick for speed + polish. Share as link; PPTX export often needs cleanup. |
| **[Plus AI](https://plusai.com)** | Stay inside PowerPoint / Google Slides | Best when brand masters already exist. |
| **[Beautiful.ai](https://www.beautiful.ai)** | Consistent “consulting” layouts | Smart slides reflow; strong for exec readouts. |
| **[Pitch](https://pitch.com)** | Team brand system + AI assist | Good for multi-person stakeholder decks. |
| **[Microsoft Copilot](https://www.microsoft.com/microsoft-365/copilot)** in PowerPoint | Enterprise M365 | Best if your org already pays for Copilot. |
| **[Canva](https://www.canva.com) Magic Studio** | Visual / marketing-heavy | Fine for posters; weaker for dense technical claims. |
| **[SlideSpeak](https://slidespeak.co)** | Doc/PDF → slides | Drop in `publish/out/next-gen-ai-compiler-survey.pdf`. |
| **[NotebookLM](https://notebooklm.google.com)** | Source-grounded briefing | Upload our PDF; then restyle elsewhere. |
| **[Presentations.ai](https://presentations.ai)** | High-stakes pitch polish | Optional final pass. |
| **[Decktopus](https://www.decktopus.com)** | One-shot AI decks | Quick external share. |

**Deprecated:** **Tome** presentation product was shut down (2025). Prefer Gamma / Plus / Beautiful.ai instead.

---

## Diagram / visualization tools (better than grid posters)

| Tool | Best for | Notes |
|---|---|---|
| **[Napkin.ai](https://napkin.ai)** | Text → clean diagrams | Excellent for “four jobs”, hybrid contract, codesign ladder. |
| **[Eraser.io](https://www.eraser.io)** | Architecture diagrams from prompts/code | Stack / control-plane drawings. |
| **[Whimsical](https://whimsical.com)** | Flowcharts + AI | Conflicts “vs” diagrams, era paths. |
| **[tldraw](https://tldraw.com)** / FigJam | Collaborative sketch → tidy | Fast workshop visuals. |
| **[Excalidraw](https://excalidraw.com)** (+ AI plugins) | Hand-drawn technical feel | Good for open-source aesthetic. |
| **Mermaid / D2 / Graphviz** in docs | Versioned diagrams in git | Keep structure in-repo; style elsewhere. |
| **[Figma](https://www.figma.com)** (+ AI) | Full visual system | Highest ceiling; highest effort. |

---

## Agentic / API-friendly options

| Tool | Role |
|---|---|
| **Gamma Agent / API** (paid tiers) | Conversational refine; some automation into Zapier/Make |
| **Plus AI** inside PPT/Slides | Agent edits on your masters |
| **NotebookLM** | Grounded Q&A → outline for Gamma |
| **Cursor / Claude** → outline only | Generate slide *outline* from `docs/SURVEY.md` §5 / §5.7; paste into Gamma—not raw PIL art |
| **2Slides** (API-oriented) | If you need programmatic deck generation with better templates than python-pptx |

---

## Suggested workflow (this survey)

1. **Source of truth:** edit `docs/SURVEY.md` (§5) / CLAIMS; `python3 publish/build_pdf.py`.
2. **Outline:** ask an agent for a 12–14 slide outline from §0.1, §5, §5.7 (P23 verdict), C1/C2/C9/C10.
3. **Pretty deck:** paste outline into **Gamma** (or Plus AI if PPTX-native is required).
4. **Diagrams:** rebuild key figures in **Napkin** or **Eraser** (hybrid contract, four jobs, freeze→serve, resource envelope)—export PNG/SVG into the deck.
5. **Grounding check:** spot-check speedups and conflict IDs against the PDF / INDEX; never trust the design tool for numbers.

## Prompt starter (Gamma)

```text
Create a 12–14 slide editorial presentation (not a dashboard) titled
"The next compiler is agentic — not replaced."

Visual direction: one composition per slide; deep charcoal or paper;
one amber/steel accent; no purple gradients; no dense grids; no stat strips.
Prefer large diagrammatic ideas over bullet walls.

Must cover:
- Thesis: agents search / compilers decide (hybrid)
- Hard limit: free IR rewrite fails (mlirAgent)
- Four jobs a–d
- Codesign ladder coverage→perf
- Commercialization: typed contract, freeze artifacts, P23
  (tokens/latency/capability shape the SKU; falsify always-on LLM-as-opt)
- Conflicts C1, C2, C3, C9, C10 as tension — do not average
- Closing one-page check

Tone: technical, calm, prediction-first. Mechanisms over speedup charts.
```

## What to keep in this repo

| Artifact | Keep? |
|---|---|
| English PDF | Yes — canonical manuscript |
| Editorial / visual PPTX from python | Optional drafts only |
| PIL posters | Optional; replace key slides with Napkin/Eraser exports when presenting |

Rebuild in-repo decks with `python3 publish/build_pptx.py` / `build_visual.py` only when you need a git-tracked stub—not as the final look.
