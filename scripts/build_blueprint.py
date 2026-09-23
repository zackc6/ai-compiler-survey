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
.xs{font-size:13px;fill:#42576a}
.rung{fill:white;stroke:#087f70;stroke-width:1;stroke-opacity:.55}
.rungstart{fill:white;stroke:#087f70;stroke-width:2.2}
.runglate{fill:white;stroke:#087f70;stroke-width:1;stroke-dasharray:4 3}
</style>'''

class Drawing:
    def __init__(self, height: int, title: str, description: str, width: int = 1120):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>', STYLE,
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#33495d"/></marker>',
            '<marker id="green-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#087f70"/></marker></defs>',
            f'<rect width="{width}" height="{height}" fill="white"/>']

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
    d = Drawing(800, "Where the agent acts in an end-to-end AI compiler", (
        "One possible starting design. Humans fix the workload, objective, allowed actions, budget, and acceptance "
        "rules for an experiment. In application optimization, an agent, a learned policy, and structured search "
        "propose candidates with the same feedback and budget; compiler tools build them; checks and measurement "
        "decide; accepted artifacts are stored and deployed with a fallback and no optimizer-model calls by default. "
        "Development traces, excluding final-evaluation tasks, feed two development loops. Compiler development "
        "generates heuristics, analyses, transformations, or backend pieces. Optional, late-stage controller "
        "development starts with instructions or retrieval logic and widens only after measured failures. Each loop "
        "iterates on development feedback, freezes a selected version for a hidden final check, and promotes it "
        "only if it passes."), width=1400)
    d.text(30, 34, "Where the agent acts in an end-to-end AI compiler", "title")
    # Human-owned contract
    d.box(30, 50, 1340, 56, "contract")
    d.text(46, 73, "Human-owned experiment contract", "smallhead")
    d.text(46, 96, "Workload, objective, allowed actions, budget, and acceptance rules stay fixed within the experiment.", "body")
    d.text(1354, 96, "No loop may relax them", "note red", "end")

    # Application optimization
    d.box(20, 124, 1360, 270, "panel")
    d.text(36, 148, "Application optimization", "heading")
    d.text(1364, 148, "Start with a strong baseline and a whole-application profile", "note", "end")
    top, h = 166, 170
    d.box(30, top, 130, h)
    d.lines(42, 190, ["Baseline and", "profile"], "smallhead", 20)
    d.lines(42, 242, ["strong compiled", "or library", "baseline;", "whole-app profile"], "xs", 19)
    d.box(204, top, 240, h)
    d.text(216, 190, "Search controller", "smallhead green")
    d.box(214, 198, 220, 50, "agent")
    d.text(224, 218, "Agent", "smallhead green")
    d.text(224, 238, "proposes, builds, diagnoses", "xs")
    d.box(214, 254, 220, 26); d.text(324, 272, "Learned policy", "xs", "middle")
    d.box(214, 286, 220, 26); d.text(324, 304, "Structured search / tuner", "xs", "middle")
    d.text(324, 328, "same feedback, same budget", "xs", "middle")
    d.box(488, top, 190, h)
    d.text(500, 190, "Compiler tools", "smallhead")
    d.lines(500, 220, ["representations", "transformations", "lowering", "code generation"], "xs", 20)
    d.text(500, 324, "keep, generate, or replace", "xs green")
    d.box(722, top, 200, h)
    d.text(734, 190, "Check and measure", "smallhead")
    d.lines(734, 220, ["static checks, compile", "tests and numerics", "scoped equivalence", "kernel time", "application metric", "search cost"], "xs", 19)
    d.box(966, top, 180, h)
    d.lines(978, 190, ["Artifact and", "experiment store"], "smallhead", 20)
    d.lines(978, 242, ["accepted artifacts", "failed candidates", "controller versions", "and memory kept", "separately"], "xs", 19)
    d.box(1190, top, 180, h)
    d.text(1202, 190, "Deploy", "smallhead")
    d.lines(1202, 220, ["accepted artifacts", "working fallback", "no optimizer-model", "calls by default;", "the app may still", "contain models"], "xs", 19)
    for x1, x2 in ((160, 204), (444, 488), (678, 722), (922, 966), (1146, 1190)):
        d.path([(x1, 252), (x2 - 2, 252)])
    # Feedback inside application optimization
    d.path([(822, top + h), (822, 358), (324, 358), (324, top + h + 2)], "feedback")
    d.text(520, 380, "failures, profiles, search cost", "xs", "middle")

    # Production profiles and development traces
    d.path([(1280, top + h), (1280, 414), (95, 414), (95, top + h + 2)], "feedback")
    d.text(112, 410, "production profiles for fresh work", "xs")
    d.path([(1056, top + h), (1056, 432), (60, 432), (60, 460)], "feedback")
    d.path([(740, 432), (740, 460)], "feedback")
    d.text(1046, 428, "development traces, excluding final-evaluation tasks", "xs", "end")

    # Controller development
    d.box(20, 460, 680, 290, "panel")
    d.text(36, 484, "Controller development (optional)", "heading")
    d.text(346, 484, "no application-level evidence yet", "note red")
    d.box(34, 500, 270, 200, "agent")
    d.text(46, 522, "Fixed proposer", "smallhead green")
    rungs = [("improvement procedure", "later", "runglate"), ("agent code", "", "rung"),
             ("search strategy, orchestration", "", "rung"), ("instructions, retrieval logic", "start", "rungstart")]
    for k, (label, tag, kind) in enumerate(rungs):
        y = 534 + k * 32
        d.box(46, y, 246, 26, kind)
        d.text(56, y + 18, label, "xs")
        if tag:
            d.text(284, y + 18, tag, "xs green", "end")
    d.lines(46, 674, ["widen only after measured failures;", "memory-only change is a test arm"], "xs", 17)
    d.box(334, 530, 150, 130)
    d.text(346, 554, "Search jobs", "smallhead")
    d.lines(346, 578, ["complete jobs on", "development", "workloads; pinned", "model, toolchain"], "xs", 19)
    d.box(514, 500, 176, 200, "final")
    d.text(526, 522, "Final check", "smallhead red")
    d.lines(526, 546, ["freeze the version", "hidden tasks, results", "submission limit", "four arms: fixed,", "memory only, evolved,", "conventional search", "new workload families"], "xs", 19)
    d.path([(304, 595), (332, 595)])
    d.path([(484, 595), (512, 595)])
    d.path([(409, 660), (409, 724), (169, 724), (169, 702)], "feedback")
    d.text(289, 740, "application results, failures, search cost", "xs", "middle")
    d.text(602, 722, "results stay out", "xs red", "middle")
    d.text(602, 738, "of development", "xs red", "middle")

    # Compiler development
    d.box(720, 460, 660, 290, "panel")
    d.text(736, 484, "Compiler development", "heading")
    d.box(734, 500, 220, 130, "agent")
    d.text(746, 522, "Agent", "smallhead green")
    d.lines(746, 548, ["generates a heuristic,", "analysis, transformation,", "or backend piece"], "xs", 19)
    d.box(984, 500, 170, 130)
    d.text(996, 522, "Build and run", "smallhead")
    d.lines(996, 548, ["development", "workloads"], "xs", 19)
    d.box(1184, 500, 184, 170, "final")
    d.text(1196, 522, "Final check", "smallhead red")
    d.lines(1196, 546, ["freeze the version", "hidden regression", "and performance", "tasks", "submission limit"], "xs", 19)
    d.path([(954, 565), (982, 565)])
    d.path([(1154, 565), (1182, 565)])
    d.path([(1069, 630), (1069, 670), (844, 670), (844, 632)], "feedback")
    d.text(956, 690, "development results", "xs", "middle")
    d.text(1276, 692, "results stay out", "xs red", "middle")
    d.text(1276, 708, "of development", "xs red", "middle")
    d.text(956, 734, "Measure each development change alone, then combined.", "xs", "middle")

    # Promotions back into the application loop
    d.path([(602, 500), (602, 446), (400, 446), (400, top + h + 2)], "promote", halo=True)
    d.text(394, 384, "promoted controller", "xs green", "end")
    d.path([(1276, 500), (1276, 446), (640, 446), (640, top + h + 2)], "promote", halo=True)
    d.text(646, 384, "promoted compiler", "xs green")

    # Legend
    d.box(30, 768, 16, 14, "agent"); d.text(54, 780, "agent activity", "xs")
    d.path([(170, 775), (208, 775)]); d.text(216, 780, "candidate or artifact flow", "xs")
    d.path([(400, 775), (438, 775)], "feedback"); d.text(446, 780, "development feedback", "xs")
    d.path([(610, 775), (648, 775)], "promote"); d.text(656, 780, "promotion after the final check", "xs")
    d.box(880, 768, 16, 14, "final"); d.text(904, 780, "final evaluation withheld from development", "xs")
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
    outputs = {"architecture-overview.svg": overview(), "controller-development.svg": controller()}
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
