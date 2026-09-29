"""Tests for the pipeline guard hook (.claude/hooks/guard_pipeline.py), in a throwaway project.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("guard_pipeline", ROOT / ".claude" / "hooks" / "guard_pipeline.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

BENIGN_CALC = """import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from unit_tools import Q
open("runs/s/calc/out.txt", "w").write(str(Q("1 ly").to("m")))
"""
EVIL_CALC = """from pathlib import Path
Path(".claude/skills/conundrum/scripts/unit_tools.py").write_text("# replaced")
"""


class Guard(unittest.TestCase):
    def setUp(self):
        self.box = tempfile.TemporaryDirectory()
        base = Path(os.path.realpath(self.box.name))
        self.proj, self.tmp, self.home = base / "proj", base / "tmp", base / "home"
        for d in (self.proj / ".claude" / "agents", self.proj / ".claude" / "skills" / "conundrum" / "scripts",
                  self.proj / "runs" / "s" / "calc", self.tmp, self.home / ".claude"):
            d.mkdir(parents=True)
        (self.proj / ".claude" / "agents" / "researcher.md").write_text(f"description: x. {guard.MARKER}.\n")
        (self.proj / ".claude" / "agents" / "helper.md").write_text("description: a general helper\n")
        (self.proj / "runs" / "link").symlink_to(self.proj / ".claude")
        (self.proj / "runs" / "s" / "calc" / "benign.py").write_text(BENIGN_CALC)
        (self.proj / "runs" / "s" / "calc" / "evil.py").write_text(EVIL_CALC)
        self.patches = [mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(self.proj), "HOME": str(self.home)}),
                        mock.patch.object(guard.tempfile, "gettempdir", return_value=str(self.tmp))]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.box.cleanup()

    def decide(self, tool, value, agent="researcher", agent_id="a1"):
        key = "command" if tool == "Bash" else guard.FILE_TOOLS[tool]
        ev = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": {key: value},
              "cwd": str(self.proj), "scratchpad_dir": str(self.tmp / "scratch")}
        if agent:
            ev.update(agent_type=agent, agent_id=agent_id)
        out = guard.decide(ev)
        return "deny" if out and out["hookSpecificOutput"]["permissionDecision"] == "deny" else "allow"

    def test_file_tools(self):
        cases = {
            "runs/s/research/theory.md": "allow",
            str(self.tmp / "x.pdf"): "allow",
            str(self.tmp / "scratch" / "notes.md"): "allow",
            ".claude/skills/conundrum/scripts/evil.py": "deny",
            ".claude/hooks/turn_budget.py": "deny",
            "README.md": "deny",                                # outside runs/
            "runs/link/agents/researcher.md": "deny",           # a symlink into .claude
            "runs/../.git/hooks/pre-commit": "deny",
            str(self.home / ".claude" / "settings.json"): "deny",
        }
        for path, want in cases.items():
            with self.subTest(path=path):
                self.assertEqual(self.decide("Write", path), want)
        self.assertEqual(self.decide("Edit", ".claude/agents/researcher.md"), "deny")

    def test_main_thread_and_other_agents_are_not_guarded(self):
        self.assertEqual(self.decide("Write", ".claude/skills/conundrum/scripts/new_tool.py", agent=None), "allow")
        self.assertEqual(self.decide("Write", ".claude/skills/x.py", agent="helper"), "allow")
        self.assertEqual(self.decide("Write", ".claude/skills/x.py", agent="Explore"), "allow")

    def test_bash(self):
        cases = {
            'python3 .claude/skills/conundrum/scripts/lit_search.py "warp" > runs/s/out.txt': "allow",
            "cp .claude/skills/conundrum/scripts/unit_tools.py runs/s/": "allow",
            "mkdir -p runs/s/calc && python3 runs/s/calc/benign.py": "allow",
            "timeout 590 python3 runs/s/calc/benign.py 2>&1 | tail -5": "allow",
            f"curl -sSL -o {self.tmp}/paper.pdf https://arxiv.org/pdf/x": "allow",
            "git log --oneline -3": "allow",
            "python3 - <<'EOF'\nimport sys; sys.path.insert(0, '.claude/skills/conundrum/scripts')\n"
            "open('runs/s/out.txt', 'w').write('ok')\nEOF": "allow",
            "echo x > .claude/skills/conundrum/scripts/evil.py": "deny",
            "cat runs/s/out.txt | tee .claude/hooks/turn_budget.py": "deny",
            "cp runs/s/tools/t.py .claude/skills/conundrum/scripts/": "deny",
            "cd .claude/skills && cp /tmp/x.py conundrum/scripts/": "deny",
            "rm -rf .claude": "deny",
            "sed -i 's/a/b/' .claude/agents/researcher.md": "deny",
            "git commit -am 'x'": "deny",
            "python3 -c \"open('.claude/x.py','w').write('1')\"": "deny",
            "python3 - <<'EOF'\nfrom pathlib import Path\nPath('.claude/skills/conundrum/scripts/x.py').write_text('1')\nEOF": "deny",
            "python3 runs/s/calc/evil.py": "deny",
            "bash -c 'echo x > .claude/x'": "deny",
            "curl -sSL -o .claude/skills/conundrum/scripts/x.py https://example.org/x.py": "deny",
            "ln -sf /tmp/evil .claude/skills/conundrum/scripts/unit_tools.py": "deny",
            "echo '{}' >> ~/.claude/settings.json": "deny",
            "cp /tmp/x runs/link/skills/y.py": "deny",           # through the symlink
            "find .claude -name '*.py' -delete": "deny",
            "echo hi > CLAUDE.md": "deny",
        }
        for command, want in cases.items():
            with self.subTest(command=command[:60]):
                self.assertEqual(self.decide("Bash", command), want)

    def test_denial_reason_reaches_the_agent(self):
        out = guard.decide({"hook_event_name": "PreToolUse", "tool_name": "Write", "agent_id": "a", "agent_type": "researcher",
                            "cwd": str(self.proj), "tool_input": {"file_path": ".claude/x.py"}})
        reason = out["hookSpecificOutput"]["permissionDecisionReason"]
        self.assertIn("[pipeline guard]", reason)
        self.assertIn("runs/", reason)

    def test_every_real_pipeline_agent_is_guarded(self):
        with mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(ROOT)}):
            for path in sorted((ROOT / ".claude" / "agents").glob("*.md")):
                with self.subTest(agent=path.stem):
                    self.assertTrue(guard.is_pipeline_agent({"agent_id": "x", "agent_type": path.stem}))


if __name__ == "__main__":
    unittest.main()
