#!/usr/bin/env python3
"""Run one /conundrum calculation or check script with a time limit, and save everything it printed.

Every pipeline calculation runs through this: the math checker's checks, and the lenses', refuters'
and crux advocates' scripts in runs/<slug>/calc/. The judge and the auditor can't run code, so the
log is how they check a cited number against what the script printed. The log goes beside the
script, as <script>.log. It holds the command, start time, duration,
exit code, the Python and library versions, a count of the PASS, FAIL and UNDECIDED lines, and
the script's full output and errors.

    python3 .claude/skills/conundrum/scripts/math_run.py runs/<slug>/math/<lens>/M-CONSTRAINTS-03.py
    python3 .claude/skills/conundrum/scripts/math_run.py <script> --timeout 300

- Only scripts under runs/ are run.
- A script whose code would write into the pipeline's own files is refused, by the same check
  the pipeline guard applies to scripts run directly.
- The default time limit is 110 s, just under the Bash tool's default of 2 minutes. For a longer
  limit, raise the Bash tool's timeout parameter to match. The most allowed is 590 s.
- It prints a one-line summary and the last 150 lines of output (the log keeps all of it), and
  exits with the script's exit code: 124 on a timeout, 2 when it refuses.
"""
from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

GUARD = Path(__file__).resolve().parents[3] / "hooks" / "guard_pipeline.py"
DEFAULT_TIMEOUT = 110
MAX_TIMEOUT = 590
TAIL = 150


def versions() -> str:
    found = [f"python {platform.python_version()}"]
    for name in ("sympy", "mpmath", "numpy", "scipy"):
        try:
            found.append(f"{name} {importlib.metadata.version(name)}")
        except importlib.metadata.PackageNotFoundError:
            pass
    return ", ".join(found)


def refusal(script: Path, root: Path) -> str | None:
    """Why this script may not run, or None."""
    runs = (root / "runs").resolve()
    real = script.resolve()
    if runs not in real.parents:
        return f"{script} is not under runs/"
    if real.suffix != ".py" or not real.is_file():
        return f"{script} is not a Python file"
    if GUARD.is_file():
        spec = importlib.util.spec_from_file_location("guard_pipeline", GUARD)
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        try:
            guard.check_code(real.read_text(errors="replace"), f"script {script}")
        except guard.Denied as why:
            return str(why)
    return None


def run(script: Path, timeout: float) -> tuple[int, str, str, float, bool]:
    start = time.monotonic()
    try:
        done = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=timeout)
        return done.returncode, done.stdout, done.stderr, time.monotonic() - start, False
    except subprocess.TimeoutExpired as late:
        text = lambda b: b.decode(errors="replace") if isinstance(b, bytes) else (b or "")   # noqa: E731
        return 124, text(late.stdout), text(late.stderr), time.monotonic() - start, True


def counts(stdout: str) -> dict:
    tally = {"PASS": 0, "FAIL": 0, "UNDECIDED": 0}
    for line in stdout.splitlines():
        word = line.split(" ", 1)[0]
        if word in tally:
            tally[word] += 1
    return tally


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("script", type=Path)
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"seconds (default {DEFAULT_TIMEOUT}, most {MAX_TIMEOUT})")
    args = ap.parse_args(argv)
    why = refusal(args.script, Path.cwd())
    if why:
        print(f"refused: {why}", file=sys.stderr)
        return 2
    limit = min(max(args.timeout, 1), MAX_TIMEOUT)
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    code, out, err, took, late = run(args.script, limit)
    tally = counts(out)
    summary = ", ".join(f"{n} {k}" for k, n in tally.items()) if any(tally.values()) else "no PASS/FAIL lines"
    status = f"124 (timed out after {limit:g} s)" if late else str(code)
    log = args.script.with_name(args.script.name + ".log")
    log.write_text(
        f"# math_run log\n"
        f"command:  python3 {args.script}\n"
        f"started:  {started}\n"
        f"duration: {took:.1f} s\n"
        f"exit:     {status}\n"
        f"versions: {versions()}\n"
        f"counts:   {summary}\n\n"
        f"--- stdout ---\n{out}\n--- stderr ---\n{err}\n")
    print(f"exit {status} in {took:.1f} s: {summary}. Log: {log}")
    lines = out.rstrip("\n").splitlines()
    if lines:
        head = f"... ({len(lines) - TAIL} earlier lines are in the log)\n" if len(lines) > TAIL else ""
        print(head + "\n".join(lines[-TAIL:]))
    if err.strip():
        print("--- stderr (end) ---\n" + "\n".join(err.rstrip("\n").splitlines()[-20:]))
    return code


if __name__ == "__main__":
    sys.exit(main())
