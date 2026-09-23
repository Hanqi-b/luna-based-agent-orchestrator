import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_settings(path):
    """Read the small, flat TOML subset used by this repository."""
    settings = {}
    section = settings
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = settings.setdefault(line[1:-1], {})
            continue
        if "=" not in line:
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        value = value.strip('"')
        if value in {"true", "false"}:
            value = value == "true"
        elif value.isdigit():
            value = int(value)
        section[key] = value
    return settings


class LayoutTests(unittest.TestCase):
    def test_single_installation_source_and_skill_name(self):
        self.assertFalse((ROOT / "profiles").exists())
        self.assertTrue((ROOT / "codex").is_dir())
        self.assertTrue((ROOT / "agents").is_dir())
        self.assertTrue(
            (ROOT / "agents/skills/luna-based-agent-orchestrator/SKILL.md").is_file()
        )
        self.assertFalse((ROOT / "agents/skills/astra-orchestrator").exists())

    def test_preserved_model_matrix(self):
        config = load_settings(ROOT / "codex/config.toml")

        self.assertEqual(config["model"], "gpt-6-sol")
        self.assertEqual(config["model_reasoning_effort"], "high")
        self.assertEqual(config["agents"]["enabled"], True)
        self.assertEqual(config["agents"]["max_concurrent_threads_per_session"], 4)
        self.assertEqual(config["agents"]["default_subagent_model"], "gpt-6-luna")
        self.assertEqual(config["agents"]["default_subagent_reasoning_effort"], "max")

        expected = {
            "explorer.toml": ("gpt-6-luna", "max", "read-only"),
            "researcher.toml": ("gpt-6-luna", "max", "read-only"),
            "tester.toml": ("gpt-6-luna", "max", "workspace-write"),
            "worker.toml": ("gpt-5.6-luna", "max", "workspace-write"),
            "reviewer.toml": ("gpt-6-sol", "max", "read-only"),
        }
        for filename, (model, effort, sandbox) in expected.items():
            with self.subTest(filename=filename):
                role = load_settings(ROOT / "codex/agents" / filename)
                self.assertEqual(role["model"], model)
                self.assertEqual(role["model_reasoning_effort"], effort)
                self.assertEqual(role["sandbox_mode"], sandbox)

    def test_installers_use_single_source_without_plan_selection(self):
        shell = (ROOT / "setup.sh").read_text(encoding="utf-8")
        powershell = (ROOT / "setup.ps1").read_text(encoding="utf-8")
        for installer in (shell, powershell):
            with self.subTest(installer=installer[:20]):
                self.assertNotIn("profiles/", installer)
                self.assertNotIn("Read-Plan", installer)
                self.assertNotIn("select_plan", installer)
                self.assertNotIn("Plus", installer)
                self.assertNotIn("Pro  -", installer)


if __name__ == "__main__":
    unittest.main()
