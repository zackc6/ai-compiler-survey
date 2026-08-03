#!/usr/bin/env python3
"""Translate assembled English survey markdown to zh-CN / zh-TW."""

from __future__ import annotations

import re
import time
from pathlib import Path

from glossary import apply_glossary, protect, unprotect
from opencc import OpenCC

# Skip translating fenced code and inline-heavy lines where possible.
FENCE_RE = re.compile(r"(```.*?```)", re.DOTALL)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HTML_RE = re.compile(r"(<[^>]+>)")

MAX_CHUNK = 3500


def _translate_plain(text: str, translator) -> str:
    if not text.strip():
        return text
    protected, mapping = protect(text)
    # Apply glossary on English before MT for critical phrases still present.
    # (Most glossary terms already replaced in pre-pass on full doc.)
    chunks: list[str] = []
    buf = ""
    for para in protected.split("\n"):
        candidate = (buf + "\n" + para) if buf else para
        if len(candidate) > MAX_CHUNK and buf:
            chunks.append(buf)
            buf = para
        else:
            buf = candidate
    if buf:
        chunks.append(buf)

    out_parts: list[str] = []
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            out_parts.append(chunk)
            continue
        # Retry a few times on transient MT errors.
        last_err: Exception | None = None
        for attempt in range(4):
            try:
                translated = translator.translate(chunk)
                out_parts.append(translated)
                last_err = None
                break
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                time.sleep(1.5 * (attempt + 1))
        if last_err is not None:
            # Keep English chunk rather than failing the whole build.
            out_parts.append(chunk)
        if i + 1 < len(chunks):
            time.sleep(0.35)
    return unprotect("\n".join(out_parts), mapping)


def translate_markdown(md: str, target: str = "zh-CN") -> str:
    """target: zh-CN or zh-TW. English source → zh-CN via MT, then OpenCC for TW."""
    from deep_translator import GoogleTranslator

    # Pre-replace glossary on English source for better domain wording.
    md = apply_glossary(md)

    translator = GoogleTranslator(source="en", target="zh-CN")

    # Preserve fenced code blocks.
    pieces = FENCE_RE.split(md)
    out: list[str] = []
    for i, piece in enumerate(pieces):
        if i % 2 == 1:  # code fence
            out.append(piece)
            continue
        # Preserve HTML tags by splitting.
        html_parts = HTML_RE.split(piece)
        rebuilt: list[str] = []
        for j, hp in enumerate(html_parts):
            if j % 2 == 1:
                rebuilt.append(hp)
                continue
            # Translate link text but keep URLs.
            def repl_link(m: re.Match[str]) -> str:
                label = m.group(1)
                url = m.group(2)
                if label.startswith("http") or label.endswith(".md"):
                    return m.group(0)
                tlabel = _translate_plain(label, translator)
                return f"[{tlabel}]({url})"

            with_links = LINK_RE.sub(repl_link, hp)
            # Translate remaining non-empty segments line-wise in batches.
            rebuilt.append(_translate_plain(with_links, translator))
        out.append("".join(rebuilt))

    zh_cn = "".join(out)
    if target == "zh-CN":
        return zh_cn
    if target == "zh-TW":
        return OpenCC("s2twp").convert(zh_cn)
    raise ValueError(f"unsupported target {target}")


def translate_file(src: Path, dest: Path, target: str) -> Path:
    text = src.read_text(encoding="utf-8")
    dest.write_text(translate_markdown(text, target=target), encoding="utf-8")
    return dest
