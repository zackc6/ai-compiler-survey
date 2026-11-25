#!/usr/bin/env python3
"""Mechanical source discovery for the survey.

Enumerates candidate sources and changes to known systems from structured feeds, not web search, which
is where recent sweeps missed TileLoom, TASO/Tensat, PeepholeBench, LLVM-Bench,
CIRBench and TileFoundry. Eight channels:

  arxiv   - arXiv API listings by category and keyword, over a date window
  venues  - DBLP tables of contents for a fixed venue set (OSDI, SOSP, ASPLOS,
            PLDI, CGO, MLSys, ISCA, MICRO, ICML, NeurIPS, ICLR, EMNLP)
  cites   - OpenAlex "cited by" for the Tier A digests (forward citation expansion)
  refs    - OpenAlex references of every digest (backward expansion; no date window, no
            keyword filter): foundational and mechanism-layer works our sources build on
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
import email.utils
import json
import math
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
DIAG_KEEP = ("HTTP", "refs:", "proceedings ", "failed", "venue ", "usenix ", "feed ", "truncated", "threshold", "unparsable",
             "repoevent ", "cites incomplete")


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)
    DIAG.append(msg)


# OpenAlex meters usage in US dollars per day. Sources (read 24 November 2026): openalex.org/pricing
# says every account gets $1 a day free, and help.openalex.org/api/authentication says a free key
# gives 10x the keyless budget, so keyless is about $0.10 a day (derived). That page says only the
# per-second limits count per IP; it does not document the unit of the keyless daily budget. A 429
# body in run 45460680024 mentioned the mailto address, so we infer (undocumented) that keyless
# requests sharing our fixed mailto share one budget. A list or filter request costs $0.0001 and
# any search (including a title.search filter) $0.001. Until 24 November
# the venue listings spent ~136 searches, so the budget was gone before cites and refs ran and
# both returned nothing. OA tracks estimated spend, and a daily_budget 429 trips a breaker that
# skips every later OpenAlex call and marks the dependent channels DEGRADED.
OPENALEX_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
OA_SOFT_CAP = 0.8 if OPENALEX_KEY else 0.08  # USD; below the daily budget, leaving room for lists
OA = {"lists": 0, "searches": 0, "skipped": 0, "breaker": "", "per_second_429": 0, "channel": "", "skipped_in": {},
      "sleep_429": 0.0}
OA_LONG_WAIT = 600.0      # s; a Retry-After longer than this is inferred to be the daily budget (OpenAlex documents no such threshold)
# ChatGPT 18:58: a 429's `reason` and body are server text that may echo request data (the key
# included), and the breaker line reaches Actions logs and the published ledger. Only allowlisted
# reason tokens and fixed body markers are ever logged; any other reason is logged as "other".
# The documented values (help.openalex.org/api/authentication, read 24 November 2026).
OA_429_REASONS = frozenset({"daily_budget", "requests_per_second", "broad_boolean_query", "wide_or_filter",
                            "semantic_search"})
OA_429_MARKERS = (("insufficient budget", "insufficient-budget"), ("no api key", "keyless"),
                  ("mailto", "mailto-mentioned"), ("every network", "all-networks"))


def _oa_429_summary(raw_body: bytes) -> tuple[str, str]:
    """(allowlisted reason, "other" or "", comma-joined fixed markers found in the body). Never raw text."""
    try:
        reason = str(json.loads(raw_body or b"{}").get("reason", "") or "")
    except Exception:  # noqa: BLE001
        reason = ""
    if reason and reason not in OA_429_REASONS:
        reason = "other"
    low = raw_body[:4096].decode("utf-8", "replace").lower()
    return reason, ",".join(tag for phrase, tag in OA_429_MARKERS if phrase in low)
OA_429_SLEEP_CAP = 900.0  # s; total time the run may spend waiting on OpenAlex per-second 429s


def _oa_cost() -> float:
    return OA["lists"] * 0.0001 + OA["searches"] * 0.001


def _retry_after(value: str | None, now: dt.datetime | None = None) -> float:
    """Retry-After in seconds (RFC 9110: delay-seconds or an HTTP-date). A missing, malformed,
    negative or non-finite value gives 1 s, so time.sleep never sees NaN or a negative number
    (ChatGPT/Codex 18:33: float('-5') and float('nan') reached time.sleep and raised)."""
    if not value or not value.strip():
        return 1.0
    value = value.strip()
    try:
        wait = float(value)
    except ValueError:
        try:
            when = email.utils.parsedate_to_datetime(value)
        except (TypeError, ValueError, IndexError):
            return 1.0
        if when is None:
            return 1.0
        if when.tzinfo is None:
            when = when.replace(tzinfo=dt.timezone.utc)
        return max((when - (now or dt.datetime.now(dt.timezone.utc))).total_seconds(), 0.0)
    return wait if math.isfinite(wait) and wait >= 0 else 1.0


def get(url: str, timeout: int = 40, retries: int = 2) -> bytes | None:
    oa = "api.openalex.org" in url
    if oa:
        if OA["breaker"]:
            OA["skipped"] += 1
            OA["skipped_in"][OA["channel"]] = OA["skipped_in"].get(OA["channel"], 0) + 1
            return None
        is_search = ("search=" in url or "search:" in url)
        if is_search and _oa_cost() + 0.001 > OA_SOFT_CAP:
            # Searches cost 10x a list; keep the remaining budget for the cheap list requests.
            if not OA.get("capped"):
                OA["capped"] = True
                log(f"  openalex search cap: estimated spend ${_oa_cost():.4f} reached the ${OA_SOFT_CAP:.2f} "
                    f"soft cap; further searches skipped (list requests continue)")
            OA["skipped"] += 1
            OA["skipped_in"][OA["channel"]] = OA["skipped_in"].get(OA["channel"], 0) + 1
            return None
        if OPENALEX_KEY and "/rate-limit" not in url:
            url += ("&" if "?" in url else "?") + "api_key=" + urllib.parse.quote(OPENALEX_KEY)
    shown = re.sub(r"api_key=[^&]+", "api_key=***", url)[:110]
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
            if oa and "/rate-limit" not in url:
                OA["searches" if ("search=" in url or "search:" in url) else "lists"] += 1
            return body
        except urllib.error.HTTPError as e:  # noqa: PERF203
            if oa and e.code == 429:
                raw_body = b""
                try:
                    raw_body = e.read() or b""
                except Exception:  # noqa: BLE001
                    raw_body = b""
                reason, markers = _oa_429_summary(raw_body)
                wait = _retry_after(e.headers.get("Retry-After") if e.headers else None)
                pause = min(wait, 30) + attempt  # one duration for the cap check, the sleep and the accounting
                # Run 45437945681 (69cc338): the keyless daily-budget 429 arrived with no parseable
                # reason but Retry-After ~26,900 s (the time to 00:00 UTC). Only reason=daily_budget
                # tripped the breaker, so every later call retried 3 x 30 s and the job hit its 2 h
                # timeout without writing a ledger. We infer (OpenAlex does not document it) that a
                # per-second limit never asks for minutes, so a Retry-After above OA_LONG_WAIT is
                # treated as the daily budget whatever the body says, and the breaker line says
                # "inferred". If per-second waits alone pass OA_429_SLEEP_CAP in total, it trips too.
                cause = ""
                if reason == "daily_budget":
                    cause = "daily_budget"
                elif wait > OA_LONG_WAIT:
                    cause = f"daily budget inferred (Retry-After {wait:.0f}s, reason {reason or 'absent'})"
                elif OA["sleep_429"] + pause > OA_429_SLEEP_CAP:
                    cause = f"persistent 429s ({OA['sleep_429']:.0f}s already spent waiting)"
                if cause:
                    OA["skipped_in"][OA["channel"]] = OA["skipped_in"].get(OA["channel"], 0) + 1
                    OA["breaker"] = f"{cause} in {OA['channel'] or '?'} after ~${_oa_cost():.4f} ({OA['lists']} lists, {OA['searches']} searches)"
                    log(f"  openalex breaker tripped: {OA['breaker']}; retry-after={wait:g}s; "
                        f"429 body markers: {markers or 'none'}; remaining OpenAlex calls skipped: {shown}")
                    return None
                OA["per_second_429"] += 1
                log(f"  HTTP 429 reason={reason or '?'} retry-after={wait:g}s ({attempt + 1}/{retries + 1}): {shown}")
                OA["sleep_429"] += pause
                time.sleep(pause)
                continue
            log(f"  HTTP {e.code} ({attempt + 1}/{retries + 1}): {shown}")
            if e.code in (401, 403, 404):
                return None
            if e.code == 429 and "arxiv.org" in url:
                ra = (e.headers.get("Retry-After") if e.headers else None) or ""
                time.sleep(min(float(ra), 120) if ra.replace(".", "", 1).isdigit() else 20 * (attempt + 1))
                continue
            time.sleep((8 if e.code == 429 else 2) * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            log(f"  fetch failed ({attempt + 1}/{retries + 1}): {shown} -> {e}")
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
# Category pages that failed or did not parse. test-34 (24 Nov 2026, the fourth run that day from
# runner IPs) lost cs.LG, cs.SE and cs.PF pages to arXiv 429s and fell from 123 to 74 raw rows, but
# the channel still returned rows, so the ledger did not say DEGRADED. Any entry now does.
ARXIV_INCOMPLETE: list[str] = []


def arxiv_candidates(since: dt.date, max_per_cat: int = 20000, page: int = 500) -> list[dict]:
    """Page each category back to the window boundary.

    The earlier fixed 400-record cap ended cs.LG (several hundred listings a day) after about a
    day of a 21-day window and said nothing (Codex 13:25). Now paging stops only at the window
    boundary or the end of the listing; reaching the safety cap, a failed or unparsable page, or an
    empty page before the boundary is recorded in ARXIV_INCOMPLETE with category and offset, which
    marks the channel DEGRADED. arXiv serves slices of at most 2000 and asks for 3 s between calls.
    """
    out = []
    ns = {"a": "http://www.w3.org/2005/Atom",
          "os": "http://a9.com/-/spec/opensearch/1.1/"}
    for cat in ARXIV_CATS:
        start = 0
        reached_boundary = False
        while start < max_per_cat:
            q = urllib.parse.quote(f"cat:{cat}")
            url = (f"https://export.arxiv.org/api/query?search_query={q}&sortBy=submittedDate"
                   f"&sortOrder=descending&start={start}&max_results={page}")
            data = get(url, timeout=60, retries=4)
            if not data:
                ARXIV_INCOMPLETE.append(f"{cat} from offset {start} failed")
                break
            try:
                root = ET.fromstring(data)
            except ET.ParseError:
                ARXIV_INCOMPLETE.append(f"{cat} offset {start} unparsable")
                break
            entries = root.findall("a:entry", ns)
            if not entries:
                total = root.findtext("os:totalResults", default="", namespaces=ns)
                if not (total.isdigit() and start >= int(total)):
                    # arXiv sometimes returns an empty slice mid-listing; that is lost coverage.
                    ARXIV_INCOMPLETE.append(f"{cat} empty page at offset {start} before window boundary")
                reached_boundary = True  # nothing more to read either way
                break
            for e in entries:
                pub = e.findtext("a:published", default="", namespaces=ns)[:10]
                if pub and dt.date.fromisoformat(pub) < since:
                    reached_boundary = True
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
            if reached_boundary:
                break
            start += len(entries)
            time.sleep(3)  # arXiv API etiquette
        else:
            # Loop condition ran out: cap reached while every record read was still in the window.
            ARXIV_INCOMPLETE.append(f"{cat} cap {max_per_cat} reached at offset {start}, window not exhausted")
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

# Codex 16:39: gating on the calendar year let an already published current-year listing
# (MLSys 2026, 135 papers; OSDI 2026, 437 titles in test 35) fail silently. From this (month, day)
# of the venue's own year its listing is expected to be published, so an empty or failed listing
# degrades coverage. These dates are a declared assumption (conference month plus margin), not a
# scraped fact; NeurIPS posts proceedings in the following year, so it has no same-year entry.
# ChatGPT 18:18: MLSys 2026 ran 18-22 May (mlsys.org/Conferences/2026/Dates), so 1 July is a margin
# heuristic, not the verified posting date. USENIX states OSDI '26 full proceedings are public from
# 13 July; 1 June is when the parsed object, the technical-sessions program (titles), is expected.
PUBLISHED_FROM = {"MLSys": (7, 1), "OSDI": (6, 1), "ATC": (6, 1)}
# Last held edition. USENIX sunset ATC after ATC '25 (usenix.org/blog/usenix-atc-announcement), and
# usenix.org/conference/atc26 is HTTP 404 (test 35, 24 Nov 2026). Without this, the venue-year gate
# would record "ATC 2026 USENIX program unavailable" on every run from 1 June 2026, a permanent false
# DEGRADED that would hide real ones. A year after the last edition is not fetched and not a miss.
VENUE_LAST_YEAR = {"ATC": 2025}


def _today() -> dt.date:
    return dt.date.today()


def _listing_expected(name: str, y: int) -> bool:
    """True when the venue-year listing should already be published (past year, or current year
    after the venue's PUBLISHED_FROM date)."""
    today = _today()
    if y < today.year:
        return True
    md = PUBLISHED_FROM.get(name)
    return bool(md) and y == today.year and today >= dt.date(y, *md)


def _usenix_program(name: str, y: int) -> list[str]:
    if y > VENUE_LAST_YEAR.get(name, y):
        log(f"  usenix {name} {y}: not held (last edition {VENUE_LAST_YEAR[name]}); not fetched")
        return []
    slug = USENIX[name].format(yy=str(y)[2:])
    data = get(f"https://www.usenix.org/conference/{slug}/technical-sessions", timeout=40, retries=1)
    past = _listing_expected(name, y)  # a published program must parse; an unpublished one may not
    if not data:
        log(f"  usenix {name} {y}: unavailable")
        if past:
            VENUE_INCOMPLETE.append(f"{name} {y} USENIX program unavailable")
        return []
    html = data.decode("utf-8", "ignore")
    titles = re.findall(r'<h2[^>]*class="[^"]*node-title[^"]*"[^>]*>\s*<a[^>]*>(.*?)</a>', html, re.S)
    if not titles:
        titles = re.findall(r'<a href="/conference/' + slug + r'/presentation/[^"]+">(.*?)</a>', html, re.S)
    titles = [re.sub(r"<[^>]+>", "", t).strip() for t in titles]
    log(f"  usenix {name} {y}: {len(html)} bytes, {len(titles)} titles")
    if not titles and past:
        # Codex 16:35 (same class as the proceedings sites): zero parsed titles is a parse failure.
        VENUE_INCOMPLETE.append(f"{name} {y} USENIX program parsed 0 titles ({len(html)} bytes)")
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


VENUE_TERMS = ["compiler", "superoptim", "autotun", "kernel", "megakernel", "triton", "mlir", "llvm",
               "ptx", "tensor program", "equality saturation", "e-graph", "lowering", "halide", "tvm", "xla",
               "cost model", "cuda", "tile", "code generation", "accelerator", "scheduling", "agent"]


# ChatGPT 19:24: help.openalex.org/api/paging (updated 14 Oct 2026) documents per_page 1-100,
# "100 is the supported maximum"; per_page=200 is accepted only as deprecated legacy behaviour
# "and will be removed". Basic paging also requires page * per_page <= 10,000.
OA_PAGE_SIZE = 100
OA_BASIC_PAGING_LIMIT = 10_000
VENUE_MAX_PAGES = OA_BASIC_PAGING_LIMIT // OA_PAGE_SIZE  # 100 pages; ICML 2026 has 6,418 works
# Venue-years whose listing is partial (a failed or unparsable page, or the page cap). Any entry
# marks the venue channel DEGRADED even when other venue-years or proceedings returned rows.
VENUE_INCOMPLETE: list[str] = []


def _openalex_venue(name: str, term: str, y: int) -> list[dict]:
    """Every work of a venue-year, paged as plain list requests and filtered on titles locally.

    History: until 24 November 2026 the first 200 works were kept, silently truncating ICLR,
    NeurIPS, ICML and MLSys (AccelOpt was lost that way). The 24 November replacement pushed the
    title filter into OpenAlex as title.search OR-groups, but each of those is a $0.001 search and
    a "broad boolean" query (1 request/s), so ~136 of them spent the keyless daily budget. Basic
    page= paging costs $0.0001 per list call of up to OA_PAGE_SIZE (100) works and needs no key (cursor paging answered 401). A
    venue-year larger than VENUE_MAX_PAGES pages (the 10,000-work basic-paging limit) is logged as
    truncated and DEGRADED; a keyed cursor option or publisher fallback is a separate question."""
    ids = _openalex_sources(term)
    if not ids:
        # ChatGPT 12:50: an unresolved venue source used to return [] silently, so a whole
        # venue-year vanished without a trace. Record it (breaker skips are counted separately).
        if not OA["breaker"]:
            log(f"  openalex venue {name} {y}: source unresolved for '{term[:40]}'")
            VENUE_INCOMPLETE.append(f"{name} {y} source unresolved")
        return []
    res: list[dict] = []
    total = None
    for page in range(1, VENUE_MAX_PAGES + 1):
        url = (f"https://api.openalex.org/works?filter=primary_location.source.id:{'|'.join(ids)},"
               f"publication_year:{y}&per-page={OA_PAGE_SIZE}&page={page}"
               f"&select=title,doi,publication_date,primary_location{MAILTO}")
        time.sleep(0.2)
        data = get(url, timeout=60, retries=3)
        if not data:
            log(f"  openalex venue {name} {y}: truncated, page {page} failed after {len(res)} works"
                + (f" of {total}" if total else "") + (" (breaker)" if OA["breaker"] else ""))
            VENUE_INCOMPLETE.append(f"{name} {y} page {page} failed after {len(res)}"
                                    + (f" of {total}" if total else "") + " works")
            return [] if not res and OA["breaker"] else _venue_filter(res)
        try:
            js = json.loads(data)
        except Exception as e:  # noqa: BLE001
            log(f"  openalex venue parse failed {name} {y}: {e}")
            VENUE_INCOMPLETE.append(f"{name} {y} page {page} unparsable after {len(res)} works")
            break
        total = (js.get("meta") or {}).get("count", total)
        batch = js.get("results", [])
        res += batch
        if total is not None and len(res) >= total:
            break
        if len(batch) < OA_PAGE_SIZE:
            # A short page normally ends the listing; if meta.count says records remain, the
            # listing stopped early and is recorded as incomplete (ChatGPT 12:50).
            if total is not None and len(res) < total:
                log(f"  openalex venue {name} {y}: short page {page} ({len(batch)} works) at {len(res)} of {total}")
                VENUE_INCOMPLETE.append(f"{name} {y} short page {page} at {len(res)} of {total} works")
            break
    else:
        if total and len(res) < total:
            log(f"  openalex venue {name} {y}: truncated at {len(res)} of {total} works")
            VENUE_INCOMPLETE.append(f"{name} {y} truncated at {len(res)} of {total} works")
    kept = _venue_filter(res)
    log(f"  openalex venue {name} {y}: {len(res)} works listed" + (f" of {total}" if total is not None else "")
        + f", {len(kept)} title-matched")
    return kept


def _venue_filter(works: list[dict]) -> list[dict]:
    return [w for w in works if any(t in (w.get("title") or "").lower() for t in VENUE_TERMS)]


# Proceedings sites that publish complete title lists (same software for MLSys and NeurIPS).
PROCEEDINGS = {"MLSys": "https://proceedings.mlsys.org/paper_files/paper/{y}",
               "NeurIPS": "https://papers.nips.cc/paper_files/paper/{y}"}


# ChatGPT 18:18: a year root can be one volume of several. On 24 Nov 2026
# papers.nips.cc/paper_files/paper/2025 listed the 64-paper Creative AI volume and linked ("See also")
# to /paper_files/paper/2025/vol38-main-conference (5,823 papers, main + position + datasets tracks),
# which links back. Same-year sibling volumes are followed, breadth-first, URL-deduplicated, at most
# this many pages; reaching the bound is recorded as incomplete.
PROCEEDINGS_MAX_VOLUMES = 6
# Titles with inline markup or under 8 characters are not parsed. More title-less links than this share
# of a volume's unique links is treated as a template change, not as a few odd titles.
PROCEEDINGS_TITLE_SHORTFALL = 0.01
# Per-volume denominators (links, titled, untitled, advertised) for the ledger: ChatGPT 18:42 asked that
# the tolerated title shortfall be visible as counts, since the omitted titles' relevance is unknown.
PROCEEDINGS_AUDIT: list[str] = []


def _proceedings_titles(name: str, y: int) -> list[tuple[str, str]]:
    base = PROCEEDINGS[name].format(y=y)
    host = base.split("/paper_files")[0]
    expected = _listing_expected(name, y)
    queue, seen, urls = [base], set(), set()
    out: list[tuple[str, str]] = []
    main_track = 0
    root_bytes = None
    while queue:
        url = queue.pop(0)
        if url in seen:
            continue
        if len(seen) >= PROCEEDINGS_MAX_VOLUMES:
            log(f"  proceedings {name} {y}: volume bound {PROCEEDINGS_MAX_VOLUMES} reached; not read: {', '.join(queue[:5])}")
            if expected:
                VENUE_INCOMPLETE.append(f"{name} {y} more than {PROCEEDINGS_MAX_VOLUMES} proceedings volumes; not all read")
            break
        seen.add(url)
        vol = "root" if url == base else url.rsplit("/", 1)[1]
        data = get(url, timeout=60, retries=1)
        if not data:
            log(f"  proceedings {name} {y} {vol}: unavailable")
            # A past year's proceedings should exist; the current year's may not be published yet
            # (NeurIPS posts in the following months), so only published years degrade the channel.
            if expected:
                VENUE_INCOMPLETE.append(f"{name} {y} proceedings site unavailable" if vol == "root"
                                        else f"{name} {y} proceedings volume {vol} unavailable")
            continue
        html = data.decode("utf-8", "ignore")
        if vol == "root":
            root_bytes = len(html)
        links = set(re.findall(r'href="(/paper_files/paper/' + str(y) + r'/hash/[^"]+)"', html))
        titled = set()
        for m in re.finditer(r'<a[^>]*href="(/paper_files/paper/\d{4}/hash/[^"]+)"[^>]*>([^<]{8,300})</a>', html):
            titled.add(m.group(1))
            if host + m.group(1) in urls:
                continue
            urls.add(host + m.group(1))
            out.append((re.sub(r"\s+", " ", m.group(2)).strip(), host + m.group(1)))
            main_track += m.group(1).endswith("-Abstract-Conference.html")
        adv = re.search(r"(\d[\d,]*)\s+papers\b", re.sub(r"<[^>]+>", " ", html))
        adv_n = int(adv.group(1).replace(",", "")) if adv else None
        log(f"  proceedings {name} {y} {vol}: {len(links)} unique paper links, {len(titled & links)} titled"
            + (f", publisher advertises {adv_n} (a list denominator, not recall)" if adv_n is not None
               else ", no advertised count"))
        # ChatGPT 18:42: the audit used to run only when a page had paper links, so a fetched volume
        # that advertised N > 0 papers but parsed zero links (template change, interstitial, other
        # anchor syntax) passed silently whenever another volume supplied main-track titles. Every
        # fetched volume of a published year is now audited on its own, zero links included.
        PROCEEDINGS_AUDIT.append(f"{name} {y} {vol}: {len(links)} links, {len(titled & links)} titled, "
                                 f"{len(links - titled)} untitled, advertised "
                                 + (str(adv_n) if adv_n is not None else "none"))
        if expected and not links:
            VENUE_INCOMPLETE.append(f"{name} {y} proceedings volume {vol} parsed 0 paper links"
                                    + (f" of {adv_n} advertised" if adv_n is not None else "")
                                    + f" ({len(html)} bytes)")
        if expected and links:
            if adv_n is not None and len(links) < adv_n:
                VENUE_INCOMPLETE.append(f"{name} {y} proceedings volume {vol} lists {len(links)} of "
                                        f"{adv_n} advertised papers")
            if len(links - titled) > PROCEEDINGS_TITLE_SHORTFALL * len(links):
                VENUE_INCOMPLETE.append(f"{name} {y} proceedings volume {vol}: {len(links - titled)} of "
                                        f"{len(links)} paper links have no parseable title")
        for sib in re.findall(r'href="(/paper_files/paper/' + str(y) + r'/[A-Za-z0-9_.-]+)/?"', html):
            if sib.rsplit("/", 1)[1] not in ("hash", "file") and host + sib not in seen:
                queue.append(host + sib)
    log(f"  proceedings {name} {y}: {len(out)} titles, {main_track} main-track, "
        f"{len(seen)} volume page(s) visited")
    if not expected or root_bytes is None and not out:
        return out
    if not out:
        # Codex 16:35: a 200 response with zero parsed titles (changed template, interstitial)
        # used to log "0 titles" and pass as a complete listing. A published listing that parses
        # to zero titles is a parse failure and degrades the channel.
        VENUE_INCOMPLETE.append(f"{name} {y} proceedings page parsed 0 titles ({root_bytes} bytes)")
    elif not main_track and y >= 2022:
        # Non-zero is not complete either: on 24 November 2026 papers.nips.cc/paper_files/paper/2025
        # listed only the 64-paper Creative AI track, and test 35 logged "NeurIPS 2025: 64 titles"
        # as a full listing. Since 2022 both sites mark main-track papers "-Abstract-Conference.html".
        # Counted over every volume visited, so this fires only when no sibling volume supplied them.
        VENUE_INCOMPLETE.append(f"{name} {y} proceedings page has no main-track papers "
                                f"({len(out)} titles from other tracks only)")
    return out


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
    for name in PROCEEDINGS:
        for y in years:
            for title, url in _proceedings_titles(name, y):
                kh = [k for k in CORE if k in title.lower()]
                if kh:
                    out.append({"channel": "venue", "id": "", "title": title, "date": str(y), "url": url,
                                "why": f"{name} {y} (proceedings site): " + ", ".join(kh[:5])})
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
# Seeds whose cited-by results are missing or partial (ChatGPT 12:56, 24 Nov 2026): a failed DOI
# batch, a seed resolved by neither DOI nor title, a failed or unparsable cited-by page, or more
# in-window citing works than the page cap reads. Any entry marks `cites` DEGRADED even when
# other seeds returned candidates. Calls skipped by the budget breaker are not repeated here:
# the breaker already counts them against the channel.
CITES_INCOMPLETE: list[str] = []
CITES_PER_PAGE = 100
CITES_MAX_PAGES = 5  # 500 in-window citing works per seed; beyond that the seed is logged as truncated


def _confirm_seed(aid: str, title: str, hits: list[dict]) -> dict | None:
    """Pick the title-search hit that is the seed: one carrying the seed's arXiv ID (in `ids` or
    its DOI) wins; otherwise exactly one hit whose full normalized title equals the digest title.
    Several exact-title hits with different IDs, or none, are ambiguous and return None."""
    for h in hits:
        blob = " ".join(str(v) for v in (h.get("ids") or {}).values()) + " " + (h.get("doi") or "")
        if aid in blob.lower():
            return h
    want = norm_title(title)
    exact = [h for h in hits if want and norm_title(h.get("title") or "") == want]
    return exact[0] if len({h.get("id") for h in exact}) == 1 else None


def cited_by_candidates(idx: dict, since: dt.date, max_seeds: int = 60) -> list[dict]:
    """OpenAlex: works citing our Tier A arXiv seeds. Citation indexing lags, so the
    window is widened to 180 days; dedupe against the index removes known works."""
    since = min(since, dt.date.today() - dt.timedelta(days=180))
    out = []
    seeds = []
    owner_title: dict[str, str] = {}  # seed arXiv ID -> title of the Tier A digest it came from
    for p in sorted(PUBS.glob("*.md")):
        if p.name in ("INDEX.md", "_TEMPLATE.md"):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"\| \*\*Evidence tier\*\* \| (\*\*)?A\b", t):
            m = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", t)
            if m and m.group(1) not in owner_title:
                seeds.append(m.group(1))
                owner_title[m.group(1)] = _digest_title(t)
    seeds = seeds[:max_seeds]
    # Resolve seeds by their arXiv DOI in batched list requests ($0.0001 each). Title search
    # ($0.001 each) was the only route until 24 November 2026 and helped spend the daily budget.
    works: dict[str, dict] = {}
    for i in range(0, len(seeds), 40):
        chunk = ["10.48550/arxiv." + a for a in seeds[i:i + 40]]
        data = get("https://api.openalex.org/works?filter=doi:" + "|".join(chunk)
                   + "&per-page=50&select=id,doi,title,cited_by_count" + MAILTO, retries=3)
        if not data:
            if not OA["breaker"]:
                CITES_INCOMPLETE.append(f"DOI batch {i // 40 + 1} ({len(chunk)} seeds) failed")
            continue
        try:
            for r in json.loads(data).get("results", []):
                m = re.search(r"arxiv\.(\d{4}\.\d{4,5})", (r.get("doi") or "").lower())
                if m:
                    works[m.group(1)] = r
        except Exception:  # noqa: BLE001
            CITES_INCOMPLETE.append(f"DOI batch {i // 40 + 1} ({len(chunk)} seeds) unparsable")
    log(f"  cites: {len(seeds)} Tier A arXiv seeds, {len(works)} resolved by DOI")
    for aid in seeds:
        w = works.get(aid)
        if not w:
            # ChatGPT 13:06: use the title of the digest that owns the seed, never the first digest
            # that merely mentions its arXiv ID (a citing digest would validate the wrong paper).
            h1 = owner_title.get(aid, "")
            if not h1:
                CITES_INCOMPLETE.append(f"{aid} unresolved (no DOI match, no digest title)")
                continue
            sq = get("https://api.openalex.org/works?filter=title.search:" + urllib.parse.quote(re.sub(r"[,:|]", " ", h1)[:120])
                     + "&per-page=5&select=id,title,doi,ids,cited_by_count" + MAILTO, retries=2)
            try:
                res0 = json.loads(sq).get("results", []) if sq else []
            except Exception:  # noqa: BLE001
                res0 = []
            if not res0:
                log(f"  cites {aid}: not found in OpenAlex by DOI or title ({h1[:50]})" + (" (breaker)" if OA["breaker"] else ""))
                if not OA["breaker"]:
                    CITES_INCOMPLETE.append(f"{aid} unresolved by DOI or title")
                continue
            w = _confirm_seed(aid, h1, res0)
            if w is None:
                # ChatGPT 13:01: the first title hit is not evidence of identity. A wrong match can
                # return complete pages for another paper's citers and hide the seed's own network.
                log(f"  cites {aid}: title search returned {len(res0)} hits, none confirmed as the seed ({h1[:50]})")
                CITES_INCOMPLETE.append(f"{aid} title match unconfirmed ({len(res0)} hits, none with its arXiv ID "
                                        f"or a unique exact title)")
                continue
            # ChatGPT 13:01 live-validation ask: show what the fallback selected and why, so each
            # title-fallback seed can be checked by identifier against an independent resolver.
            how = "arXiv ID" if aid in (" ".join(str(v) for v in (w.get("ids") or {}).values()) + " "
                                        + (w.get("doi") or "")).lower() else "unique exact title"
            log(f"  cites: fallback seed {aid} -> {w['id'].rsplit('/', 1)[-1]} by {how} "
                f"(doi {(w.get('doi') or 'none').replace('https://doi.org/', '')}, "
                f"{w.get('cited_by_count', '?')} citations; {len(res0)} hits; \"{(w.get('title') or '')[:60]}\")")
        wid = w["id"].rsplit("/", 1)[-1]
        time.sleep(0.2)
        res: list[dict] = []
        total = None
        for page in range(1, CITES_MAX_PAGES + 1):
            data = get(f"https://api.openalex.org/works?filter=cites:{wid},from_publication_date:{since.isoformat()}"
                       f"&per-page={CITES_PER_PAGE}&page={page}&select=id,title,doi,publication_date,primary_location"
                       + MAILTO, retries=1)
            if not data:
                if not OA["breaker"]:
                    CITES_INCOMPLETE.append(f"{aid} page {page} failed after {len(res)} citing works")
                break
            try:
                j = json.loads(data)
                batch = j.get("results", [])
                total = (j.get("meta") or {}).get("count", total)
            except Exception:  # noqa: BLE001
                CITES_INCOMPLETE.append(f"{aid} page {page} unparsable after {len(res)} citing works")
                break
            res += batch
            if total is not None and len(res) >= total:
                break
            if len(batch) < CITES_PER_PAGE:
                if total is not None and len(res) < total:
                    CITES_INCOMPLETE.append(f"{aid} short page {page} at {len(res)} of {total} citing works")
                break
            time.sleep(0.2)
        else:
            if total is not None and len(res) < total:
                CITES_INCOMPLETE.append(f"{aid} truncated at {len(res)} of {total} citing works")
        log(f"  cites {aid} ({(w.get('title') or '')[:40]}, {w.get('cited_by_count', '?')} total): {len(res)}"
            + (f" of {total}" if total is not None else "") + f" citing works since {since}")
        for r in res:
            title = r.get("title") or ""
            loc = (r.get("primary_location") or {}).get("landing_page_url") or ""
            out.append({"channel": "cites", "id": (r.get("doi") or "").replace("https://doi.org/", ""),
                        "title": title, "date": r.get("publication_date", ""), "url": loc or r.get("id", ""),
                        "why": f"cites {aid} ({(w.get('title') or '')[:50]})"})
        time.sleep(0.5)
    if CITES_INCOMPLETE:
        log(f"  cites incomplete: {len(CITES_INCOMPLETE)} seeds or batches missing or partial: "
            + "; ".join(CITES_INCOMPLETE[:6]) + (" …" if len(CITES_INCOMPLETE) > 6 else ""))
    return out


