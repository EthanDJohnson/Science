#!/usr/bin/env python3
"""Turn and tool-call counter for /conundrum agents (a Claude Code hook).

Agents can't count their own turns reliably. Asking each one to keep a counter file would cost
tokens every turn and still depend on the agent remembering. This hook counts for them, outside
the model.

Events (configured in .claude/settings.json):
  PostToolBatch  fires once per model turn, after all of that turn's tool calls resolve. The hook
                 adds one turn and len(tool_calls) calls to the agent's tally, and injects a short
                 reminder into that agent's context when a threshold is crossed:
                   - every 10 tool calls: the count, plus a nudge to append settled findings;
                   - at the first-draft call, for agents that write one document;
                   - at the top of the call budget;
                   - on each of the last 5 turns before the maxTurns cutoff.
  SubagentStop   deletes the agent's tally.

Only agents whose definition .claude/agents/<agent_type>.md has a budget line ("aim for about
N–M tool calls") are counted. The main conversation and every other agent are left alone.
Reminders start with "[turn budget]" and cost roughly 30-60 tokens each; nothing is printed
otherwise. The hook never blocks anything and always exits 0.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from pathlib import Path

TAG = "[turn budget]"
LAST_TURNS = 5


def project_dir(event: dict) -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".")


def load_budget(event: dict) -> dict | None:
    agent_type = event.get("agent_type") or ""
    if not re.fullmatch(r"[\w.-]+", agent_type):
        return None   # absent, or a plugin-scoped name: not one of ours
    try:
        text = (project_dir(event) / ".claude" / "agents" / f"{agent_type}.md").read_text()
    except OSError:
        return None
    budget = re.search(r"aim for about (\d+)–(\d+) tool calls", text)
    if not budget:
        return None
    cap = re.search(r"^maxTurns:\s*(\d+)\s*$", text, re.M)
    draft = re.search(r"first draft of .*? by about call (\d+)", text)
    return {
        "lo": int(budget.group(1)),
        "hi": int(budget.group(2)),
        "cap": int(cap.group(1)) if cap else None,
        "draft_by": int(draft.group(1)) if draft else None,
        "appends": "**Checkpoints:**" in text,
    }


def state_path(event: dict) -> Path:
    base = event.get("scratchpad_dir") or tempfile.gettempdir()
    safe = re.sub(r"[^\w.-]", "_", str(event["agent_id"]))
    return Path(base) / "conundrum-turn-budget" / f"{safe}.json"


def message(b: dict, before: dict, after: dict) -> str | None:
    calls0, calls1, turns = before["calls"], after["calls"], after["turns"]
    new_ten = calls1 // 10 > calls0 // 10
    notes = []
    if b["appends"] and new_ten:
        notes.append("Append anything you have settled that isn't in your file yet, in your next step.")
    if b["draft_by"] is not None and calls0 < b["draft_by"] <= calls1:
        notes.append("Write the complete first draft of your file now if you haven't.")
    if calls0 < b["hi"] <= calls1:
        notes.append("That is the top of your budget: finish your file and return, unless another step "
                     "would change your answer.")
    if b["cap"] is not None and turns >= b["cap"] - LAST_TURNS:
        left = max(0, b["cap"] - turns)
        notes.append(f"About {left} turn{'' if left == 1 else 's'} remain{'s' if left == 1 else ''} before you "
                     "are cut off: make sure your file is complete now, then return.")
    if not notes and not new_ten:
        return None
    status = f"{TAG} {calls1} tool calls in {turns} turns so far; budget about {b['lo']}–{b['hi']} calls"
    status += f", hard limit {b['cap']} turns." if b["cap"] is not None else "."
    return " ".join([status, *notes])


def handle(event: dict) -> dict | None:
    if not event.get("agent_id"):
        return None   # main conversation
    name = event.get("hook_event_name")
    if name == "SubagentStop":
        try:
            state_path(event).unlink()
        except OSError:
            pass
        return None
    if name != "PostToolBatch":
        return None
    budget = load_budget(event)
    if budget is None:
        return None
    path = state_path(event)
    try:
        before = json.loads(path.read_text())
    except (OSError, ValueError):
        before = {"turns": 0, "calls": 0}
    after = {"turns": before["turns"] + 1,
             "calls": before["calls"] + max(1, len(event.get("tool_calls") or []))}
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(after))
    os.replace(tmp, path)
    text = message(budget, before, after)
    if text is None:
        return None
    return {"hookSpecificOutput": {"hookEventName": "PostToolBatch", "additionalContext": text}}


def main() -> int:
    try:
        out = handle(json.load(sys.stdin))
        if out:
            print(json.dumps(out))
    except Exception:   # a counting hook must never break the agent it counts
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
