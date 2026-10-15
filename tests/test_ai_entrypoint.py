from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "AI_START_HERE.md"


class AIEntrypointTests(unittest.TestCase):
    def test_discoverable_from_both_readmes_and_contributor_guide(self):
        for name in ("README.md", "README.ru.md", "AGENTS.md"):
            with self.subTest(source=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertIn("[AI_START_HERE.md](AI_START_HERE.md)", text)

    def test_referenced_local_markdown_files_exist(self):
        text = ENTRYPOINT.read_text(encoding="utf-8")
        references = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        self.assertGreater(len(references), 8)
        for reference in references:
            if reference.startswith(("https://", "http://", "#")):
                continue
            relative = reference.split("#", 1)[0]
            with self.subTest(reference=relative):
                self.assertTrue((ROOT / relative).exists())

    def test_model_entrypoint_points_to_authoritative_contracts(self):
        text = ENTRYPOINT.read_text(encoding="utf-8")
        for expected in (
            "onboarding/contract.yaml",
            "skills/bootstrap-instance/SKILL.md",
            "skills/rebuild-context/SKILL.md",
            "skills/capability-route/SKILL.md",
            "skills/orchestrate-action/SKILL.md",
            "docs/fresh-session-demo.md",
        ):
            with self.subTest(path=expected):
                self.assertIn(expected, text)

    def test_explore_does_not_imply_mutation_or_verification(self):
        text = ENTRYPOINT.read_text(encoding="utf-8")
        self.assertIn("Explore is read-only", text)
        self.assertIn("explicit approval", text)
        self.assertIn("executed != verified", text)
        self.assertIn("do not mark onboarding verified", text)


if __name__ == "__main__":
    unittest.main()
