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
import urllib.error
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
CORE = [
    "compiler", "superoptim", "autotun", "auto-tun", "autoschedul", "kernel", "megakernel",
    "mega-kernel", "triton", "mlir", "llvm", "ptx", "tensor program", "tensor compiler",
    "equality saturation", "e-graph", "egraph", "lowering", "scheduling language", "halide",
    "tvm", "xla", "inductor", "torch.compile", "cost model", "cuda", "tile",
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


DIAG: list[str] = []


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)
    DIAG.append(msg)


def get(url: str, timeout: int = 40, retries: int = 2) -> bytes | None:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:  # noqa: PERF203
            log(f"  HTTP {e.code} ({attempt + 1}/{retries + 1}): {url[:110]}")
            if e.code in (403, 404, 429):
                return None
            time.sleep(2 + 3 * attempt)
        except Exception as e:  # noqa: BLE001
            log(f"  fetch failed ({attempt + 1}/{retries + 1}): {url[:110]} -> {e}")
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
                core_title = [k for k in CORE if k in title.lower()]
                core_abs = [k for k in CORE if k in summ[:1500].lower()]
                if core_title or (len(core_abs) >= 2 and len(hits) >= 3):
                    out.append({"channel": "arxiv", "id": aid, "title": title, "date": pub,
                                "url": f"https://arxiv.org/abs/{aid.split('v')[0]}",
                                "why": ", ".join(hits[:6]), "cat": cat})
            if stop:
                break
            start += 100
            time.sleep(3)  # arXiv API etiquette
    return out


# --------------------------------------------------------------------------- venues
TOC = {  # DBLP table-of-contents keys; {y} is the year, {yy} the two-digit year
    "OSDI": ["db/conf/osdi/osdi{y}"], "SOSP": ["db/conf/sosp/sosp{y}"],
    "ASPLOS": ["db/conf/asplos/asplos{y}", "db/conf/asplos/asplos{y}-1", "db/conf/asplos/asplos{y}-2",
               "db/conf/asplos/asplos{y}-3", "db/conf/asplos/asplos{y}-4"],
    "PLDI": ["db/conf/pldi/pldi{y}", "db/journals/pacmpl/pacmpl{v}"], "CGO": ["db/conf/cgo/cgo{y}"],
    "CC": ["db/conf/cc/cc{y}"], "MLSys": ["db/conf/mlsys/mlsys{y}"], "ISCA": ["db/conf/isca/isca{y}"],
    "MICRO": ["db/conf/micro/micro{y}"], "EuroSys": ["db/conf/eurosys/eurosys{y}"],
    "SC": ["db/conf/sc/sc{y}"], "PPoPP": ["db/conf/ppopp/ppopp{y}"], "ATC": ["db/conf/usenix/usenix{y}"],
    "HPCA": ["db/conf/hpca/hpca{y}"], "ICML": ["db/conf/icml/icml{y}"], "NeurIPS": ["db/conf/nips/neurips{y}"],
    "ICLR": ["db/conf/iclr/iclr{y}"], "EMNLP": ["db/conf/emnlp/emnlp{y}"], "OOPSLA": ["db/journals/pacmpl/pacmpl{v}"],
}


def _dblp_toc_api(key: str) -> list[dict] | None:
    """DBLP search API with a toc: query; returns hits or None on failure."""
    q = urllib.parse.quote(f"toc:{key}.bht:", safe="")
    data = get(f"https://dblp.org/search/publ/api?q={q}&h=1000&format=json", timeout=40, retries=1)
    if not data:
        return None
    try:
        j = json.loads(data)
        hits = j["result"]["hits"].get("hit", []) or []
        return [h.get("info", {}) for h in hits]
    except Exception as e:  # noqa: BLE001
        log(f"  dblp api parse failed for {key}: {e}; first bytes: {data[:80]!r}")
        return None


USENIX = {"OSDI": "osdi{yy}", "ATC": "atc{yy}"}


def _usenix_program(name: str, y: int) -> list[str]:
    slug = USENIX[name].format(yy=str(y)[2:])
    data = get(f"https://www.usenix.org/conference/{slug}/technical-sessions", timeout=40, retries=1)
    if not data:
        return []
    html = data.decode("utf-8", "ignore")
    titles = re.findall(r'<h2[^>]*class="[^"]*node-title[^"]*"[^>]*>\s*<a[^>]*>(.*?)</a>', html, re.S)
    if not titles:
        titles = re.findall(r'<a href="/conference/' + slug + r'/presentation/[^"]+">(.*?)</a>', html, re.S)
    titles = [re.sub(r"<[^>]+>", "", t).strip() for t in titles]
    log(f"  usenix {name} {y}: {len(html)} bytes, {len(titles)} titles")
    return titles


