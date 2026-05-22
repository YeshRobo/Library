from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from library_cli.validator import summarize_findings, validate_repository  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def test_current_repository_example_is_valid(self) -> None:
        result = validate_repository(ROOT)
        self.assertTrue(result.ok, summarize_findings(result.findings))

    def test_missing_required_seed_field_fails(self) -> None:
        with copied_repo() as repo:
            seed_path = repo / "library/knowledge/03_seeds/project_release_notes.yaml"
            data = yaml.safe_load(seed_path.read_text(encoding="utf-8"))
            data.pop("target_title")
            seed_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            result = validate_repository(repo)

        self.assertFalse(result.ok)
        self.assertIn("target_title", summarize_findings(result.findings))

    def test_missing_referenced_file_fails(self) -> None:
        with copied_repo() as repo:
            source_path = repo / "library/knowledge/01_sources/project_release_notes_source.md"
            source_path.unlink()

            result = validate_repository(repo)

        self.assertFalse(result.ok)
        self.assertIn("references missing path", summarize_findings(result.findings))

    def test_path_traversal_fails(self) -> None:
        with copied_repo() as repo:
            map_path = repo / "library/knowledge/05_maps/project_release_notes.yaml"
            data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
            data["source_entries"] = ["../secret.md"]
            map_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            result = validate_repository(repo)

        self.assertFalse(result.ok)
        self.assertIn("must stay inside the repository", summarize_findings(result.findings))


class copied_repo:
    def __enter__(self) -> Path:
        self._tempdir = tempfile.TemporaryDirectory()
        destination = Path(self._tempdir.name) / "Library"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "*.egg-info"),
        )
        return destination

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._tempdir.cleanup()


if __name__ == "__main__":
    unittest.main()