# --------------------------------------------------------------------------- references
def _digest_title(t: str) -> str:
    # Some digests start with a UTF-8 BOM; it used to leak into title searches ("\ufeff# Ansor").
    return t.lstrip("\ufeff").splitlines()[0].lstrip("# ").split(" (")[0].strip()


def _digest_keys(t: str) -> tuple[str, str]:
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", t)
    if m:
        return "10.48550/arxiv." + m.group(1), ""
    m = re.search(r"doi\.org/(10\.\d{4,9}/[^\s)\]|>]+)", t) or re.search(r"\b(10\.1145/\d+\.\d+|10\.1145/\d+)", t)
    if m:
        return m.group(1).lower().rstrip("."), ""
    return "", _digest_title(t)


MECHANISM_TERMS = ["memory", "reflect", "skill", "self-improv", "self-evolv", "experience", "agent",
                   "harness", "workflow", "superoptim", "autotun", "search", "compiler", "kernel"]

# Sources the method once missed. Each run must recover them from the raw candidates (before the
# index dedupe) or say which ones it missed: a regression test for the channels themselves.
KNOWN_POSITIVES = [
    ("AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization", "venue"),
    ("Reflexion: Language Agents with Verbal Reinforcement Learning", "refs"),
    ("Voyager: An Open-Ended Embodied Agent with Large Language Models", "refs"),
    ("MemGPT: Towards LLMs as Operating Systems", "refs"),
    ("TASO: Optimizing Deep Learning Computation with Automatic Generation of Graph Substitutions", "refs"),
    ("Ansor: Generating High-Performance Tensor Programs for Deep Learning", "refs"),
]


