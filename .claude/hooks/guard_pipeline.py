#!/usr/bin/env python3
"""Keep /conundrum pipeline agents from changing the pipeline itself (a Claude Code PreToolUse hook).

Pipeline agents read web pages and PDFs, so a page could try to talk one into editing the toolkit
that later agents trust, the agent definitions, the workflows, or the hooks that run on every
turn. This hook stops that for the pipeline agents: those whose definition in .claude/agents/
says "Use only when the conundrum workflow asks for it". The main conversation and every other
agent are left alone, so promoting a calculator at a checkpoint and ordinary development work.

Rules for pipeline agents:
- Write, Edit and NotebookEdit may touch only files under runs/, the session scratchpad or the
  system temp directory, after resolving symlinks.
- Bash may not write into protected places: this project's .claude/ and .git/, CLAUDE.md,
  CLAUDE.local.md, .mcp.json, and ~/.claude/. Checked:
  - redirections, tee, and download or unpack targets;
  - cp/mv/install/ln/rsync destinations;
  - rm/touch/mkdir/chmod/truncate targets and in-place sed or perl;
  - cd, which moves later relative paths;
  - bash -c;
  - Python, Perl, Ruby or Node code, inline, in a heredoc or in a script file, where a file write
    and a protected path appear on the same line.
  git is limited to read-only subcommands.
The Bash checks are best-effort: code that builds a path at run time can slip past them.
SKILL.md's git status check at each checkpoint backs them up.

The hook denies with a reason the agent sees, never prompts, and allows anything it can't parse
rather than break the agent (the permission system and the checkpoint check still apply).
"""
from __future__ import annotations

import json
import os
import re
import shlex
import sys
import tempfile
from pathlib import Path

MARKER = "Use only when the conundrum workflow asks for it"
FILE_TOOLS = {"Write": "file_path", "Edit": "file_path", "MultiEdit": "file_path", "NotebookEdit": "notebook_path"}
PROTECTED_DIRS = (".claude", ".git")
PROTECTED_FILES = ("CLAUDE.md", "CLAUDE.local.md", ".mcp.json")
ALL_ARGS_ARE_TARGETS = {"rm", "rmdir", "touch", "mkdir", "chmod", "chown", "truncate", "unlink", "shred", "tee"}
LAST_ARG_IS_TARGET = {"cp", "mv", "install", "ln", "rsync", "scp"}
INTERPRETERS = {"python", "python3", "perl", "ruby", "node"}
SHELLS = {"bash", "sh", "zsh", "dash"}
WRAPPERS = {"sudo", "command", "exec", "nohup", "env", "time", "nice", "stdbuf"}
GIT_READ_ONLY = {"status", "log", "diff", "show", "ls-files", "rev-parse", "blame", "grep", "describe", "cat-file"}
PROTECTED_TEXT = re.compile(r"(^|[\s'\"(=/])(\.claude|\.git)(/|['\"\s)]|$)|CLAUDE(\.local)?\.md|\.mcp\.json|~/\.claude")
WRITE_TEXT = re.compile(
    r"open\s*\([^)]*['\"][rbt]*[wax+][rwaxbt+]*['\"]|write_text|write_bytes|shutil\.\w+|"
    r"os\.(remove|unlink|rename|replace|makedirs|mkdir|symlink|rmdir|chmod|truncate)|"
    r"\.(unlink|rename|replace|symlink_to|touch|mkdir|chmod)\s*\(|subprocess|os\.system|"
    r"writeFileSync|appendFileSync|unlinkSync|renameSync|File\.(write|open)|>\s*['\"]")


class Denied(Exception):
    pass


