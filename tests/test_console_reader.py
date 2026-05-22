from __future__ import annotations

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from library_console.repository import ConsoleRepositoryError, LibraryRepository  # noqa: E402


class ConsoleReaderTests(unittest.TestCase):
    def test_summary_counts_library_surfaces(self) -> None:
        repository = LibraryRepository(ROOT)

        summary = repository.summary()

        self.assertEqual(summary["targetCount"], 1)
        self.assertEqual(summary["sourceCount"], 1)
        self.assertEqual(summary["bookCount"], 1)
        self.assertTrue(summary["validation"]["ok"])

    def test_target_detail_includes_book_surface(self) -> None:
        repository = LibraryRepository(ROOT)

        detail = repository.target_detail("project_release_notes")

        surface_kinds = [surface["kind"] for surface in detail["surfaces"]]
        self.assertIn("book", surface_kinds)
        book_surface = next(surface for surface in detail["surfaces"] if surface["kind"] == "book")
        self.assertTrue(book_surface["exists"])
        self.assertIn("# Book: Project Release Notes", book_surface["content"])

    def test_missing_target_raises_key_error(self) -> None:
        repository = LibraryRepository(ROOT)

        with self.assertRaises(KeyError):
            repository.target_detail("missing_target")

    def test_unsafe_source_path_is_rejected(self) -> None:
        with copied_repo() as repo:
            map_path = repo / "library/knowledge/05_maps/project_release_notes.yaml"
            data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
            data["source_entries"] = ["../secret.md"]
            map_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            repository = LibraryRepository(repo)

            with self.assertRaises(ConsoleRepositoryError):
                repository.target_detail("project_release_notes")

    def test_malformed_yaml_is_reported_by_validation(self) -> None:
        with copied_repo() as repo:
            map_path = repo / "library/knowledge/05_maps/project_release_notes.yaml"
            map_path.write_text(":\n", encoding="utf-8")

            repository = LibraryRepository(repo)
            targets = repository.list_targets()
            validation = repository.validation_status()

        self.assertEqual(len(targets), 1)
        self.assertFalse(validation["ok"])
        self.assertIn("invalid YAML", "\n".join(finding["message"] for finding in validation["findings"]))


class copied_repo:
    def __enter__(self) -> Path:
        self._tempdir = tempfile.TemporaryDirectory()
        destination = Path(self._tempdir.name) / "Library"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "*.egg-info", "node_modules", "dist"),
        )
        return destination

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self._tempdir.cleanup()


if __name__ == "__main__":
    unittest.main()
