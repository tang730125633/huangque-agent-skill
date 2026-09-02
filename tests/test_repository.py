import hashlib
import json
import re
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

    def test_manifest_uses_deterministic_lf_newlines(self):
        self.assertNotIn(b"\r", (ROOT / "manifest.json").read_bytes())

    def test_release_and_mcp_version_boundaries(self):
        self.assertEqual(self.manifest["skill"]["version"], "0.3.0")
        self.assertEqual(self.manifest["source_ref"], "v0.3.0")
        self.assertEqual(
            self.manifest["cli"],
            {
                "minimum": "0.10.2",
                "tested": "0.13.5",
                "latest": "0.13.5",
                "installer": "0.13.5",
                "installer_wheel_sha256": "387c686e83d2976ade3ec8ee29210c450792dd5e5c51369b8a6fcf07b2eb9fab",
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

    def test_director_upload_keeps_quote_cost_and_idempotent_recovery_contract(self):
        text = (ROOT / "skills/use-huangque-cli/SKILL.md").read_text(encoding="utf-8")
        workflow = text.split("## Director workflows\n", 1)[1].split("\n## ", 1)[0]
        for phrase in (
            "hq run director-breakdown-upload",
            "--quote-token <quote_token>",
            "--expected-cost <cost>",
            "Idempotency-Key",
            "same file",
            "do not obtain a new quote",
            "director-scene-video-generate",
            "director-scene-talking-generate",
        ):
            self.assertIn(phrase, workflow)
        self.assertNotIn("hq director-breakdown-upload", workflow)

    def _digital_human_route(self, mode):
        text = (ROOT / "skills/use-huangque-cli/SKILL.md").read_text(encoding="utf-8")
        workflow = text.split("## Digital-human one-click runs\n", 1)[1].split("\n## ", 1)[0]
        prefix = f"| `{mode}` |"
        row = next(line for line in workflow.splitlines() if line.startswith(prefix))
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        self.assertEqual(5, len(cells))
        return workflow, cells, [set(re.findall(r"`([^`]+)`", cell)) for cell in cells]

    def test_digital_human_text_run_has_complete_field_routing(self):
        workflow, cells, route = self._digital_human_route("text")
        self.assertEqual({"text"}, route[0])
        self.assertEqual({"dh-run-*"}, route[1])
        self.assertEqual({"narration_mode=text", "script", "run_id"}, route[2])
        self.assertEqual(
            {"run_id", "plan_digest", "narration_mode=text", "script"}, route[3]
        )
        self.assertEqual(
            {
                "request_id", "consent_token", "plan_digest",
                "narration_mode=text", "script", "run_id",
            },
            route[4],
        )
        self.assertIn("no `run_id`", cells[2])
        self.assertIn("no `run_id`", cells[4])
        self.assertIn("Before either text or audio narration", workflow)
        self.assertIn("same client run identifier", workflow)

    def test_digital_human_audio_run_has_complete_field_routing(self):
        workflow, cells, route = self._digital_human_route("audio")
        self.assertEqual({"audio"}, route[0])
        self.assertEqual({"dh-run-*", "--run-id"}, route[1])
        self.assertEqual(
            {"narration_mode=audio", "audio_upload_id", "run_id"}, route[2]
        )
        self.assertEqual(
            {"run_id", "plan_digest", "narration_mode=audio", "audio_upload_id"},
            route[3],
        )
        self.assertEqual(
            {
                "request_id", "consent_token", "plan_digest",
                "narration_mode=audio", "audio_upload_id", "run_id",
            },
            route[4],
        )
        self.assertIn("no `run_id`", cells[2])
        self.assertIn("no `run_id`", cells[4])
        for phrase in (
            "digital-human-oneclick-audio-upload",
            "quote_token",
            "digital-human-oneclick-status",
            "digital-human-oneclick-recover",
            "refund_pending",
            "never recreate completed or still-running children",
            "never infer consent",
        ):
            self.assertIn(phrase, workflow)


if __name__ == "__main__":
    unittest.main()
