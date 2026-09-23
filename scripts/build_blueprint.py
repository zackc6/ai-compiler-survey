#!/usr/bin/env python3
"""Build the two architecture figures in docs/SURVEY.md.

Edit this script, not the SVGs. Review both against the narrative when components,
feedback, evaluation boundaries, or promotion rules change. --check verifies file
synchronization, not semantic agreement.
"""
from __future__ import annotations
from html import escape
from math import hypot
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
STYLE = '''<style>
text{font-family:"IBM Plex Sans",Arial,"Liberation Sans",sans-serif;fill:#182838}
.title{font-size:25px;font-weight:700}
.heading{font-size:18px;font-weight:700}
.smallhead{font-size:16px;font-weight:700}
.body{font-size:16px}
.note{font-size:14.5px;fill:#42576a}
.label{font-size:14.5px;fill:#42576a}
.green{fill:#096d61}.red{fill:#9c4337}
.panel{fill:#f7f9fc;stroke:#bcc9d6;stroke-width:1.3}
.card{fill:white;stroke:#b4c2cf;stroke-width:1.3}
.agent{fill:#e2f3ee;stroke:#087f70;stroke-width:1.8}
.final{fill:#fff5ee;stroke:#b36b43;stroke-width:1.6}
.contract{fill:#eaf0f7;stroke:#aebfd0;stroke-width:1.3}
.flow,.feedback,.promote{fill:none;stroke:#33495d;stroke-width:1.8;stroke-linejoin:round}
.feedback{stroke:#65798c;stroke-dasharray:6 4}
.promote{stroke:#087f70;stroke-width:2.2}
.halo{fill:none;stroke:white;stroke-width:6;stroke-linejoin:round}
</style>'''

