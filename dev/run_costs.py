#!/usr/bin/env python3
"""What a /conundrum run cost: turns, tool calls, tokens and cost at API list prices, per agent.

Reads the Claude Code transcripts of one session: the main conversation and every agent it
started, subagents and workflow agents alike. From the project root, after a run:

    python3 dev/run_costs.py                              # this project's most recent session
    python3 dev/run_costs.py <session id, or its start>   # another session
    python3 dev/run_costs.py path/to/<session>.jsonl
    python3 dev/run_costs.py --since "2026-09-30 14:05"   # only work after the run started (local time)

What is exact and what is estimated:
- Turns, tool calls, uncached input, cache writes and cache reads are exact.
- Output tokens are exact for replies whose transcript recorded the final count, as the main
  conversation's does. Agent transcripts record each reply's usage as it began streaming, when
  its output was a few tokens. For those replies the output is estimated from the visible text
  and tool calls, plus the length of each thinking block's signature: the thinking text isn't
  stored, but its encrypted signature is, and it grows with the thinking. The coefficients were
  fitted on 338 Opus 5.5 replies with recorded counts (total within 1%, median error 8% per
  reply), and every report re-checks them on the replies that have recorded counts. They are
  uncalibrated for other models, and undercount Haiku, whose signatures are shorter.
- Not included: the model calls that WebSearch and WebFetch make on their own, and the main
  session's side calls (permission checks, summaries). The report counts the web calls.

A subscription's usage limits aren't dollars, but the list-price cost is a rough proxy for how
much of a usage window a run takes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# USD per million tokens: input, output, cache read. A cache write costs 1.25x input for the
# 5-minute cache and 2x for the 1-hour cache. The first key found in the model ID wins.
PRICES = {
    "opus-5-5": (4.0, 20.0, 0.20),
    "sonnet-5-5": (2.0, 10.0, 0.20),
    "fable-5-1": (10.0, 50.0, 0.25),
    "haiku-4-5": (1.0, 5.0, 0.10),
}
# Output estimate for replies without a recorded count (see the docstring).
TOKENS_PER_VISIBLE_CHAR = 0.42
TOKENS_PER_SIGNATURE_CHAR = 0.30
SIGNATURE_OVERHEAD = 850   # characters of each signature that don't grow with the thinking
WEB_TOOLS = ("WebSearch", "WebFetch")


@dataclass
class Reply:
    """One API request and its reply, merged from the transcript rows that share a message ID."""
    model: str
    start: datetime
    usage: dict
    final: bool = False          # the transcript recorded the finished reply's usage
    visible_chars: int = 0       # text, tool names and tool inputs
    signatures: list = field(default_factory=list)
    tools: list = field(default_factory=list)
    blocks: set = field(default_factory=set)

    @property
    def estimated_output(self) -> int:
        thinking = sum(max(0, s - SIGNATURE_OVERHEAD) for s in self.signatures)
        est = TOKENS_PER_VISIBLE_CHAR * self.visible_chars + TOKENS_PER_SIGNATURE_CHAR * thinking
        return max(self.usage.get("output_tokens", 0), round(est))

    @property
    def output(self) -> int:
        return self.usage.get("output_tokens", 0) if self.final else self.estimated_output

    @property
    def cache_write(self) -> int:
        return self.usage.get("cache_creation_input_tokens", 0)

    @property
    def cache_read(self) -> int:
        return self.usage.get("cache_read_input_tokens", 0)

    @property
    def cost(self) -> float | None:
        price = next((p for key, p in PRICES.items() if key in self.model), None)
        if price is None:
            return None
        inp, out, read = price
        split = self.usage.get("cache_creation") or {}
        hour = split.get("ephemeral_1h_input_tokens", 0)
        write = 2.0 * inp * hour + 1.25 * inp * (self.cache_write - hour)
        return (inp * self.usage.get("input_tokens", 0) + write + read * self.cache_read + out * self.output) / 1e6


@dataclass
class Agent:
    name: str                    # "main conversation", or the agent's type
    description: str = ""
    replies: list = field(default_factory=list)

    def total(self, attr: str) -> int:
        return sum(getattr(r, attr) for r in self.replies)

    @property
    def uncached(self) -> int:
        return sum(r.usage.get("input_tokens", 0) for r in self.replies)

    @property
    def tool_calls(self) -> int:
        return sum(len(r.tools) for r in self.replies)

    @property
    def estimated(self) -> bool:
        return any(not r.final for r in self.replies)

    @property
    def cost(self) -> float | None:
        costs = [r.cost for r in self.replies]
        return None if None in costs else sum(costs)

    @property
    def models(self) -> str:
        return ", ".join(sorted({short_model(r.model) for r in self.replies}))

    @property
    def minutes(self) -> float:
        if not self.replies:
            return 0.0
        return (self.replies[-1].start - self.replies[0].start).total_seconds() / 60


def short_model(model: str) -> str:
    return re.sub(r"^claude-|-\d{8}$", "", model)


def parse_time(text: str) -> datetime:
    """An ISO time; one without a zone is local time."""
    t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    return t if t.tzinfo else t.astimezone()


# ---------------------------------------------------------------- reading transcripts
def rows(path: Path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:   # a line cut off mid-write
                continue


def add_block(reply: Reply, block: dict) -> None:
    kind = block.get("type")
    key = (kind, block.get("id") or block.get("signature") or block.get("data") or block.get("text"))
    if key in reply.blocks:          # rows can repeat a block
        return
    reply.blocks.add(key)
    if kind == "text":
        reply.visible_chars += len(block.get("text", ""))
    elif kind == "tool_use":
        reply.tools.append(block.get("name", ""))
        reply.visible_chars += len(block.get("name", "")) + len(json.dumps(block.get("input", {})))
    elif kind == "thinking":
        if block.get("signature"):
            reply.signatures.append(len(block["signature"]))
        else:
            reply.visible_chars += len(block.get("thinking", ""))
    elif kind == "redacted_thinking":
        reply.signatures.append(len(block.get("data", "")))


def replies(records, since: datetime | None = None) -> list[Reply]:
    """Merge a transcript's assistant rows into one Reply per API request."""
    merged: dict[str, Reply] = {}
    for r in records:
        m = r.get("message") or {}
        if r.get("type") != "assistant" or not m.get("usage") or m.get("model") in (None, "<synthetic>"):
            continue
        key = m.get("id") or r.get("requestId") or r.get("uuid")
        reply = merged.get(key)
        if reply is None:
            reply = merged[key] = Reply(model=m["model"], start=parse_time(r["timestamp"]), usage=dict(m["usage"]))
        elif m["usage"].get("output_tokens", 0) > reply.usage.get("output_tokens", 0):
            reply.usage = dict(m["usage"])
        reply.final = reply.final or bool(m.get("stop_reason"))
        for block in m.get("content") or []:
            if isinstance(block, dict):
                add_block(reply, block)
    out = sorted(merged.values(), key=lambda x: x.start)
    return [x for x in out if since is None or x.start >= since]


