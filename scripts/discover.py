#!/usr/bin/env python3
"""Mechanical source discovery for the survey.

Enumerates candidate sources from structured feeds instead of web search, which
is where recent sweeps missed TileLoom, TASO/Tensat, PeepholeBench, LLVM-Bench,
CIRBench and TileFoundry. Four channels:

  arxiv   - arXiv API listings by category and keyword, over a date window
  venues  - DBLP tables of contents for a fixed venue set (OSDI, SOSP, ASPLOS,
            PLDI, CGO, MLSys, ISCA, MICRO, ICML, NeurIPS, ICLR, EMNLP)
  cites   - OpenAlex "cited by" for the Tier A digests (citation expansion)
  github  - new or recently pushed repositories in organizations the survey
            already references (TileFoundry-class misses), plus PyPI releases
            for known packages

Every candidate is deduplicated against reference/publications/INDEX.md by
arXiv id, DOI, GitHub path and normalized title. Output is a Markdown ledger
under reference/discovery/ that the agents triage (INCLUDE / EXCLUDE / PENDING)
in the Review thread. The script never edits the index.

Network: run it where arxiv.org, dblp.org, api.openalex.org, api.github.com and
pypi.org are reachable (the GitHub Actions runner). Each channel fails soft.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "reference" / "publications" / "INDEX.md"
REPOS = ROOT / "reference" / "repos.md"
PUBS = ROOT / "reference" / "publications"
OUT_DIR = ROOT / "reference" / "discovery"

UA = {"User-Agent": "ai-compiler-survey-discovery/1.0 (github.com/zackc6/ai-compiler-survey)"}

# Topic vocabulary. Deliberately broad: titles rarely say "LLM" or "agent".
KEYWORDS = [
    "compiler", "superoptim", "autotun", "auto-tun", "autoschedul", "kernel",
    "megakernel", "mega-kernel", "tile", "triton", "mlir", "llvm", "ptx", "cuda",
    "tensor program", "tensor compiler", "code generation", "program synthesis",
    "equality saturation", "e-graph", "egraph", "rewrite", "lowering",
    "scheduling language", "halide", "tvm", "xla", "inductor", "torch.compile",
    "accelerator", "npu", "tpu", "gpu", "simulator", "cost model", "serving",
    "inference engine", "collective", "distributed training", "sharding",
    "harness", "self-improv", "agentic", "coding agent", "benchmark",
    "verification", "equivalence", "translation validation", "alive2",
]
ARXIV_CATS = ["cs.PL", "cs.DC", "cs.AR", "cs.LG", "cs.SE", "cs.PF"]
# DBLP venue keys (stream keys), checked for the current and previous year.
VENUES = {
    "OSDI": "conf/osdi", "SOSP": "conf/sosp", "ASPLOS": "conf/asplos",
    "PLDI": "conf/pldi", "CGO": "conf/cgo", "CC": "conf/cc", "MLSys": "conf/mlsys",
    "ISCA": "conf/isca", "MICRO": "conf/micro", "EuroSys": "conf/eurosys",
    "ICML": "conf/icml", "NeurIPS": "conf/nips", "ICLR": "conf/iclr",
    "EMNLP": "conf/emnlp", "OOPSLA": "journals/pacmpl", "SC": "conf/sc",
    "PPoPP": "conf/ppopp", "ATC": "conf/usenix", "HPCA": "conf/hpca",
}
PYPI_PACKAGES = ["tilefoundry", "tilelang", "tirx-harness", "kcoral", "helion", "triton",
                 "tvm", "mirage-project", "cuda-tile", "openevolve", "flashinfer"]


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def get(url: str, timeout: int = 40, retries: int = 2) -> bytes | None:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            log(f"  fetch failed ({attempt + 1}/{retries + 1}): {url[:100]} -> {e}")
            time.sleep(2 + 3 * attempt)
    return None


def norm_title(t: str) -> str:
    t = re.sub(r"[^a-z0-9 ]", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def keyword_hit(text: str) -> list[str]:
    low = text.lower()
    return [k for k in KEYWORDS if k in low]


# --------------------------------------------------------------------------- index
def load_index() -> dict:
    text = INDEX.read_text(encoding="utf-8")
    pubs = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in PUBS.glob("*.md"))
    repos = REPOS.read_text(encoding="utf-8") if REPOS.exists() else ""
    blob = text + "\n" + pubs + "\n" + repos
    arxiv_ids = {m.lower() for m in re.findall(r"(\d{4}\.\d{4,5})(?:v\d+)?", blob)}
    dois = {m.lower() for m in re.findall(r"10\.\d{4,9}/[^\s)\]|>]+", blob)}
    ghs = {m.lower() for m in re.findall(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", blob)}
    titles = set()
    for line in text.splitlines():
        m = re.search(r"\[([^\]]+)\]\([a-z0-9._-]+\.md\)", line)
        if m:
            titles.add(norm_title(m.group(1)))
    orgs = sorted({g.split("/")[0] for g in ghs})
    return {"arxiv": arxiv_ids, "doi": dois, "github": ghs, "titles": titles, "orgs": orgs}


def known(idx: dict, *, arxiv: str = "", doi: str = "", gh: str = "", title: str = "") -> bool:
    if arxiv and arxiv.lower().split("v")[0] in idx["arxiv"]:
        return True
    if doi and doi.lower() in idx["doi"]:
        return True
    if gh and gh.lower() in idx["github"]:
        return True
    if title:
        nt = norm_title(title)
        if nt in idx["titles"]:
            return True
        # loose containment for subtitle variants
        for t in idx["titles"]:
            if len(nt) > 25 and (nt in t or t in nt):
                return True
    return False


# --------------------------------------------------------------------------- arxiv
def arxiv_candidates(since: dt.date, max_per_cat: int = 400) -> list[dict]:
    out = []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for cat in ARXIV_CATS:
        start = 0
        while start < max_per_cat:
            q = urllib.parse.quote(f"cat:{cat}")
            url = (f"https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate"
                   f"&sortOrder=descending&start={start}&max_results=100")
            data = get(url)
            if not data:
                break
            root = ET.fromstring(data)
            entries = root.findall("a:entry", ns)
            if not entries:
                break
            stop = False
            for e in entries:
                pub = e.findtext("a:published", default="", namespaces=ns)[:10]
                if pub and dt.date.fromisoformat(pub) < since:
                    stop = True
                    break
                title = " ".join(e.findtext("a:title", default="", namespaces=ns).split())
                summ = e.findtext("a:summary", default="", namespaces=ns)
                aid = e.findtext("a:id", default="", namespaces=ns).rsplit("/", 1)[-1]
                hits = keyword_hit(title + " " + summ[:1500])
                if len(hits) >= 2:
                    out.append({"channel": "arxiv", "id": aid, "title": title, "date": pub,
                                "url": f"https://arxiv.org/abs/{aid.split('v')[0]}",
                                "why": ", ".join(hits[:6]), "cat": cat})
            if stop:
                break
            start += 100
            time.sleep(3)  # arXiv API etiquette
    return out


# --------------------------------------------------------------------------- venues
def venue_candidates(years: list[int]) -> list[dict]:
    out = []
    for name, key in VENUES.items():
        for y in years:
            url = (f"https://dblp.org/search/publ/api?q=streamid%3A{urllib.parse.quote(key, safe='')}"
                   f"%3A%20year%3A{y}%3A&h=1000&format=json")
            data = get(url)
            if not data:
                continue
            try:
                hits = json.loads(data)["result"]["hits"].get("hit", [])
            except Exception:  # noqa: BLE001
                continue
            for h in hits:
                info = h.get("info", {})
                title = info.get("title", "").rstrip(".")
                kh = keyword_hit(title)
                if not kh:
                    continue
                out.append({"channel": "venue", "id": info.get("doi", "") or info.get("key", ""),
                            "title": title, "date": str(info.get("year", y)),
                            "url": info.get("ee", "") or f"https://dblp.org/rec/{info.get('key','')}",
                            "why": f"{name} {y}: " + ", ".join(kh[:5])})
            time.sleep(1)
    return out


# --------------------------------------------------------------------------- citations
def cited_by_candidates(idx: dict, since: dt.date, max_seeds: int = 40) -> list[dict]:
    """OpenAlex: works citing our Tier A arXiv seeds, filtered to the window."""
    out = []
    seeds = []
    for p in sorted(PUBS.glob("*.md")):
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "| **Evidence tier** | **A**" in t:
            m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", t)
            if m:
                seeds.append(m.group(1))
    seeds = seeds[:max_seeds]
    for aid in seeds:
        wq = get(f"https://api.openalex.org/works/https://arxiv.org/abs/{aid}?select=id,cited_by_api_url,title")
        if not wq:
            continue
        try:
            w = json.loads(wq)
        except Exception:  # noqa: BLE001
            continue
        cb = w.get("cited_by_api_url")
        if not cb:
            continue
        data = get(cb + f"&per-page=100&filter=from_publication_date:{since.isoformat()}&select=id,title,doi,publication_date,primary_location")
        if not data:
            continue
        try:
            res = json.loads(data).get("results", [])
        except Exception:  # noqa: BLE001
            continue
        for r in res:
            title = r.get("title") or ""
            loc = (r.get("primary_location") or {}).get("landing_page_url") or ""
            out.append({"channel": "cites", "id": (r.get("doi") or "").replace("https://doi.org/", ""),
                        "title": title, "date": r.get("publication_date", ""), "url": loc or r.get("id", ""),
                        "why": f"cites {aid} ({(w.get('title') or '')[:50]})"})
        time.sleep(0.5)
    return out


# --------------------------------------------------------------------------- github / pypi
def github_candidates(idx: dict, since: dt.date) -> list[dict]:
    out = []
    token = os.environ.get("GITHUB_TOKEN", "")
    hdr = dict(UA)
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    for org in idx["orgs"]:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&sort=pushed"
        try:
            req = urllib.request.Request(url, headers=hdr)
            with urllib.request.urlopen(req, timeout=30) as r:
                repos = json.loads(r.read())
        except Exception:  # noqa: BLE001
            # user accounts are not orgs; try /users
            try:
                req = urllib.request.Request(f"https://api.github.com/users/{org}/repos?per_page=100&sort=pushed", headers=hdr)
                with urllib.request.urlopen(req, timeout=30) as r:
                    repos = json.loads(r.read())
            except Exception:  # noqa: BLE001
                continue
        if not isinstance(repos, list):
            continue
        for rp in repos:
            full = rp.get("full_name", "")
            created = (rp.get("created_at") or "")[:10]
            pushed = (rp.get("pushed_at") or "")[:10]
            desc = rp.get("description") or ""
            if rp.get("fork") or rp.get("archived"):
                continue
            recent = (created and dt.date.fromisoformat(created) >= since)
            kh = keyword_hit(rp.get("name", "") + " " + desc)
            if recent and (kh or rp.get("stargazers_count", 0) >= 20):
                out.append({"channel": "github", "id": full, "title": f"{full}: {desc}"[:160],
                            "date": created, "url": rp.get("html_url", ""),
                            "why": f"new repo in tracked org {org}; stars {rp.get('stargazers_count', 0)}; pushed {pushed}"})
        time.sleep(0.3)
    for pkg in PYPI_PACKAGES:
        data = get(f"https://pypi.org/pypi/{pkg}/json", timeout=20, retries=1)
        if not data:
            continue
        try:
            j = json.loads(data)
        except Exception:  # noqa: BLE001
            continue
        rel = j.get("releases", {})
        latest = None
        for ver, files in rel.items():
            for f in files:
                up = (f.get("upload_time") or "")[:10]
                if up and (latest is None or up > latest[1]):
                    latest = (ver, up)
        if latest and dt.date.fromisoformat(latest[1]) >= since:
            info = j.get("info", {})
            out.append({"channel": "pypi", "id": f"pypi:{pkg}", "title": f"{pkg} {latest[0]}: {info.get('summary','')}"[:160],
                        "date": latest[1], "url": info.get("project_url") or f"https://pypi.org/project/{pkg}/",
                        "why": "release of a tracked package"})
    return out


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD; default: 21 days ago")
    ap.add_argument("--channels", default="arxiv,venues,cites,github")
    ap.add_argument("--out", help="output ledger path")
    args = ap.parse_args()
    today = dt.date.today()
    since = dt.date.fromisoformat(args.since) if args.since else today - dt.timedelta(days=21)
    chans = set(args.channels.split(","))
    idx = load_index()
    log(f"index: {len(idx['arxiv'])} arXiv ids, {len(idx['doi'])} DOIs, {len(idx['github'])} repos, "
        f"{len(idx['titles'])} titles, {len(idx['orgs'])} orgs")

    cands: list[dict] = []
    if "arxiv" in chans:
        cands += arxiv_candidates(since)
    if "venues" in chans:
        cands += venue_candidates([today.year, today.year - 1])
    if "cites" in chans:
        cands += cited_by_candidates(idx, since)
    if "github" in chans:
        cands += github_candidates(idx, since)

    seen = set()
    new, already = [], 0
    for c in cands:
        key = (c["channel"], norm_title(c["title"])[:80])
        if key in seen:
            continue
        seen.add(key)
        aid = c["id"] if c["channel"] == "arxiv" else ""
        doi = c["id"] if c["channel"] in ("venue", "cites") and c["id"].startswith("10.") else ""
        gh = c["id"] if c["channel"] == "github" else ""
        if known(idx, arxiv=aid, doi=doi, gh=gh, title=c["title"]):
            already += 1
            continue
        new.append(c)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else OUT_DIR / f"{today.isoformat()}.md"
    by = {}
    for c in new:
        by.setdefault(c["channel"], []).append(c)
    lines = [f"# Discovery ledger — {today.isoformat()}", "",
             f"Window: since {since.isoformat()}. Channels: {', '.join(sorted(chans))}. "
             f"Candidates: {len(cands)} raw, {already} already indexed, **{len(new)} new**.", "",
             "Triage every row in the Review thread as INCLUDE (digest it), EXCLUDE (reason), or PENDING "
             "(what is missing). Mark the decision in the last column of this file in the same batch. "
             "A row left blank means the sweep is not complete.", ""]
    for ch in ("github", "pypi", "arxiv", "venue", "cites"):
        rows = by.get(ch, [])
        if not rows:
            continue
        lines += [f"## {ch} ({len(rows)})", "", "| Date | Candidate | Why it surfaced | Decision |", "|---|---|---|---|"]
        for c in sorted(rows, key=lambda r: r["date"], reverse=True):
            t = c["title"].replace("|", "/")
            lines.append(f"| {c['date']} | [{t}]({c['url']}) | {c['why']} | |")
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out} ({len(new)} new candidates)")
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
