#!/usr/bin/env python3
"""Build next-gen-ai-compiler-survey.pdf from living survey docs."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from assemble import OUT, ROOT, assemble

STYLE = Path(__file__).resolve().parent / "style.css"
PDF_NAME = "next-gen-ai-compiler-survey.pdf"


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def md_to_html(bundle: Path, html: Path) -> None:
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
            "title=Next-Generation AI Compiler Survey",
            f"--css={STYLE}",
            "-o",
            str(html),
        ]
    )
    # Ensure CSS is embedded for WeasyPrint/file:// reliability.
    css = STYLE.read_text(encoding="utf-8")
    text = html.read_text(encoding="utf-8")
    if "</head>" in text and "<style>" not in text:
        text = text.replace("</head>", f"<style>\n{css}\n</style>\n</head>")
        html.write_text(text, encoding="utf-8")



def normalize_pdf(pdf: Path) -> None:
    """Rewrite via pypdf for broader viewer compatibility (e.g. GitHub)."""
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        return
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Next-Generation AI Compiler Survey",
        "/Producer": "pypdf",
    })
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
            "--print-media-type",
            str(html),
            str(pdf),
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--engine",
        choices=("weasyprint", "wkhtmltopdf"),
        default="weasyprint",
        help="PDF engine (default: weasyprint)",
    )
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        print("ERROR: pandoc is required", file=sys.stderr)
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    bundle = assemble()
    html = OUT / "survey.html"
    pdf = OUT / PDF_NAME

    md_to_html(bundle, html)

    try:
        if args.engine == "weasyprint":
            html_to_pdf_weasy(html, pdf)
        else:
            html_to_pdf_wkhtml(html, pdf)
    except Exception as exc:  # noqa: BLE001 — surface engine errors clearly
        print(f"ERROR: PDF engine failed: {exc}", file=sys.stderr)
        if args.engine == "weasyprint" and shutil.which("wkhtmltopdf"):
            print("Retrying with wkhtmltopdf…", file=sys.stderr)
            html_to_pdf_wkhtml(html, pdf)
        else:
            return 1

    normalize_pdf(pdf)

    print(f"Bundle : {bundle.relative_to(ROOT)}")
    print(f"HTML   : {html.relative_to(ROOT)}")
    print(f"PDF    : {pdf.relative_to(ROOT)} ({pdf.stat().st_size // 1024} KiB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