REFS_CUT: set[str] = set()  # unindexed refs leads dropped by the top-N cap (for the regression)
# Referenced works are ranked by citing-digest count and only this many are resolved to titles;
# a work below the cut has no title, so the known-positive check cannot see it by name.
REFS_RESOLVE_CAP = 4000  # test-32 (24 Nov): 2,668 distinct referenced works; 1,500 cut 1,168
REFS_AUDIT: dict[str, int] = {}
REFS_INCOMPLETE: list[str] = []  # unresolved seeds (with reason) and failed or short metadata batches
# ChatGPT 24 Nov (review of 6d41a41): the seed audit is rendered in its own uncapped ledger section,
# not through the capped, keyword-filtered fetch log. Matched-but-empty seeds are a different fact
# from unresolved identity and are listed apart (they do not mark refs DEGRADED).
REFS_SEED_GAPS: list[str] = []
REFS_SEED_EMPTY: list[str] = []


def references_candidates(idx: dict, min_digests: int = 2, top: int = 80) -> list[dict]:
    """Backward references: works that several of our digests cite but the index lacks.

    No date window and no compiler-vocabulary filter, on purpose. Every other channel is
    time-windowed and keyword-filtered, so a foundational or mechanism-layer source (Reflexion,
    Voyager, MemGPT, STOKE, TASO) can never surface through them: it is old, and it does not say
    "compiler". If two or more of our own sources build on it, the survey should know why it is
    absent. Added 24 November 2026 after the agent-memory miss. Papers are resolved in batches by
    DOI (arXiv papers by their 10.48550 DOI); title search is a fallback for papers without one."""
    by_doi: dict[str, str] = {}
    by_title: dict[str, str] = {}
    # ChatGPT 13:11: every seed that contributes no reference list is named with its reason, and
    # a request failure is kept apart from a valid zero-hit answer; any entry marks refs DEGRADED.
    seed_gaps: list[str] = []
    dup_seeds: list[tuple[str, str]] = []  # (stem, stem already holding the same DOI or title)
    for p in sorted(PUBS.glob("*.md")):
        if p.name in ("INDEX.md", "_TEMPLATE.md"):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"\| \*\*Type\*\* \| paper", t):
            continue
        doi, title = _digest_keys(t)
        if doi:
            if doi in by_doi:
                dup_seeds.append((p.stem, by_doi[doi]))
            else:
                by_doi[doi] = p.stem
        elif len(title) >= 12:
            if title in by_title:
                dup_seeds.append((p.stem, by_title[title]))
            else:
                by_title[title] = p.stem
        else:
            seed_gaps.append(f"{p.stem} unresolved (no DOI, no usable title)")
    counts: dict[str, set[str]] = {}
    resolved = empty = 0
    empty_seeds: list[str] = []  # matched (DOI or unique exact title) but OpenAlex lists no references
    doi_hit: set[str] = set()       # digests matched by DOI, with or without a reference list
    doi_hit_refs: set[str] = set()  # ... of which OpenAlex returned a non-empty reference list
    title_hit: set[str] = set()
    title_unconfirmed: list[str] = []  # title searches with hits but no unique exact-title record

    def add(work: dict, stem: str) -> None:
        nonlocal resolved, empty
        refs = work.get("referenced_works") or []
        resolved += 1
        if not refs:
            empty += 1
            empty_seeds.append(stem)
        for w in refs:
            counts.setdefault(w.rsplit("/", 1)[-1], set()).add(stem)

    dois = list(by_doi)
    for i in range(0, len(dois), 40):
        chunk = dois[i:i + 40]
        time.sleep(0.2)
        data = get("https://api.openalex.org/works?filter=doi:" + "|".join(chunk)
                   + "&per-page=50&select=id,doi,title,referenced_works" + MAILTO, retries=2)
        try:
            res = json.loads(data).get("results", []) if data else None
        except Exception:  # noqa: BLE001
            res = None
        if res is None:
            seed_gaps.append(f"DOI batch {i // 40 + 1} ({len(chunk)} seeds) "
                             + ("failed" if not data else "unparsable") + " -> title fallback")
            res = []
        for r in res:
            d = (r.get("doi") or "").replace("https://doi.org/", "").lower()
            if d in by_doi and by_doi[d] not in doi_hit:
                doi_hit.add(by_doi[d])
                if r.get("referenced_works"):
                    doi_hit_refs.add(by_doi[d])
                add(r, by_doi[d])
    # Only a DOI *miss* falls back to a title search. A DOI hit with an empty reference list is the
    # same OpenAlex record; searching its title again would cost $0.001 and count it twice.
    doi_miss = [stem for stem in by_doi.values() if stem not in doi_hit]
    title_only = len(by_title)
    for stem in doi_miss:
        title = _digest_title((PUBS / f"{stem}.md").read_text(encoding="utf-8", errors="ignore"))
        if len(title) >= 12:
            if title in by_title:
                dup_seeds.append((stem, by_title[title]))
            else:
                by_title[title] = stem
        else:
            seed_gaps.append(f"{stem} unresolved (DOI miss, no usable title)")
    title_failed: list[str] = []
    title_zero: list[str] = []
    for title, stem in by_title.items():
        time.sleep(0.2)
        q = re.sub(r"[,:|]", " ", title)[:120]
        data = get("https://api.openalex.org/works?filter=title.search:" + urllib.parse.quote(q)
                   + "&per-page=5&select=id,title,referenced_works" + MAILTO, retries=2)
        try:
            res = json.loads(data).get("results", []) if data else None
        except Exception:  # noqa: BLE001
            res = None
        if res is None:
            title_failed.append(stem)
            seed_gaps.append(f"{stem} title search " + ("failed" if not data else "unparsable"))
            continue
        if not res:
            title_zero.append(stem)
            seed_gaps.append(f"{stem} unresolved (title search: 0 hits)")
            continue
        # ChatGPT 13:06: same identity standard as cites. A 30-character prefix let a different
        # paper with a shared opening supply the reference list; require exactly one record whose
        # full normalized title equals the digest title (same cost: one search call either way).
        want = norm_title(title)
        exact = [h for h in res if want and norm_title(h.get("title") or "") == want]
        if len({h.get("id") for h in exact}) == 1:
            title_hit.add(stem)
            add(exact[0], stem)
        else:
            title_unconfirmed.append(stem)
            seed_gaps.append(f"{stem} title match unconfirmed ({len(res)} hits, no unique exact title)")
    log(f"  refs: {len(by_doi)} paper digests by DOI, {len(by_title)} by title; {resolved} resolved, "
        f"{empty} with no reference list; {len(counts)} distinct referenced works")
    REFS_AUDIT.update({"doi_seeds": len(by_doi), "doi_hit": len(doi_hit), "doi_hit_refs": len(doi_hit_refs),
                       "doi_miss": len(doi_miss), "title_only": title_only, "title_hit": len(title_hit),
                       "title_unconfirmed": len(title_unconfirmed), "title_failed": len(title_failed),
                       "title_zero": len(title_zero), "distinct": len(counts)})
    DIAG.append(f"refs: audit — DOI seeds {len(by_doi)}: {len(doi_hit)} matched ({len(doi_hit_refs)} with a "
                f"reference list, {len(doi_hit) - len(doi_hit_refs)} empty), {len(doi_miss)} missed -> title "
                f"fallback; title-only seeds {title_only}; title searches matched {len(title_hit)} "
                f"(unique exact title), {len(title_unconfirmed)} with hits but no unique exact title, "
                f"{len(title_zero)} with 0 hits, {len(title_failed)} failed requests"
                + (": " + ", ".join(title_unconfirmed[:8]) + (" …" if len(title_unconfirmed) > 8 else "")
                   if title_unconfirmed else ""))
    if seed_gaps:
        DIAG.append(f"refs seeds unresolved: {len(seed_gaps)} — " + "; ".join(seed_gaps))
    REFS_SEED_GAPS[:] = seed_gaps
    REFS_SEED_EMPTY[:] = sorted(empty_seeds) + [f"{s} (duplicate key of {o}; its citations are counted under {o})"
                                                for s, o in dup_seeds]
    ranked = sorted(((len(v), k) for k, v in counts.items() if len(v) >= 1), reverse=True)[:REFS_RESOLVE_CAP]
    REFS_AUDIT["precut"] = max(0, len(counts) - REFS_RESOLVE_CAP)
    if REFS_AUDIT["precut"]:
        DIAG.append(f"refs truncated: {REFS_AUDIT['precut']} referenced works ranked below the "
                    f"{REFS_RESOLVE_CAP:,}-work cap were never resolved to titles")
    out: list[dict] = []
    returned = 0
    failed_batches: list[str] = []
    for i in range(0, len(ranked), 50):
        chunk = [k for _, k in ranked[i:i + 50]]
        time.sleep(0.2)
        data = get("https://api.openalex.org/works?filter=openalex:" + "|".join(chunk)
                   + "&per-page=50&select=id,title,doi,publication_date,ids,primary_location" + MAILTO, retries=2)
        try:
            res = json.loads(data).get("results", []) if data else None
        except Exception:  # noqa: BLE001
            res = None
        if res is None:
            failed_batches.append(f"batch {i // 50 + 1} ({len(chunk)} works) failed")
            res = []
        elif len(res) < len(chunk):
            failed_batches.append(f"batch {i // 50 + 1} returned {len(res)} of {len(chunk)}")
        returned += len(res)
        for r in res:
            wid = r["id"].rsplit("/", 1)[-1]
            title = r.get("title") or ""
            doi = (r.get("doi") or "").replace("https://doi.org/", "")
            m = re.search(r"(\d{4}\.\d{4,5})", doi + json.dumps(r.get("primary_location") or {}))
            ax = m.group(1) if m else ""
            indexed = known(idx, arxiv=ax, doi=doi, title=title)
            by = sorted(counts[wid])
            # Two or more citing digests: always a lead. One: only if the title names an agent or
            # optimizer mechanism, so single-citation foundations (a memory or reflection paper
            # cited once) still surface without flooding the ledger with every reference.
            if not indexed and len(by) < min_digests and not any(k in title.lower() for k in MECHANISM_TERMS):
                continue
            loc = (r.get("primary_location") or {}).get("landing_page_url") or (f"https://doi.org/{doi}" if doi else r["id"])
            out.append({"channel": "refs", "id": doi, "title": title, "date": r.get("publication_date", ""),
                        "url": loc, "n": len(by), "indexed": indexed,
                        "why": f"cited by {len(by)} digests: " + ", ".join(by[:6]) + (" …" if len(by) > 6 else "")})
    out.sort(key=lambda c: -c["n"])
    # Indexed works are returned too (the index dedupe in main drops them) so the known-positive
    # regression can see what the channel recovers; only unindexed leads are capped.
    fresh = [c for c in out if not c["indexed"]]
    REFS_CUT.update(norm_title(c["title"])[:50] for c in fresh[top:])
    # ChatGPT 12:50: report works actually returned, not works requested; a failed or short
    # metadata batch marks refs DEGRADED even when other batches returned candidates.
    REFS_AUDIT.update({"requested": len(ranked), "returned": returned, "failed_batches": len(failed_batches)})
    REFS_INCOMPLETE[:] = seed_gaps + failed_batches
    if failed_batches:
        DIAG.append(f"refs incomplete: {returned} of {len(ranked)} requested works returned; "
                    + "; ".join(failed_batches[:6]) + (" …" if len(failed_batches) > 6 else ""))
    log(f"  refs: {returned} of {len(ranked)} requested referenced works resolved; {len(out) - len(fresh)} already indexed; "
        f"{len(fresh)} unindexed leads (top {top} kept)")
    return [c for c in out if c["indexed"]] + fresh[:top]


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
def _github_fetch_json(url: str):
    headers = dict(UA)
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def github_repo_metadata(name: str, fetch_json, max_hops: int = 3) -> dict:
    """Return the GitHub repository object for an indexed name, following renames.

    GitHub answers ``GET /repos/<old-name>`` for a renamed repository either with a
    301 to ``/repositories/<id>`` (which urllib follows on its own) or, through a
    client that does not follow redirects, with the redirect itself. Both end in a
    body whose ``full_name`` is the canonical name. Anything else (404, rate limit,
    a non-object body) raises, so the caller can report it; nothing is guessed.
    """
    url = f"https://api.github.com/repos/{name}"
    for _ in range(max_hops + 1):
        try:
            data = fetch_json(url)
        except urllib.error.HTTPError as exc:
            location = (exc.headers or {}).get("Location") if exc.code in (301, 302, 307, 308) else None
            if not location:
                raise
            url = location
            continue
        if not isinstance(data, dict) or not data.get("full_name"):
            raise ValueError("repository metadata without full_name")
        return data
    raise ValueError(f"more than {max_hops} redirects")


