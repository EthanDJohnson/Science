#!/usr/bin/env python3
"""Preflight for /conundrum: Python packages and which research sources are reachable.

Run from the project root:  python3 .claude/skills/conundrum/scripts/check_env.py
Prints one line per check and a summary the skill relays to the user. Always exits 0.
"""
from __future__ import annotations

import importlib
import json
import os
import sys
import urllib.error
import urllib.request

PACKAGES = [("sympy", True), ("mpmath", True), ("numpy", True), ("scipy", True), ("pypdf", False)]
HINTS = {"pypdf": "lets fetch_text.py quote PDFs verbatim: pip install pypdf cffi"}
SOURCES = [
    ("arXiv API", "https://export.arxiv.org/api/query?search_query=all:test&max_results=1"),
    ("INSPIRE-HEP API", "https://inspirehep.net/api/literature?q=t%20test&size=1&fields=titles.title"),
    ("arxiv.org pages", "https://arxiv.org/abs/gr-qc/0009013"),
    ("doi.org", "https://doi.org/10.1088/0264-9381/11/5/001"),
    ("Crossref API", "https://api.crossref.org/works?rows=1&query=test"),
    ("Semantic Scholar API", "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1&fields=title"),
]


def check_packages():
    out = []
    for name, required in PACKAGES:
        try:
            mod = importlib.import_module(name)
            out.append({"package": name, "ok": True, "version": getattr(mod, "__version__", "?"),
                        "required": required})
        except ImportError:
            out.append({"package": name, "ok": False, "version": None, "required": required})
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # e.g. pypdf over a broken cryptography package: a pyo3 PanicException
            out.append({"package": name, "ok": False, "version": None, "required": required,
                        "broken": f"installed but fails to import ({type(exc).__name__}); pip install cffi"})
    return out


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Test the named host only. doi.org redirects to publishers, some of which bounce
    automated clients to bot-check domains; that is the publisher, not the network."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def check_sources(timeout=8.0):
    opener = urllib.request.build_opener(_NoRedirect)
    out = []
    for name, url in SOURCES:
        req = urllib.request.Request(url, headers={"User-Agent": "conundrum-skill/1.0 preflight"})
        try:
            with opener.open(req, timeout=timeout) as resp:
                out.append({"source": name, "ok": True, "detail": f"HTTP {resp.status}"})
        except urllib.error.HTTPError as exc:
            # Any HTTP answer (redirect, 404, 429 rate limit) means the host is reachable.
            # The proxy's own refusals arrive as URLError ("Tunnel connection failed").
            detail = f"HTTP {exc.code}" + (" (rate-limited right now)" if exc.code == 429 else "")
            out.append({"source": name, "ok": True, "detail": detail})
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            out.append({"source": name, "ok": False, "detail": str(getattr(exc, "reason", exc))[:80]})
    return out


def workflow_concurrency() -> tuple[int, int]:
    """CPUs available to this process, and the agents a workflow runs at once: min(16, CPUs - 2)."""
    cpus = len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else (os.cpu_count() or 1)
    return cpus, max(1, min(16, cpus - 2))


def main() -> int:
    packages, sources = check_packages(), check_sources()
    cpus, parallel = workflow_concurrency()
    if "--json" in sys.argv:
        print(json.dumps({"python": sys.version.split()[0], "cpus": cpus, "workflow_parallel_agents": parallel,
                          "packages": packages, "sources": sources}, indent=2))
        return 0
    print(f"python {sys.version.split()[0]}")
    print(f"cpus    {cpus} (workflows run up to {parallel} agent{'s' if parallel != 1 else ''} at once)")
    for p in packages:
        tag = "ok" if p["ok"] else ("MISSING (required)" if p["required"] else "missing (optional)")
        if p.get("broken"):
            tag = f"BROKEN: {p['broken']}"
        elif not p["ok"] and p["package"] in HINTS:
            tag += f": {HINTS[p['package']]}"
        print(f"package {p['package']:<6} {tag}{' ' + p['version'] if p['version'] else ''}")
    for s in sources:
        print(f"source  {s['source']:<20} {'reachable' if s['ok'] else 'BLOCKED'} ({s['detail']})")
    missing = [p["package"] for p in packages if p["required"] and not p["ok"]]
    blocked = [s["source"] for s in sources if not s["ok"]]
    print()
    if missing:
        print(f"ACTION: install required packages: pip install {' '.join(missing)}")
    if len(blocked) == len(sources):
        print("NOTE: no literature source is reachable. Research will rely on search summaries; "
              "such claims are marked ACCESS: search-summary and weighted down.")
    elif blocked:
        print(f"NOTE: blocked: {', '.join(blocked)}. Researchers will use the reachable sources and WebSearch.")
    if parallel < 5:
        print(f"NOTE: only {parallel} agents run at once here. The time estimates in SKILL.md were measured at "
              "2 at once; a machine with more CPUs runs faster.")
    if not missing and not blocked:
        print("READY: all packages present and all sources reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
