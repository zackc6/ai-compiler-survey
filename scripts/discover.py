#!/usr/bin/env python3
"""Mechanical source discovery for the survey.

Enumerates candidate sources and changes to known systems from structured feeds, not web search, which
is where recent sweeps missed TileLoom, TASO/Tensat, PeepholeBench, LLVM-Bench,
CIRBench and TileFoundry. Seven channels:

  arxiv   - arXiv API listings by category and keyword, over a date window
  venues  - DBLP tables of contents for a fixed venue set (OSDI, SOSP, ASPLOS,
            PLDI, CGO, MLSys, ISCA, MICRO, ICML, NeurIPS, ICLR, EMNLP)
  cites   - OpenAlex "cited by" for the Tier A digests (citation expansion)
  repoevent - commit updates in already-indexed repositories (event-level, no popularity filter)
  github  - new or recently pushed repositories in organizations the survey
            already references (TileFoundry-class misses), plus PyPI releases
            for known packages
  ghsearch - GitHub repository search by topic across all owners, for new
            projects outside tracked organizations
  blogs   - RSS/Atom feeds of project blogs, forums and independent writers
            listed in reference/discovery/feeds.txt, plus Hacker News stories,
            for position pieces such as TVM's "Rethinking abstractions in the
            agentic era" that never appear on arXiv

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
# Diagnostic categories rendered into the ledger's fetch log (failures, venue sizes, and the
# recall limits of the blogs/HN/GitHub channels: truncation, star-threshold drops, unparsable pages).
DIAG_KEEP = ("HTTP", "failed", "venue ", "usenix ", "feed ", "truncated", "threshold", "unparsable")


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
    urls = {u.lower().rstrip("/") for u in re.findall(r"https?://[^\s)\]|>]+", blob)}
    urls |= {u + "/" for u in urls}
    return {"arxiv": arxiv_ids, "doi": dois, "github": ghs, "titles": titles, "orgs": orgs, "urls": urls}


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


OPENALEX_VENUES = {  # display-name search terms for OpenAlex sources
    "ASPLOS": "Architectural Support for Programming Languages and Operating Systems",
    "PLDI": "Programming Language Design and Implementation", "CGO": "Code Generation and Optimization",
    "CC": "Compiler Construction", "MLSys": "Machine Learning and Systems", "ISCA": "International Symposium on Computer Architecture",
    "MICRO": "International Symposium on Microarchitecture", "EuroSys": "European Conference on Computer Systems",
    "SC": "High Performance Computing, Networking, Storage and Analysis", "PPoPP": "Principles and Practice of Parallel Programming",
    "HPCA": "High-Performance Computer Architecture", "SOSP": "Symposium on Operating Systems Principles",
    "OOPSLA": "Proceedings of the ACM on Programming Languages", "ICML": "International Conference on Machine Learning",
    "NeurIPS": "Neural Information Processing Systems", "ICLR": "International Conference on Learning Representations",
    "EMNLP": "Empirical Methods in Natural Language Processing",
}
MAILTO = "&mailto=survey-discovery@users.noreply.github.com"


_SRC_CACHE: dict[str, list[str]] = {}


def _openalex_sources(term: str) -> list[str]:
    if term in _SRC_CACHE:
        return _SRC_CACHE[term]
    data = get(f"https://api.openalex.org/sources?search={urllib.parse.quote(term)}&per-page=5&select=id,display_name{MAILTO}", timeout=40, retries=1)
    ids = []
    if data:
        try:
            for r in json.loads(data).get("results", []):
                ids.append(r["id"].rsplit("/", 1)[-1])
        except Exception as e:  # noqa: BLE001
            log(f"  openalex sources parse failed for {term}: {e}")
    # keep only sources whose name contains the key phrase (drops ICMLA for ICML, etc.)
    if data:
        try:
            keep = []
            for r in json.loads(data).get("results", []):
                dn = (r.get("display_name") or "").lower()
                if term.lower() in dn or all(w in dn for w in term.lower().split()[:3]):
                    keep.append(r["id"].rsplit("/", 1)[-1])
            ids = keep or ids[:1]
        except Exception:  # noqa: BLE001
            pass
    log(f"  openalex sources '{term[:40]}': {ids}")
    _SRC_CACHE[term] = ids
    time.sleep(1.2)
    return ids


def _openalex_venue(name: str, term: str, y: int) -> list[dict]:
    ids = _openalex_sources(term)
    if not ids:
        return []
    url = (f"https://api.openalex.org/works?filter=primary_location.source.id:{'|'.join(ids)},"
           f"publication_year:{y}&per-page=200&select=title,doi,publication_date,primary_location{MAILTO}")
    time.sleep(1.2)
    data = get(url, timeout=40, retries=1)
    if not data:
        return []
    try:
        res = json.loads(data).get("results", [])
    except Exception as e:  # noqa: BLE001
        log(f"  openalex venue parse failed {name} {y}: {e}")
        return []
    log(f"  openalex venue {name} {y}: {len(res)} works")
    return res


def venue_candidates(years: list[int]) -> list[dict]:
    out = []
    for name in USENIX:
        for y in years:
            for title in _usenix_program(name, y):
                kh = [k for k in CORE if k in title.lower()] or [k for k in ("serving", "inference", "accelerator", "distributed training") if k in title.lower()]
                if kh:
                    out.append({"channel": "venue", "id": "", "title": title, "date": str(y),
                                "url": f"https://www.usenix.org/conference/{USENIX[name].format(yy=str(y)[2:])}/technical-sessions",
                                "why": f"{name} {y} (USENIX program): " + ", ".join(kh[:5])})
    for name, term in OPENALEX_VENUES.items():
        for y in years:
            for r in _openalex_venue(name, term, y):
                title = (r.get("title") or "").strip()
                kh = [k for k in CORE if k in title.lower()]
                if not kh:
                    continue
                doi = (r.get("doi") or "").replace("https://doi.org/", "")
                src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name", "")
                out.append({"channel": "venue", "id": doi, "title": title, "date": r.get("publication_date", str(y)),
                            "url": f"https://doi.org/{doi}" if doi else ((r.get("primary_location") or {}).get("landing_page_url") or ""),
                            "why": f"{name} {y} via OpenAlex ({src[:40]}): " + ", ".join(kh[:5])})
            time.sleep(0.3)
    return out


# --------------------------------------------------------------------------- citations
def cited_by_candidates(idx: dict, since: dt.date, max_seeds: int = 60) -> list[dict]:
    """OpenAlex: works citing our Tier A arXiv seeds. Citation indexing lags, so the
    window is widened to 180 days; dedupe against the index removes known works."""
    since = min(since, dt.date.today() - dt.timedelta(days=180))
    out = []
    seeds = []
    for p in sorted(PUBS.glob("*.md")):
        if p.name in ("INDEX.md", "_TEMPLATE.md"):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if "| **Evidence tier** | **A**" in t:
            m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", t)
            if m:
                seeds.append(m.group(1))
    seeds = seeds[:max_seeds]
    for aid in seeds:
        h1 = ""
        for p2 in PUBS.glob("*.md"):
            if p2.name in ("INDEX.md", "_TEMPLATE.md"):
                continue
            t2 = p2.read_text(encoding="utf-8", errors="ignore")
            if aid in t2:
                h1 = t2.splitlines()[0].lstrip("# ").split(" (")[0].split(": ")[-1].strip() or t2.splitlines()[0].lstrip("# ").strip()
                break
        if not h1:
            continue
        time.sleep(1.2)
        sq = get("https://api.openalex.org/works?filter=title.search:" + urllib.parse.quote(h1[:120]) + "&per-page=1&select=id,title,cited_by_count" + MAILTO, retries=1)
        try:
            res0 = json.loads(sq).get("results", []) if sq else []
        except Exception:  # noqa: BLE001
            res0 = []
        if not res0:
            log(f"  cites {aid}: title not found in OpenAlex ({h1[:50]})")
            continue
        w = res0[0]
        wid = w["id"].rsplit("/", 1)[-1]
        time.sleep(1.2)
        data = get(f"https://api.openalex.org/works?filter=cites:{wid},from_publication_date:{since.isoformat()}&per-page=100&select=id,title,doi,publication_date,primary_location" + MAILTO, retries=1)
        if not data:
            continue
        try:
            res = json.loads(data).get("results", [])
        except Exception:  # noqa: BLE001
            continue
        log(f"  cites {aid} ({(w.get('title') or '')[:40]}, {w.get('cited_by_count', '?')} total): {len(res)} citing works since {since}")
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



# --------------------------------------------------------------------------- indexed repository commit history
def indexed_repo_event_candidates(idx: dict, since: dt.date, *, max_repos: int = 120,
                                  max_events: int = 8, fetch_json=None) -> list[dict]:
    """Enumerate commit events even for repositories ALREADY in the index.

    These are review leads, not new systems or independent evidence families.
    The optional fetch_json callback permits network-free deterministic tests.
    Truncation and fetch failures must remain visible in Channel diagnostics.
    """
    priority = ("apache/tvm-tirx", "tile-ai/tilelang",
                "nvidia/auto-ontology", "triton-lang/triton",
                "mlc-ai/tirx-harness", "llvm/llvm-project")
    repos = sorted(r for r in idx["github"] if re.fullmatch(r"[\w.-]+/[\w.-]+", r))
    repos = [r for r in priority if r in repos] + [r for r in repos if r not in priority]
    if max_repos > 0 and len(repos) > max_repos:
        DIAG.append(f"repoevent truncated: only {max_repos}/{len(repos)} indexed repos checked; "
                    f"unvisited include {', '.join(repos[max_repos:max_repos+5])}")
        repos = repos[:max_repos]

    def fetch(url: str):
        headers = dict(UA)
        if os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    fetch_json = fetch_json or fetch
    out = []
    for repo in repos:
        url = (f"https://api.github.com/repos/{repo}/commits?since={since.isoformat()}T00%3A00%3A00Z"
               f"&per_page={max_events+1}")
        try:
            commits = fetch_json(url)
            if not isinstance(commits, list):
                raise ValueError("non-list GitHub commits response")
        except Exception as exc:  # fail soft, but record omissions
            DIAG.append(f"repoevent failed: {repo}: {exc}")
            continue
        if len(commits) > max_events:
            DIAG.append(f"repoevent truncated: {repo}: first {max_events} of >{max_events} commits; "
                        "older updates require review")
        for event in commits[:max_events]:
            sha = event.get("sha", "")
            data = event.get("commit") or {}
            date = ((data.get("committer") or {}).get("date") or "")[:10]
            if not sha or (date and date < since.isoformat()):
                continue
            subject = (data.get("message") or "").split("\n", 1)[0]
            out.append({"channel": "repoevent", "id": f"{repo}@{sha}",
                        "title": f"{repo}: {subject}"[:160], "date": date,
                        "url": event.get("html_url") or f"https://github.com/{repo}/commit/{sha}",
                        "why": f"indexed-repo COMMIT event {sha[:12]}; family {repo}; "
                               f"observed in sweep {dt.date.today()}; "
                               "inspect changed files, tests and design impact"})
        # A tag may mark an already-existing commit; commit enumeration alone misses
        # a newly published release. Treat release metadata as its own event.
        releases_url = f"https://api.github.com/repos/{repo}/releases?per_page=5"
        try:
            releases = fetch_json(releases_url)
            if not isinstance(releases, list):
                raise ValueError("non-list GitHub releases response")
        except Exception as exc:
            DIAG.append(f"repoevent releases failed: {repo}: {exc}")
            continue
        for release in releases:
            published = (release.get("published_at") or "")[:10]
            tag = release.get("tag_name") or ""
            if not published or published < since.isoformat() or not tag:
                continue
            out.append({"channel": "repoevent", "id": f"{repo}@release:{tag}",
                        "title": f"{repo}: release {tag}"[:160], "date": published,
                        "url": release.get("html_url") or f"https://github.com/{repo}/releases/tag/{tag}",
                        "why": f"indexed-repo RELEASE {tag}; family {repo}; "
                               f"observed in sweep {dt.date.today()}; "
                               "review changelog, design and compatibility"})
    return out


# --------------------------------------------------------------------------- blogs, forums, HN
FEEDS = OUT_DIR / "feeds.txt"
AGENT_TERMS = ["agent", "agentic", "llm", "language model", "claude", "gpt", "codex", "gemini",
               "self-improv", "autonomous", "ai-generated", "ai generated", "ai compiler", "ai-written"]
HN_QUERIES = ["compiler agent", "agentic compiler", "AI compiler", "kernel agent", "LLM kernel",
              "GPU kernel LLM", "MLIR", "Triton kernel", "tile language", "megakernel", "TVM", "superoptimizer"]
GH_QUERIES = ["agentic compiler", "compiler agent", "kernel agent", "kernel generation llm", "agent gpu kernel",
              "tile language", "tile programming", "megakernel", "tensor compiler", "kernel optimization agent",
              "mlir agent", "superoptimizer", "lean kernel verification", "equality saturation",
              "autotuning", "tensor program optimization"]
# Compiler-specific CORE terms: on a general ("theme") feed these alone admit an item, with or
# without agent vocabulary, so non-agent alternatives (equality saturation, autotuning, cost
# models) are not filtered out. Broad CORE terms ("kernel", "cuda", "tile", "ptx") also occur in
# unrelated posts (Linux kernel, CUDA release notes), so on theme feeds they need an OPT_CONTEXT
# word (below) or an agent term.
# Agent terms are otherwise used only as tags.
STRICT_CORE = [k for k in CORE if k not in ("kernel", "cuda", "tile", "ptx")]
# Optimization / code-generation context: a broad CORE term plus one of these admits a theme-feed
# item without agent vocabulary, so non-agent GPU posts ("Optimizing CUDA matrix multiplication",
# "Faster PTX code generation") are not filtered out by an agent-vocabulary gate.
OPT_CONTEXT = ["optimiz", "code generation", "codegen", "scheduling", "matrix multipl", "matmul",
               "gemm", "fusion", "vectoriz", "occupancy", "register allocation", "instruction selection"]
HN_MAX_PAGES, HN_MIN_POINTS = 3, 5
GH_MAX_PAGES, GH_MIN_STARS_NEW, GH_MIN_STARS_ACTIVE = 3, 5, 25


def _theme_hit(text: str, scope: str) -> list[str]:
    low = text.lower()
    core = [k for k in CORE if k in low]
    if not core:
        return []
    agent = [k for k in AGENT_TERMS if k in low]
    if scope == "core" or any(k in STRICT_CORE for k in core):
        return core + agent
    ctx = [k for k in OPT_CONTEXT if k in low]
    if ctx:
        return core + ctx + agent
    return core + agent if agent else []


def _parse_date(s: str) -> str:
    s = (s or "").strip()
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z", "%d %b %Y %H:%M:%S %z"):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return ""


def parse_feed(data: bytes, base: str = "") -> list[dict]:
    """RSS 2.0 and Atom items as {title, url, date, summary}. Namespace-tolerant.

    Relative item links (e.g. Jekyll feeds that emit "/2026/11/03/post") are resolved
    against `base`, the feed URL, so ledger links work and deduplication sees one form."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []
    def local(tag: str) -> str:
        return tag.rsplit("}", 1)[-1]
    items = []
    for el in root.iter():
        if local(el.tag) not in ("item", "entry"):
            continue
        rec = {"title": "", "url": "", "date": "", "summary": ""}
        for ch in el:
            t = local(ch.tag)
            if t == "title":
                rec["title"] = (ch.text or "").strip()
            elif t == "link":
                # Atom: prefer rel="alternate" (or no rel, which defaults to alternate) over
                # rel="self"/"edit"/"replies", which point at API or feed endpoints.
                href = (ch.get("href") or (ch.text or "")).strip()
                rel = ch.get("rel", "alternate")
                if rel == "alternate" and href and not rec.get("_alt"):
                    rec["url"], rec["_alt"] = href, True
                elif href and not rec["url"]:
                    rec["url"] = href
            elif t in ("pubDate", "published", "updated", "date") and not rec["date"]:
                rec["date"] = _parse_date(ch.text or "")
            elif t in ("description", "summary", "content") and not rec["summary"]:
                rec["summary"] = re.sub(r"<[^>]+>", " ", ch.text or "")[:600]
        rec.pop("_alt", None)
        if rec["url"] and base:
            rec["url"] = urllib.parse.urljoin(base, rec["url"])
        if rec["title"]:
            items.append(rec)
    return items


