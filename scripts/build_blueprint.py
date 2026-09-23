#!/usr/bin/env python3
"""Render docs/blueprint.svg, the end-to-end compiler blueprint used in docs/SURVEY.md.

The drawing summarizes the survey's architecture: the human-owned contract, the
application-search loop, compiler improvement, controller improvement, validation,
measurement, artifact storage, and deployment. Edit this script, not the SVG, whenever
the survey's components, loops, evaluation boundaries, or forecast schedule change.

    python3 scripts/build_blueprint.py          # write docs/blueprint.svg
    python3 scripts/build_blueprint.py --check  # exit 1 if the SVG is stale
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "blueprint.svg"

LABEL = (
    "End-to-end agentic compiler. Humans fix the workload, objective and validation contract. "
    "Loop 1: an agent competes with structured search and learned policies to propose candidates; "
    "the compiler substrate builds them; validation gates reject failures; the target measures kernel time, "
    "application metric and search cost; accepted artifacts go to a store and a deterministic runtime. "
    "Loop 2: an agent generates compiler components that merge only after a held-out regression check. "
    "Loop 3: a fixed proposer suggests a restricted, versioned controller change, compared with a fixed controller, "
    "a memory-only variant and conventional search on a frozen evaluator, and promoted only if application results "
    "or search efficiency improve. No loop may relax the validation contract."
)

# Light palette only: the SVG must read identically on GitHub, in the PDF, and in print.
STYLE = """<style>
.bg{fill:#FFFFFF}
.panel{fill:#FFFFFF;stroke:#C6CCD6;stroke-width:1.2}
.panel3{fill:#FFFFFF;stroke:#C6CCD6;stroke-width:1.2;stroke-dasharray:8 4}
.sub{fill:#EEF0F4;stroke:#C6CCD6;stroke-width:1}
.agent{fill:#DDF1EC;stroke:#0B7A69;stroke-width:1.6}
.contract{fill:#E7EAF1;stroke:#C6CCD6;stroke-width:1.2}
.frozen{fill:#EEF0F4;stroke:#B8322A;stroke-width:1.4;stroke-dasharray:4 3}
.pill{fill:#FFFFFF;stroke:#C6CCD6}
.warnpill{fill:none;stroke:#B8322A}
.rung{fill:#FFFFFF;stroke:#0B7A69;stroke-width:.8;stroke-opacity:.5}
.rungStart{fill:#FFFFFF;stroke:#0B7A69;stroke-width:2}
.rungLate{fill:none;stroke:#0B7A69;stroke-width:.8;stroke-dasharray:3 3}
.lock rect{fill:#B8322A} .lock path{stroke:#B8322A;stroke-width:1.6}
text{fill:#18202C;font-family:"IBM Plex Sans","Helvetica Neue",Arial,"Liberation Sans",sans-serif}
.t{font-size:13px}
.s{font-size:12px;fill:#586173}
.h,.hA{font-family:"IBM Plex Sans Condensed","Arial Narrow","Liberation Sans Narrow",Arial,sans-serif;font-weight:600;font-size:14.5px}
.hA{fill:#0B7A69}
.eyebrow,.note,.lbl,.lblA,.lblF,.pillT,.warnT,.tagA{font-family:"IBM Plex Mono",Menlo,Consolas,"Liberation Mono",monospace}
.eyebrow{font-size:11px;letter-spacing:.08em;fill:#586173}
.note,.warnT,.tagA{font-size:10.5px}
.note{fill:#586173}
.lbl,.lblA,.lblF,.pillT{font-size:11px}
.lbl{fill:#586173} .lblA,.tagA{fill:#0B7A69} .lblF,.warnT{fill:#B8322A}
.flow{stroke:#18202C;stroke-width:1.4}
.flowA{stroke:#0B7A69;stroke-width:1.8}
.fb{stroke:#586173;stroke-width:1.4;stroke-dasharray:5 4;fill:none}
.forbid{stroke:#B8322A;stroke-width:1.4;stroke-dasharray:4 4}
.xmark line{stroke:#B8322A;stroke-width:2.2}
.mk{fill:#18202C} .mkA{fill:#0B7A69} .mkF{fill:#B8322A}
</style>"""

S: list[str] = []


def a(s: str) -> None:
    S.append(s)


def box(x, y, w, h, cls="panel", rx=6):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')


def text(x, y, s, cls="t", anchor="start"):
    a(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{s}</text>')


def line(x1, y1, x2, y2, cls="flow", marker="arr"):
    m = f' marker-end="url(#{marker})"' if marker else ""
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{m}/>')


def poly(pts, cls="flow", marker="arr"):
    p = " ".join(f"{x},{y}" for x, y in pts)
    m = f' marker-end="url(#{marker})"' if marker else ""
    a(f'<polyline points="{p}" class="{cls}" fill="none"{m}/>')


def stack(x, y0, w, items, h=34, gap=8, cls="sub", tcls="t"):
    y = y0
    for s in items:
        box(x, y, w, h, cls, rx=4)
        text(x + w / 2, y + h / 2 + 4.5, s, tcls, "middle")
        y += h + gap
    return y


def render() -> str:
    S.clear()
    W, H = 1200, 918
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{LABEL}">')
    a(f'<rect class="bg" x="0" y="0" width="{W}" height="{H}"/>')
    a(STYLE)
    a('''<defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mk"/></marker>
    <marker id="arrA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mkA"/></marker>
    <marker id="arrF" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="mkF"/></marker>
    </defs>''')

    # --- Contract band (human-owned) ---
    box(30, 20, 1140, 64, "contract", rx=6)
    text(46, 44, "FIXED BY HUMANS", "eyebrow")
    text(46, 68, "Workload · objective (e.g. throughput under a latency limit) · validation contract: semantics, numerical or statistical tolerance, supported inputs", "t")

    # --- Row 2 ---
    Y, HH = 130, 230
    # A: profile
    box(30, Y, 120, HH); text(90, Y + 24, "Baseline &amp;", "h", "middle"); text(90, Y + 42, "profile", "h", "middle")
    text(90, Y + 80, "strong compiled", "s", "middle"); text(90, Y + 96, "or library baseline", "s", "middle")
    text(90, Y + 128, "whole-app profile", "s", "middle"); text(90, Y + 144, "finds the", "s", "middle"); text(90, Y + 160, "addressable time", "s", "middle")

    # B: control plane
    bx, bw = 200, 240
    box(bx, Y, bw, HH); text(bx + 14, Y + 22, "Optimizer control plane", "h")
    box(bx + 12, Y + 34, bw - 24, 96, "agent", rx=4)
    text(bx + 24, Y + 54, "Agent", "hA")
    for i, s in enumerate(["proposes configs and scope", "synthesizes kernels, rewrites", "diagnoses failed candidates", "reuses prior experiments"]):
        text(bx + 24, Y + 74 + i * 17, s, "s")
    stack(bx + 12, Y + 138, bw - 24, ["Learned policy", "Structured search / tuner"], h=32, gap=8)
    text(bx + bw / 2, Y + HH - 6, "same feedback · same budget", "note", "middle")

    # C: substrate
    cx, cw = 490, 190
    box(cx, Y, cw, HH); text(cx + 14, Y + 22, "Compiler substrate", "h")
    stack(cx + 12, Y + 36, cw - 24, ["Representations", "Transformations", "Lowering", "Code generation"])
    text(cx + cw / 2, Y + HH - 6, "keep · generate · replace", "note", "middle")

    # D: validation
    dx, dw = 730, 170
    box(dx, Y, dw, HH); text(dx + 14, Y + 22, "Validation gates", "h")
    stack(dx + 12, Y + 36, dw - 24, ["Static checks", "Compile", "Tests &amp; numerics", "Scoped equivalence"])
    text(dx + dw / 2, Y + HH - 6, "record: tested vs proven", "note", "middle")

    # E: measure
    ex, ew = 950, 220
    box(ex, Y, ew, HH); text(ex + 14, Y + 22, "Measure on the target", "h")
    stack(ex + 12, Y + 36, ew - 24, ["Kernel time", "Application metric", "Search cost"])
    text(ex + ew / 2, Y + 186, "tokens · device-hours · time", "s", "middle")
    text(ex + ew / 2, Y + HH - 6, "gain must beat measurement noise", "note", "middle")

    # Contract arrows (down)
    line(bx + 60, 84, bx + 60, Y - 2, "flow", "arr"); text(bx + 66, 108, "actions, budget", "lbl")
    line(dx + 95, 84, dx + 95, Y - 2, "flow", "arr"); text(dx + 101, 108, "acceptance", "lbl")
    line(ex + 125, 84, ex + 125, Y - 2, "flow", "arr"); text(ex + 131, 108, "objective", "lbl")
    # Forbidden edge: agent -> contract
    line(bx + 190, Y + 34, bx + 190, 86, "forbid", "arrF")
    a(f'<g class="xmark"><line x1="{bx+183}" y1="100" x2="{bx+197}" y2="114"/><line x1="{bx+197}" y1="100" x2="{bx+183}" y2="114"/></g>')
    text(bx + 202, 112, "may not relax", "lblF")

    # Forward flow along row 2 (y = 245)
    fy = Y + 115
    line(150, fy, bx - 2, fy); 
    line(bx + bw, fy, cx - 2, fy); text((bx + bw + cx) / 2, fy - 8, "candidate", "lbl", "middle")
    line(cx + cw, fy, dx - 2, fy); text((cx + cw + dx) / 2, fy - 8, "build", "lbl", "middle")
    line(dx + dw, fy, ex - 2, fy); text((dx + dw + ex) / 2, fy - 8, "passes", "lbl", "middle")

    # Feedback bus (y = 400): measure -> control plane, validation rejections join, store history joins
    by = 400
    poly([(ex + 60, Y + HH), (ex + 60, by), (bx + 125, by), (bx + 125, Y + HH + 2)], "fb", "arr")
    line(dx + 95, Y + HH, dx + 95, by, "fb", None)
    text(dx + 101, Y + HH + 22, "rejections", "lbl")
    text(ex + 66, Y + HH + 22, "profiles, cost", "lbl")
    a(f'<rect x="330" y="{by-11}" width="200" height="22" rx="11" class="pill"/>')
    text(430, by + 4, "Loop 1 · per workload", "pillT", "middle")

    # --- Row 3 ---
    R = 450
    # F: store
    fx, fw = 950, 220
    box(fx, R, fw, 120); text(fx + 14, R + 22, "Artifact &amp; experiment store", "h")
    for i, s in enumerate(["kernels, configs, heuristics", "failed and slow candidates too", "controller, memory: own versions"]):
        text(fx + 14, R + 48 + i * 20, s, "s")
    line(ex + 190, Y + HH, ex + 190, R - 2); text(ex + 196, 434, "accept", "lbl")
    line(fx + 30, R, fx + 30, by + 2, "fb", "arr"); text(fx + 36, 434, "history", "lbl")

    # G: runtime
    gx, gw = 640, 260
    box(gx, R, gw, 120); text(gx + 14, R + 22, "Deployed runtime", "h")
    for i, s in enumerate(["runs accepted artifacts", "keeps a working fallback", "no model in the execution path"]):
        text(gx + 14, R + 48 + i * 20, s, "s")
    line(fx, R + 60, gx + gw + 2, R + 60); text((fx + gx + gw) / 2, R + 52, "ship", "lbl", "middle")
    # drift back to profile
    poly([(gx + 30, R), (gx + 30, 424), (90, 424), (90, Y + HH + 2)], "fb", "arr")
    text(110, 440, "production profiles, drift", "lbl")

    # H: offline compiler improvement
    hx, hw = 200, 400
    box(hx, R, hw, 150); text(hx + 14, R + 22, "Loop 2 · compiler improvement, offline", "h")
    box(hx + 12, R + 36, 176, 96, "agent", rx=4)
    text(hx + 24, R + 56, "Agent", "hA")
    for i, s in enumerate(["generates a heuristic,", "transformation, or", "backend piece"]):
        text(hx + 24, R + 76 + i * 17, s, "s")
    box(hx + 212, R + 36, 176, 96, "sub", rx=4)
    text(hx + 300, R + 64, "Held-out corpus", "t", "middle")
    text(hx + 300, R + 82, "regression check", "t", "middle")
    text(hx + 300, R + 104, "separate from", "s", "middle"); text(hx + 300, R + 120, "search workloads", "s", "middle")
    line(hx + 188, R + 84, hx + 210, R + 84)
    line(560, R + 36, 560, Y + HH + 2, "flowA", "arrA")
    text(566, 378, "merge into", "lblA"); text(566, 392, "default path", "lblA")


    # --- Row 4: Loop 3, controller improvement (non-recursive by default) ---
    L3 = 630
    text(200, 620, "Loops 2 and 3: measure each change alone, then combined", "lbl")
    box(200, L3, 970, 210, "panel3")
    text(214, L3 + 22, "Loop 3 · controller improvement, offline", "h")
    a(f'<rect x="610" y="{L3+9}" width="118" height="18" rx="9" class="warnpill"/>')
    text(669, L3 + 22, "narrow evidence", "warnT", "middle")
    # proposer with scope ladder
    box(212, L3 + 36, 330, 160, "agent", rx=4)
    text(224, L3 + 56, "Fixed proposer", "hA")
    rungs = [("improvement procedure (recursive)", "later", "rungLate"),
             ("controller code", "", "rung"),
             ("workflow, budget split, topology", "", "rung"),
             ("instructions, retrieval policy", "start here", "rungStart"),
             ("memory snapshot only", "baseline arm", "rung")]
    for k, (s, tag, cls) in enumerate(rungs):
        y = L3 + 66 + k * 24
        box(224, y, 306, 20, cls, rx=3)
        text(232, y + 14, s, "s")
        if tag:
            text(522, y + 14, tag, "tagA" if tag == "start here" else "note", "end")
    line(542, L3 + 116, 570, L3 + 116)
    # four-arm comparison on frozen evaluator
    box(572, L3 + 36, 340, 160, "frozen", rx=4)
    text(586, L3 + 56, "Four arms on a frozen evaluator", "h")
    for k, s in enumerate(["fixed controller · fixed + memory only", "evolved version · conventional search",
                           "same compiler tools, model, hardware,", "per-job budget; held-out workload", "families; repeated runs",
                           "gates, measurement, held-out set: read-only"]):
        text(586, L3 + 78 + k * 18, s, "s" if k < 5 else "lblF")
    a(f'<g class="lock"><rect x="884" y="{L3+46}" width="16" height="12" rx="2"/><path d="M887,{L3+46} v-4 a5,5 0 0 1 10,0 v4" fill="none"/></g>')
    line(912, L3 + 116, 928, L3 + 116)
    # promote / roll back
    box(930, L3 + 36, 228, 160, "sub", rx=4)
    text(944, L3 + 56, "Promote or roll back", "h")
    for k, s in enumerate(["application result and search", "cost, reported separately", "development cost disclosed", "version N kept for rollback", "fresh searches only use", "promoted versions"]):
        text(944, L3 + 78 + k * 18, s, "s")
    # input: development traces only
    line(fx + 150, R + 120, fx + 150, L3 - 2, "fb", "arr"); text(fx + 156, R + 140, "development", "lbl"); text(fx + 156, R + 154, "traces only", "lbl")
    # output: promote -> control plane
    poly([(1044, L3 + 196), (1044, L3 + 226), (170, L3 + 226), (170, Y + 190), (bx - 2, Y + 190)], "flowA", "arrA")
    text(600, L3 + 220, "promoted controller version guides later searches", "lblA", "middle")

    # Legend
    LY = 900
    box(30, LY - 12, 16, 14, "agent", rx=3); text(52, LY, "where the agent acts", "s")
    line(210, LY - 5, 250, LY - 5); text(258, LY, "candidate / artifact flow", "s")
    line(440, LY - 5, 480, LY - 5, "fb"); text(488, LY, "feedback", "s")
    line(570, LY - 5, 610, LY - 5, "forbid", "arrF"); text(618, LY, "boundary the optimizer may not cross", "s")
    a('</svg>')

    return "\n".join(S) + "\n"


def main() -> int:
    svg = render()
    if "--check" in sys.argv[1:]:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != svg:
            print("docs/blueprint.svg is stale; run python3 scripts/build_blueprint.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