def load_session(path: Path, since: datetime | None = None) -> list[Agent]:
    """The main conversation, then each agent in the order it started."""
    main_rows, side = [], {}
    for r in rows(path):
        if r.get("isSidechain"):     # older versions kept agents in the main file
            side.setdefault(r.get("agentId") or "sidechain", []).append(r)
        else:
            main_rows.append(r)
    agents = [Agent("main conversation", replies=replies(main_rows, since))]
    files = {p.stem.removeprefix("agent-"): p for p in sorted(path.with_suffix("").glob("**/agent-*.jsonl"))}
    for agent_id, records in side.items():
        if agent_id not in files:
            agents.append(Agent("agent", agent_id, replies(records, since)))
    for agent_id, p in files.items():
        meta = {}
        try:
            meta = json.loads(p.with_suffix(".meta.json").read_text())
        except (OSError, json.JSONDecodeError):
            pass
        agents.append(Agent(meta.get("agentType") or "agent", meta.get("description") or meta.get("label") or agent_id,
                            replies(rows(p), since)))
    first = [agents[0]] + sorted((a for a in agents[1:] if a.replies), key=lambda a: a.replies[0].start)
    return [a for a in first if a.replies]


# ---------------------------------------------------------------- finding the session
def projects_root() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude").expanduser() / "projects"


def project_sessions(project: Path) -> list[Path]:
    """This project's session transcripts, newest first."""
    folder = projects_root() / re.sub(r"[^A-Za-z0-9]", "-", str(project))
    found = list(folder.glob("*.jsonl")) if folder.is_dir() else []
    if not found:   # the folder naming differs: look for sessions whose rows name this project
        for p in projects_root().glob("*/*.jsonl"):
            for i, r in enumerate(rows(p)):
                if r.get("cwd"):
                    if Path(r["cwd"]) == project:
                        found.append(p)
                    break
                if i > 50:
                    break
    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


def find_session(arg: str | None, project: Path) -> Path:
    if arg and Path(arg).is_file():
        return Path(arg)
    sessions = project_sessions(project)
    if arg:
        sessions = [p for p in sessions if p.stem.startswith(arg)] or \
                   [p for p in projects_root().glob(f"*/{arg}*.jsonl")]
    if not sessions:
        raise FileNotFoundError(f"no session transcript {'starting ' + arg if arg else 'for ' + str(project)} "
                                f"under {projects_root()}")
    return sessions[0]


