"""Tests for dev/run_costs.py on a synthetic session: a main conversation, a subagent and a workflow agent.

Run from the project root:
    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[5]
spec = importlib.util.spec_from_file_location("run_costs", ROOT / "dev" / "run_costs.py")
rc = importlib.util.module_from_spec(spec)
sys.modules["run_costs"] = rc   # dataclasses look their module up
spec.loader.exec_module(rc)

PROJECT = "/work/Science"
USAGE = {"input_tokens": 10, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 20000,
         "cache_creation": {"ephemeral_5m_input_tokens": 1000, "ephemeral_1h_input_tokens": 0}}
BASH = {"type": "tool_use", "id": "toolu_1", "name": "Bash", "input": {"command": "ls"}}
SEARCH = {"type": "tool_use", "id": "toolu_2", "name": "WebSearch", "input": {"query": "warp"}}


def assistant(msg_id, model, t, content, output, stop=None):
    return {"type": "assistant", "timestamp": t, "cwd": PROJECT,
            "message": {"id": msg_id, "model": model, "content": content, "stop_reason": stop,
                        "usage": dict(USAGE, output_tokens=output)}}


class RunCosts(unittest.TestCase):
    def setUp(self):
        self.box = tempfile.TemporaryDirectory()
        self.config = Path(self.box.name)
        folder = self.config / "projects" / "-work-Science"
        (folder / "S1" / "subagents").mkdir(parents=True)
        (folder / "S1" / "workflows" / "wf_1").mkdir(parents=True)
        self.session = folder / "S1.jsonl"
        main = [
            {"type": "user", "timestamp": "2026-09-30T10:00:00Z", "cwd": PROJECT, "message": {"content": "go"}},
            # one reply streamed over two rows: the first holds the stream-start usage, the last the final
            assistant("msg_1", "claude-opus-5-5", "2026-09-30T10:00:01Z",
                      [{"type": "thinking", "thinking": "", "signature": "s" * 1850}], 5),
            assistant("msg_1", "claude-opus-5-5", "2026-09-30T10:00:01Z", [BASH], 500, "tool_use"),
            assistant("msg_2", "claude-opus-5-5", "2026-09-30T10:05:00Z", [{"type": "text", "text": "done"}], 100, "end_turn"),
            assistant("msg_2", "claude-opus-5-5", "2026-09-30T10:05:00Z", [{"type": "text", "text": "done"}], 100, "end_turn"),
            assistant("msg_x", "<synthetic>", "2026-09-30T10:06:00Z", [{"type": "text", "text": "API error"}], 0, "stop"),
        ]
        self.write(self.session, main)
        # a subagent's transcript never records the final usage
        self.write(folder / "S1" / "subagents" / "agent-abc.jsonl", [
            assistant("msg_3", "claude-sonnet-5-5", "2026-09-30T10:01:00Z",
                      [{"type": "thinking", "thinking": "", "signature": "s" * 2850}], 3),
            assistant("msg_3", "claude-sonnet-5-5", "2026-09-30T10:01:00Z", [SEARCH], 3)])
        (folder / "S1" / "subagents" / "agent-abc.meta.json").write_text(
            json.dumps({"agentType": "researcher", "description": "Find papers", "model": "sonnet"}))
        self.write(folder / "S1" / "workflows" / "wf_1" / "agent-def.jsonl", [
            assistant("msg_4", "claude-mystery-9", "2026-09-30T10:02:00Z", [{"type": "text", "text": "x" * 100}], 2)])
        self.env = mock.patch.dict(os.environ, {"CLAUDE_CONFIG_DIR": str(self.config)})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.box.cleanup()

    @staticmethod
    def write(path, records):
        path.write_text("\n".join(json.dumps(r) for r in records) + "\n")

    def test_finds_the_latest_session_of_the_project(self):
        self.assertEqual(rc.find_session(None, Path(PROJECT)), self.session)
        self.assertEqual(rc.find_session("S1", Path(PROJECT)), self.session)
        with self.assertRaises(FileNotFoundError):
            rc.find_session("nope", Path(PROJECT))

    def test_main_conversation_uses_the_recorded_counts(self):
        main = rc.load_session(self.session)[0]
        self.assertEqual(main.name, "main conversation")
        self.assertEqual(len(main.replies), 2)              # the duplicate row and the synthetic reply don't count
        self.assertEqual(main.tool_calls, 1)
        self.assertEqual(main.total("output"), 600)
        self.assertFalse(main.estimated)
        per_reply = (4 * 10 + 1.25 * 4 * 1000 + 0.20 * 20000) / 1e6
        self.assertAlmostEqual(main.cost, 2 * per_reply + 20 * 600 / 1e6)

    def test_agent_output_is_estimated_from_text_and_signatures(self):
        agents = {a.name: a for a in rc.load_session(self.session)}
        researcher = agents["researcher"]
        self.assertEqual(researcher.description, "Find papers")
        self.assertTrue(researcher.estimated)
        visible = len("WebSearch") + len(json.dumps(SEARCH["input"]))
        want = round(rc.TOKENS_PER_VISIBLE_CHAR * visible + rc.TOKENS_PER_SIGNATURE_CHAR * (2850 - rc.SIGNATURE_OVERHEAD))
        self.assertEqual(researcher.total("output"), want)
        self.assertAlmostEqual(researcher.cost, (2 * 10 + 1.25 * 2 * 1000 + 0.20 * 20000 + 10 * want) / 1e6)

    def test_workflow_agents_are_found_and_unknown_models_flagged(self):
        agents = rc.load_session(self.session)
        self.assertEqual([a.name for a in agents], ["main conversation", "researcher", "agent"])
        self.assertIsNone(agents[2].cost)
        text = rc.report(self.session, agents)
        self.assertIn("No price for claude-mystery-9", text)
        self.assertIn("1 WebSearch", text)
        self.assertIn("~ marks estimated output", text)
        self.assertIn("Output estimate check, opus-5-5", text)

    def test_since_drops_earlier_replies(self):
        since = datetime(2026, 9, 30, 10, 1, 30, tzinfo=timezone.utc)
        agents = rc.load_session(self.session, since)
        self.assertEqual([a.name for a in agents], ["main conversation", "agent"])
        self.assertEqual(len(agents[0].replies), 1)
        self.assertEqual(rc.parse_time("2026-09-30T10:01:30Z"), since)

    def test_one_hour_cache_writes_cost_double(self):
        reply = rc.Reply("claude-opus-5-5", datetime.now(timezone.utc), final=True, usage={
            "input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 1000,
            "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": 1000}})
        self.assertAlmostEqual(reply.cost, 2 * 4 * 1000 / 1e6)

    def test_command_line(self):
        with mock.patch("sys.stdout") as out:
            self.assertEqual(rc.main([str(self.session)]), 0)
        printed = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("researcher: Find papers", printed)
        self.assertIn("Total:", printed)


if __name__ == "__main__":
    unittest.main()
