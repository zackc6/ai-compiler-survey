#!/usr/bin/env python3
"""Offline regression fixtures for the blogs channel of scripts/discover.py.

Run: python3 scripts/test_discover_feeds.py   (no network; exits non-zero on failure)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import discover as d  # noqa: E402

ATOM = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Faster tensor compiler with equality saturation</title>
    <link rel="self" href="https://api.example.org/posts/1"/>
    <link rel="alternate" href="https://example.org/posts/1.html"/>
    <updated>2026-11-01T00:00:00Z</updated>
  </entry>
  <entry>
    <title>Default rel</title>
    <link rel="replies" href="https://example.org/posts/2/comments"/>
    <link href="https://example.org/posts/2.html"/>
  </entry>
  <entry>
    <title>Only self</title>
    <link rel="self" href="https://api.example.org/posts/3"/>
  </entry>
</feed>"""

REL_ATOM = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom"><entry>
  <title>Rethinking abstractions</title>
  <link href="/2026/11/03/rethinking-abstractions-in-the-agentic-era" rel="alternate" type="text/html"/>
  <published>2026-11-03T00:00:00+00:00</published>
</entry></feed>"""

REL_RSS = b"""<?xml version="1.0"?><rss><channel><item>
<title>Relative RSS</title><link>posts/b.html</link></item></channel></rss>"""

RSS = b"""<?xml version="1.0"?><rss><channel><item>
<title>Autotuning GEMMs</title><link>https://example.org/a</link>
<pubDate>Mon, 02 Nov 2026 10:00:00 +0000</pubDate></item></channel></rss>"""


def main() -> int:
    fails = []
    items = d.parse_feed(ATOM)
    want = ["https://example.org/posts/1.html", "https://example.org/posts/2.html", "https://api.example.org/posts/3"]
    got = [i["url"] for i in items]
    if got != want:
        fails.append(f"atom link selection: {got} != {want}")
    if any("_alt" in i for i in items):
        fails.append("internal _alt key leaked into items")
    rss = d.parse_feed(RSS)
    if not rss or rss[0]["url"] != "https://example.org/a" or rss[0]["date"] != "2026-11-02":
        fails.append(f"rss parse: {rss}")
    # Relative feed links resolve against the feed URL (ChatGPT 08:14: TVM feed emits "/2026/...").
    rel = d.parse_feed(REL_ATOM, base="https://tvm.apache.org/feed.xml")
    if not rel or rel[0]["url"] != "https://tvm.apache.org/2026/11/03/rethinking-abstractions-in-the-agentic-era":
        fails.append(f"relative atom link not resolved: {rel}")
    rel = d.parse_feed(REL_RSS, base="https://example.org/blog/feed.xml")
    if not rel or rel[0]["url"] != "https://example.org/blog/posts/b.html":
        fails.append(f"relative rss link not resolved: {rel}")
    if d.parse_feed(ATOM, base="https://other.example/feed.xml")[0]["url"] != "https://example.org/posts/1.html":
        fails.append("absolute link altered by base resolution")
    cases = [  # (text, scope, admitted?)
        ("Faster tensor compiler with equality saturation", "theme", True),   # non-agent alternative
        ("Autotuning GEMMs with a learned cost model", "theme", True),
        ("CUDA 13.2 release notes", "theme", False),                          # broad term, no agent term
        ("An LLM agent that writes CUDA kernels", "theme", True),
        ("Linux kernel 6.20 scheduler", "theme", False),
        ("Linux kernel 6.20 scheduler", "core", True),                        # core feeds keep any CORE term
        ("Our new office opens", "core", False),
        ("Optimizing CUDA matrix multiplication", "theme", True),             # non-agent, broad term + context
        ("Fast tile scheduling on GPUs", "theme", True),
        ("Faster PTX code generation", "theme", True),
        ("Linux kernel GPU driver update", "theme", False),
    ]
    for text, scope, ok in cases:
        if bool(d._theme_hit(text, scope)) != ok:
            fails.append(f"_theme_hit({text!r}, {scope}) expected {ok}")
    # Recall-limit diagnostics must survive into the rendered fetch log.
    for msg in ("hn truncated: MLIR: stopped after 3 pages (300 stories)",
                "ghsearch truncated: tile language: 300 of 412 repositories retrieved",
                "ghsearch threshold: autotuning: 17 repositories below the star threshold dropped",
                "hn unparsable: TVM (page 2)"):
        if not any(k in msg for k in d.DIAG_KEEP):
            fails.append(f"diagnostic filtered out of ledger: {msg!r}")
    for f in fails:
        print("FAIL", f)
    print("OK" if not fails else f"{len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