# ---------------------------------------------------------------- the report
def tokens(n: int) -> str:
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e4 else f"{n / 1e3:.1f}k"


def dollars(cost: float | None, estimated: bool) -> str:
    return "?" if cost is None else f"{'~' if estimated else ''}${cost:,.2f}"


def table(header: list, lines: list) -> str:
    widths = [max(len(str(x)) for x in col) for col in zip(header, *lines)]
    fmt = lambda row: "  ".join(str(x).ljust(w) if i == 0 else str(x).rjust(w)  # noqa: E731
                                for i, (x, w) in enumerate(zip(row, widths)))
    return "\n".join([fmt(header), fmt(["-" * w for w in widths])] + [fmt(r) for r in lines])


def row_for(label: str, group: list) -> list:
    rs = [r for a in group for r in a.replies]
    est = any(not r.final for r in rs)
    costs = [r.cost for r in rs]
    return [label, len(rs), sum(len(r.tools) for r in rs),
            tokens(sum(r.usage.get("input_tokens", 0) + r.cache_write for r in rs)),
            tokens(sum(r.cache_read for r in rs)),
            ("~" if est else "") + tokens(sum(r.output for r in rs)),
            dollars(None if None in costs else sum(costs), est)]


def calibration(agents: list) -> list[str]:
    """How the output estimate compares with the recorded counts, per model."""
    lines, by_model = [], {}
    for r in (r for a in agents for r in a.replies if r.final and r.usage.get("output_tokens")):
        est = TOKENS_PER_VISIBLE_CHAR * r.visible_chars + TOKENS_PER_SIGNATURE_CHAR * sum(
            max(0, s - SIGNATURE_OVERHEAD) for s in r.signatures)
        pair = by_model.setdefault(short_model(r.model), [0, 0.0, 0])
        pair[0] += r.usage["output_tokens"]
        pair[1] += est
        pair[2] += 1
    for model, (recorded, est, n) in sorted(by_model.items()):
        lines.append(f"Output estimate check, {model}: {est / recorded:.2f}x the recorded total over {n} replies.")
    return lines


def report(path: Path, agents: list) -> str:
    rs = [r for a in agents for r in a.replies]
    if not rs:
        return f"{path.stem}: no model replies in range."
    start, end = min(r.start for r in rs), max(r.start for r in rs)
    out = [f"Session {path.stem[:8]}: {len(agents) - 1} agents, {start:%Y-%m-%d %H:%M} to {end:%H:%M} UTC", ""]
    header = ["Agent", "Model", "Turns", "Tools", "Input+write", "Cache read", "Output", "Cost", "Time"]
    lines = []
    for a in agents:
        label = a.name if not a.description else f"{a.name}: {a.description}"
        r = row_for(label[:48], [a])
        lines.append(r[:1] + [a.models] + r[1:] + [f"{a.minutes:.0f}m"])
    out.append(table(header, lines))
    kinds = {}
    for a in agents[1:]:
        kinds.setdefault(a.name, []).append(a)
    if len(kinds) > 1:
        out += ["", table(["Agent type", "Turns", "Tools", "Input+write", "Cache read", "Output", "Cost"],
                          [row_for(f"{k} (x{len(v)})", v) for k, v in sorted(kinds.items())])]
    everyone = row_for("", agents)
    agents_only = row_for("", agents[1:]) if len(agents) > 1 else None
    out += ["", f"Total: {everyone[-1]} over {everyone[1]} turns and {everyone[2]} tool calls"
                + (f"; the agents alone {agents_only[-1]}" if agents_only else "") + "."]
    if any(not r.final for r in rs):
        out.append("~ marks estimated output (see the docstring); input and cache figures are exact.")
    unpriced = sorted({r.model for r in rs if r.cost is None})
    if unpriced:
        out.append(f"No price for {', '.join(unpriced)}: add it to PRICES.")
    out += calibration(agents)
    web = {t: sum(r.tools.count(t) for r in rs) for t in WEB_TOOLS}
    if any(web.values()):
        out.append(f"Not priced: the model calls behind {web['WebSearch']} WebSearch and "
                   f"{web['WebFetch']} WebFetch calls.")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("session", nargs="?", help="session ID (or its start) or transcript path; default: the latest")
    ap.add_argument("--since", type=parse_time, help="count only replies from this time on (ISO; local time if no zone)")
    ap.add_argument("--project", type=Path, default=Path.cwd(), help="project directory (default: the current one)")
    args = ap.parse_args(argv)
    try:
        path = find_session(args.session, args.project.resolve())
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 1
    print(report(path, load_session(path, args.since)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
