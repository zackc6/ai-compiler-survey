#!/usr/bin/env python3
"""Assemble living-survey markdown into one publishable bundle."""

from __future__ import annotations

from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "out"

LANGS = ("en", "zh-CN", "zh-TW")

# Narrative-first order for the PDF manuscript.
SECTIONS: list[tuple[str, Path]] = [
    ("Survey narrative", ROOT / "docs" / "SURVEY.md"),
    ("Roadmap", ROOT / "docs" / "ROADMAP.md"),
    ("Software stack & HW codesign reshape", ROOT / "docs" / "STACK.md"),
    ("Claims map", ROOT / "docs" / "CLAIMS.md"),
    ("Conflicts register", ROOT / "docs" / "CONFLICTS.md"),
    ("Systems comparison", ROOT / "docs" / "SYSTEMS.md"),
    ("Taxonomy", ROOT / "docs" / "TAXONOMY.md"),
    ("Publications index", ROOT / "publications" / "INDEX.md"),
]

SECTION_TITLES = {
    "en": {
        "Survey narrative": "Survey narrative",
        "Roadmap": "Roadmap",
        "Software stack & HW codesign reshape": "Software stack & HW codesign reshape",
        "Claims map": "Claims map",
        "Conflicts register": "Conflicts register",
        "Systems comparison": "Systems comparison",
        "Taxonomy": "Taxonomy",
        "Publications index": "Publications index",
        "Export notes": "Export notes",
    },
    "zh-CN": {
        "Survey narrative": "综述正文",
        "Roadmap": "路线图",
        "Software stack & HW codesign reshape": "软件栈与软硬件协同设计重塑",
        "Claims map": "主张—证据映射",
        "Conflicts register": "冲突对照",
        "Systems comparison": "系统对比",
        "Taxonomy": "分类法",
        "Publications index": "文献索引",
        "Export notes": "导出说明",
    },
    "zh-TW": {
        "Survey narrative": "綜述正文",
        "Roadmap": "路線圖",
        "Software stack & HW codesign reshape": "軟體堆疊與軟硬體協同設計重塑",
        "Claims map": "主張—證據對應",
        "Conflicts register": "衝突對照",
        "Systems comparison": "系統比較",
        "Taxonomy": "分類法",
        "Publications index": "文獻索引",
        "Export notes": "匯出說明",
    },
}

COVER = {
    "en": {
        "title": "Next-Generation AI Compiler Survey",
        "subtitle": (
            "Predicting the agentic compiler (~2027–28 and ~5 years): "
            "software-stack reshape and HW–SW codesign"
        ),
        "living": "Living survey export",
        "generated": "Generated",
        "source": "Source repository",
        "primary": "Primary narrative: docs/SURVEY.md · Roadmap: docs/ROADMAP.md · Stack: docs/STACK.md",
        "verdict": (
            "**North star.** Agents own semantic search, orchestration, and artifact synthesis. "
            "Compilers own lowering, legality, measurement, and fallback. Hardware codesign enters "
            "only through kernels, IR, tests, and profilers — not autonomous tape-out."
        ),
        "export_notes": (
            "- Full digests remain in `publications/*.md` (not inlined).\n"
            "- Tier maps: `docs/REPOS.md`, `docs/PRODUCTS.md`.\n"
            "- Rebuild: `python3 publish/build_pdf.py` (builds en / zh-CN / zh-TW).\n"
        ),
    },
    "zh-CN": {
        "title": "下一代 AI 编译器综述",
        "subtitle": "预测智能体编译器（约 2027–28 与未来五年）：软件栈重塑与软硬件协同设计",
        "living": "持续更新型综述导出",
        "generated": "生成日期",
        "source": "源仓库",
        "primary": "主叙事：docs/SURVEY.md · 路线图：docs/ROADMAP.md · 软件栈：docs/STACK.md",
        "verdict": (
            "**北极星目标。** 智能体负责语义搜索、编排与产物综合；编译器负责下降、合法性、"
            "测量与回退。硬件协同设计仅通过内核、IR、测试与 profiling 闭环进入——而非自动流片。"
        ),
        "export_notes": (
            "- 完整文献摘要仍在 `publications/*.md`（未内联）。\n"
            "- 证据分层图：`docs/REPOS.md`、`docs/PRODUCTS.md`。\n"
            "- 重新构建：`python3 publish/build_pdf.py`（同时生成 en / zh-CN / zh-TW）。\n"
        ),
    },
    "zh-TW": {
        "title": "下一代 AI 編譯器綜述",
        "subtitle": "預測智能體編譯器（約 2027–28 與未來五年）：軟體堆疊重塑與軟硬體協同設計",
        "living": "持續更新型綜述匯出",
        "generated": "產生日期",
        "source": "原始碼庫",
        "primary": "主敘事：docs/SURVEY.md · 路線圖：docs/ROADMAP.md · 軟體堆疊：docs/STACK.md",
        "verdict": (
            "**北極星目標。** 智能體負責語意搜尋、編排與產物綜合；編譯器負責下降、合法性、"
            "量測與回退。硬體協同設計僅透過核心、IR、測試與 profiling 閉環進入——而非自動流片。"
        ),
        "export_notes": (
            "- 完整文獻摘要仍在 `publications/*.md`（未內嵌）。\n"
            "- 證據分層圖：`docs/REPOS.md`、`docs/PRODUCTS.md`。\n"
            "- 重新建置：`python3 publish/build_pdf.py`（同時產生 en / zh-CN / zh-TW）。\n"
        ),
    },
}