def resolve_canonical_repos(names: list[str], fetch_json) -> list[dict]:
    """Group indexed repository names by the repository they actually denote.

    Returns one record per distinct repository, ``{"repo": canonical lower-case
    full name, "identity": "id:<n>" | "name:<n>", "aliases": [indexed names]}``,
    sorted by canonical name. Two names collapse only when GitHub reports the same
    repository id: a genuine fork has its own id and stays separate even when its
    commits carry the same SHAs. A name whose metadata cannot be read is kept under
    its indexed name and reported, never dropped.
    """
    groups: dict[str, dict] = {}
    unresolved = []
    for name in sorted(names):
        try:
            meta = github_repo_metadata(name, fetch_json)
        except Exception as exc:  # noqa: BLE001 - fail visibly, keep the name
            DIAG.append(f"repoevent metadata failed: {name}: {exc}; "
                        "identity unresolved, events will be attempted under its indexed name")
            identity, repo = f"name:{name}", name
            unresolved.append(name)
        else:
            repo = str(meta["full_name"]).lower()
            identity = f"id:{meta['id']}" if meta.get("id") else f"name:{repo}"
        group = groups.setdefault(identity, {"repo": repo, "identity": identity, "aliases": [],
                                             "unresolved": name in unresolved})
        group["aliases"].append(name)
    records = sorted(groups.values(), key=lambda g: g["repo"])
    for g in records:
        renamed = [a for a in g["aliases"] if a != g["repo"]]
        if renamed:
            DIAG.append(f"repoevent alias: {', '.join(renamed)} -> {g['repo']} ({g['identity']})")
    resolved = len(records) - len(unresolved)
    DIAG.append(f"repoevent coverage: {len(names)} indexed names -> {resolved} resolved canonical "
                f"repositories + {len(unresolved)} unresolved indexed names"
                + (f" ({', '.join(unresolved)}); unresolved names may still alias each other"
                   if unresolved else ""))
    return records


