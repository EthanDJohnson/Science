#!/usr/bin/env python3
"""Preflight for /conundrum: Python packages and which research sources are reachable.

Run from the project root:  python3 .claude/skills/conundrum/scripts/check_env.py [--install]
Prints one line per check and a summary the skill relays to the user. Always exits 0.

--install has pip install the packages in PACKAGES that are missing or fail to import, and nothing
else, into the Python running this script: the one the pipeline's scripts run on. When every package
works it installs nothing. The skill's preflight passes it without asking the user first.
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

PACKAGES = [("sympy", True), ("mpmath", True), ("numpy", True), ("scipy", True), ("pypdf", False)]
# What --install asks pip for when a package is missing or broken. cffi fixes pypdf's usual
# import crash, which comes from a broken system cryptography package.
PIP_NAMES = {"pypdf": ["pypdf", "cffi"]}
HINTS = {"pypdf": "lets fetch_text.py and find_fulltext.py quote PDFs verbatim: pip install pypdf cffi"}
PIP_TIMEOUT = 420   # seconds. SKILL.md gives the Bash call 600, which must also cover the recheck and the sources
PIP_FAILURES = [    # (pattern in pip's output, what to tell the user), first match wins
    (r"externally-managed-environment",
     "this Python is managed by the operating system (PEP 668), so pip won't install into it. Make a virtual "
     "environment (python3 -m venv .venv), activate it and start Claude Code from that shell, or install "
     "the system's packages (for example apt install python3-scipy)"),
    (r"No module named pip", "pip isn't installed for this Python (on Debian or Ubuntu: apt install python3-pip)"),
    (r"CERTIFICATE_VERIFY_FAILED", "pip couldn't verify PyPI's certificate; a proxy may need its CA bundle "
                                   "named in PIP_CERT"),
    (r"\(from versions: none\)|ProxyError|NewConnectionError|Max retries exceeded|Tunnel connection failed|"
     r"Temporary failure in name resolution|Network is unreachable",
     "PyPI isn't reachable from here. In a cloud session, the environment's Network access setting must "
     "allow pypi.org and files.pythonhosted.org"),
    (r"Permission denied", "pip can't write where this Python keeps its packages; use a virtual environment "
                           "you own"),
]
SOURCES = [
    ("arXiv API", "https://export.arxiv.org/api/query?search_query=all:test&max_results=1"),
    ("INSPIRE-HEP API", "https://inspirehep.net/api/literature?q=t%20test&size=1&fields=titles.title"),
    ("arxiv.org pages", "https://arxiv.org/abs/gr-qc/0009013"),
    ("doi.org", "https://doi.org/10.1088/0264-9381/11/5/001"),
    ("Crossref API", "https://api.crossref.org/works?rows=1&query=test"),
    ("Semantic Scholar API", "https://api.semanticscholar.org/graph/v1/paper/search?query=test&limit=1&fields=title"),
    # Free full-text finders for find_fulltext.py
    ("OpenAlex API", "https://api.openalex.org/works?per-page=1&search=test"),
    ("OSTI API", "https://www.osti.gov/api/v1/records?rows=1&q=test"),
    ("Europe PMC API", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=test&format=json&pageSize=1"),
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


def pip_names(packages) -> list:
    """What pip must install for the packages that are missing or broken, in PACKAGES order."""
    names = []
    for p in packages:
        if not p["ok"]:
            names += [n for n in PIP_NAMES.get(p["package"], [p["package"]]) if n not in names]
    return names


def pip_failure(output: str) -> str:
    for pattern, reason in PIP_FAILURES:
        if re.search(pattern, output):
            return reason
    return "pip failed; its last lines follow"


def pip_install(names, timeout=PIP_TIMEOUT) -> dict:
    """Install names with this Python's own pip. Never raises; on failure says why, with pip's last lines."""
    result = {"packages": list(names), "command": "python3 -m pip install " + " ".join(names)}
    cmd = [sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "--no-input", "--quiet", *names]
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return {**result, "ok": False, "seconds": timeout, "reason": f"pip didn't finish within {timeout} s",
                "tail": []}
    except OSError as exc:
        return {**result, "ok": False, "seconds": 0, "reason": f"pip couldn't start ({exc})", "tail": []}
    result.update(ok=proc.returncode == 0, seconds=round(time.monotonic() - start))
    if not result["ok"]:
        output = f"{proc.stdout or ''}\n{proc.stderr or ''}"
        result["reason"] = pip_failure(output)
        result["tail"] = [line.rstrip() for line in output.splitlines() if line.strip()][-8:]
    return result


def recheck_packages() -> list:
    """Check the packages again in a new Python process. Only a new process sees a site-packages
    folder the install created, as pip's first install into a user's own folder does."""
    try:
        proc = subprocess.run([sys.executable, os.path.abspath(__file__), "--packages-only", "--json"],
                              capture_output=True, text=True, errors="replace", timeout=60)
        return json.loads(proc.stdout)["packages"]
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError):
        importlib.invalidate_caches()
        return check_packages()


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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Preflight for /conundrum. Always exits 0.")
    ap.add_argument("--install", action="store_true",
                    help="pip-install the packages that are missing or broken (only those in its fixed list)")
    ap.add_argument("--packages-only", action="store_true", help="check the Python packages only, not the network")
    ap.add_argument("--json", action="store_true", help="print the results as JSON")
    args = ap.parse_args(argv)

    packages, install = check_packages(), None
    if args.install and pip_names(packages):
        install = pip_install(pip_names(packages))
        packages = recheck_packages()
    sources = [] if args.packages_only else check_sources()
    cpus, parallel = workflow_concurrency()
    if args.json:
        print(json.dumps({"python": sys.version.split()[0], "cpus": cpus, "workflow_parallel_agents": parallel,
                          "packages": packages, "install": install, "sources": sources}, indent=2))
        return 0
    print(f"python {sys.version.split()[0]}")
    print(f"cpus    {cpus} (workflows run up to {parallel} agent{'s' if parallel != 1 else ''} at once)")
    if install:
        outcome = "done" if install["ok"] else "FAILED"
        print(f"install {' '.join(install['packages'])} with pip: {outcome} in {install['seconds']} s")
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
    if install and install["ok"]:
        print(f"INSTALLED: {' '.join(install['packages'])} (pip, {install['seconds']} s).")
    elif install:
        print(f"{'ACTION' if missing else 'NOTE'}: pip could not install {' '.join(install['packages'])}: "
              f"{install['reason']}. (The command was: {install['command']})")
        for line in install["tail"]:
            print(f"  pip| {line}")
    if missing and not install:
        print(f"ACTION: required packages missing: {' '.join(missing)}. Install them with --install, "
              f"which runs python3 -m pip install {' '.join(pip_names(packages))}")
    elif missing and install["ok"]:
        print(f"ACTION: pip finished, but {' '.join(missing)} still fail to import; see the package lines above.")
    if sources and len(blocked) == len(sources):
        print("NOTE: no literature source is reachable. Research will rely on search summaries; "
              "such claims are marked ACCESS: search-summary and weighted down.")
    elif blocked:
        print(f"NOTE: blocked: {', '.join(blocked)}. Researchers will use the reachable sources and WebSearch.")
    if parallel < 5 and not args.packages_only:
        print(f"NOTE: only {parallel} agents run at once here. The time estimates in SKILL.md were measured at "
              "2 at once; a machine with more CPUs runs faster.")
    if not missing and not blocked:
        print("READY: the required packages work" + ("." if args.packages_only else " and every source is reachable."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
