#!/usr/bin/env python3
"""Assemble living-survey markdown into one publishable bundle."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "out"

LANGS = ("en", "zh-CN", "zh-TW")

# Narrative-first order for the PDF manuscript.
SECTIONS: list[tuple[str, Path]] = [
    ("Survey narrative", ROOT / "docs" / "SURVEY.md"),
    ("Reference guide", ROOT / "reference" / "README.md"),
    ("Products prediction signals", ROOT / "reference" / "products.md"),
    ("Repos forge evidence", ROOT / "reference" / "repos.md"),
    ("Publications index", ROOT / "reference" / "publications" / "INDEX.md"),
]

SECTION_TITLES = {
    "en": {
        "Survey narrative": "Survey narrative",
        "Reference guide": "Reference guide",
        "Products prediction signals": "Products (prediction signals)",
        "Repos forge evidence": "Repos & forge evidence",
        "Publications index": "Publications index",
        "Export notes": "Export notes",
    },
    "zh-CN": {
        "Survey narrative": "综述正文",
        "Reference guide": "参考文献指南",
        "Products prediction signals": "产品信号",
        "Repos forge evidence": "仓库与协同证据",
        "Publications index": "文献索引",
        "Export notes": "导出说明",
    },
    "zh-TW": {
        "Survey narrative": "綜述正文",
        "Reference guide": "參考文獻指南",
        "Products prediction signals": "產品信號",
        "Repos forge evidence": "倉庫與協同證據",
        "Publications index": "文獻索引",
        "Export notes": "匯出說明",
    },
}

COVER = {
    "en": {
        "title": "Next-Generation AI Compiler Survey and Design Guide",
        "subtitle": (
            "Evidence, architectural choices, and experiments for a performance-first compiler. "
            "Forecasts for 2027, 2029, 2031, 2036, and beyond."
        ),
        "living": "Living survey export",
        "generated": "Generated",
        "primary": "A single reading path from technical trends to design decisions, with source appendices.",
        "verdict": (
            "**Design hypothesis.** The compiler increasingly becomes an agentic optimization system. "
            "Test that hypothesis against strong alternatives. Prioritize runtime performance, "
            "then developer productivity and portability. Treat passes, lowering, representations, "
            "and the division between agents and compiler components as choices to evaluate."
        ),
        "export_notes": (
            "- Detailed digests remain in the repository’s publication directory. Source links in this PDF open external references.\n"
            "- Product and implementation appendices support the design decisions; they are not independent replications.\n"
            "- The existing presentation is an earlier snapshot and has not been aligned with this revision.\n"
            "- Rebuild: `python3 publish/build_pdf.py`.\n"
        ),
    },
    "zh-CN": {
        "title": "下一代 AI 编译器综述",
        "subtitle": "以性能为首要目标的编译器设计指南：2027、2029、2031、2036 年及更远期预测",
        "living": "持续更新型综述导出",
        "generated": "生成日期",
        "primary": "从技术趋势到设计决策的完整阅读路径，并附参考资料。",
        "verdict": (
            "**设计假设。** 编译器逐渐成为智能体优化系统。用强基线检验这一假设；优先考虑运行性能，"
            "其次是开发效率和可移植性。编译阶段、降低流程及智能体与编译器的边界都是需要实验评估的选择。"
        ),
        "export_notes": (
            "- 完整文献摘要仍在 `reference/publications/*.md`（未内联）。\n"
            "- 证据分层图：`reference/repos.md`、`reference/products.md`。\n"
            "- 重新构建：`python3 publish/build_pdf.py --lang zh-CN`。\n"
        ),
    },
    "zh-TW": {
        "title": "下一代 AI 編譯器綜述",
        "subtitle": "以效能為首要目標的編譯器設計指南：2027、2029、2031、2036 年及更遠期預測",
        "living": "持續更新型綜述匯出",
        "generated": "產生日期",
        "primary": "從技術趨勢到設計決策的完整閱讀路徑，並附參考資料。",
        "verdict": (
            "**設計假設。** 編譯器逐漸成為智能體最佳化系統。用強基準檢驗這一假設；優先考慮執行效能，"
            "其次是開發效率和可攜性。編譯階段、降低流程及智能體與編譯器的邊界都是需要實驗評估的選擇。"
        ),
        "export_notes": (
            "- 完整文獻摘要仍在 `reference/publications/*.md`（未內嵌）。\n"
            "- 證據分層圖：`reference/repos.md`、`reference/products.md`。\n"
            "- 重新建置：`python3 publish/build_pdf.py --lang zh-TW`。\n"
        ),
    },
}

PDF_NAMES = {
    # English is the only PDF kept in out/ — no .en suffix.
    "en": "next-gen-ai-compiler-survey.pdf",
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
{c["primary"]}
</p>

<div class="verdict">

{c["verdict"]}

</div>

</div>
"""