def indexed_repo_event_candidates(idx: dict, since: dt.date, *, max_repos: int = 120,
                                  max_events: int = 8, fetch_json=None) -> list[dict]:
    """Enumerate commit events even for repositories ALREADY in the index.

    These are review leads, not new systems or independent evidence families.
    The optional fetch_json callback permits network-free deterministic tests.
    Truncation and fetch failures must remain visible in Channel diagnostics.

    Indexed names are first resolved to canonical repositories (a renamed
    repository such as ``amd-agi/geak-agent`` -> ``amd-agi/geak`` is one
    repository, not two), so the ``max_repos`` cap counts distinct repositories,
    each repository is fetched once, and one truncation line names its aliases.
    """
    priority = ("apache/tvm-tirx", "tile-ai/tilelang",
                "mlc-ai/tirx-harness", "nvidia/auto-ontology")
    fetch_json = fetch_json or _github_fetch_json
    names = sorted(r for r in idx["github"] if re.fullmatch(r"[\w.-]+/[\w.-]+", r))
    records = resolve_canonical_repos(names, fetch_json)
    records = ([g for g in records if g["repo"] in priority]
               + [g for g in records if g["repo"] not in priority])
    if max_repos > 0 and len(records) > max_repos:
        unres = sum(1 for g in records if g.get("unresolved"))
        DIAG.append(f"repoevent truncated: only {max_repos}/{len(records)} repository groups "
                    f"selected for event fetching ({len(records) - unres} resolved + {unres} unresolved; "
                    f"{len(names)} indexed names); unvisited include "
                    f"{', '.join(g['repo'] for g in records[max_repos:max_repos+5])}")
        records = records[:max_repos]

    out = []
    for group in records:
        repo, aliases = group["repo"], group["aliases"]
        renamed = [a for a in aliases if a != repo]
        label = f"{repo} (indexed as {', '.join(aliases)})" if renamed else repo
        provenance = f"family {repo}" + (f" (indexed as {', '.join(aliases)})" if renamed else "")
        repo_limit = max(max_events, 50) if repo in priority else max_events
        url = (f"https://api.github.com/repos/{repo}/commits?since={since.isoformat()}T00%3A00%3A00Z"
               f"&per_page={min(repo_limit+1, 100)}")
        try:
            commits = fetch_json(url)
            if not isinstance(commits, list):
                raise ValueError("non-list GitHub commits response")
        except Exception as exc:  # fail soft, but record omissions
            DIAG.append(f"repoevent failed: {label}: {exc}")
            continue
        if len(commits) > repo_limit:
            DIAG.append(f"repoevent truncated: {label}: first {repo_limit} of >{repo_limit} commits; "
                        "older updates require review")
        for event in commits[:repo_limit]:
            sha = event.get("sha", "")
            data = event.get("commit") or {}
            date = ((data.get("committer") or {}).get("date") or "")[:10]
            if not sha or (date and date < since.isoformat()):
                continue
            subject = (data.get("message") or "").split("\n", 1)[0]
            out.append({"channel": "repoevent", "id": f"{repo}@{sha}",
                        "title": f"{repo}: {subject}"[:160], "date": date,
                        "url": event.get("html_url") or f"https://github.com/{repo}/commit/{sha}",
                        "why": f"indexed-repo COMMIT event {sha[:12]}; {provenance}; "
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
            DIAG.append(f"repoevent releases failed: {label}: {exc}")
            continue
        for release in releases:
            published = (release.get("published_at") or "")[:10]
            tag = release.get("tag_name") or ""
            if not published or published < since.isoformat() or not tag:
                continue
            out.append({"channel": "repoevent", "id": f"{repo}@release:{tag}",
                        "title": f"{repo}: release {tag}"[:160], "date": published,
                        "url": release.get("html_url") or f"https://github.com/{repo}/releases/tag/{tag}",
                        "why": f"indexed-repo RELEASE {tag}; {provenance}; "
                               f"observed in sweep {dt.date.today()}; "
                               "review changelog, design and compatibility"})
    return out


def canonical_event_url(url: str) -> str:
    """Normalize a GitHub event URL for deduplication, without conflating events.

    Host and the owner/repository path segments are case-insensitive on GitHub and
    are lower-cased; a commit SHA or release tag is kept as is (tags are
    case-sensitive). Query strings, fragments and a trailing slash are dropped.
    ``/commit/<sha>`` and ``/releases/tag/<tag>`` therefore never collide.
    """
    parts = urllib.parse.urlsplit(url.strip())
    segments = [s for s in parts.path.split("/") if s]
    segments[:2] = [s.lower() for s in segments[:2]]
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}/" + "/".join(segments)


def dedupe_repo_events(rows: list[dict]) -> list[dict]:
    """Second guard: collapse indexed-repo event rows that share a canonical URL.

    Keeps the first row (input order is deterministic: priority repositories, then
    canonical name order, then API order), appends the other rows' families to its
    provenance, and reports the before/after counts in the diagnostics. Title or
    SHA-prefix equality never merges rows; only the normalized event URL does.
    """
    kept: dict[str, dict] = {}
    for row in rows:
        key = canonical_event_url(row["url"])
        if key not in kept:
            kept[key] = dict(row)
            continue
        family = re.search(r"family ([^\s;]+)", row["why"])
        other = family.group(1) if family else row["id"].split("@", 1)[0]
        if other not in kept[key]["why"]:
            kept[key]["why"] += f"; also listed under {other}"
    out = list(kept.values())
    if len(out) != len(rows):
        DIAG.append(f"repoevent dedupe: {len(rows)} event rows before URL dedupe, {len(out)} after")
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
# Do not gate HN discovery by popularity: a low-vote first-party architecture post
# can still be a useful lead. Only the bounded page cap limits retrieval.
HN_MAX_PAGES, HN_MIN_POINTS = 3, None
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


def hn_numeric_filters(since_epoch: int, min_points: int | None = None) -> str:
    """Bound discovery by publication date, not by votes (votes are not evidence).

    Optional thresholds support reproducing an earlier sweep; routine sweeps use
    min_points=None. The HN_MAX_PAGES limit still warrants truncation diagnostics.
    """
    date_filter = f"created_at_i>{since_epoch}"
    return date_filter if min_points is None else f"{date_filter},points>{min_points}"


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
    # No popularity threshold: obscure architectural posts must be discoverable.
    # HN_MAX_PAGES bounds cost and its truncation is explicitly logged.
    for q in HN_QUERIES:
        hits = []
        for page in range(HN_MAX_PAGES):
            u = ("https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=100"
                 f"&page={page}&query={urllib.parse.quote(q)}"
                 f"&numericFilters={hn_numeric_filters(ts, HN_MIN_POINTS)}")
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


def render_fetch_log(refs_ran: bool) -> list[str]:
    """Ledger diagnostics: the refs seed audit in full (uncapped, unfiltered), then the capped fetch log.

    ChatGPT (review of 6d41a41): the `refs seeds unresolved` line matched neither the priority
    keys nor DIAG_KEEP when every gap was a 0-hit or unconfirmed title, so the ledger could show
    DEGRADED while omitting the seeds; the status line shows only six. The audit now has its own
    section that lists every seed, so the ledger is the complete record."""
    lines: list[str] = []
    if refs_ran:
        lines += ["### refs seed audit (complete)", "",
                  f"Seeds with no reference list because their identity is unresolved or the request failed "
                  f"({len(REFS_SEED_GAPS)}; any entry marks refs DEGRADED):", ""]
        lines += [f"- {g}" for g in REFS_SEED_GAPS] or ["- none"]
        lines += ["", f"Seeds matched, but OpenAlex lists no references, or duplicate keys "
                      f"({len(REFS_SEED_EMPTY)}; identity resolved, not DEGRADED):", ""]
        lines += [f"- {s}" for s in REFS_SEED_EMPTY] or ["- none"]
        lines.append("")
    lines += ["Fetch log (failures and venue page sizes):", ""]
    top = [d for d in DIAG if any(k in d for k in ("timing ", "refs:", "refs seeds", "cites:", "proceedings ", "truncated",
                                                   "openalex venue", "openalex budget", "openalex breaker",
                                                   "openalex search cap"))]
    mid = [d for d in DIAG if d not in top and ("openalex" in d.lower() or "HTTP" in d)]
    low = [d for d in DIAG if d not in top and d not in mid and ("cites " in d or any(t in d for t in DIAG_KEEP))]
    lines += [f"- {d}" for d in (top + mid + low)[:400]]
    lines.append("")
    return lines


def corpus_commit(croot: Path) -> tuple[str, dt.date] | None:
    """Full SHA and UTC commit date of a frozen-corpus worktree, or None outside git.

    Codex 14:58: the frozen cutoff must follow the snapshot. The default cutoff is the day after
    the corpus commit, and an explicit --since that disagrees with it marks the ledger DEGRADED."""
    import subprocess
    try:
        out = subprocess.run(["git", "-C", str(croot), "log", "-1", "--format=%H %cI"],
                             capture_output=True, text=True, check=True).stdout.split()
        when = dt.datetime.fromisoformat(out[1].replace("Z", "+00:00")).astimezone(dt.timezone.utc)
        return out[0], when.date()
    except Exception:  # noqa: BLE001
        return None


# --------------------------------------------------------------------------- main
_ARXIV_ID = re.compile(r"(?:arxiv\.org/(?:abs|pdf|html)/|10\.48550/arxiv\.|^|\s)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_DOI_ID = re.compile(r"doi\.org/(10\.\d{4,9}/[^\s)\]|>]+)", re.I)
_GH_ID = re.compile(r"github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", re.I)


