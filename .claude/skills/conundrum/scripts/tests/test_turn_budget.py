"""Tests for the turn-budget hook (.claude/hooks/turn_budget.py).

The hook counts each conundrum agent's turns and tool calls and injects "[turn budget]"
reminders at thresholds. Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("turn_budget", ROOT / ".claude" / "hooks" / "turn_budget.py")
tb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tb)


class TurnBudget(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(ROOT)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def event(self, agent_type, agent_id="a1", calls=1, name="PostToolBatch"):
        ev = {"hook_event_name": name, "cwd": str(ROOT), "scratchpad_dir": self.tmp.name,
              "tool_calls": [{"tool_name": "Bash"}] * calls}
        if agent_type is not None:
            ev.update(agent_type=agent_type, agent_id=agent_id)
        return ev

    def run_turns(self, agent_type, calls_per_turn, turns, agent_id="a1"):
        out = {}
        for turn in range(1, turns + 1):
            res = tb.handle(self.event(agent_type, agent_id, calls_per_turn))
            if res:
                out[turn] = res["hookSpecificOutput"]["additionalContext"]
        return out

    def test_every_pipeline_agent_has_a_parsable_budget(self):
        for path in sorted((ROOT / ".claude" / "agents").glob("*.md")):
            with self.subTest(agent=path.stem):
                b = tb.load_budget({"agent_type": path.stem, "cwd": str(ROOT)})
                self.assertIsNotNone(b, "no budget line the hook can read")
                self.assertLess(b["hi"], b["cap"])
                if "**Writing:** write no files" in path.read_text():   # returns its document as text
                    continue
                self.assertTrue(b["appends"] or b["draft_by"] is not None,
                                "neither a Checkpoints rule nor a first-draft call")

    def test_main_thread_and_other_agents_are_left_alone(self):
        self.assertIsNone(tb.handle(self.event(None)))
        self.assertEqual(self.run_turns("Explore", 5, 10), {})
        self.assertEqual(self.run_turns("some-plugin:reviewer", 5, 10), {})

    def test_appending_agent_reminders(self):
        out = self.run_turns("researcher", 1, 60)
        self.assertEqual(sorted(out)[:4], [10, 20, 30, 40])
        self.assertIn("10 tool calls in 10 turns", out[10])
        self.assertIn("Append anything you have settled", out[10])
        self.assertIn("top of your budget", out[40])
        self.assertIn("About 5 turns remain", out[55])
        self.assertIn("About 1 turn remains", out[59])
        self.assertTrue(all(text.startswith(tb.TAG) for text in out.values()))

    def test_draft_agent_reminders_count_calls_and_turns_separately(self):
        out = self.run_turns("report-auditor", 3, 12)    # 3 parallel calls per turn
        draft_turn = next(t for t, text in out.items() if "first draft" in text)
        self.assertEqual(draft_turn, 7)                 # calls 18 -> 21 crosses call 20
        self.assertIn("21 tool calls in 7 turns", out[7])
        self.assertIn("top of your budget", out[12])   # calls 33 -> 36 crosses 35
        self.assertNotIn("Append anything", " ".join(out.values()))

    def test_an_agent_that_returns_text_is_told_to_finish_its_output(self):
        # A deep judge reads ~45 files; at 3 per turn it must not be told to wrap up by call 36.
        early = self.run_turns("adjudicator", 3, 12, agent_id="early")
        self.assertNotIn("top of your budget", " ".join(early.values()))
        out = self.run_turns("adjudicator", 3, 20)      # calls 57 -> 60 cross the top of the budget, 55
        top = next(text for text in out.values() if "top of your budget" in text)
        self.assertIn("finish your final output", top)
        self.assertNotIn("your file", " ".join(out.values()))

    def test_agents_are_counted_independently_and_cleaned_up(self):
        self.run_turns("researcher", 1, 9, agent_id="x")
        self.assertEqual(self.run_turns("researcher", 1, 9, agent_id="y"), {})   # y keeps its own tally
        tenth = tb.handle(self.event("researcher", "x"))                          # x's tenth call
        self.assertIn("10 tool calls in 10 turns", tenth["hookSpecificOutput"]["additionalContext"])
        state = Path(self.tmp.name) / "conundrum-turn-budget" / "x.json"
        self.assertEqual(json.loads(state.read_text()), {"turns": 10, "calls": 10})
        tb.handle(self.event("researcher", "x", name="SubagentStop"))
        self.assertFalse(state.exists())

    def test_bad_input_never_raises(self):
        with mock.patch("sys.stdin") as stdin:
            stdin.read.return_value = "not json"
            self.assertEqual(tb.main(), 0)


if __name__ == "__main__":
    unittest.main()
