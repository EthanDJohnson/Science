"""Consistency checks across the skill, agents, workflows and settings.

Catches the mistakes that only show up at run time: an agentType with no agent file,
a lens in the catalog the workflow doesn't know, a referenced file that doesn't exist,
a model or effort value Claude Code would reject. Run from the project root:

    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CLAUDE = ROOT / ".claude"
SKILL = CLAUDE / "skills" / "conundrum"
AGENTS = CLAUDE / "agents"
WORKFLOWS = CLAUDE / "workflows"

MODELS = {"sonnet", "opus", "fable", "haiku", "inherit"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
KNOWN_TOOLS = {"Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "WebFetch"}


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    assert match, f"{path} has no frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields, match.group(2)


def workflow_source(name: str) -> str:
    return (WORKFLOWS / f"{name}.js").read_text()


def pipeline_agents() -> dict:
    return {p.stem: frontmatter(p) for p in sorted(AGENTS.glob("*.md"))}


class AgentDefinitions(unittest.TestCase):
    def test_every_agent_is_well_formed(self):
        agents = pipeline_agents()
        self.assertGreaterEqual(len(agents), 16)
        for stem, (fm, body) in agents.items():
            with self.subTest(agent=stem):
                self.assertEqual(fm.get("name"), stem)
                self.assertIn(fm.get("model"), MODELS)
                self.assertIn(fm.get("effort"), EFFORTS)
                self.assertTrue(fm.get("maxTurns", "").isdigit())
                tools = {t.strip() for t in fm.get("tools", "").split(",")}
                self.assertTrue(tools <= KNOWN_TOOLS, tools - KNOWN_TOOLS)
                self.assertIn("Use only when the conundrum workflow asks for it", fm.get("description", ""))
                self.assertTrue("schemas.md" in body or "rubric.md" in body)
                if "python3 " in body:
                    self.assertIn("Bash", tools, "runs python3 but has no Bash tool")
                self.assertIn("Write", tools)

    def test_models_follow_the_plan(self):
        agents = pipeline_agents()
        self.assertEqual(agents["researcher"][0]["model"], "sonnet")
        self.assertEqual(agents["researcher"][0]["effort"], "high")
        self.assertEqual(agents["adjudicator"][0]["model"], "fable")
        self.assertEqual(agents["lens-constraints"][0]["effort"], "xhigh")
        for stem in ("candidate-builder", "falsifier", "dossier-compiler"):
            self.assertEqual(agents[stem][0]["model"], "opus", stem)

    def test_every_agent_writes_early_and_reports_back(self):
        # Smoke-test fixes: a turn-capped agent that never wrote its file lost all its work,
        # and a WROTE agent that ends without {ok, path, summary} counts as failed.
        for stem, (fm, body) in pipeline_agents().items():
            with self.subTest(agent=stem):
                rules = body.partition("## Ground rules")[2]
                self.assertTrue(rules, "no Ground rules section")
                budget = re.search(r"aim for about (\d+)–(\d+) tool calls.*?by about call (\d+)", rules)
                self.assertIsNotNone(budget, "no write-early budget line")
                lo, hi, first = map(int, budget.groups())
                self.assertLess(first, hi)
                self.assertLess(hi, int(fm["maxTurns"]), "maxTurns leaves no headroom over the budget")
                self.assertIn("Edit", fm["tools"], "told to improve with Edit but lacks the tool")
                self.assertIn("Finish by returning", rules)
                if stem not in ("candidate-builder", "falsifier"):
                    self.assertIn("`ok`", rules)
                    self.assertIn("`summary`", rules)

    def test_calculation_and_citation_safety_rules(self):
        for stem, (fm, body) in pipeline_agents().items():
            tools = {t.strip() for t in fm["tools"].split(",")}
            with self.subTest(agent=stem):
                if "calc/" in body:
                    self.assertIn("10 minutes", body)
                    self.assertIn("pkill -f", body)
                if "WebSearch" in tools:
                    self.assertIn("summar", body.partition("## Ground rules")[2],
                              "WebSearch agents must be told results are summaries, not quotes")
                if "gr_tensors.py" in body and "calc/" in body:
                    self.assertIn("run_in_background", body)

    def test_referenced_repo_files_exist(self):
        pattern = re.compile(r"\.claude/skills/conundrum/[\w./-]+\.(?:md|py)")
        sources = [p for p in AGENTS.glob("*.md")] + [SKILL / "SKILL.md"] + list((SKILL / "references").glob("*.md"))
        for path in sources:
            for ref in set(pattern.findall(path.read_text())):
                with self.subTest(file=path.name, ref=ref):
                    self.assertTrue((ROOT / ref).exists(), f"{path.name} references missing {ref}")


class WorkflowWiring(unittest.TestCase):
    def test_literal_agent_types_exist(self):
        for name in ("conundrum-research", "conundrum-analyze"):
            for agent_type in re.findall(r"agentType: '([\w-]+)'", workflow_source(name)):
                with self.subTest(workflow=name, agent=agent_type):
                    self.assertTrue((AGENTS / f"{agent_type}.md").exists())

    def test_every_lens_has_an_agent_and_a_catalog_entry(self):
        src = workflow_source("conundrum-analyze")
        lenses = re.findall(r"'(\w+)'", re.search(r"const LENSES = \[(.*?)\]", src).group(1))
        self.assertEqual(len(lenses), 8)
        catalog = (SKILL / "references" / "lenses.md").read_text()
        for lens in lenses:
            with self.subTest(lens=lens):
                self.assertTrue((AGENTS / f"lens-{lens}.md").exists())
                self.assertIn(f"`{lens}`", catalog)
        for lens_file in AGENTS.glob("lens-*.md"):
            self.assertIn(lens_file.stem.removeprefix("lens-"), lenses, f"{lens_file.name} is not wired in")

    def test_default_lens_sets_only_use_known_lenses(self):
        src = workflow_source("conundrum-analyze")
        lenses = set(re.findall(r"'(\w+)'", re.search(r"const LENSES = \[(.*?)\]", src).group(1)))
        block = re.search(r"const DEFAULT_LENSES = \{(.*?)\n\}", src, re.S).group(1)
        for row in re.findall(r"\[(.*?)\]", block):
            self.assertTrue(set(re.findall(r"'(\w+)'", row)) <= lenses, row)

    def test_skill_calls_the_saved_workflow_names(self):
        skill = (SKILL / "SKILL.md").read_text()
        for name in ("conundrum-research", "conundrum-analyze"):
            meta_name = re.search(r"name: '([\w-]+)'", workflow_source(name)).group(1)
            self.assertEqual(meta_name, name)
            self.assertIn(f'name: "{name}"', skill)


class SkillAndSettings(unittest.TestCase):
    def test_skill_frontmatter(self):
        fm, body = frontmatter(SKILL / "SKILL.md")
        self.assertEqual(fm["name"], "conundrum")
        self.assertEqual(fm["disable-model-invocation"], "true")
        self.assertLessEqual(len(fm["description"]), 1536)
        self.assertIn("$ARGUMENTS", body)

    def test_settings_allow_what_the_agents_need(self):
        allow = json.loads((CLAUDE / "settings.json").read_text())["permissions"]["allow"]
        for rule in ("WebSearch", "WebFetch", "Bash(python3 runs/*)",
                     "Bash(python3 .claude/skills/conundrum/scripts/*)", "Edit(runs/**)"):
            self.assertIn(rule, allow)


if __name__ == "__main__":
    unittest.main()