def venue_candidates(years: list[int]) -> list[dict]:
    out = []
    for name, keys in TOC.items():
        for y in years:
            got = 0
            for k in keys:
                key = k.format(y=y, yy=str(y)[2:], v=y - 2016)
                infos = _dblp_toc_api(key)
                if infos is None:
                    continue
                got += len(infos)
                for info in infos:
                    title = (info.get("title") or "").rstrip(".").strip()
                    kh = keyword_hit(title)
                    if not kh:
                        continue
                    doi = info.get("doi", "") or ""
                    out.append({"channel": "venue", "id": doi, "title": title, "date": str(info.get("year", y)),
                                "url": info.get("ee", "") or (f"https://doi.org/{doi}" if doi else ""),
                                "why": f"{name} {y}: " + ", ".join(kh[:5])})
                time.sleep(1.5)
            log(f"  venue {name} {y}: {got} dblp entries")
            if got == 0 and name in USENIX:
                for title in _usenix_program(name, y):
                    kh = keyword_hit(title)
                    if kh:
                        out.append({"channel": "venue", "id": "", "title": title, "date": str(y),
                                    "url": f"https://www.usenix.org/conference/{USENIX[name].format(yy=str(y)[2:])}/technical-sessions",
                                    "why": f"{name} {y} (USENIX program): " + ", ".join(kh[:5])})
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
        w = None
        wq = get(f"https://api.openalex.org/works/https://arxiv.org/abs/{aid}?select=id,cited_by_api_url,title", retries=0)
        if wq:
            try:
                w = json.loads(wq)
            except Exception:  # noqa: BLE001
                w = None
        if not w or not w.get("cited_by_api_url"):
            # fall back to a title search using the digest's H1
            h1 = ""
            for p2 in PUBS.glob("*.md"):
                t2 = p2.read_text(encoding="utf-8", errors="ignore")
                if aid in t2:
                    h1 = t2.splitlines()[0].lstrip("# ").split("(")[0].strip()
                    break
            if not h1:
                continue
            sq = get("https://api.openalex.org/works?search=" + urllib.parse.quote(h1) + "&per-page=1&select=id,cited_by_api_url,title", retries=0)
            try:
                res0 = json.loads(sq).get("results", []) if sq else []
            except Exception:  # noqa: BLE001
                res0 = []
            if not res0:
                continue
            w = res0[0]
        cb = w.get("cited_by_api_url")
        if not cb:
            log(f"  cites {aid}: no cited_by url")
            continue
        data = get(cb + f"&per-page=100&filter=from_publication_date:{since.isoformat()}&select=id,title,doi,publication_date,primary_location")
        if not data:
            continue
        try:
            res = json.loads(data).get("results", [])
        except Exception:  # noqa: BLE001
            continue
        log(f"  cites {aid}: {len(res)} citing works since {since}")
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
            recent_created = bool(created) and dt.date.fromisoformat(created) >= since
            recent_push = bool(pushed) and dt.date.fromisoformat(pushed) >= since
            kh = keyword_hit(rp.get("name", "") + " " + desc)
            if known(idx, gh=full):
                continue
            core = [k for k in CORE if k in (rp.get("name", "") + " " + desc).lower()]
            if (recent_created and (kh or rp.get("stargazers_count", 0) >= 20)) or (recent_push and core and rp.get("stargazers_count", 0) >= 10):
                out.append({"channel": "github", "id": full, "title": f"{full}: {desc}"[:160],
                            "date": created, "url": rp.get("html_url", ""),
                            "why": f"{'new' if recent_created else 'active'} repo in tracked org {org}; stars {rp.get('stargazers_count', 0)}; pushed {pushed}"})
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
    per = {}
    for c in cands:
        per[c["channel"]] = per.get(c["channel"], 0) + 1
    lines += ["## Channel diagnostics", "", f"Raw candidates per channel: {json.dumps(per)}", "",
              "Fetch log (failures and venue page sizes):", ""]
    lines += [f"- {d}" for d in DIAG if any(t in d for t in ("HTTP", "failed", "venue ", "usenix ", "cites ", "dblp"))][:160]
    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out} ({len(new)} new candidates)")
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
