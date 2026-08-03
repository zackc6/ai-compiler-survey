#!/usr/bin/env python3
"""Build a graph-heavy PowerPoint deck from the living survey (English)."""

from __future__ import annotations

import re
from collections import Counter
from datetime import date
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "out"
PPTX_NAME = "next-gen-ai-compiler-survey.pptx"

# Visual system — avoid purple/cream AI clichés; cool ink + teal accent.
INK = RGBColor(0x14, 0x1C, 0x24)
TEAL = RGBColor(0x0F, 0x6E, 0x6E)
AMBER = RGBColor(0xC4, 0x7B, 0x2C)
SLATE = RGBColor(0x3D, 0x4A, 0x55)
MUTED = RGBColor(0x6B, 0x78, 0x84)
SOFT = RGBColor(0xE8, 0xEE, 0xF0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SERIES = [
    RGBColor(0x0F, 0x6E, 0x6E),
    RGBColor(0xC4, 0x7B, 0x2C),
    RGBColor(0x2F, 0x5D, 0x8C),
    RGBColor(0x8B, 0x45, 0x3F),
    RGBColor(0x4A, 0x6B, 0x4A),
    RGBColor(0x6B, 0x78, 0x84),
]


def _set_run(run, size=18, bold=False, color=INK, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def add_title_bar(slide, title: str, subtitle: str | None = None):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.9)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = INK
    bar.line.fill.background()
    tf = bar.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    _set_run(run, 22, True, WHITE, "Calibri")
    if subtitle:
        box = slide.shapes.add_textbox(Inches(0.4), Inches(0.95), Inches(12.5), Inches(0.35))
        p = box.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = subtitle
        _set_run(run, 12, False, MUTED)


def blank_slide(prs: Presentation):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank


def style_chart(chart, has_legend=True):
    chart.has_legend = has_legend
    if has_legend:
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
    plot = chart.plots[0]
    plot.has_data_labels = False
    # Color series when possible
    try:
        for i, series in enumerate(chart.series):
            series.format.fill.solid()
            series.format.fill.fore_color.rgb = SERIES[i % len(SERIES)]
    except Exception:
        pass


def add_chart(slide, chart_type, left, top, width, height, categories, series_map, legend=True):
    data = CategoryChartData()
    data.categories = categories
    for name, values in series_map.items():
        data.add_series(name, values)
    chart = slide.shapes.add_chart(
        chart_type, left, top, width, height, data
    ).chart
    style_chart(chart, has_legend=legend)
    return chart


def parse_index():
    idx = (ROOT / "publications" / "INDEX.md").read_text(encoding="utf-8")
    groups, kinds, years = Counter(), Counter(), Counter()
    for line in idx.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        year, kind, group = cols[0], cols[1], cols[2]
        if year in {"Year", "---"} or year.startswith("---"):
            continue
        if not (
            re.match(r"^\d", year)
            or year.endswith("+")
            or year in {"ongoing", "2010s+", "2025/26"}
        ):
            continue
        groups[group] += 1
        kinds[kind] += 1
        # Normalize year buckets for chart
        y = year
        if year.endswith("+") or year in {"ongoing", "2010s+", "2025/26"}:
            y = "other/ongoing"
        elif year.isdigit() and int(year) < 2023:
            y = "≤2022"
        years[y] += 1
    return groups, kinds, years


def slide_title(prs):
    s = blank_slide(prs)
    bg = s.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = INK
    bg.line.fill.background()
    accent = s.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(5.9), Inches(13.333), Inches(0.12)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = TEAL
    accent.line.fill.background()
    box = s.shapes.add_textbox(Inches(0.7), Inches(2.0), Inches(12), Inches(2.2))
    tf = box.text_frame
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = "Next-Generation AI Compiler Survey"
    _set_run(r, 36, True, WHITE)
    p2 = tf.add_paragraph()
    r2 = p2.add_run()
    r2.text = "Agentic compiler prediction · stack reshape · HW–SW codesign"
    _set_run(r2, 18, False, RGBColor(0xB8, 0xC4, 0xCC))
    foot = s.shapes.add_textbox(Inches(0.7), Inches(6.3), Inches(12), Inches(0.6))
    p = foot.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = f"Living survey export · {date.today().isoformat()} · graphs from CLAIMS / ROADMAP / INDEX"
    _set_run(r, 12, False, MUTED)


def slide_north_star(prs):
    s = blank_slide(prs)
    add_title_bar(s, "North star architecture", "Hybrid agent control plane over classical data plane")
    layers = [
        (0.5, 1.6, 12.3, 1.5, TEAL, "Agent control plane",
         "(a) online specialize   (b) offline heuristic evolve\n"
         "(c) oracle engineering / review   (d) ASIC bring-up / codesign"),
        (0.5, 3.4, 12.3, 1.3, SLATE, "Classical data plane",
         "Inductor / XLA / MLIR / Triton / Helion / Tile → device libraries\n"
         "legality · lowering · OpInfo / Alive2 / benchmarks · fallback"),
        (0.5, 5.0, 12.3, 1.2, AMBER, "HW codesign feedback (not autonomous tape-out)",
         "sim + silicon traces → ISA / dialect / memory-system RFCs"),
    ]
    for left, top, w, h, color, title, body in layers:
        shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        _set_run(r, 16, True, WHITE)
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = body
        _set_run(r2, 12, False, WHITE)


def slide_era_timeline(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Era timeline — intensity of LLM/agent involvement", "Qualitative index 0–5 (survey synthesis, not a benchmark)")
    cats = ["2018–22\nDL compilers", "2020–23\nMLGO / RL gyms", "2023–24\nLLM on IR", "2025–26\nAgentic hybrid", "2027–28\nCI-gated agents", "2029–31\nMulti-HW default"]
    vals = [1, 2, 3, 5, 4, 5]
    add_chart(
        s, XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.4),
        cats, {"Agent/LLM role intensity": vals}, legend=False,
    )


def slide_agent_jobs(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Four agent jobs — relative emphasis in Tier A map", "Share of survey attention across jobs (illustrative weights)")
    add_chart(
        s, XL_CHART_TYPE.DOUGHNUT,
        Inches(0.4), Inches(1.4), Inches(6.5), Inches(5.5),
        ["(a) Online specialize", "(b) Offline heuristics", "(c) Oracle review", "(d) Bring-up / codesign"],
        {"Jobs": [34, 22, 16, 28]},
    )
    # Side cards
    cards = [
        ("(a) Online", "CompileIQ, GEAK, AutoKernel, ACCLAIM"),
        ("(b) Offline", "Magellan, AlphaEvolve / OpenEvolve"),
        ("(c) Review", "Archer, Alive2 / opt oracles"),
        ("(d) Codesign", "TritorX, KernelEvolve, Ascend diagnosis"),
    ]
    for i, (t, b) in enumerate(cards):
        top = 1.5 + i * 1.25
        box = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(top), Inches(5.5), Inches(1.1)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = SOFT
        box.line.color.rgb = TEAL
        tf = box.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = t
        _set_run(r, 14, True, TEAL)
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = b
        _set_run(r2, 11, False, SLATE)


def slide_tiers(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Evidence tiers — how sources feed the prediction", "Prefer A; B is substrate; C is demoted noise")
    add_chart(
        s, XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.5), Inches(1.5), Inches(7.2), Inches(5.4),
        ["Tier A\nreshape compile", "Tier B\nsubstrate", "Tier C\ndelivery only"],
        {"Role weight in prediction": [70, 25, 5]},
        legend=False,
    )
    note = s.shapes.add_textbox(Inches(8.0), Inches(2.0), Inches(4.8), Inches(4.5))
    tf = note.text_frame
    tf.word_wrap = True
    bullets = [
        "A — TritorX, KernelEvolve, Magellan, ACCLAIM, GEAK, CompileIQ, Archer, mlirAgent (−)",
        "B — llvm-project, Helion, StableHLO, Triton, PyTorch Inductor",
        "C — generic Gerrit/SCM chat without compiler oracles",
        "Rule: grow A, keep B thin, do not catalog C",
    ]
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = "• " + b
        _set_run(r, 12, False, SLATE)


def slide_claims_status(prs):
    s = blank_slide(prs)
    add_title_bar(s, "CLAIMS.md status mix", "Architecture / process / codesign claims")
    # Counts from CLAIMS
    statuses = ["Supported", "Contested", "Watch"]
    arch = [3, 1, 0]   # A1 A2 A3 A5 supported; A4 contested
    # recount properly: A1-5: S,S,S,C,S → S4 C1; P/S: P1 C, P2 W, P3 S, S1 S, S4 S, S5 W → S3 C1 W2; H: S,S,S → S3
    # Better aggregate all:
    # Supported: A1,A2,A3,A5,P3,S1,S4,H1,H2,H3 = 10
    # Contested: A4,P1 = 2
    # Watch: P2,S5 = 2
    add_chart(
        s, XL_CHART_TYPE.COLUMN_STACKED,
        Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.4),
        ["Architecture (A*)", "Process/Stack (P*/S*)", "Codesign (H*)"],
        {
            "Supported": [4, 3, 3],
            "Contested": [1, 1, 0],
            "Watch": [0, 2, 0],
        },
    )


def slide_conflicts(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Open conflicts C1–C10 — settlement urgency", "Higher = more blocking for 2027–28 roadmap confidence")
    cats = [f"C{i}" for i in range(1, 11)]
    # Qualitative urgency scores
    urgency = [5, 5, 4, 4, 3, 3, 2, 2, 5, 3]
    add_chart(
        s, XL_CHART_TYPE.LINE_MARKERS,
        Inches(0.4), Inches(1.4), Inches(8.2), Inches(5.5),
        cats, {"Settlement urgency (1–5)": urgency}, legend=False,
    )
    box = s.shapes.add_textbox(Inches(8.8), Inches(1.6), Inches(4.2), Inches(5.2))
    tf = box.text_frame
    tf.word_wrap = True
    labels = [
        "C1 Magellan vs MLGO",
        "C2 Vendor wins vs benches",
        "C3 Free rewrite vs advisory",
        "C4 Triton vs Tile multi-DSL",
        "C5 Online vs offline agents",
        "C6 Replace vs control plane",
        "C7 Generic vs oracle review",
        "C8 DL compile vs AI-for-LLVM",
        "C9 Coverage vs peak bring-up",
        "C10 Codesign vs auto tape-out",
    ]
    for i, lab in enumerate(labels):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = lab
        _set_run(r, 11, False, SLATE)


def slide_stack_layers(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Stack layers — agent pressure by layer", "Where agentic compile changes the job (0–10)")
    cats = [
        "1 Framework", "2 Kernel DSL", "3 Portable IR", "4 Mid/back",
        "5 Oracles", "6 Artifacts", "7 Serving", "8 Silicon/sim",
    ]
    vals = [7, 9, 6, 8, 9, 8, 7, 8]
    add_chart(
        s, XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.4),
        cats, {"Agent pressure": vals}, legend=False,
    )


def slide_roadmap_confidence(prs):
    s = blank_slide(prs)
    add_title_bar(s, "5-year predicted shifts — confidence", "From ROADMAP Horizon B")
    cats = [
        "Default path\nstays classical",
        "Artifact store\nin VCS",
        "Hetero serving\nvia agents",
        "HW codesign\nfeedback loop",
        "Verification\ncompose",
        "Humans own\noracles",
        "No auto\ntape-out",
    ]
    # map High=3, Med-high=2.5, Medium=2
    conf = [2.5, 3, 2.5, 2, 2, 3, 3]
    add_chart(
        s, XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.4),
        cats, {"Confidence (1–3)": conf}, legend=False,
    )


def slide_index_groups(prs, groups: Counter):
    s = blank_slide(prs)
    add_title_bar(s, "Bibliography mix — digests by group", f"n={sum(groups.values())} digests in publications/INDEX.md")
    items = groups.most_common()
    cats = [g if len(g) < 28 else g[:25] + "…" for g, _ in items]
    vals = [n for _, n in items]
    add_chart(
        s, XL_CHART_TYPE.BAR_CLUSTERED,
        Inches(0.4), Inches(1.4), Inches(12.5), Inches(5.6),
        cats, {"Digests": vals}, legend=False,
    )


def slide_index_kinds_years(prs, kinds: Counter, years: Counter):
    s = blank_slide(prs)
    add_title_bar(s, "Source kinds & year mix", "What the living bibliography is made of")
    add_chart(
        s, XL_CHART_TYPE.PIE,
        Inches(0.3), Inches(1.4), Inches(6.2), Inches(5.5),
        list(kinds.keys()), {"Kind": list(kinds.values())},
    )
    # year order
    order = ["≤2022", "2023", "2024", "2025", "2026", "other/ongoing"]
    ycats = [y for y in order if y in years]
    yvals = [years[y] for y in ycats]
    add_chart(
        s, XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(6.8), Inches(1.4), Inches(6.0), Inches(5.5),
        ycats, {"Digests / year bucket": yvals}, legend=False,
    )


def slide_reported_speedups(prs):
    s = blank_slide(prs)
    add_title_bar(
        s,
        "Author-reported headlines (NOT cross-benchmark)",
        "Mechanisms matter more than bars — see CONFLICTS C2",
    )
    cats = [
        "ACCLAIM\nvs -O3",
        "AutoKernel\nRMSNorm",
        "KForge Arc\nKB-L2",
        "Ascend diag.\ngeo-mean",
        "Helion B200\nvs eager",
        "CompileIQ\nhot kernels",
        "CompileIQ\nhighly tuned",
    ]
    # Convert to percent-ish comparable display: use speedup factor
    vals = [1.25, 5.29, 5.13, 4.35, 3.27, 1.15, 1.025]
    add_chart(
        s, XL_CHART_TYPE.COLUMN_CLUSTERED,
        Inches(0.5), Inches(1.5), Inches(12.3), Inches(5.0),
        cats, {"Reported factor vs baseline": vals}, legend=False,
    )
    note = s.shapes.add_textbox(Inches(0.5), Inches(6.6), Inches(12.3), Inches(0.5))
    p = note.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Different suites, hardware, and baselines — do not rank systems from this chart alone."
    _set_run(r, 11, True, AMBER)


def slide_codesign_ladder(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Codesign ladder (C9)", "Coverage-first then peak-perf — still agentic compiler")
    steps = [
        ("1. Spec / sim", "ISA docs + QEMU/\nfuture-device sim"),
        ("2. Coverage", "TritorX-class\nATen / OpInfo"),
        ("3. Perf search", "KernelEvolve /\nGEAK / AutoKernel"),
        ("4. Serve", "e2e latency /\nTCO gates"),
        ("5. Feedback", "traces → next\nISA / dialect RFC"),
    ]
    for i, (t, b) in enumerate(steps):
        left = 0.4 + i * 2.55
        shape = s.shapes.add_shape(
            MSO_SHAPE.CHEVRON if i < 4 else MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(2.5), Inches(2.4), Inches(2.2),
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = TEAL if i % 2 == 0 else SLATE
        shape.line.fill.background()
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = t
        _set_run(r, 14, True, WHITE)
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = b
        _set_run(r2, 11, False, WHITE)
        p2.alignment = PP_ALIGN.CENTER
    foot = s.shapes.add_textbox(Inches(0.5), Inches(5.3), Inches(12.3), Inches(1.2))
    tf = foot.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = (
        "C10 stance: agents stress toolchains and file ISA/IR pain; humans + EDA own tape-out. "
        "Do not expand this survey into autonomous chip design."
    )
    _set_run(r, 13, False, SLATE)


def slide_online_offline(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Online vs offline control (C5)", "Both stick; different artifacts and cost models")
    add_chart(
        s, XL_CHART_TYPE.RADAR_MARKERS,
        Inches(0.3), Inches(1.3), Inches(7.0), Inches(5.7),
        ["Latency sensitivity", "Ship as C++/ACF", "Per-workload adapt", "Reviewability", "Token/$ cost", "CI default readiness"],
        {
            "Online (a)": [5, 2, 5, 3, 4, 3],
            "Offline (b)": [2, 5, 2, 5, 3, 4],
        },
    )
    box = s.shapes.add_textbox(Inches(7.5), Inches(2.0), Inches(5.3), Inches(4.5))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate([
        "Online artifacts: pass lists, hints, kernels, ACFs, traces",
        "Offline artifacts: evolved heuristics, MLGO features, datasets",
        "Engineering (c) and bring-up (d) span both clocks",
        "Settlement: which shows up as default flag / CI job",
    ]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r = p.add_run()
        r.text = "• " + line
        _set_run(r, 13, False, SLATE)


def slide_falsifiers(prs):
    s = blank_slide(prs)
    add_title_bar(s, "What would falsify the prediction", "From SURVEY §5.3 + ROADMAP non-goals")
    items = [
        ("Default agent lowering", "A major stack ships default lowering with no classical admit/fallback and sustained correctness."),
        ("Both heuristic paths die", "Magellan-class synthesis and MLGO advisors both disappear from production."),
        ("Kernel agents plateau", "Fusion-heavy public suites stay below eager forever with only library workarounds."),
        ("Autonomous tape-out", "Production microarch primarily agent-proposed and validated only via agentic compile oracles."),
    ]
    for i, (t, b) in enumerate(items):
        top = 1.4 + i * 1.35
        shape = s.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(top), Inches(12.3), Inches(1.2)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = SOFT
        shape.line.color.rgb = AMBER
        tf = shape.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = t
        _set_run(r, 14, True, AMBER)
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = b
        _set_run(r2, 12, False, SLATE)


def slide_takeaways(prs):
    s = blank_slide(prs)
    add_title_bar(s, "Takeaways", "One-page success check")
    points = [
        "Predicted architecture: agentic control plane + classical data plane (+ codesign feedback).",
        "Four jobs: online · offline heuristics · oracle review · ASIC bring-up/codesign.",
        "Evidence vs noise: Tier A/B/C — demote generic SCM AI; keep negative results.",
        "Conflicts C1–C10 are features: do not average Magellan/MLGO or vendor/bench ceilings.",
        "Roadmap 2027–28: CI-gated specialize + bring-up ladder; not LLM-as-opt; not auto tape-out.",
        "Rebuild: python3 publish/build_pdf.py && python3 publish/build_pptx.py",
    ]
    for i, text in enumerate(points):
        top = 1.35 + i * 0.9
        num = s.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(0.5), Inches(top), Inches(0.55), Inches(0.55)
        )
        num.fill.solid()
        num.fill.fore_color.rgb = TEAL
        num.line.fill.background()
        tf = num.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = str(i + 1)
        _set_run(r, 14, True, WHITE)
        box = s.shapes.add_textbox(Inches(1.3), Inches(top), Inches(11.5), Inches(0.7))
        p = box.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = text
        _set_run(r, 14, False, INK)


def build() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    groups, kinds, years = parse_index()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide_title(prs)
    slide_north_star(prs)
    slide_era_timeline(prs)
    slide_agent_jobs(prs)
    slide_tiers(prs)
    slide_claims_status(prs)
    slide_conflicts(prs)
    slide_stack_layers(prs)
    slide_roadmap_confidence(prs)
    slide_index_groups(prs, groups)
    slide_index_kinds_years(prs, kinds, years)
    slide_reported_speedups(prs)
    slide_online_offline(prs)
    slide_codesign_ladder(prs)
    slide_falsifiers(prs)
    slide_takeaways(prs)

    out = OUT / PPTX_NAME
    prs.save(str(out))
    return out


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path} ({path.stat().st_size // 1024} KiB)")