def load_feeds() -> list[tuple[str, str, str]]:
    if not FEEDS.exists():
        return []
    out = []
    for line in FEEDS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 2:
            out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else "theme"))
    return out


def blog_candidates(since: dt.date) -> list[dict]:
    out = []
    for url, label, scope in load_feeds():
        data = get(url, timeout=25, retries=1)
        if not data:
            DIAG.append(f"feed failed: {label} {url}")
            continue
        items = parse_feed(data, base=url)
        if not items:
            DIAG.append(f"feed empty or unparsable: {label} {url}")
            continue
        for it in items:
            if it["date"] and dt.date.fromisoformat(it["date"]) < since:
                continue
            hits = _theme_hit(it["title"] + " " + it["summary"], scope)
            if not hits:
                continue
            out.append({"channel": "blog", "id": it["url"], "title": f"{label}: {it['title']}"[:160],
                        "date": it["date"], "url": it["url"],
                        "why": f"{scope} feed; terms: {', '.join(sorted(set(hits))[:5])}"})
        time.sleep(0.2)
    # Hacker News stories (Algolia API) with discussion, for posts on sites no feed covers.
    ts = int(dt.datetime.combine(since, dt.time()).timestamp())
    # Threshold: HN_MIN_POINTS drops unvoted self-promotion (most stories below it have no
    # comments). It is a recall trade-off, so the ledger reports it; set 0 to disable.
    for q in HN_QUERIES:
        hits = []
        for page in range(HN_MAX_PAGES):
            u = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=100"
                 f"&page={page}&query={urllib.parse.quote(q)}"
                 f"&numericFilters=created_at_i>{ts},points>{HN_MIN_POINTS}")
            data = get(u, timeout=20, retries=1)
            if not data:
                DIAG.append(f"hn failed: {q} (page {page})")
                break
            try:
                j = json.loads(data)
            except Exception:  # noqa: BLE001
                DIAG.append(f"hn unparsable: {q} (page {page})")
                break
            hits += j.get("hits", [])
            if page + 1 >= int(j.get("nbPages", 0) or 0):
                break
        else:
            DIAG.append(f"hn truncated: {q}: stopped after {HN_MAX_PAGES} pages ({len(hits)} stories)")
        for h in hits:
            title = h.get("title") or ""
            th = _theme_hit(title, "theme") or _theme_hit(title, "core")
            if not th:
                continue
            link = h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
            out.append({"channel": "blog", "id": link, "title": f"HN: {title}"[:160],
                        "date": (h.get("created_at") or "")[:10], "url": link,
                        "why": f"Hacker News {h.get('points', 0)} points, {h.get('num_comments', 0)} comments; "
                               f"thread news.ycombinator.com/item?id={h.get('objectID')}"})
        time.sleep(0.3)
    return out


