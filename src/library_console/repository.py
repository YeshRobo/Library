"""Read-only repository reader for the Library console."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path, PurePosixPath
import re
from typing import Any

import yaml

from library_cli.validator import VALID_STAGES, validate_repository


class ConsoleRepositoryError(ValueError):
    """Raised when the console reader cannot safely satisfy a read."""


class LibraryRepository:
    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

    def health(self) -> dict[str, str]:
        return {"status": "ok", "service": "library_console"}

    def validation_status(self) -> dict[str, Any]:
        result = validate_repository(self.root)
        return {
            "ok": result.ok,
            "findings": [asdict(finding) for finding in result.findings],
        }

    def summary(self) -> dict[str, Any]:
        targets = self.list_targets()
        validation = self.validation_status()
        source_paths = {source for target in targets for source in target["sourceEntries"]}
        return {
            "targetCount": len(targets),
            "sourceCount": len(source_paths),
            "bookCount": sum(1 for target in targets if target["paths"].get("book")),
            "validation": {
                "ok": validation["ok"],
                "findingCount": len(validation["findings"]),
            },
        }

    def list_targets(self) -> list[dict[str, Any]]:
        seed_dir = self.root / "library/knowledge/03_seeds"
        targets: list[dict[str, Any]] = []
        for seed_path in sorted(seed_dir.glob("*.yaml")):
            seed_data = self._load_yaml_mapping(seed_path)
            slug = _string_value(seed_data.get("target_slug"), seed_path.stem)
            target_paths = self._target_paths(slug, seed_path)
            map_data = self._load_yaml_mapping(self.root / target_paths["map"])
            target_text = self._read_optional_text(target_paths["target"])
            source_entries = _string_list(map_data.get("source_entries"))
            if not source_entries:
                source_entries = _supporting_file_paths(seed_data.get("supporting_artifacts"))
            evidence_entries = [*source_entries, *_string_list(map_data.get("artifact_entries"))]

            targets.append(
                {
                    "slug": slug,
                    "title": _string_value(seed_data.get("target_title"), _title_from_slug(slug)),
                    "purpose": _string_value(seed_data.get("target_purpose"), ""),
                    "brief": _string_value(seed_data.get("target_purpose"), ""),
                    "status": _string_value(seed_data.get("status"), "unknown"),
                    "stage": _stage_from_markdown(target_text),
                    "sourceEntries": source_entries,
                    "evidenceEntries": evidence_entries,
                    "paths": {key: value for key, value in target_paths.items() if self._path_exists(value)},
                }
            )

        return sorted(targets, key=lambda target: target["title"].lower())

    def target_detail(self, slug: str) -> dict[str, Any]:
        target = self._find_target(slug)
        target_paths = self._target_paths(slug, self.root / f"library/knowledge/03_seeds/{slug}.yaml")
        seed_data = self._load_yaml_mapping(self.root / target_paths["seed"])
        map_data = self._load_yaml_mapping(self.root / target_paths["map"])
        source_entries = _string_list(map_data.get("source_entries")) or target["sourceEntries"]
        member_files = map_data.get("member_files") if isinstance(map_data.get("member_files"), list) else []

        surfaces = [self._surface("source", _surface_label(path), path) for path in source_entries]
        surfaces.extend(
            [
                self._surface("target", "Target Index", target_paths["target"]),
                self._surface("map", "Map", target_paths["map"]),
                self._surface("brief", "Brief", target_paths["brief"]),
                self._surface("book", "Book", target_paths["book"]),
            ]
        )

        return {
            **target,
            "seed": seed_data,
            "map": map_data,
            "memberFiles": member_files,
            "surfaces": surfaces,
        }

    def _find_target(self, slug: str) -> dict[str, Any]:
        for target in self.list_targets():
            if target["slug"] == slug:
                return target
        raise KeyError(slug)

    def _target_paths(self, slug: str, seed_path: Path) -> dict[str, str]:
        return {
            "seed": self._relative_path(seed_path),
            "target": f"library/knowledge/04_targets/{slug}.md",
            "map": f"library/knowledge/05_maps/{slug}.yaml",
            "brief": f"library/knowledge/06_briefs/{slug}.md",
            "book": f"library/knowledge/07_books/{slug}.md",
        }

    def _surface(self, kind: str, label: str, relative_path: str) -> dict[str, Any]:
        path = self._resolve_repo_path(relative_path)
        exists = path.is_file()
        return {
            "kind": kind,
            "label": label,
            "path": relative_path,
            "exists": exists,
            "content": path.read_text(encoding="utf-8") if exists else "",
        }

    def _read_optional_text(self, relative_path: str) -> str:
        path = self._resolve_repo_path(relative_path)
        if not path.is_file():
            return ""
        return path.read_text(encoding="utf-8")

    def _path_exists(self, relative_path: str) -> bool:
        return self._resolve_repo_path(relative_path).exists()

    def _load_yaml_mapping(self, path: Path) -> dict[str, Any]:
        if not path.is_file():
            return {}
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            return {}
        return data if isinstance(data, dict) else {}

    def _relative_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError as exc:
            raise ConsoleRepositoryError(f"path is outside the repository: {path}") from exc

    def _resolve_repo_path(self, value: str) -> Path:
        if not isinstance(value, str) or not value.strip():
            raise ConsoleRepositoryError("repo path must be a non-empty string")

        normalized = value.strip()
        if normalized.startswith("~") or re.match(r"^[A-Za-z]:", normalized):
            raise ConsoleRepositoryError(f"repo path must not be absolute: {value}")

        pure = PurePosixPath(normalized)
        if pure.is_absolute() or ".." in pure.parts:
            raise ConsoleRepositoryError(f"repo path must stay inside the repository: {value}")

        target = (self.root / Path(*pure.parts)).resolve()
        try:
            target.relative_to(self.root)
        except ValueError as exc:
            raise ConsoleRepositoryError(f"repo path resolves outside the repository: {value}") from exc
        return target


def _string_value(value: Any, fallback: str) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else fallback


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _supporting_file_paths(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    paths: list[str] = []
    for item in value:
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            paths.append(item["path"].strip())
    return [path for path in paths if path]


def _stage_from_markdown(text: str) -> str:
    for stage in sorted(VALID_STAGES):
        if f"`{stage}`" in text:
            return stage
    return "unknown"


def _title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("_"))


def _surface_label(path: str) -> str:
    return Path(path).stem.replace("_", " ").title()