PDF_NAMES = {
    "en": "next-gen-ai-compiler-survey.en.pdf",
    "zh-CN": "next-gen-ai-compiler-survey.zh-CN.pdf",
    "zh-TW": "next-gen-ai-compiler-survey.zh-TW.pdf",
}


def cover_md(today: str, lang: str = "en") -> str:
    c = COVER[lang]
    return f"""<div class="cover">

# {c["title"]}

<p class="subtitle">{c["subtitle"]}</p>

<p class="meta">
<strong>{c["living"]}</strong><br/>
{c["generated"]}: {today}<br/>
{c["source"]}: ai-compiler-survey<br/>
{c["primary"]}
</p>

<div class="verdict">

{c["verdict"]}

</div>

</div>
"""


def rewrite_links(text: str) -> str:
    """Best-effort link rewrite so PDF-relative paths stay meaningful."""
    replacements = {
        "](../publications/": "](publications/",
        "](../STATUS.md)": "](STATUS.md)",
        "](CONFLICTS.md)": "](#conflicts-register)",
        "](ROADMAP.md)": "](#roadmap)",
        "](STACK.md)": "](#software-stack--hw-codesign-reshape)",
        "](CLAIMS.md)": "](#claims-map)",
        "](REPOS.md)": "](docs/REPOS.md)",
        "](PRODUCTS.md)": "](docs/PRODUCTS.md)",
        "](SYSTEMS.md)": "](#systems-comparison)",
        "](TAXONOMY.md)": "](#taxonomy)",
        "](WORKFLOW.md)": "](docs/WORKFLOW.md)",
        "](../docs/SURVEY.md)": "](#survey-narrative)",
        "](../docs/ROADMAP.md)": "](#roadmap)",
        "](../docs/STACK.md)": "](#software-stack--hw-codesign-reshape)",
        "](../docs/CONFLICTS.md)": "](#conflicts-register)",
        "](../docs/REPOS.md)": "](docs/REPOS.md)",
        "](../docs/PRODUCTS.md)": "](docs/PRODUCTS.md)",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    return text


def strip_first_h1(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        if lines and lines[0].strip() == "":
            lines = lines[1:]
    return "\n".join(lines).strip() + "\n"


def assemble(lang: str = "en") -> Path:
    if lang not in LANGS:
        raise ValueError(f"unsupported lang {lang}")
    OUT.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    titles = SECTION_TITLES[lang]
    parts: list[str] = [cover_md(today, lang=lang)]

    # Body always assembled from English sources; translation happens later for zh_*.
    for title, path in SECTIONS:
        if not path.is_file():
            raise FileNotFoundError(path)
        body = strip_first_h1(path.read_text(encoding="utf-8"))
        body = rewrite_links(body)
        local_title = titles[title]
        anchor = title.lower().replace(" ", "-").replace("&", "").replace("--", "-")
        parts.append(
            f'<div class="section-break"></div>\n\n'
            f"## {local_title} {{#{anchor}}}\n\n"
            f"{body}\n"
        )

    parts.append(
        "\n---\n\n"
        f"## {titles['Export notes']}\n\n"
        f"{COVER[lang]['export_notes']}"
    )

    suffix = "" if lang == "en" else f".{lang}"
    # For zh, write English body first as *.en-body.md then translate overwrites bundle.
    bundle = OUT / f"survey-bundle{suffix}.md"
    if lang == "en":
        bundle.write_text("\n".join(parts), encoding="utf-8")
        return bundle

    # Assemble with Chinese section titles but English body; caller translates body.
    en_titles = SECTION_TITLES["en"]
    # Re-assemble using Chinese cover/titles already in parts — body still English.
    bundle.write_text("\n".join(parts), encoding="utf-8")
    _ = en_titles  # kept for clarity / future per-doc locale overlays
    return bundle


if __name__ == "__main__":
    path = assemble("en")
    print(f"Wrote {path}")
