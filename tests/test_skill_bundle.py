import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class SkillBundleTests(unittest.TestCase):
    def test_all_skills_are_declared_exactly_once(self):
        bundle = yaml.safe_load((SKILLS / "default-assistant.yaml").read_text(encoding="utf-8"))
        self.assertEqual(bundle["id"], "truthrail-default-assistant")
        self.assertEqual(bundle["source"]["protocol"], "0.2")
        groups = ("default_skills", "setup_skills", "optional_skills")
        skill_ids = [skill_id for group in groups for skill_id in bundle.get(group, [])]
        self.assertEqual(len(skill_ids), 9)
        self.assertEqual(len(skill_ids), len(set(skill_ids)))
        declared = set(skill_ids)
        present = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertEqual(present, declared, "missing or unregistered skill contract")

        for skill_id in sorted(declared):
            with self.subTest(skill=skill_id):
                path = SKILLS / skill_id / "SKILL.md"
                content = path.read_text(encoding="utf-8")
                self.assertTrue(content.startswith("---\n"))
                parts = content.split("---", 2)
                self.assertEqual(len(parts), 3)
                metadata = yaml.safe_load(parts[1])
                self.assertIsInstance(metadata, dict)
                self.assertEqual(metadata["name"], skill_id)
                self.assertTrue(metadata.get("description", "").strip())
                self.assertTrue(parts[2].strip())

    def test_no_retired_product_names_in_portable_skills(self):
        old_label = re.compile(r"agent[-_ ]hub", re.IGNORECASE)
        for path in sorted(SKILLS.rglob("*")):
            if not path.is_file():
                continue
            with self.subTest(path=str(path.relative_to(ROOT))):
                content = path.read_text(encoding="utf-8")
                self.assertIsNone(old_label.search(content))
                self.assertNotIn("an " + "Truthrail", content)

    def test_skill_safety_and_contract_references(self):
        contents = {
            p.parent.name: p.read_text(encoding="utf-8")
            for p in SKILLS.glob("*/SKILL.md")
        }
        self.assertTrue((ROOT / "capabilities" / "contract.yaml").is_file())
        self.assertIn("capabilities/contract.yaml", contents["activate-capability"])
        self.assertIn("explicit authorization", contents["bootstrap-instance"])
        self.assertIn("never grants permission", contents["capability-route"])
        self.assertIn("explicit user authorization", contents["orchestrate-action"])
        self.assertIn("executed != verified", contents["orchestrate-action"])
        self.assertIn("live target-system evidence", contents["rebuild-context"])
        self.assertIn("Do not infer inactivity", contents["recent-activity"])


if __name__ == "__main__":
    unittest.main()
