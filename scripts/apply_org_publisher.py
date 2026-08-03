#!/usr/bin/env python3
"""Add Org + Publisher fields to digests and regenerate INDEX columns."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publications"
INDEX = PUB / "INDEX.md"

# filename -> (org, publisher)
# Org = company/university that produced the work (primary affiliations)
# Publisher = venue, blog host, forge, or preprint host
META: dict[str, tuple[str, str]] = {
    # Surveys & vision
    "new-compiler-stack-survey.md": ("ICT, CAS · UCAS · University of Leeds", "arXiv"),
    "compiler-next.md": ("Queen's University", "arXiv"),
    "mlir-formal-theories.md": ("Qualcomm Technologies International", "arXiv"),
    "compiler-2.0-cgo2026.md": ("MIT CSAIL", "ACM/IEEE Ken Kennedy Award · HPCA/CGO/PPoPP/CC 2026"),
    "compiler-2.0-cgo2022.md": ("MIT CSAIL", "CGO 2022 · YouTube"),
    "compiler-2.0-modernize-ml.md": ("MIT CSAIL", "ACM CC 2020"),
    "compiler-2.0-mocha-aarno.md": ("Aarno Labs · MIT · UIUC (DARPA MOCHA)", "Aarno Labs / DARPA"),
    "automated-kernel-generation-survey.md": ("BAAI · PKU · HKUST(GZ) et al.", "arXiv"),
    # Classic DL compilers
    "tvm-osdi18.md": ("UW · AWS · Berkeley et al.", "USENIX OSDI 2018"),
    "ansor-osdi20.md": ("UW · AWS · OctoML et al.", "USENIX OSDI 2020"),
    "tvm-ansor-blog.md": ("Apache TVM", "Apache TVM blog"),
    "flextensor-asplos20.md": ("Peking University et al.", "ACM ASPLOS 2020"),
    "tensorir-asplos.md": ("UW · AWS · OctoML et al.", "ACM ASPLOS 2023"),
    "mlir-arxiv.md": ("Google · multi-institution", "arXiv (MLIR)"),
    "stablehlo-roadmap.md": ("OpenXLA / Google", "OpenXLA"),
    "helion-blog.md": ("Meta (PyTorch)", "PyTorch blog"),
    "helion-github.md": ("Meta (PyTorch)", "GitHub"),
    # MLGO & RL gyms
    "mlgo-paper.md": ("Google · CMU", "arXiv"),
    "mlgo-google-blog.md": ("Google Research", "Google Research blog"),
    "mlgo-infoq.md": ("InfoQ (covering Google MLGO)", "InfoQ"),
    "mlgo-llvm-docs.md": ("LLVM / Google MLGO", "LLVM docs"),
    "compilergym.md": ("Meta FAIR", "GitHub"),
    "llvm-gsoc-pass-ordering.md": ("LLVM community (GSoC)", "LLVM Discourse"),
    # Foundation LLMs
    "llm-for-compiler-opt-2023.md": ("Meta", "arXiv"),
    "meta-llm-compiler.md": ("Meta", "arXiv"),
    "meta-llm-compiler-page.md": ("Meta AI", "Meta AI Research"),
    "cummins-linkedin-llm-compiler.md": ("Meta (Chris Cummins)", "LinkedIn"),
    "compiler-feedback-llms.md": ("Meta", "arXiv"),
    "hn-llm-compiler-opt-2023.md": ("Hacker News community", "Hacker News"),
    "hn-meta-llm-compiler-40819479.md": ("Hacker News community", "Hacker News"),
    "hn-meta-llm-compiler-40812436.md": ("Hacker News community", "Hacker News"),
    # Agentic & RL
    "compiler-r1.md": ("ISCAS · UCAS", "arXiv"),
    "compiler-r1-github.md": ("ISCAS / Mind4Compiler", "GitHub"),
    "llm-veriopt.md": ("multi-institution", "CGO 2026"),
    "magellan.md": ("Google DeepMind / Google", "arXiv"),
    "magellan-llvm-slides.md": ("Google DeepMind / Google", "LLVM Developers' Meeting 2025"),
    "alphaevolve-paper.md": ("Google DeepMind", "arXiv"),
    "alphaevolve-blog.md": ("Google DeepMind", "DeepMind blog"),
    "awarecompiler.md": ("ISCAS · UCAS · NTU Singapore", "arXiv"),
    "autopass.md": ("Shaanxi Normal University · Northwest University · University of Leeds", "arXiv"),
    "hintpilot.md": ("Zhejiang University · Purdue", "arXiv"),
    "acclaim.md": ("AWS AI · Georgia Tech", "arXiv"),
    "acclaim-github.md": ("Amazon Science / AWS AI", "GitHub"),
    "generative-compilation.md": ("ETH Zurich · INSAIT/Sofia University · UC Berkeley", "arXiv"),
    # GPU kernels
    "kernelbench.md": ("Stanford · Princeton", "arXiv"),
    "kernelbench-blog.md": ("Stanford (Scaling Intelligence)", "Stanford blog"),
    "kernelbench-github.md": ("Stanford (Scaling Intelligence)", "GitHub"),
    "kernelbench-x.md": ("Tsinghua University", "arXiv"),
    "geak.md": ("AMD", "arXiv"),
    "geak-rocm-blog.md": ("AMD", "AMD ROCm blog"),
    "geak-github.md": ("AMD AGI", "GitHub"),
    "geak-v3-rocm-blog.md": ("AMD", "AMD ROCm blog"),
    "kernelllm.md": ("Meta", "Hugging Face"),
    "reasoning-compiler.md": ("UC San Diego", "arXiv"),
    "agentcompile.md": ("City University of Hong Kong", "arXiv"),
    "mliragent.md": ("UC Berkeley (ucb-bar)", "GitHub"),
    "autokernel.md": ("RightNow AI", "arXiv"),
    "autokernel-github.md": ("RightNow AI", "GitHub"),
    "kernel-forge.md": ("University of Michigan", "arXiv"),
    "kernelblaster.md": ("NVIDIA · UC Berkeley", "arXiv"),
    "awesome-llm-kernel-generation.md": ("FlagOpen / flagos-ai", "GitHub"),
    "kernelagent.md": ("Meta (PyTorch)", "GitHub"),
    # Company infra
    "cuda-tile-blog.md": ("NVIDIA", "NVIDIA Developer blog"),
    "cuda-tile-cpp.md": ("NVIDIA", "NVIDIA Developer blog"),
    "cuda-13-3-compileiq.md": ("NVIDIA", "NVIDIA Developer blog"),
    "compileiq-deep-dive.md": ("NVIDIA", "NVIDIA Developer blog"),
    "compileiq-docs.md": ("NVIDIA", "NVIDIA docs"),
    "compileiq-docs-expectations.md": ("NVIDIA", "NVIDIA docs"),
    "compileiq-github.md": ("NVIDIA", "GitHub"),
    "modular-mlir-blog.md": ("Modular", "Modular blog"),
    "anthropic-claude-c-compiler.md": ("Anthropic", "Anthropic Engineering"),
    "ars-claude-c-compiler.md": ("Ars Technica (covering Anthropic)", "Ars Technica"),
    "modular-claude-c-compiler.md": ("Modular", "Modular blog"),
    "hn-claude-c-compiler.md": ("Hacker News community", "Hacker News"),
    "trt-llm-claude-agents-pr.md": ("NVIDIA", "GitHub (TensorRT-LLM)"),
    # Forums
    "llvm-ml-workshop-2025.md": ("LLVM community", "LLVM Discourse"),
    "llvm-ml-workshop-2026.md": ("LLVM community", "LLVM Discourse"),
    "llvm-ml-workshop-2023.md": ("LLVM community", "LLVM Discourse"),
    "llvm-agent-pr-review.md": ("LLVM community", "LLVM Discourse"),
    "compilers-magellan-notice.md": ("comp.compilers community", "comp.compilers"),
    "ieee-pulse-llm-compilers.md": ("IEEE EMBS Pulse", "IEEE Pulse"),
    "moonlight-magellan-review.md": ("Moonlight", "Moonlight"),
    "mlgo-emitc-rfc.md": ("Google / LLVM community", "LLVM Discourse"),
    # Correctness / review / code
    "souper.md": ("Google", "GitHub"),
    "archer-paper.md": ("CUHK (cuhk-s3)", "arXiv"),
    "archer-github.md": ("CUHK (cuhk-s3)", "GitHub"),
    "gerrit-ai-code-review.md": ("Google", "Gerrit googlesource"),
    "reviewai-gerrit-plugin.md": ("Amarula Solutions", "GitHub"),
    "gerritforge-ai-review-provider.md": ("GerritForge", "GitHub"),
    "openevolve.md": ("Algorithmic SuperIntelligence", "GitHub"),
    "heurigym.md": ("Cornell University", "GitHub"),
    "claudes-c-compiler-github.md": ("Anthropic", "GitHub"),
    "ml-compiler-opt-github.md": ("Google", "GitHub"),
    "hintpilot-github.md": ("Zhejiang University (ZJU-PL)", "GitHub"),
    "llvm-project-github.md": ("LLVM Foundation / community", "GitHub"),
    # HW codesign
    "tritorx.md": ("Meta", "arXiv"),
    "kernelevolve.md": ("Meta", "ISCA 2026 · arXiv"),
    "kernelevolve-blog.md": ("Meta", "Engineering at Meta"),
    "compiler-grounded-triton-npu.md": ("Huawei Technologies", "arXiv"),
    "kforge.md": ("Gimlet Labs", "MLArchSys @ ISCA 2026 · arXiv"),
}


def upsert_fields(text: str, org: str, publisher: str) -> str:
    """Insert or replace Org/Publisher rows after Year (or Type if no Year)."""
    # Drop existing Org/Publisher rows
    text = re.sub(r"\| \*\*Org\*\* \|[^\n]*\n", "", text)
    text = re.sub(r"\| \*\*Publisher\*\* \|[^\n]*\n", "", text)

    org_row = f"| **Org** | {org} |\n"
    pub_row = f"| **Publisher** | {publisher} |\n"
    insert = org_row + pub_row

    m = re.search(r"(\| \*\*Year\*\* \|[^\n]*\n)", text)
    if m:
        pos = m.end()
        return text[:pos] + insert + text[pos:]
    m = re.search(r"(\| \*\*Type\*\* \|[^\n]*\n)", text)
    if m:
        pos = m.end()
        return text[:pos] + insert + text[pos:]
    # Fallback: after field table header separator
    m = re.search(r"(\|---\|---\|\n)", text)
    if m:
        pos = m.end()
        return text[:pos] + insert + text[pos:]
    raise ValueError("no insertion point")


def rebuild_index() -> None:
    index_text = INDEX.read_text(encoding="utf-8")

    # New 7-column rows: Year | Kind | Group | Org | Publisher | Digest | Source
    row7 = re.compile(
        r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| [^|]+ \| [^|]+ \| "
        r"(\[[^\]]+\]\(([a-zA-Z0-9_./+-]+\.md)\)[^\|]*) \| (\[[^\]]+\]\([^)]+\)) \|$",
        re.M,
    )
    # Legacy 5-column rows: Year | Kind | Group | Digest | Source
    row5 = re.compile(
        r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \| "
        r"(\[[^\]]+\]\(([a-zA-Z0-9_./+-]+\.md)\)[^\|]*) \| (\[[^\]]+\]\([^)]+\)) \|$",
        re.M,
    )

    def fmt(year: str, kind: str, group: str, digest_cell: str, fname: str, source: str) -> str:
        org, publisher = META.get(Path(fname).name, ("—", "—"))
        return (
            f"| {year.strip()} | {kind.strip()} | {group.strip()} | {org} | {publisher} | "
            f"{digest_cell.strip()} | {source.strip()} |"
        )

    def repl7(m: re.Match[str]) -> str:
        year, kind, group, digest_cell, fname, source = m.groups()
        return fmt(year, kind, group, digest_cell, fname, source)

    def repl5(m: re.Match[str]) -> str:
        year, kind, group, digest_cell, fname, source = m.groups()
        return fmt(year, kind, group, digest_cell, fname, source)

    new_body = row7.sub(repl7, index_text)
    new_body = row5.sub(repl5, new_body)
    new_body = new_body.replace(
        "| Year | Kind | Group | Digest | Source |\n|---|---|---|---|---|",
        "| Year | Kind | Group | Org | Publisher | Digest | Source |\n|---|---|---|---|---|---|---|",
    )
    new_body = re.sub(
        r"\| Year \| Kind \| Group \| Digest \| Source \|\n\|---\|---\|---\|---\|---\|",
        "| Year | Kind | Group | Org | Publisher | Digest | Source |\n|---|---|---|---|---|---|---|",
        new_body,
    )
    INDEX.write_text(new_body, encoding="utf-8")


def main() -> int:
    missing = []
    updated = 0
    for p in sorted(PUB.glob("*.md")):
        if p.name in {"INDEX.md", "_TEMPLATE.md"}:
            continue
        if p.name not in META:
            missing.append(p.name)
            continue
        org, publisher = META[p.name]
        text = p.read_text(encoding="utf-8")
        new = upsert_fields(text, org, publisher)
        if new != text:
            p.write_text(new, encoding="utf-8")
            updated += 1
        else:
            # still rewrite to ensure present
            p.write_text(new, encoding="utf-8")
            updated += 1

    rebuild_index()
    print(f"updated_digests={updated}")
    if missing:
        print("MISSING META for:")
        for m in missing:
            print(" ", m)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