def rewrite_links(text: str, source: Path) -> str:
    """Resolve repository links to inlined sections or external primary sources."""
    sections = {
        path.resolve(): title.lower().replace(" ", "-").replace("&", "").replace("--", "-")
        for title, path in SECTIONS
    }
    legacy = {
        "CONFLICTS.md": "6-conflicts-keep-unresolved-until-evidence-settles",
        "CLAIMS.md": "7-prediction-claims--evidence",
        "SYSTEMS.md": "8-systems-gallery",
        "TAXONOMY.md": "02-vocabulary-and-taxonomy",
        "WORKFLOW.md": "9-how-to-update-this-survey",
        "STACK.md": "56-stack-reshape-sw--hw-codesign",
    }

    def resolve(match: re.Match[str]) -> str:
        label, target = match.groups()
        if target.startswith(("https://", "http://", "mailto:", "#")):
            return match.group(0)
        relative, _, fragment = target.partition("#")
        path = (source.parent / relative).resolve()
        if path in sections:
            return f"[{label}](#{fragment or sections[path]})"
        if path.name in legacy:
            return f"[{label}](#{legacy[path.name]})"
        if path.parent == ROOT / "reference" / "publications" and path.is_file():
            digest = path.read_text(encoding="utf-8-sig")
            primary = re.search(r"\| \*\*Link\*\* \|.*?\]\((https?://[^)]+)\)", digest)
            if primary:
                return f"[{label}]({primary[1]})"
        if path == ROOT / "reference" / "publications":
            return f"[{label}](#publications-index)"
        # Non-inlined maintenance files remain named, rather than becoming broken file URLs.
        return label

    return re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", resolve, text)


def publication_appendix(text: str) -> str:
    """Keep the full catalog while giving its seven-column source table a readable print layout."""
    groups: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7 or cells[0] == "Year":
            continue
        year, kind, group, org, publisher, digest, source = cells
        title = re.search(r"\[([^\]]+)\]\([^)]+\)", digest)
        url = re.search(r"\]\((https?://[^)]+)\)", source)
        if not title or not url:
            raise ValueError(f"Malformed publication index row: {line}")
        groups.setdefault(group, []).append(
            f"| {year}; {kind} | [{title[1]}]({url[1]}) | {org}. Published by {publisher}. |"
        )
    parts = [
        "Each title opens its primary source. The complete source digests remain in the repository. "
        "Multiple records about one system are one evidence family; the catalog is not a count of independent confirmations.",
        '<div class="source-index">',
    ]
    for group, rows in groups.items():
        table = "\n".join(["| Date and type | Source | Organization and publisher |",
                           "|---|---|---|", *rows])
        parts.extend([f"### {group}", table])
    parts.extend(["</div>", f"**Total: {sum(map(len, groups.values()))} source digests.**"])
    return "\n\n".join(parts)


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
        if path.name == "INDEX.md":
            body = publication_appendix(body)
        body = rewrite_links(body, path)
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
