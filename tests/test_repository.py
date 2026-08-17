import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

    def test_core_skill_has_standard_frontmatter(self):
        text = (ROOT / "skills/use-huangque-cli/SKILL.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"\A---\nname: use-huangque-cli\ndescription: .+\n---\n")

    def test_manifest_hashes_match(self):
        for item in self.manifest["files"]:
            actual = hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest()
            self.assertEqual(actual, item["sha256"], item["path"])

    def test_versions_and_pi_package_match(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        version = self.manifest["skill"]["version"]
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertEqual(package["version"], version)
        self.assertEqual(package["pi"]["skills"], ["./skills/use-huangque-cli"])

    def test_all_five_entries_are_declared(self):
        self.assertEqual(
            set(self.manifest["adapters"]),
            {"deepseek", "codex", "openclaw", "pi", "mcp"},
        )
        destinations = [
            adapter["destination"]
            for adapter in self.manifest["adapters"].values()
            if "destination" in adapter
        ]
        self.assertEqual(len(destinations), len(set(destinations)))

    def test_skill_keeps_paid_confirmation_contract(self):
        text = (ROOT / "skills/use-huangque-cli/SKILL.md").read_text(encoding="utf-8")
        for phrase in ("--confirm", "--quote-token", "request_id", "Never print credentials"):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