def _owning_ids(t: str) -> dict:
    """Identifiers of the digest's own source: read only from its `| **Link** |` row, never from
    related-work links in the body (Codex 14:13: a cited paper must not stand in for the source)."""
    row = next((ln for ln in t.splitlines() if ln.startswith("| **Link** |")), "")
    arx = {m.group(1) for m in re.finditer(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", row)}
    dois = {m.group(1).lower().rstrip(".") for m in _DOI_ID.finditer(row)}
    arx |= {d.split("arxiv.", 1)[1] for d in dois if d.startswith("10.48550/arxiv.")}
    gh = {m.group(1).lower().removesuffix(".git") for m in _GH_ID.finditer(row)}
    yr = re.search(r"^\| \*\*Year\*\* \| (\d{4})", t, re.M)
    return {"arxiv": arx, "doi": dois, "gh": gh, "year": int(yr.group(1)) if yr else 0, "has_link": bool(row)}


def heldout_sources(later_root: Path) -> list[dict]:
    """Digests in the later tree that the frozen corpus (PUBS) lacks, with their own identifiers."""
    have = {p.name for p in PUBS.glob("*.md")}
    out = []
    for p in sorted((later_root / "reference" / "publications").glob("*.md")):
        if p.name in ("INDEX.md", "_TEMPLATE.md") or p.name in have:
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        typ = re.search(r"\| \*\*Type\*\* \| ([a-z-]+)", t)
        out.append({"stem": p.stem, "title": _digest_title(t), "type": typ.group(1) if typ else "?", **_owning_ids(t)})
    return out


def _cand_ids(c: dict) -> dict:
    cid = (c.get("id") or "").strip().lower()
    blob = cid + " " + (c.get("url") or "").lower()
    arx = {m.group(1) for m in _ARXIV_ID.finditer(blob)}
    doi = {cid} if cid.startswith("10.") else set()
    doi |= {m.group(1).lower().rstrip(".") for m in _DOI_ID.finditer(blob)}
    gh = {cid.removesuffix(".git")} if re.fullmatch(r"[a-z0-9_.-]+/[a-z0-9_.-]+", cid) else set()
    gh |= {m.group(1).lower().removesuffix(".git") for m in _GH_ID.finditer(blob)}
    return {"arxiv": arx, "doi": doi, "gh": gh}


# Effective window of each channel (Codex 14:23): the publication-date class below is not a channel
# eligibility rule, because only arxiv, blogs and new-repo listings are bounded by `since`.
CHANNEL_WINDOWS = (
    "arxiv: submissions since the window start; "
    "refs: no date window (references of indexed Tier A digests); "
    "cites: citing works published since the earlier of the window start and 180 days ago; "
    "venues: listings for the current and preceding calendar years, with no window filter; "
    "github: tracked-org repos created since the window start, or older repos pushed since it, plus PyPI releases since it; "
    "ghsearch: repos pushed since the window start, whatever their creation date; "
    "blogs: posts since the window start; "
    "repoevent: already-indexed repos only, so it cannot recover a held-out source")


def _eligibility(h: dict, since: dt.date) -> str:
    """Publication-date class of a held-out source relative to the window start ("before window",
    "in window", "indeterminate", "undated"). It is not a statement about which channels can list the
    source: see CHANNEL_WINDOWS (Codex 14:23). Precision follows the
    evidence (Codex 14:19): an arXiv id gives year and month only, a Year row gives the year only, so
    a source dated in the cutoff month (or cutoff year) is "indeterminate" unless the window starts on
    the first day of that month (or year)."""
    if h["arxiv"]:
        a = min(h["arxiv"])
        ym, cut = (2000 + int(a[:2]), int(a[2:4])), (since.year, since.month)
        if ym != cut:
            return "in window" if ym > cut else "before window"
        return "in window" if since.day == 1 else "indeterminate"
    if h["year"]:
        if h["year"] != since.year:
            return "in window" if h["year"] > since.year else "before window"
        return "in window" if (since.month, since.day) == (1, 1) else "indeterminate"
    return "undated"


def match_heldout(h: dict, cands: list[dict]) -> tuple[set, set, set]:
    """(channels matched by an exact owning identifier, channels matched by full normalized title only,
    channels whose title-only match needs adjudication). A title match whose candidate carries an
    identifier of the same type that differs from the digest's own is a different work and is ignored."""
    nt = norm_title(h["title"])
    by_id, by_title, title_ids = set(), set(), {}
    for c in cands:
        ci = _cand_ids(c)
        if (h["arxiv"] & ci["arxiv"]) or (h["doi"] & ci["doi"]) or (h["gh"] & ci["gh"]):
            by_id.add(c["channel"])
            continue
        if nt and norm_title(c.get("title") or "") == nt:
            if any(h[k] and ci[k] and not (h[k] & ci[k]) for k in ("arxiv", "doi")):
                continue  # same title, different identifier: not this source
            by_title.add(c["channel"])
            key = next(iter(sorted(ci["arxiv"] or ci["doi"] or ci["gh"])), "")
            if key:
                title_ids.setdefault(key, set()).add(c["channel"])
    # Ambiguous: a short title (under four words), or title-only hits carrying two or more distinct identifiers.
    ambiguous = set()
    if by_title and (len(nt.split()) < 4 or len(title_ids) > 1):
        ambiguous, by_title = by_title, set()
    return by_id, by_title, ambiguous


def recall_section(later_root: Path, cands: list[dict], since: dt.date) -> list[str]:
    """Retrospective known-set recovery estimate (ChatGPT 13:49, Action 13:52; matching tightened per
    Codex 14:13). Metadata and citation counts are current, so this is not a historical replay."""
    held = heldout_sources(later_root)
    by_ch: dict[str, int] = {}
    rows, tally = [], {}
    for h in held:
        by_id, by_title, amb = match_heldout(h, cands)
        got = by_id | by_title
        for ch in got:
            by_ch[ch] = by_ch.get(ch, 0) + 1
        el = _eligibility(h, since)
        t = tally.setdefault(el, [0, 0, 0])
        t[0] += 1
        t[1] += bool(got)
        t[2] += bool(amb and not got)
        kind = "identifier" if by_id else "title only" if by_title else "ambiguous title" if amb else ""
        ym = f"20{min(h['arxiv'])[:2]}-{min(h['arxiv'])[2:4]}" if h["arxiv"] else (str(h["year"]) if h["year"] else "?")
        shown = ", ".join(sorted(got)) or ("**adjudicate:** " + ", ".join(sorted(amb)) if amb else "**not recovered**")
        rows.append(f"| {h['stem']} | {h['type']} | {ym} | {el} | {shown} | {kind or '—'} |")
    n = len(held)
    rec = sum(v[1] for v in tally.values())
    adj = sum(v[2] for v in tally.values())
    elig = "; ".join(f"{k}: {v[1]} of {v[0]} recovered" + (f", {v[2]} to adjudicate" if v[2] else "")
                     for k, v in sorted(tally.items()))
    nolink = [h["stem"] for h in held if not h["has_link"]]
    return ["## Frozen-corpus recovery estimate", "",
            f"Held-out set: {n} digests present in the later tree but absent from the frozen corpus. "
            f"Recovered by any channel before dedupe: **{rec} of {n}** ({adj} more need adjudication and are not counted). "
            f"By publication-date class relative to the window start {since.isoformat()}: {elig or 'none'}. "
            f"Per channel: {json.dumps(by_ch, sort_keys=True)}. "
            "A match uses only the digest's own identifiers (its Link row) or its full normalized title; a title-only "
            "match is labelled so a reviewer can check it, and a short or multiply-identified title is not counted. "
            "This is a retrospective known-set recovery estimate (current OpenAlex metadata and citations, today's "
            "arXiv/GitHub listings), not a historical replay. The date classes describe the source's publication "
            "date, not which channels could list it; channel windows differ (" + CHANNEL_WINDOWS + "), so a source "
            "dated before the window start can still be recovered by refs, cites, venues, github or ghsearch. "
            "\"indeterminate\" means the source's date (arXiv month or Year row) falls in the "
            "cutoff month or year and is too coarse to place it either side of the window start. Failed or DEGRADED channels above lower the denominator's meaning, so read the Status "
            "line first." + (f" Digests without a Link row (title matching only): {', '.join(nolink)}." if nolink else ""),
            "", "| Held-out digest | Type | Date | Date class | Recovered by | Match |", "|---|---|---|---|---|---|", *rows, ""]


RUN_START = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")


def ledger_date(out: Path, today: dt.date) -> str:
    """Header date for the ledger (ChatGPT/Codex 00:54). When the output file is named YYYY-MM-DD.md,
    as the workflow's --out always is, that date is the run's publication date and the header must
    agree with the path, branch and announcement. Only the header uses it; windows and eligibility
    still derive from `today`, so candidate generation is unchanged."""
    try:
        return dt.date.fromisoformat(out.stem).isoformat()
    except ValueError:
        return today.isoformat()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD; default: 21 days ago")
    ap.add_argument("--channels", default="arxiv,venues,cites,refs,github,ghsearch,blogs,repoevent")
    ap.add_argument("--out", help="output ledger path")
    ap.add_argument("--corpus-root", help="read INDEX, digests, repos.md and feeds.txt from this tree "
                    "(a git worktree of a historical SHA) instead of the working copy")
    ap.add_argument("--recall-against", help="with --corpus-root: a later tree whose extra digests form the "
                    "held-out set; report which of them the raw candidates recover, per channel")
    args = ap.parse_args()
    global INDEX, REPOS, PUBS, FEEDS
    if args.corpus_root:
        # ChatGPT 13:49: freeze the whole discovery input corpus, not only INDEX. Every corpus read
        # (index dedupe, refs seeds, cites seeds, org/repo watchlists, feeds) goes through these four.
        croot = Path(args.corpus_root).resolve()
        INDEX = croot / "reference" / "publications" / "INDEX.md"
        REPOS = croot / "reference" / "repos.md"
        PUBS = croot / "reference" / "publications"
        # ChatGPT 15:05: bind FEEDS unconditionally. A snapshot without feeds.txt (4336d72) must read
        # as "no feeds", never fall back to today's watchlist; load_feeds() already returns [] if absent.
        FEEDS = croot / "reference" / "discovery" / "feeds.txt"
        log(f"corpus root: {croot} ({len([p for p in PUBS.glob('*.md') if p.name not in ('INDEX.md', '_TEMPLATE.md')])} digests)")
    today = dt.date.today()
    since = dt.date.fromisoformat(args.since) if args.since else today - dt.timedelta(days=21)
    corpus, cutoff_note = None, ""
    if args.corpus_root:
        corpus = corpus_commit(croot)
        if corpus:
            expected_since = corpus[1] + dt.timedelta(days=1)
            if not args.since:
                since = expected_since
            cutoff_note = (f"Frozen corpus: `{corpus[0][:12]}` committed {corpus[1].isoformat()} UTC; cutoff "
                           f"{since.isoformat()} ({'explicit --since' if args.since else 'derived: day after the corpus commit'}"
                           + (f"; expected {expected_since.isoformat()}" if since != expected_since else "") + ").")
        else:
            cutoff_note = f"Frozen corpus: commit unknown (not a git tree); cutoff {since.isoformat()} unchecked."
        cutoff_note += (f" Frozen feeds: {len(load_feeds())} from the snapshot's feeds.txt." if FEEDS.exists() else
                        " Frozen feeds: none (the snapshot has no reference/discovery/feeds.txt; the current "
                        "watchlist is not used).")
    # ChatGPT 15:05: reject unknown channel names; "none" is the explicit fixture mode (no network).
    # ChatGPT 16:08: named known_channels so it does not shadow the module-level known() dedupe below.
    known_channels = {"arxiv", "venues", "cites", "refs", "github", "ghsearch", "blogs", "repoevent"}
    chans = set() if args.channels.strip() == "none" else {c.strip() for c in args.channels.split(",") if c.strip()}
    if chans - known_channels or (not chans and args.channels.strip() != "none"):
        ap.error(f"unknown channel(s): {', '.join(sorted(chans - known_channels)) or '(empty)'}; "
                 f"choose from {', '.join(sorted(known_channels))}, or 'none' for fixture mode")
    idx = load_index()
    log(f"index: {len(idx['arxiv'])} arXiv ids, {len(idx['doi'])} DOIs, {len(idx['github'])} repos, "
        f"{len(idx['titles'])} titles, {len(idx['orgs'])} orgs")

    cands: list[dict] = []
    _t0 = time.time()

    def _lap(name: str) -> None:
        nonlocal _t0
        log(f"  timing {name}: {time.time() - _t0:.0f}s, {len(cands)} raw so far")
        _t0 = time.time()

    if "arxiv" in chans:
        OA["channel"] = "arxiv"
        cands += arxiv_candidates(since)
        _lap("arxiv")
    # OpenAlex channels run in order of what nothing else can replace: refs has no date window and
    # no keyword filter; cites follows; venue listings last (proceedings sites and arXiv overlap them).
    # ChatGPT 16:08: probe the budget only when an OpenAlex channel runs, so --channels none stays offline.
    if chans & {"refs", "cites", "venues"}:
        rl = get("https://api.openalex.org/rate-limit" + (f"?api_key={urllib.parse.quote(OPENALEX_KEY)}" if OPENALEX_KEY else ""), retries=0)
        try:
            r0 = json.loads(rl).get("rate_limit", {}) if rl else {}
            log(f"  openalex budget at start: {r0.get('daily_remaining_usd', '?')} of {r0.get('daily_budget_usd', '?')} USD remaining")
        except Exception:  # noqa: BLE001
            log("  openalex budget at start: unknown (rate-limit endpoint unreadable)")
    if "refs" in chans:
        OA["channel"] = "refs"
        cands += references_candidates(idx)
        _lap("refs")
    if "cites" in chans:
        OA["channel"] = "cites"
        cands += cited_by_candidates(idx, since)
        _lap("cites")
    if "venues" in chans:
        OA["channel"] = "venues"
        cands += venue_candidates([today.year, today.year - 1])
        _lap("venues")
    if "github" in chans:
        OA["channel"] = "github"
        cands += github_candidates(idx, since)
        _lap("github")
    if "ghsearch" in chans:
        OA["channel"] = "ghsearch"
        cands += ghsearch_candidates(idx, since)
        _lap("ghsearch")
    if "blogs" in chans:
        OA["channel"] = "blogs"
        cands += blog_candidates(since)
        _lap("blogs")
    if "repoevent" in chans:
        OA["channel"] = "repoevent"
        cands += dedupe_repo_events(indexed_repo_event_candidates(idx, since))
        _lap("repoevent")

    seen = set()
    new, already = [], 0
    for c in cands:
        # A known repository may repeat a commit subject: only its SHA identifies the event.
        key = (c["channel"], c["id"]) if c["channel"] == "repoevent" else (c["channel"], norm_title(c["title"])[:80])
        if key in seen:
            continue
        seen.add(key)
        aid = c["id"] if c["channel"] == "arxiv" else ""
        doi = c["id"] if c["channel"] in ("venue", "cites", "refs") and c["id"].startswith("10.") else ""
        gh = c["id"] if c["channel"] == "github" else ""
        if c["channel"] == "blog" and c["id"].lower() in idx["urls"]:
            already += 1
            continue
        if c["channel"] != "repoevent" and known(idx, arxiv=aid, doi=doi, gh=gh, title=c["title"]):
            already += 1
            continue
        new.append(c)

    raw_titles: dict[str, set[str]] = {}
    for c in cands:
        raw_titles.setdefault(norm_title(c["title"])[:50], set()).add(c["channel"])
    per_raw = {}
    for c in cands:
        per_raw[c["channel"]] = per_raw.get(c["channel"], 0) + 1
    expected = {"arxiv": "arxiv", "venues": "venue", "cites": "cites", "refs": "refs"}
    degraded = [f"{v}: zero raw candidates" for k, v in expected.items() if k in chans and per_raw.get(v, 0) == 0]
    # A channel that lost OpenAlex calls to the budget breaker is degraded even if it returned rows.
    for ch, n in OA["skipped_in"].items():
        label = {"venues": "venue (OpenAlex listings)"}.get(ch, ch)
        if ch and ch not in degraded and label not in degraded:
            degraded.append(f"{label}: {n} OpenAlex calls skipped by the budget breaker or search cap")
    if "arxiv" in chans and ARXIV_INCOMPLETE:
        degraded.append(f"arxiv: {len(ARXIV_INCOMPLETE)} category pages incomplete ("
                        + "; ".join(ARXIV_INCOMPLETE[:6]) + (" …" if len(ARXIV_INCOMPLETE) > 6 else "") + ")")
    if "venues" in chans and VENUE_INCOMPLETE:
        degraded.append(f"venue: {len(VENUE_INCOMPLETE)} venue-year listings incomplete ("
                        + "; ".join(VENUE_INCOMPLETE[:6]) + (" …" if len(VENUE_INCOMPLETE) > 6 else "") + ")")
    if "refs" in chans and REFS_INCOMPLETE:
        degraded.append(f"refs: {len(REFS_INCOMPLETE)} seeds or metadata batches incomplete ("
                        + "; ".join(REFS_INCOMPLETE[:6]) + (" …" if len(REFS_INCOMPLETE) > 6 else "") + ")")
    if "cites" in chans and CITES_INCOMPLETE:
        degraded.append(f"cites: {len(CITES_INCOMPLETE)} seeds or batches incomplete ("
                        + "; ".join(CITES_INCOMPLETE[:6]) + (" …" if len(CITES_INCOMPLETE) > 6 else "") + ")")
    if corpus and since != corpus[1] + dt.timedelta(days=1):
        degraded.append(f"cutoff: --since {since.isoformat()} does not follow frozen corpus `{corpus[0][:12]}` "
                        f"(committed {corpus[1].isoformat()}); date classes and windows are relative to the wrong day")
    elif args.corpus_root and not corpus:
        degraded.append("cutoff: frozen corpus commit unknown, so --since cannot be checked against it")
    regress = []
    for t, ch in KNOWN_POSITIVES:
        key = norm_title(t)[:50]
        got = sorted(raw_titles.get(key, set()))
        if ch in got:
            verdict = "recovered by " + ", ".join(got)
        elif {"venue": "venues"}.get(ch, ch) not in chans:
            verdict = f"NOT TESTED: expected channel {ch} omitted from this run" + (f"; seen in {', '.join(got)}" if got else "")
        else:
            if key in REFS_CUT:
                why = "truncated (ranked below the refs top-N cap)"
            elif ch == "refs" and REFS_AUDIT.get("precut"):
                why = (f"possibly truncated before title resolution ({REFS_AUDIT['precut']} works below the "
                       f"{REFS_RESOLVE_CAP:,}-work cap are unnamed), or not cited by any resolved digest")
            elif ch == "refs" and REFS_INCOMPLETE:
                why = f"possibly lost in {len(REFS_INCOMPLETE)} unresolved seeds or incomplete metadata batches"
            elif ch == "venue" and VENUE_INCOMPLETE:
                why = f"possibly truncated ({len(VENUE_INCOMPLETE)} venue-year listings incomplete)"
            elif OA["skipped_in"].get({"venue": "venues"}.get(ch, ch)):
                why = "fetch failure (OpenAlex budget breaker)"
            elif per_raw.get(ch, 0) == 0:
                why = f"fetch failure ({ch} returned nothing)"
            else:
                why = f"not surfaced by {ch} although it returned {per_raw.get(ch, 0)} rows"
            verdict = f"MISSED via expected {ch}: {why}" + (f"; seen only in {', '.join(got)}" if got else "")
        regress.append(f"{t.split(':')[0]}: {verdict}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.out) if args.out else OUT_DIR / f"{today.isoformat()}.md"
    by = {}
    for c in new:
        by.setdefault(c["channel"], []).append(c)
    source_count = sum(c["channel"] != "repoevent" for c in new)
    event_count = len(new) - source_count
    sha = os.environ.get("GITHUB_SHA", "")
    if not sha:
        try:
            import subprocess
            sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
        except Exception:  # noqa: BLE001
            sha = "unknown"
    ledger_d = ledger_date(out, today)
    lines = [f"# Discovery ledger — {ledger_d}", "",
             *([f"Ledger date taken from the output path; windows and eligibility were computed on "
                f"{today.isoformat()} (the run crossed UTC midnight after the workflow bound its date).", ""]
               if ledger_d != today.isoformat() else []),
             f"Provenance: script `{sha[:12] or 'unknown'}` ({os.environ.get('GITHUB_REF_NAME', 'local')}), "
             f"run started {RUN_START} UTC. OpenAlex: key {'present' if OPENALEX_KEY else 'absent (keyless, about $0.10/day; budget unit undocumented, inferred shared per mailto)'}; "
             f"{OA['lists']} lists + {OA['searches']} searches = about ${_oa_cost():.4f}; "
             f"{OA['per_second_429']} per-second 429s; breaker: {OA['breaker'] or 'not tripped'}"
             + ("; search soft cap reached" if OA.get("capped") else "")
             + (f", {OA['skipped']} calls skipped" if OA["skipped"] else "") + ".", "",
             *([cutoff_note, ""] if cutoff_note else []),
             f"Window: since {since.isoformat()}. Channels: {', '.join(sorted(chans)) or 'none'}. "
             f"Candidates: {len(cands)} raw, {already} already indexed, "
             f"**{source_count} new source leads**, **{event_count} indexed-repo events**.", "",
             ("**Status: DEGRADED** — " + "; ".join(degraded) + ". "
              "Read the diagnostics before trusting this ledger's coverage." if degraded else
              "**Status: NOT RUN** — fixture mode (`--channels none`); no channel was executed, so this ledger "
              "says nothing about coverage." if not chans else "**Status: all enumerated channels returned candidates.**"),
             "",
             "Known-positive regression (sources the method once missed; checked before the index dedupe): "
             + "; ".join(regress) + ".", "",
             *(["Proceedings volume denominators (publication-list counts, not recall; untitled links are "
                "tolerated up to " + f"{PROCEEDINGS_TITLE_SHORTFALL:.0%}" + " of a volume and their relevance is unknown): "
                + "; ".join(PROCEEDINGS_AUDIT) + ".", ""] if "venues" in chans and PROCEEDINGS_AUDIT else []),
             "Limits of this check: it matches titles only, so a work cut before metadata resolution "
             "(refs cap) or on a failed venue page cannot be named, only flagged as possibly truncated; "
             "a date-windowed channel cannot recover a source older than its window (out-of-window, not a miss). "
             "The CoALA mechanism-checklist control is a sweep-checklist test (§4.6 rows), not a channel test, "
             "and is not run here. Same-day ledgers must still be reconciled as a union with channel provenance "
             "before discovery is called closed.", "",
             "Triage source rows as INCLUDE (digest it), EXCLUDE (reason), or PENDING "
             "(what is missing). For indexed-repo events use UPDATE-DIGEST, "
             "NOTE-IN-REPOS or IGNORE with a reason. Mark every Decision cell "
             "on the batch branch; blank means the sweep is unfinished.", ""]
    for ch in ("refs", "repoevent", "blog", "github", "pypi", "arxiv", "venue", "cites"):
        rows = by.get(ch, [])
        if not rows:
            continue
        heading = {"repoevent": "Events in indexed repositories",
                   "refs": "Foundational gaps: works our digests cite that the index lacks"}.get(ch, ch)
        lines += [f"## {heading} ({len(rows)})", ""]
        if ch == "repoevent":
            lines.append("Existing evidence-family updates only; decide UPDATE-DIGEST, "
                         "NOTE-IN-REPOS or IGNORE. These rows never count as new sources.")
            lines.append("")
        groups = [("", rows)]
        if ch == "refs":
            # ChatGPT 13:06: the foundational-gap table holds only works cited by two or more digests,
            # as documented; single-digest mechanism-term leads are a separate, labelled table.
            multi = [c for c in rows if c.get("n", 0) >= 2]
            single = [c for c in rows if c.get("n", 0) < 2]
            lines.append("No date window and no compiler-keyword filter. Each row in the first table is cited "
                         f"by two or more digests ({len(multi)} rows); INCLUDE as background, or EXCLUDE with "
                         "the reason it is outside scope.")
            lines.append("")
            groups = [("", multi)]
            if single:
                groups.append(("Single-digest leads (cited by one digest; admitted only because the title names "
                               f"an agent or optimizer mechanism; weaker signal than a foundational gap) ({len(single)})",
                               single))
        for sub, grp in groups:
            if sub:
                lines += [f"### {sub}", ""]
            if not grp:
                continue
            lines += ["| Date | Candidate | Why it surfaced | Decision |", "|---|---|---|---|"]
            for c in sorted(grp, key=lambda r: (r["date"], r["title"], r["url"]), reverse=True):
                t = c["title"].replace("|", "/")
                lines.append(f"| {c['date']} | [{t}]({c['url']}) | {c['why']} | |")
            lines.append("")
    per = {}
    for c in cands:
        per[c["channel"]] = per.get(c["channel"], 0) + 1
    if args.recall_against:
        lines += recall_section(Path(args.recall_against).resolve(), cands, since)
    lines += ["## Channel diagnostics", "", f"Raw candidates per channel: {json.dumps(per)}", ""]
    lines += render_fetch_log("refs" in chans)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"wrote {out} ({len(new)} new candidates)")
    print(str(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
