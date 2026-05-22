from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from library_agents.common.providers import ProviderResponse  # noqa: E402
from library_agents.common.workflows import load_workflow  # noqa: E402
from library_agents.source_artifact_agent.common.types import (  # noqa: E402
    CandidateValidationError,
    SourceArtifactRequest,
)
from library_agents.source_artifact_agent.orchestrator import run_source_artifact_agent  # noqa: E402
from library_cli.cli import main as cli_main  # noqa: E402


class SourceArtifactAgentTests(unittest.TestCase):
    def test_workflow_catalog_loads(self) -> None:
        workflow = load_workflow(ROOT, "source_artifact")

        self.assertEqual(workflow.workflow_id, "source_artifact")
        self.assertEqual(workflow.default_provider, "mock")
        self.assertIn("library/knowledge/01_sources", workflow.allowed_read_roots)
        self.assertIn("library/knowledge/02_artifacts", workflow.allowed_read_roots)

    def test_dry_run_plans_artifacts_without_writing(self) -> None:
        with copied_repo() as repo:
            request = SourceArtifactRequest(
                repo_root=repo,
                source_path="library/knowledge/01_sources/project_release_notes_source.md",
                dry_run=True,
            )

            outcome = run_source_artifact_agent(request)

            self.assertEqual(outcome.status, "dry_run")
            self.assertIsNone(outcome.run_record_path)
            self.assertIn("library/knowledge/01_sources/project_release_notes_source.md", outcome.read_paths)
            self.assertTrue(any(path.endswith("source_card.yaml") for path in outcome.draft_paths))
            self.assertFalse((repo / "library/knowledge/02_artifacts/project_release_notes_source/source_card.yaml").exists())

    def test_write_creates_drafts_and_run_record(self) -> None:
        with copied_repo() as repo:
            accepted_book = repo / "library/knowledge/07_books/project_release_notes.md"
            before = accepted_book.read_text(encoding="utf-8")
            request = SourceArtifactRequest(
                repo_root=repo,
                source_path="library/knowledge/01_sources/project_release_notes_source.md",
                dry_run=False,
            )

            outcome = run_source_artifact_agent(request)

            artifact_root = repo / "library/knowledge/02_artifacts/project_release_notes_source"
            self.assertEqual(outcome.status, "completed")
            self.assertTrue((artifact_root / "source_card.yaml").is_file())
            self.assertTrue((artifact_root / "source_summary.md").is_file())
            self.assertTrue((artifact_root / "evidence_ledger.yaml").is_file())
            self.assertTrue((artifact_root / "artifact_manifest.yaml").is_file())
            self.assertIsNotNone(outcome.run_record_path)
            self.assertTrue((repo / outcome.run_record_path).is_file())
            self.assertEqual(accepted_book.read_text(encoding="utf-8"), before)

            run_record = yaml.safe_load((repo / outcome.run_record_path).read_text(encoding="utf-8"))
            self.assertEqual(run_record["workflow_id"], "source_artifact")
            self.assertFalse(run_record["human_approval"]["approved"])
            self.assertIn("library/knowledge/01_sources/project_release_notes_source.md", run_record["read_paths"])
            self.assertTrue(any(path.endswith("source_card.yaml") for path in run_record["draft_paths"]))

    def test_path_traversal_is_rejected(self) -> None:
        with copied_repo() as repo:
            request = SourceArtifactRequest(repo_root=repo, source_path="../secret.md")

            with self.assertRaises(ValueError):
                run_source_artifact_agent(request)

    def test_artifact_path_cannot_be_used_as_source_input(self) -> None:
        with copied_repo() as repo:
            artifact_dir = repo / "library/knowledge/02_artifacts/project_release_notes_source"
            artifact_dir.mkdir(parents=True)
            artifact_path = artifact_dir / "source_card.yaml"
            artifact_path.write_text("source_slug: project_release_notes_source\n", encoding="utf-8")
            request = SourceArtifactRequest(
                repo_root=repo,
                source_path="library/knowledge/02_artifacts/project_release_notes_source/source_card.yaml",
            )

            with self.assertRaises(ValueError):
                run_source_artifact_agent(request)

    def test_malformed_provider_payload_is_rejected_before_write(self) -> None:
        with copied_repo() as repo:
            request = SourceArtifactRequest(
                repo_root=repo,
                source_path="library/knowledge/01_sources/project_release_notes_source.md",
                dry_run=False,
            )

            with self.assertRaises(CandidateValidationError):
                run_source_artifact_agent(request, provider=BrokenProvider())

            artifact_root = repo / "library/knowledge/02_artifacts/project_release_notes_source"
            self.assertFalse((artifact_root / "source_card.yaml").exists())

    def test_cli_source_artifact_dry_run(self) -> None:
        with copied_repo() as repo:
            with redirect_stdout(io.StringIO()):
                exit_code = cli_main(
                    [
                        "source-artifact",
                        "library/knowledge/01_sources/project_release_notes_source.md",
                        "--repo-root",
                        str(repo),
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertFalse((repo / "library/knowledge/02_artifacts/project_release_notes_source/source_card.yaml").exists())


class BrokenProvider:
    name = "broken"
    model = "broken-local"

    def generate_source_artifact(self, packet: object) -> ProviderResponse:
        return ProviderResponse(payload={"source_card": {}}, usage=None)


class copied_repo:
    def __enter__(self) -> Path:
        self._tempdir = tempfile.TemporaryDirectory()
        destination = Path(self._tempdir.name) / "Library"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(
                ".git",
                "__pycache__",
                ".venv",
                "*.egg-info",
                "node_modules",
                "dist",
                "runs",
            ),
        )
        return destination

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._tempdir.cleanup()


if __name__ == "__main__":
    unittest.main()
