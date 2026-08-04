#!/usr/bin/env python3
"""Build survey PDFs in English, Simplified Chinese, and Traditional Chinese."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from assemble import COVER, LANGS, OUT, PDF_NAMES, ROOT, assemble, cover_md
from datetime import date

STYLE = Path(__file__).resolve().parent / "style.css"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def md_to_html(bundle: Path, html: Path, title: str) -> None:
    run(
        [
            "pandoc",
            str(bundle),
            "-f",
            "markdown+pipe_tables+fenced_code_blocks+gfm_auto_identifiers",
            "-t",
            "html5",
            "--standalone",
            "--metadata",
            f"title={title}",
            f"--css={STYLE}",
            "-o",
            str(html),
        ]
    )
    css = STYLE.read_text(encoding="utf-8")
    text = html.read_text(encoding="utf-8")
    if "</head>" in text and "<style>" not in text:
        text = text.replace("</head>", f"<style>\n{css}\n</style>\n</head>")
        html.write_text(text, encoding="utf-8")


def normalize_pdf(pdf: Path, title: str) -> None:
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({"/Title": title, "/Producer": "pypdf"})
    tmp = pdf.with_suffix(".tmp.pdf")
    with tmp.open("wb") as f:
        writer.write(f)
    tmp.replace(pdf)


def html_to_pdf_weasy(html: Path, pdf: Path) -> None:
    from weasyprint import HTML

    HTML(filename=str(html)).write_pdf(str(pdf))


def html_to_pdf_wkhtml(html: Path, pdf: Path) -> None:
    exe = shutil.which("wkhtmltopdf")
    if not exe:
        raise RuntimeError("wkhtmltopdf not found on PATH")
    run(
        [
            exe,
            "--enable-local-file-access",
            "--page-size",
            "A4",
            "--margin-top",
            "14mm",
            "--margin-bottom",
            "16mm",
            "--margin-left",
            "12mm",
            "--margin-right",
            "12mm",
            str(html),
            str(pdf),
        ]
    )


def render_pdf(bundle: Path, lang: str, engine: str) -> Path:
    title = COVER[lang]["title"]
    html = OUT / f"survey.{lang}.html"
    pdf = OUT / PDF_NAMES[lang]
    md_to_html(bundle, html, title=title)
    try:
        if engine == "weasyprint":
            html_to_pdf_weasy(html, pdf)
        else:
            html_to_pdf_wkhtml(html, pdf)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: PDF engine failed ({lang}): {exc}", file=sys.stderr)
        if engine == "weasyprint" and shutil.which("wkhtmltopdf"):
            print("Retrying with wkhtmltopdf…", file=sys.stderr)
            html_to_pdf_wkhtml(html, pdf)
        else:
            raise
    normalize_pdf(pdf, title=title)
    print(f"PDF[{lang}]: {pdf.relative_to(ROOT)} ({pdf.stat().st_size // 1024} KiB)")
    return pdf


def swap_cover(md: str, lang: str) -> str:
    """Replace leading cover div with locale cover."""
    today = date.today().isoformat()
    new_cover = cover_md(today, lang=lang).strip()
    start = md.find('<div class="cover">')
    end = md.find("</div>\n", md.find('<div class="verdict">'))
    if start < 0 or end < 0:
        return new_cover + "\n\n" + md
    # closing </div> of cover after verdict's </div>
    end = md.find("</div>", end + 1)
    end = md.find("\n", end) + 1
    return md[:start] + new_cover + "\n" + md[end:]


def _english_body(en_bundle: Path) -> str:
    en_text = en_bundle.read_text(encoding="utf-8")
    marker = '<div class="section-break"></div>'
    idx = en_text.find(marker)
    return en_text[idx:] if idx >= 0 else en_text


def write_locale_bundle(lang: str, translated_body: str) -> Path:
    from assemble import SECTION_TITLES

    today = date.today().isoformat()
    bundle_text = cover_md(today, lang=lang) + "\n" + translated_body
    if "publish/build_pdf.py" not in bundle_text[-800:]:
        bundle_text += (
            "\n---\n\n"
            f"## {SECTION_TITLES[lang]['Export notes']}\n\n"
            f"{COVER[lang]['export_notes']}"
        )
    out = OUT / f"survey-bundle.{lang}.md"
    out.write_text(bundle_text, encoding="utf-8")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--engine",
        choices=("weasyprint", "wkhtmltopdf"),
        default="weasyprint",
        help="PDF engine (default: weasyprint)",
    )
    parser.add_argument(
        "--lang",
        choices=(*LANGS, "all"),
        default="en",
        help="Language to build (default: en). Use --lang all for zh-CN/zh-TW too; only en is kept in out/ by default workflow.",
    )
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        print("ERROR: pandoc is required", file=sys.stderr)
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    langs = list(LANGS) if args.lang == "all" else [args.lang]

    en_bundle = assemble("en")
    (OUT / "survey-bundle.md").write_text(
        en_bundle.read_text(encoding="utf-8"), encoding="utf-8"
    )

    zh_cn_body: str | None = None
    built: list[Path] = []
    for lang in langs:
        try:
            if lang == "en":
                bundle = en_bundle
            else:
                from translate import translate_markdown
                from opencc import OpenCC

                if zh_cn_body is None:
                    print("Translating English → zh-CN (several minutes)…")
                    zh_cn_body = translate_markdown(
                        _english_body(en_bundle), target="zh-CN"
                    )
                if lang == "zh-CN":
                    body = zh_cn_body
                else:
                    print("Converting zh-CN → zh-TW via OpenCC…")
                    body = OpenCC("s2twp").convert(zh_cn_body)
                bundle = write_locale_bundle(lang, body)
            built.append(render_pdf(bundle, lang, args.engine))
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR building {lang}: {exc}", file=sys.stderr)
            return 1

    # Drop stale duplicate if an older .en.pdf alias remains.
    stale_en = OUT / "next-gen-ai-compiler-survey.en.pdf"
    if stale_en.exists() and PDF_NAMES["en"] != stale_en.name:
        stale_en.unlink()
        print(f"removed stale alias: {stale_en.relative_to(ROOT)}")

    print("Built:", ", ".join(p.name for p in built))
    return 0


if __name__ == "__main__":
    sys.exit(main())
