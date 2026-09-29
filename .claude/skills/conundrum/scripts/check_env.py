#!/usr/bin/env python3
"""Preflight for /conundrum: Python packages and which research sources are reachable.

Run from the project root:  python3 .claude/skills/conundrum/scripts/check_env.py
Prints one line per check and a summary the skill relays to the user. Always exits 0.
"""
from __future__ import annotations

import importlib
import json
import sys
import urllib.error
import urllib.request

PACKAGES = [("sympy", True), ("numpy", True), ("scipy", False)]
SOURCES = [
    ("arXiv API", "https://export.arxiv.org/api/query?search_query=all:test&max_results=1"),
    ("INSPIRE-HEP API", "https://inspirehep.net/api/literature?q=t%20test&size=1&fields=titles.title"),
    ("arxiv.org pages", "https://arxiv.org/abs/gr-qc/0009013"),
    ("doi.org", "https://doi.org/10.1088/0264-9381/11/5/001"),
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
    return out


def check_sources(timeout=8.0):
    out = []
    for name, url in SOURCES:
        req = urllib.request.Request(url, headers={"User-Agent": "conundrum-skill/1.0 preflight"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                out.append({"source": name, "ok": 200 <= resp.status < 400, "detail": f"HTTP {resp.status}"})
        except urllib.error.HTTPError as exc:
            # A 4xx from the site itself still proves the host is reachable.
            out.append({"source": name, "ok": exc.code < 500 and exc.code not in (403, 407),
                        "detail": f"HTTP {exc.code}"})
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            out.append({"source": name, "ok": False, "detail": str(getattr(exc, "reason", exc))[:80]})
    return out


def main() -> int:
    packages, sources = check_packages(), check_sources()
    if "--json" in sys.argv:
        print(json.dumps({"python": sys.version.split()[0], "packages": packages, "sources": sources}, indent=2))
        return 0
    print(f"python {sys.version.split()[0]}")
    for p in packages:
        tag = "ok" if p["ok"] else ("MISSING (required)" if p["required"] else "missing (optional)")
        print(f"package {p['package']:<6} {tag}{' ' + p['version'] if p['version'] else ''}")
    for s in sources:
        print(f"source  {s['source']:<16} {'reachable' if s['ok'] else 'BLOCKED'} ({s['detail']})")
    missing = [p["package"] for p in packages if p["required"] and not p["ok"]]
    blocked = [s["source"] for s in sources if not s["ok"]]
    print()
    if missing:
        print(f"ACTION: install required packages: pip install {' '.join(missing)}")
    if len(blocked) == len(sources):
        print("NOTE: no literature source is reachable. Research will rely on WebSearch snippets; "
              "every claim will be marked ACCESS=snippet and weighted down.")
    elif blocked:
        print(f"NOTE: blocked: {', '.join(blocked)}. Researchers will use the reachable sources and WebSearch.")
    if not missing and not blocked:
        print("READY: all packages present and all sources reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