class Drawing:
    def __init__(self, height: int, title: str, description: str):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{height}" viewBox="0 0 1120 {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>', STYLE,
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#33495d"/></marker>',
            '<marker id="green-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#087f70"/></marker></defs>',
            f'<rect width="1120" height="{height}" fill="white"/>']

    def box(self, x, y, w, h, kind="card"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" class="{kind}"/>')

    def text(self, x, y, value, kind="body", anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" class="{kind}" text-anchor="{anchor}">{escape(value)}</text>')

    def lines(self, x, y, values, kind="body", step=23):
        for i, value in enumerate(values):
            self.text(x, y + i * step, value, kind)

    def path(self, points, kind="flow", halo=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        if halo:
            self.parts.append(f'<polyline points="{coords}" class="halo"/>')
        self.parts.append(f'<polyline points="{coords}" class="{kind}"/>')
        # Explicit arrowheads render consistently in browsers and WeasyPrint.
        x, y = points[-1]
        px, py = points[-2]
        length = hypot(x - px, y - py)
        ux, uy = (x - px) / length, (y - py) / length
        bx, by = x - 10 * ux, y - 10 * uy
        triangle = f"{x},{y} {bx - 4 * uy},{by + 4 * ux} {bx + 4 * uy},{by - 4 * ux}"
        fill = "#087f70" if kind == "promote" else "#33495d"
        self.parts.append(f'<polygon points="{triangle}" fill="{fill}"/>')

    def finish(self):
        return "\n".join([*self.parts, '</svg>']) + "\n"


def overview() -> str:
    d = Drawing(610, "Three improvement targets in an AI compiler", (
        "One possible starting design. Application search uses agents, conventional search, or learned policies. "
        "Compiler tools build candidates; validation and measurement return feedback. Accepted artifacts run "
        "without optimizer-model calls during normal execution. Controller and compiler development receive "
        "development traces, propose changes, and iterate using development results. Selected versions pass "
        "separate final evaluation before promotion. Final evaluation is withheld from development. "
        "The three targets do not require three agents."))
    d.text(24, 33, "Where the three improvement loops act", "title")
    d.box(24, 52, 1072, 60, "contract")
    d.text(42, 77, "Human-owned experiment contract", "heading")
    d.text(42, 99, "Workload, objective, allowed actions, budget, and acceptance rules stay fixed within the experiment.")
    d.box(24, 134, 1072, 188, "panel")
    d.text(42, 159, "Application optimization", "heading")
    d.text(1078, 159, "Start with a strong baseline and a whole-application profile", "note", "end")
    for x, w, kind in [(42, 224, "agent"), (310, 224, "card"), (578, 224, "card"), (846, 232, "card")]:
        d.box(x, 175, w, 89, kind)
    d.text(56, 199, "Search controller", "heading green")
    d.lines(56, 222, ["Agent, search, or policy", "Propose candidates"], "note", 22)
    d.text(324, 199, "Compiler tools", "heading")
    d.lines(324, 222, ["Transform and lower", "Build runnable candidates"], "note", 22)
    d.text(592, 199, "Check and measure", "heading")
    d.lines(592, 222, ["Check application results", "Kernel time and search cost"], "note", 22)
    d.text(860, 199, "Deploy artifacts", "heading")
    d.lines(860, 221, ["Deploy accepted artifacts", "Keep a working fallback"], "note", 20)
    for x1, x2 in [(266, 310), (534, 578), (804, 846)]:
        d.path([(x1, 218), (x2 - 3, 218)])
    d.path([(690, 264), (690, 290), (154, 290), (154, 265)], "feedback")
    d.text(391, 311, "Failures, profiles, search cost", "note", "middle")
    d.lines(853, 288, ["No optimizer-model calls", "in normal execution (default)."], "note", 20)
    d.text(28, 346, "Development traces", "label")
    d.text(580, 346, "Development traces", "label")
    for left, name, target in [(24, "Controller improvement (optional)", "controller"), (576, "Compiler improvement", "compiler")]:
        d.box(left, 366, 520, 202, "panel")
        d.text(left + 18, 392, name, "heading")
        x1, x2, x3 = left + 18, left + 189, left + 360
        d.box(x1, 410, 136, 79, "agent")
        d.box(x2, 410, 136, 79)
        d.box(x3, 410, 142, 79, "final")
        d.text(x1 + 10, 433, "Agent", "smallhead green")
        d.lines(x1 + 10, 456, ["Revise reusable", target], "note", 19)
        d.text(x2 + 10, 433, "Search jobs" if target == "controller" else "Build and run", "smallhead")
        d.lines(x2 + 10, 456, ["Development", "workloads"], "note", 19)
        d.text(x3 + 10, 433, "Final check", "smallhead red")
        d.lines(x3 + 10, 456, ["Freeze version", "Hidden tasks"], "note", 19)
        d.path([(x1 + 136, 447), (x2 - 3, 447)])
        d.path([(x2 + 136, 447), (x3 - 3, 447)])
        d.path([(x2 + 68, 489), (x2 + 68, 514), (x1 + 68, 514), (x1 + 68, 490)], "feedback")
        d.text(left + 163, 536, "Development results", "note", "middle")
        d.text(left + 163, 555, "revise the next proposal", "note", "middle")
        d.text(x3 + 71, 519, "Results stay out", "note", "middle")
        d.text(x3 + 71, 539, "of development", "note", "middle")
    d.path([(154, 290), (12, 290), (12, 447), (40, 447)], "feedback")
    d.path([(560, 290), (560, 447), (590, 447)], "feedback")
    d.path([(455, 410), (455, 355), (240, 355), (240, 265)], "promote", halo=True)
    d.text(256, 350, "Promoted controller", "label green")
    d.path([(1007, 410), (1007, 335), (506, 335), (506, 265)], "promote", halo=True)
    d.text(811, 330, "Promoted compiler", "label green", "middle")
    d.box(26, 584, 15, 15, "agent")
    d.text(50, 597, "Agent activity", "note")
    d.path([(220, 591), (253, 591)], "feedback")
    d.text(263, 597, "Development feedback", "note")
    d.box(485, 584, 15, 15, "final")
    d.text(509, 597, "Final evaluation withheld from development", "note")
    return d.finish()


def controller() -> str:
    d = Drawing(630, "How the controller improves across optimization jobs", (
        "A fixed proposer uses development traces to change reusable controller instructions or retrieval policy. "
        "The candidate controller runs complete application-optimization jobs. Application results, failures, and "
        "search cost feed the next proposal. A selected controller is frozen for separate final evaluation against "
        "a fixed controller, a memory-only controller, and conventional search. Final tasks and results are withheld "
        "from development. Submission limits and reserved or refreshed workloads limit repeated-selection leakage. "
        "Promoted versions guide future searches, whose development traces can feed the next cycle."))
    d.text(24, 33, "How the controller improves across optimization jobs", "title")
    d.text(24, 58, "Optional offline experiment after application search and compiler evolution demonstrate value.")
    d.box(24, 82, 710, 318, "panel")
    d.text(42, 110, "Development: feedback is available to the proposer", "heading")
    for x, w, kind in [(42, 180, "card"), (258, 200, "agent"), (494, 222, "card")]:
        d.box(x, 143, w, 114, kind)
    d.text(56, 169, "Search traces", "smallhead")
    d.lines(56, 196, ["Failures, profiles,", "workloads and cost"], "body", 24)
    d.text(272, 169, "Fixed proposer", "smallhead green")
    d.lines(272, 196, ["Agent revises the", "controller procedure", "Version memory too"], "note", 23)
    d.text(508, 169, "Candidate controller", "smallhead")
    d.lines(508, 196, ["Run whole search jobs", "Pinned model and tools", "Matched job budget"], "note", 23)
    d.path([(222, 201), (255, 201)])
    d.path([(458, 201), (491, 201)])
    d.path([(605, 257), (605, 302), (358, 302), (358, 259)], "feedback")
    d.text(481, 325, "Application results, failures, search cost", "note", "middle")
    d.text(481, 348, "Revise the next proposal; repeat on development tasks", "note", "middle")
    d.text(42, 381, "Log total compute; measure application speed and search cost separately.")
    d.box(770, 82, 326, 318, "final")
    d.text(788, 110, "Separate final evaluation", "heading red")
    d.lines(788, 140, ["Freeze the selected controller.", "Hide final tasks and results", "from the proposer and its traces."], "body", 23)
    d.text(788, 224, "Compare four methods", "smallhead")
    d.lines(788, 249, ["Fixed controller; fixed plus memory", "Evolved; conventional search", "New workload families; repeat runs"], "note", 23)
    d.lines(788, 337, ["Limit submissions. Reserve or refresh", "tasks; count pass/fail disclosures."], "note", 23)
    d.path([(716, 201), (767, 201)])
    d.text(743, 191, "freeze", "label", "middle")
    d.box(24, 436, 412, 137, "contract")
    d.text(42, 463, "What can change?", "heading")
    d.lines(42, 490, ["Start: reusable instructions or retrieval policy.", "Later: workflow, controller code, improvement", "procedure. Recursion is a separate experiment."], "body", 25)
    d.box(470, 448, 264, 112)
    d.text(488, 476, "Future searches", "heading")
    d.lines(488, 504, ["Use the promoted controller.", "Gather development traces."], "note", 24)
    d.box(770, 436, 326, 137)
    d.text(788, 463, "Promote or retain", "heading")
    d.lines(788, 490, ["Report speed and search cost.", "Include total development cost.", "Version the change; retain rollback."], "body", 25)
    d.path([(934, 400), (934, 433)])
    d.path([(770, 504), (737, 504)], "promote")
    d.path([(602, 560), (602, 600), (12, 600), (12, 201), (39, 201)], "feedback")
    d.text(311, 621, "Future development traces exclude final-evaluation tasks and results", "note", "middle")
    return d.finish()


def main() -> int:
    outputs = {"blueprint.svg": overview(), "controller-development.svg": controller()}
    stale = []
    for name, svg in outputs.items():
        path = ROOT / "docs" / name
        if "--check" in sys.argv[1:]:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(svg, encoding="utf-8")
            print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print(f"Stale figures: {', '.join(stale)}; run python3 scripts/build_blueprint.py", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
