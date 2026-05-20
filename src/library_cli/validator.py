"""Validation logic for the v0 file-based Library model."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable

import yaml


VALID_SEED_STATUSES = {"discovered", "indexed", "mapped", "briefed", "booked"}
VALID_MAP_STATUSES = {"draft", "stable", "needs_work"}
VALID_STAGES = {"seeded", "indexed", "mapped", "briefed", "booked"}

REQUIRED_DIRECTORIES = (
    "library/sources",
    "library/sections/seeds",
    "library/sections/index",
    "library/sections/maps",
    "library/sections/briefs",
    "library/sections/books",
    "library/templates",
)

TEMPLATE_FILES = (
    "library/templates/section_seed_template.yaml",
    "library/templates/section_index_template.md",
    "library/templates/source_map_template.yaml",
    "library/templates/brief_template.md",
    "library/templates/book_template.md",
)

REQUIRED_MARKDOWN_HEADINGS = {
    "library/sections/index": ("## Section", "## Source Entries", "## Library Surfaces", "## Current Stage"),
    "library/sections/briefs": ("## Scope", "## Sources", "## Current Understanding", "## Constraints And Tensions", "## Next Use"),
    "library/sections/books": (
        "## Scope",
        "## Reading Map",
        "## Sources",
        "## Questions",
        "## Detailed Synthesis",
        "## Evidence And Traceability",
        "## Constraints And Tensions",
        "## Open Questions",
        "## Next Use",
    ),
}

PATH_PATTERN = re.compile(r"`([^`\n]+)`")


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str


@dataclass
class ValidationResult:
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(finding.level == "error" for finding in self.findings)

    def error(self, path: Path | str, message: str) -> None:
        self.findings.append(Finding("error", _display_path(path), message))


def validate_repository(repo_root: Path | str) -> ValidationResult:
    root = Path(repo_root).resolve()
    result = ValidationResult()

    if not root.exists():
        result.error(root, "repository root does not exist")
        return result

    for directory in REQUIRED_DIRECTORIES:
        if not (root / directory).is_dir():
            result.error(directory, "required directory is missing")

    for template in TEMPLATE_FILES:
        if not (root / template).is_file():
            result.error(template, "required template is missing")

    _validate_section_seeds(root, result)
    _validate_source_maps(root, result)
    _validate_markdown_sections(root, result)

    return result


def _validate_section_seeds(root: Path, result: ValidationResult) -> None:
    for path in sorted((root / "library/sections/seeds").glob("*.yaml")):
        data = _load_mapping(path, result)
        if data is None:
            continue

        slug = _require_slug(data, "section_slug", path, result)
        _require_non_empty_string(data, "section_title", path, result)
        _require_non_empty_string(data, "section_brief", path, result)
        status = _require_non_empty_string(data, "status", path, result)
        if status and status not in VALID_SEED_STATUSES:
            result.error(path, f"status must be one of {sorted(VALID_SEED_STATUSES)}")
        _require_list(data, "discovery_basis", path, result, min_items=1)
        _require_list(data, "questions", path, result, min_items=1)
        _require_list(data, "out_of_scope", path, result, min_items=1)
        _validate_supporting_files(data.get("candidate_supporting_files"), root, path, result)
        if slug and path.stem != slug:
            result.error(path, "file name must match section_slug")


def _validate_source_maps(root: Path, result: ValidationResult) -> None:
    for path in sorted((root / "library/sections/maps").glob("*.yaml")):
        data = _load_mapping(path, result)
        if data is None:
            continue

        slug = _require_slug(data, "section_slug", path, result)
        _require_non_empty_string(data, "section_title", path, result)
        status = _require_non_empty_string(data, "status", path, result)
        if status and status not in VALID_MAP_STATUSES:
            result.error(path, f"status must be one of {sorted(VALID_MAP_STATUSES)}")
        _validate_path_list(data.get("source_entries"), root, path, "source_entries", result)
        _validate_member_files(data.get("member_files"), root, path, result)
        _validate_path_list(data.get("library_surfaces"), root, path, "library_surfaces", result)
        if slug and path.stem != slug:
            result.error(path, "file name must match section_slug")


def _validate_markdown_sections(root: Path, result: ValidationResult) -> None:
    for directory, headings in REQUIRED_MARKDOWN_HEADINGS.items():
        for path in sorted((root / directory).glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if not text.startswith("# "):
                result.error(path, "markdown surface must start with a level-one heading")
            for heading in headings:
                if heading not in text:
                    result.error(path, f"missing required heading: {heading}")
            _validate_inline_paths(text, root, path, result)
            _validate_stage_values(text, path, result)


def _load_mapping(path: Path, result: ValidationResult) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        result.error(path, f"invalid YAML: {exc}")
        return None
    if not isinstance(data, dict):
        result.error(path, "expected a YAML mapping at file root")
        return None
    return data


def _require_non_empty_string(data: dict[str, Any], key: str, path: Path, result: ValidationResult) -> str | None:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        result.error(path, f"missing or invalid string field: {key}")
        return None
    return value


def _require_slug(data: dict[str, Any], key: str, path: Path, result: ValidationResult) -> str | None:
    value = _require_non_empty_string(data, key, path, result)
    if value and not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
        result.error(path, f"{key} must be lowercase snake_case")
    return value


def _require_list(data: dict[str, Any], key: str, path: Path, result: ValidationResult, min_items: int = 0) -> list[Any] | None:
    value = data.get(key)
    if not isinstance(value, list) or len(value) < min_items:
        result.error(path, f"missing or invalid list field: {key}")
        return None
    return value


def _validate_supporting_files(value: Any, root: Path, path: Path, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.error(path, "candidate_supporting_files must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            result.error(path, f"candidate_supporting_files[{index}] must be a mapping")
            continue
        candidate = item.get("path")
        reason = item.get("reason")
        _validate_existing_repo_path(candidate, root, path, f"candidate_supporting_files[{index}].path", result)
        if not isinstance(reason, str) or not reason.strip():
            result.error(path, f"candidate_supporting_files[{index}].reason must be a non-empty string")


def _validate_member_files(value: Any, root: Path, path: Path, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.error(path, "member_files must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            result.error(path, f"member_files[{index}] must be a mapping")
            continue
        _validate_existing_repo_path(item.get("path"), root, path, f"member_files[{index}].path", result)
        for key in ("role", "contribution"):
            value_for_key = item.get(key)
            if not isinstance(value_for_key, str) or not value_for_key.strip():
                result.error(path, f"member_files[{index}].{key} must be a non-empty string")


def _validate_path_list(value: Any, root: Path, path: Path, field: str, result: ValidationResult) -> None:
    if not isinstance(value, list) or not value:
        result.error(path, f"{field} must be a non-empty list")
        return
    for index, item in enumerate(value):
        _validate_existing_repo_path(item, root, path, f"{field}[{index}]", result)


def _validate_inline_paths(text: str, root: Path, path: Path, result: ValidationResult) -> None:
    for raw_value in PATH_PATTERN.findall(text):
        value = raw_value.strip()
        if not _looks_like_repo_path(value):
            continue
        _validate_existing_repo_path(value, root, path, "inline path", result)


def _validate_stage_values(text: str, path: Path, result: ValidationResult) -> None:
    if "## Current Stage" not in text:
        return
    stages = [stage for stage in VALID_STAGES if f"`{stage}`" in text]
    if not stages:
        result.error(path, f"current stage must include one of {sorted(VALID_STAGES)}")


def _validate_existing_repo_path(value: Any, root: Path, path: Path, field: str, result: ValidationResult) -> None:
    target = _resolve_safe_repo_path(value, root, path, field, result)
    if target is None:
        return
    if not target.exists():
        result.error(path, f"{field} references missing path: {value}")


def _resolve_safe_repo_path(value: Any, root: Path, path: Path, field: str, result: ValidationResult) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        result.error(path, f"{field} must be a non-empty repo-relative path")
        return None

    normalized = value.strip()
    if normalized.startswith("~") or re.match(r"^[A-Za-z]:", normalized):
        result.error(path, f"{field} must not be absolute: {value}")
        return None

    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts:
        result.error(path, f"{field} must stay inside the repository: {value}")
        return None

    target = (root / Path(*pure.parts)).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        result.error(path, f"{field} resolves outside the repository: {value}")
        return None
    return target


def _looks_like_repo_path(value: str) -> bool:
    if value.startswith(("http://", "https://", "mailto:")):
        return False
    if value in VALID_STAGES:
        return False
    return "/" in value and any(value.endswith(suffix) for suffix in (".md", ".yaml", ".yml", ".json", ".txt"))


def _display_path(path: Path | str) -> str:
    if isinstance(path, Path):
        return path.as_posix()
    return path


def summarize_findings(findings: Iterable[Finding]) -> str:
    return "\n".join(f"{finding.level}: {finding.path}: {finding.message}" for finding in findings)
