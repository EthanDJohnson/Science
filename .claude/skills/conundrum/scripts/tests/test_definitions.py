"""Consistency checks across the skill, agents, workflows and settings.

Catches the mistakes that only show up at run time: an agentType with no agent file,
a lens in the catalog the workflow doesn't know, a referenced file that doesn't exist,
a model or effort value Claude Code would reject. Run from the project root:

    python3 -m unittest discover -s .claude/skills/conundrum/scripts/tests -v
"""
import importlib.util
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
        self.assertGreaterEqual(len(agents), 17)
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
                if "**Writing:** write no files" in body:
                    self.assertFalse({"Write", "Edit"} & tools, "returns text but can write files")
                else:
                    self.assertIn("Write", tools)

    def test_models_follow_the_plan(self):
        agents = pipeline_agents()
        self.assertEqual(agents["researcher"][0]["model"], "sonnet")
        self.assertEqual(agents["researcher"][0]["effort"], "high")
        self.assertEqual(agents["adjudicator"][0]["model"], "fable")
        self.assertEqual(agents["lens-constraints"][0]["effort"], "xhigh")
        for stem in ("candidate-builder", "falsifier", "dossier-compiler"):
            self.assertEqual(agents[stem][0]["model"], "opus", stem)

    def test_every_agent_checkpoints_and_reports_back(self):
        # Smoke-test fixes: a cut-off agent that never wrote its file lost all its work, and an agent
        # that ends without {ok, path, summary} counts as failed. maxTurns is a safety net well above
        # the call budget, because agents overshoot budgets (measured: 48 calls against a budget of 25-40).
        appenders = {"researcher", "source-checker", "math-checker"} | {s for s in pipeline_agents() if s.startswith("lens-")}
        for stem, (fm, body) in pipeline_agents().items():
            with self.subTest(agent=stem):
                rules = body.partition("## Ground rules")[2]
                self.assertTrue(rules, "no Ground rules section")
                budget = re.search(r"aim for about (\d+)–(\d+) tool calls", rules)
                self.assertIsNotNone(budget, "no call budget")
                self.assertGreaterEqual(int(fm["maxTurns"]), 1.4 * int(budget.group(2)),
                                        "maxTurns leaves too little headroom over the budget")
                self.assertIn("Finish by returning", rules)
                if "**Writing:** write no files" in rules:   # returns its document as text (the judge)
                    for field in ("`ok`", "`report`", "`summary`"):
                        self.assertIn(field, rules)
                    continue
                self.assertIn("Edit", fm["tools"], "told to improve with Edit but lacks the tool")
                if stem in appenders:
                    self.assertIn("**Checkpoints:**", rules)
                    self.assertIn("same step as your next tool call", rules)
                else:
                    self.assertRegex(rules, r"\*\*First draft:\*\* write a complete first draft .* by about call \d+")
                self.assertIn("**Resuming:**", rules)
                self.assertIn("already exists", rules)
                self.assertIn("Finish by returning", rules)
                if stem not in ("candidate-builder", "falsifier"):
                    self.assertIn("`ok`", rules)
                    self.assertIn("`summary`", rules)

    def test_ground_rules_match_their_generator(self):
        # dev/agent_rules.py is the single source of every agent's ground rules and maxTurns.
        spec = importlib.util.spec_from_file_location("agent_rules", ROOT / "dev" / "agent_rules.py")
        rules = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rules)
        self.assertEqual(set(rules.SPEC), set(pipeline_agents()), "agents and the generator's SPEC disagree")
        for path in sorted(AGENTS.glob("*.md")):
            with self.subTest(agent=path.stem):
                self.assertEqual(rules.render(path), path.read_text(),
                                 "edited by hand: change dev/agent_rules.py and run it instead")

    def test_no_agent_writes_a_file_claude_code_refuses(self):
        # Claude Code refuses a subagent's write to REPORT*.md, SUMMARY*.md, FINDINGS*.md or ANALYSIS*.md
        # ("Subagents should return findings as text, not write report files"), ignoring case.
        blocked = re.compile(r"^(report|summary|findings|analysis).*\.md$", re.I)
        spec = importlib.util.spec_from_file_location("agent_rules", ROOT / "dev" / "agent_rules.py")
        rules = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rules)
        for name, s in rules.SPEC.items():
            if "target" in s:
                with self.subTest(agent=name):
                    self.assertIsNone(blocked.match(Path(s["target"]).name), s["target"])
        for name in ("conundrum-research", "conundrum-analyze"):
            for path in re.findall(r"[Ww]rite \$\{dir\}/([\w/.<>${}-]+\.md)", workflow_source(name)):
                with self.subTest(workflow=name, path=path):
                    self.assertIsNone(blocked.match(Path(path).name), path)
        self.assertIn("report", (AGENTS / "adjudicator.md").read_text())
        self.assertIn("reportPath", (SKILL / "SKILL.md").read_text())

    def test_calculation_and_citation_safety_rules(self):
        for stem, (fm, body) in pipeline_agents().items():
            tools = {t.strip() for t in fm["tools"].split(",")}
            with self.subTest(agent=stem):
                if "calc/" in body:
                    self.assertIn("10 minutes", body)
                    self.assertIn("pkill -f", body)
                    self.assertIn("poll", body, "calculation agents must be told not to poll")
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
        self.assertEqual(len(lenses), 9)
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

    def test_foundations_type_is_wired_through(self):
        src = workflow_source("conundrum-analyze")
        self.assertIn("foundations: [", src)
        self.assertIn("'position'", src)
        self.assertIn("`foundations`", (SKILL / "SKILL.md").read_text())
        self.assertIn("**foundations**", (SKILL / "references" / "lenses.md").read_text())
        schemas = (SKILL / "references" / "schemas.md").read_text()
        self.assertIn("design|foundations", schemas)
        self.assertIn("**position**", schemas)
        self.assertIn("**Foundations questions**", (SKILL / "references" / "rubric.md").read_text())
        self.assertIn("`position`", (AGENTS / "candidate-builder.md").read_text())

    def test_every_refuter_angle_is_defined_for_the_falsifier(self):
        src = workflow_source("conundrum-analyze")
        block = re.search(r"const ANGLES_BY_TYPE = \{(.*?)\n\}", src, re.S).group(1)
        angles = set(re.findall(r"'(\w+)'", block))
        angles |= set(re.findall(r"'(\w+)'", re.search(r"const DEFAULT_ANGLES = \[(.*?)\]", src).group(1)))
        self.assertIn("magnitude", angles)
        falsifier = (AGENTS / "falsifier.md").read_text()
        for angle in sorted(angles):
            self.assertIn(f"- **{angle}:**", falsifier, f"the {angle} angle is used but never defined")

    def test_anomaly_type_is_wired_through(self):
        # One wording of the anomaly null everywhere; it must not swallow the method systematics.
        null = ("no single dominant cause: a statistical fluctuation, or several smaller effects or "
                "underestimated uncertainties, none of which dominates")
        for path in (AGENTS / "candidate-builder.md", AGENTS / "lens-statistician.md",
                     SKILL / "references" / "schemas.md"):
            text = " ".join(path.read_text().split())
            self.assertIn(null, text, path.name)
            self.assertNotIn("artifact or known effect", text, path.name)
        self.assertIn("## Prediction matrix", (SKILL / "references" / "schemas.md").read_text())
        self.assertIn("`## Prediction matrix`", (AGENTS / "candidate-builder.md").read_text())
        rubric = (SKILL / "references" / "rubric.md").read_text()
        self.assertIn("**Anomaly questions**", rubric)
        self.assertIn("(For anomaly questions use:", rubric)
        self.assertIn("rule 9", (AGENTS / "adjudicator.md").read_text())
        self.assertIn("anomaly: {", workflow_source("conundrum-research"))
        self.assertIn("args: {slug, depth, type, tools, prior}", (SKILL / "SKILL.md").read_text())

    def test_math_checks_are_wired_through(self):
        src = workflow_source("conundrum-analyze")
        self.assertIn("agentType: 'math-checker'", src)
        self.assertIn("## math/<lens>.md", (SKILL / "references" / "schemas.md").read_text())
        self.assertIn("math checks", (SKILL / "references" / "rubric.md").read_text())
        for reader in ("candidate-builder", "falsifier", "adjudicator", "report-auditor"):
            self.assertIn("math/", (AGENTS / f"{reader}.md").read_text(), reader)
        checker = (AGENTS / "math-checker.md").read_text()
        for tool in ("math_checks.py", "math_run.py"):
            self.assertIn(tool, checker)
        self.assertIn("Never import, copy or run the lens's scripts", checker)

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

    def test_tool_catalog_matches_the_toolkit(self):
        catalog = (SKILL / "references" / "tools.md").read_text()
        scripts = {p.name for p in (SKILL / "scripts").glob("*.py")}
        listed = set(re.findall(r"`(\w+\.py)`", catalog))
        self.assertEqual(scripts - listed, set(), "toolkit scripts missing from tools.md")
        self.assertEqual({f for f in listed if f in scripts or not f.startswith("<")} - scripts, set(),
                         "tools.md lists scripts that don't exist")
        research = workflow_source("conundrum-research")
        self.assertIn("agentType: 'toolsmith'", research)
        self.assertIn("/tools/", research)

    def test_turn_budget_hook_is_registered(self):
        hooks = json.loads((CLAUDE / "settings.json").read_text())["hooks"]
        for event in ("PostToolBatch", "SubagentStop"):
            commands = [h["command"] for group in hooks[event] for h in group["hooks"]]
            self.assertTrue(any(".claude/hooks/turn_budget.py" in c for c in commands), event)
        self.assertTrue((CLAUDE / "hooks" / "turn_budget.py").exists())

    def test_pipeline_guard_is_registered(self):
        groups = json.loads((CLAUDE / "settings.json").read_text())["hooks"]["PreToolUse"]
        guard = [g for g in groups if any(".claude/hooks/guard_pipeline.py" in h["command"] for h in g["hooks"])]
        self.assertEqual(len(guard), 1)
        self.assertTrue({"Write", "Edit", "NotebookEdit", "Bash"} <= set(guard[0]["matcher"].split("|")))
        self.assertTrue((CLAUDE / "hooks" / "guard_pipeline.py").exists())
        self.assertIn("git status --short -- .claude", (SKILL / "SKILL.md").read_text())

    def test_earlier_runs_are_wired_through(self):
        skill = (SKILL / "SKILL.md").read_text()
        for step in ("prior_runs.py list", "prior_runs.py import", "prior_runs.py record", "prior_runs.py mark",
                     "## Prior runs", "What changed since", "prior}"):
            self.assertIn(step, skill)
        self.assertIn("prior?", re.search(r"whenToUse: '([^']*)'", workflow_source("conundrum-research")).group(1))
        self.assertIn("PROVENANCE.md", (AGENTS / "researcher.md").read_text())
        self.assertIn("PRIOR", (AGENTS / "dossier-compiler.md").read_text())
        schemas = (SKILL / "references" / "schemas.md").read_text()
        for part in ("## Prior runs", "PRIOR: <run>", "## run.json", "Read only this run"):
            self.assertIn(part, schemas)
        self.assertIn("PRIOR", (SKILL / "references" / "rubric.md").read_text())
        for path in AGENTS.glob("*.md"):
            self.assertIn("never another run's folder", path.read_text(), path.stem)

    def test_settings_allow_what_the_agents_need(self):
        allow = json.loads((CLAUDE / "settings.json").read_text())["permissions"]["allow"]
        for rule in ("WebSearch", "WebFetch", "Bash(python3 runs/*)",
                     "Bash(python3 .claude/skills/conundrum/scripts/*)", "Edit(runs/**)"):
            self.assertIn(rule, allow)


if __name__ == "__main__":
    unittest.main()
