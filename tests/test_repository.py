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

    def test_release_and_mcp_version_boundaries(self):
        self.assertEqual(self.manifest["skill"]["version"], "0.1.1")
        self.assertEqual(self.manifest["source_ref"], "v0.1.1")
        self.assertEqual(
            self.manifest["cli"],
            {
                "minimum": "0.10.2",
                "tested": "0.12.0",
                "latest": "0.12.0",
                "installer": "0.12.0",
            },
        )
        self.assertEqual(self.manifest["adapters"]["mcp"]["minimum_cli"], "0.12.0")

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

    def test_template_video_workflow_keeps_live_and_recovery_contracts(self):
        text = (ROOT / "skills/use-huangque-cli/SKILL.md").read_text(encoding="utf-8")
        workflow = text.split("## Template videos\n", 1)[1].split("\n## ", 1)[0]
        for phrase in (
            "matrix-template-capability",
            "matrix-template-templates",
            "matrix-template-generate",
            "matrix-template-batch-generate",
            "template_id",
            "font_family",
            "2-5",
            "job_id",
            "structured recovery instruction",
        ):
            self.assertIn(phrase, workflow)
        self.assertIn("Do not invent template IDs, fonts, prices, or input fields.", workflow)
        self.assertIn("do not create a fresh batch.", workflow.lower())
        self.assertIn("only when the live capability discovery contains", workflow)


if __name__ == "__main__":
    unittest.main()