def project_dir(event: dict) -> Path:
    return Path(os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."))


def is_pipeline_agent(event: dict) -> bool:
    agent_type = event.get("agent_type") or ""
    if not event.get("agent_id") or not re.fullmatch(r"[\w.-]+", agent_type):
        return False
    try:
        return MARKER in (project_dir(event) / ".claude" / "agents" / f"{agent_type}.md").read_text()
    except OSError:
        return False


def resolve(path: str, cwd: Path) -> Path:
    p = Path(os.path.expanduser(path))
    return Path(os.path.realpath(p if p.is_absolute() else cwd / p))


def _inside(p: Path, base: Path) -> bool:
    return p == base or base in p.parents


def is_protected(p: Path, proj: Path) -> bool:
    bases = [proj / d for d in PROTECTED_DIRS] + [Path(os.path.realpath(os.path.expanduser("~/.claude")))]
    return any(_inside(p, b) for b in bases) or p in {proj / f for f in PROTECTED_FILES}


def writable_areas(event: dict, proj: Path) -> list:
    areas = [proj / "runs", Path(os.path.realpath(tempfile.gettempdir()))]
    if event.get("scratchpad_dir"):
        areas.append(Path(os.path.realpath(event["scratchpad_dir"])))
    return areas


# ---------------------------------------------------------------- file tools
def check_file_tool(event: dict, proj: Path) -> None:
    key = FILE_TOOLS[event["tool_name"]]
    target = (event.get("tool_input") or {}).get(key)
    if not target:
        return
    p = resolve(target, Path(event.get("cwd") or proj))
    if is_protected(p, proj):   # checked first: a project inside /tmp must not make .claude/ writable
        raise Denied(f"pipeline agents may not write to {target}")
    if not any(_inside(p, a) for a in writable_areas(event, proj)):
        raise Denied(f"pipeline agents may write only under runs/ (or temp files); {target} is outside")


# ---------------------------------------------------------------- Bash
def check_code(code: str, where: str) -> None:
    for line in code.splitlines():
        if PROTECTED_TEXT.search(line) and WRITE_TEXT.search(line):
            raise Denied(f"{where} writes to a protected path (.claude/, .git/, CLAUDE.md ...): {line.strip()[:120]}")


def split_heredocs(command: str) -> tuple[str, list]:
    """Remove heredoc bodies from a command; return the rest and the bodies."""
    bodies, lines, out, i = [], command.split("\n"), [], 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        tags = re.findall(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", line)
        i += 1
        for tag in tags:
            body = []
            while i < len(lines) and lines[i].strip() != tag:
                body.append(lines[i])
                i += 1
            i += 1
            bodies.append("\n".join(body))
    return "\n".join(out), bodies


def simple_commands(command: str) -> list:
    lex = shlex.shlex(command, posix=True, punctuation_chars=";&|()<>")
    lex.whitespace_split = True
    lex.commenters = ""
    cmds, cur = [], []
    for tok in lex:
        if tok in (";", "&&", "||", "|", "&", "(", ")", "\n", "|&"):
            if cur:
                cmds.append(cur)
            cur = []
        else:
            cur.append(tok)
    if cur:
        cmds.append(cur)
    return cmds


def check_bash(command: str, event: dict, proj: Path, cwd: Path, depth: int = 0) -> None:
    if depth > 3:
        return
    rest, bodies = split_heredocs(command)
    for body in bodies:
        check_code(body, "inline code")
    try:
        cmds = simple_commands(rest)
    except ValueError:
        if PROTECTED_TEXT.search(rest) and re.search(r"[>|]|\b(cp|mv|rm|tee|ln|touch|mkdir|chmod|sed|git)\b", rest):
            raise Denied("unparseable command that names a protected path")
        return
    for words in cmds:
        cwd = check_simple(words, event, proj, cwd, depth)


def check_simple(words: list, event: dict, proj: Path, cwd: Path, depth: int) -> Path:
    targets = []
    # redirections anywhere in the command
    for i, w in enumerate(words):
        if w in (">", ">>", ">|", "&>", "&>>") and i + 1 < len(words):
            if not re.fullmatch(r"&?\d+|-", words[i + 1]):
                targets.append(words[i + 1])
    words = [w for i, w in enumerate(words) if w not in (">", ">>", ">|", "&>", "&>>", "<", ">&")
             and not (i > 0 and words[i - 1] in (">", ">>", ">|", "&>", "&>>", "<", ">&"))]
    while words and (re.fullmatch(r"\w+=.*", words[0]) or words[0] in WRAPPERS):
        words = words[1:]
    if words and words[0] == "timeout":
        words = [w for w in words[1:] if not re.fullmatch(r"-\S*|\d+[smhd]?", w)] if len(words) > 1 else []
    if not words:
        pass
    else:
        verb, args = os.path.basename(words[0]), words[1:]
        plain = [a for a in args if not a.startswith("-")]
        if verb == "cd":
            if plain and not plain[0].startswith("$"):
                cwd = resolve(plain[0], cwd)
        elif verb == "git":
            sub = next((a for a in args if not a.startswith("-")), "")
            if sub not in GIT_READ_ONLY:
                raise Denied(f"pipeline agents may not run 'git {sub}'; only read-only git is allowed")
        elif verb in ALL_ARGS_ARE_TARGETS:
            targets += plain
        elif verb in LAST_ARG_IS_TARGET:
            t_opt = next((args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-t", "--target-directory")), None)
            t_eq = next((a.split("=", 1)[1] for a in args if a.startswith("--target-directory=")), None)
            targets += [t_opt or t_eq] if (t_opt or t_eq) else plain[-1:]
        elif verb in ("sed", "perl") and any(a.startswith("-i") or a.startswith("-pi") for a in args):
            targets += plain
        elif verb == "dd":
            targets += [a[3:] for a in args if a.startswith("of=")]
        elif verb in ("curl", "wget"):
            targets += [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-o", "--output", "-O", "--output-document")]
        elif verb in ("tar", "unzip"):
            targets += [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-C", "--directory", "-d")]
        elif verb in SHELLS and "-c" in args:
            inner = args[args.index("-c") + 1] if args.index("-c") + 1 < len(args) else ""
            check_bash(inner, event, proj, cwd, depth + 1)
        elif verb.rstrip("0123456789.") in INTERPRETERS or verb in INTERPRETERS:
            flag = next((i for i, a in enumerate(args) if a in ("-c", "-e", "-E")), None)
            if flag is not None and flag + 1 < len(args):
                check_code(args[flag + 1], "inline code")
            else:
                script = next((a for a in args if not a.startswith("-")), None)
                if script and script != "-":
                    path = resolve(script, cwd)
                    if path.is_file() and path.stat().st_size < 2_000_000:
                        check_code(path.read_text(errors="replace"), f"script {script}")
        elif verb in ("xargs", "find") and any(PROTECTED_TEXT.search(a) for a in args) and \
                any(a in ("-delete", "-exec", "-execdir", "rm", "mv", "cp", "tee") for a in args):
            raise Denied(f"{verb} acting on a protected path")
    for t in targets:
        if t and not t.startswith("$") and is_protected(resolve(t, cwd), proj):
            raise Denied(f"pipeline agents may not write to {t}")
    return cwd


def decide(event: dict) -> dict | None:
    if event.get("hook_event_name") != "PreToolUse" or not is_pipeline_agent(event):
        return None
    proj = project_dir(event)
    tool = event.get("tool_name")
    try:
        if tool in FILE_TOOLS:
            check_file_tool(event, proj)
        elif tool == "Bash":
            check_bash((event.get("tool_input") or {}).get("command", ""), event, proj,
                       Path(os.path.realpath(event.get("cwd") or proj)))
    except Denied as why:
        return {"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": (f"[pipeline guard] {why}. Pipeline agents write only under runs/; "
                                         "the main session promotes anything that belongs in the toolkit.")}}
    return None


def main() -> int:
    try:
        out = decide(json.load(sys.stdin))
        if out:
            print(json.dumps(out))
    except Exception:   # never break an agent over a parsing problem
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