def ghsearch_candidates(idx: dict, since: dt.date) -> list[dict]:
    """GitHub repository search by topic, across all owners (not only tracked orgs)."""
    out = []
    hdr = dict(UA)
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        hdr["Authorization"] = f"Bearer {token}"
    # Thresholds: GH_MIN_STARS_NEW / GH_MIN_STARS_ACTIVE keep the ledger triageable (an unstarred
    # repository pushed in the window is usually a course exercise or fork-like copy). They are a
    # recall trade-off, so the number of repositories they drop is reported per query.
    for q in GH_QUERIES:
        query = f"{q} in:name,description,readme pushed:>={since.isoformat()} fork:false archived:false"
        items, total = [], 0
        for page in range(1, GH_MAX_PAGES + 1):
            u = (f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}"
                 f"&sort=stars&order=desc&per_page=100&page={page}")
            try:
                req = urllib.request.Request(u, headers=hdr)
                with urllib.request.urlopen(req, timeout=30) as r:
                    j = json.loads(r.read())
            except Exception as e:  # noqa: BLE001
                DIAG.append(f"ghsearch failed: {q} (page {page}): {e}")
                break
            total = int(j.get("total_count", 0) or 0)
            batch = j.get("items", [])
            items += batch
            if len(batch) < 100 or len(items) >= total:
                break
            time.sleep(2.5)
        if total > len(items):
            DIAG.append(f"ghsearch truncated: {q}: {len(items)} of {total} repositories retrieved")
        below = 0
        for rp in items:
            full = rp.get("full_name", "")
            if not full or known(idx, gh=full):
                continue
            stars = rp.get("stargazers_count", 0)
            created = (rp.get("created_at") or "")[:10]
            new_repo = bool(created) and dt.date.fromisoformat(created) >= since
            if stars < (GH_MIN_STARS_NEW if new_repo else GH_MIN_STARS_ACTIVE):
                below += 1
                continue
            desc = rp.get("description") or ""
            if not _theme_hit(full + " " + desc, "core"):
                continue
            out.append({"channel": "github", "id": full, "title": f"{full}: {desc}"[:160],
                        "date": created, "url": rp.get("html_url", ""),
                        "why": f"GitHub search '{q}'; {'new' if new_repo else 'active'}; stars {stars}"})
        if below:
            DIAG.append(f"ghsearch threshold: {q}: {below} repositories below the star threshold dropped")
        time.sleep(2.5)  # search API: 30 requests/min with a token
    return out


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD; default: 21 days ago")
    ap.add_argument("--channels", default="arxiv,venues,cites,github,ghsearch,blogs,repoevent")
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
    if "ghsearch" in chans:
        cands += ghsearch_candidates(idx, since)
    if "blogs" in chans:
        cands += blog_candidates(since)
    if "repoevent" in chans:
        cands += indexed_repo_event_candidates(idx, since)

    seen = set()
    new, already = [], 0
    for c in cands:
        # A known repository may repeat a commit subject: only its SHA identifies the event.
        key = (c["channel"], c["id"]) if c["channel"] == "repoevent" else (c["channel"], norm_title(c["title"])[:80])
        if key in seen:
            continue
        seen.add(key)
        aid = c["id"] if c["channel"] == "arxiv" else ""
        doi = c["id"] if c["channel"] in ("venue", "cites") and c["id"].startswith("10.") else ""
        gh = c["id"] if c["channel"] == "github" else ""
        if c["channel"] == "blog" and c["id"].lower() in idx["urls"]:
            already += 1
            continue
        if c["channel"] != "repoevent" and known(idx, arxiv=aid, doi=doi, gh=gh, title=c["title"]):
            already += 1
            continue
        new.append(c)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else OUT_DIR / f"{today.isoformat()}.md"
    by = {}
    for c in new:
        by.setdefault(c["channel"], []).append(c)
    source_count = sum(c["channel"] != "repoevent" for c in new)
    event_count = len(new) - source_count
    lines = [f"# Discovery ledger — {today.isoformat()}", "",
             f"Window: since {since.isoformat()}. Channels: {', '.join(sorted(chans))}. "
             f"Candidates: {len(cands)} raw, {already} already indexed, "
             f"**{source_count} new source leads**, **{event_count} indexed-repo events**.", "",
             "Triage source rows as INCLUDE (digest it), EXCLUDE (reason), or PENDING "
             "(what is missing). For indexed-repo events use UPDATE-DIGEST, "
             "NOTE-IN-REPOS or IGNORE with a reason. Mark every Decision cell "
             "on the batch branch; blank means the sweep is unfinished.", ""]
    for ch in ("repoevent", "blog", "github", "pypi", "arxiv", "venue", "cites"):
        rows = by.get(ch, [])
        if not rows:
            continue
        heading = ("Events in indexed repositories" if ch == "repoevent" else ch)
        lines += [f"## {heading} ({len(rows)})", ""]
        if ch == "repoevent":
            lines.append("Existing evidence-family updates only; decide UPDATE-DIGEST, "
                         "NOTE-IN-REPOS or IGNORE. These rows never count as new sources.")
            lines.append("")
        lines += ["| Date | Candidate | Why it surfaced | Decision |", "|---|---|---|---|"]
        for c in sorted(rows, key=lambda r: r["date"], reverse=True):
            t = c["title"].replace("|", "/")
            lines.append(f"| {c['date']} | [{t}]({c['url']}) | {c['why']} | |")
        lines.append("")
    per = {}
    for c in cands:
        per[c["channel"]] = per.get(c["channel"], 0) + 1
    lines += ["## Channel diagnostics", "", f"Raw candidates per channel: {json.dumps(per)}", "",
              "Fetch log (failures and venue page sizes):", ""]
    pri = [d for d in DIAG if "cites " in d or "openalex" in d.lower()]
    rest = [d for d in DIAG if d not in pri and any(t in d for t in DIAG_KEEP)]
    lines += [f"- {d}" for d in (pri + rest)[:200]]
    lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out} ({len(new)} new candidates)")
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
