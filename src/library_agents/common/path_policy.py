"""Repository path safety helpers for Library agents."""

from __future__ import annotations

from pathlib import Path, PurePosixPath
import re


class PathPolicyError(ValueError):
    """Raised when a workflow path violates the repository path policy."""


def normalize_repo_relative_path(value: str, label: str = "path") -> PurePosixPath:
    if not isinstance(value, str) or not value.strip():
        raise PathPolicyError(f"{label} must be a non-empty repo-relative path")

    normalized = value.strip()
    if normalized.startswith("~") or re.match(r"^[A-Za-z]:", normalized):
        raise PathPolicyError(f"{label} must not be absolute: {value}")

    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts:
        raise PathPolicyError(f"{label} must stay inside the repository: {value}")
    return pure


def resolve_repo_path(repo_root: Path | str, value: str, label: str = "path") -> Path:
    root = Path(repo_root).resolve()
    pure = normalize_repo_relative_path(value, label)
    target = (root / Path(*pure.parts)).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PathPolicyError(f"{label} resolves outside the repository: {value}") from exc
    return target


def repo_relative_path(repo_root: Path | str, path: Path | str) -> str:
    root = Path(repo_root).resolve()
    target = Path(path).resolve()
    try:
        return target.relative_to(root).as_posix()
    except ValueError as exc:
        raise PathPolicyError(f"path is outside the repository: {path}") from exc


def ensure_under_allowed_roots(relative_path: str, allowed_roots: list[str], label: str = "path") -> None:
    pure = normalize_repo_relative_path(relative_path, label)
    if not allowed_roots:
        raise PathPolicyError(f"{label} has no allowed roots")

    for root_value in allowed_roots:
        allowed_root = normalize_repo_relative_path(root_value, "allowed root")
        if pure == allowed_root or pure.is_relative_to(allowed_root):
            return
    raise PathPolicyError(f"{label} is outside allowed roots: {relative_path}")


def ensure_extension(relative_path: str, allowed_extensions: list[str], label: str = "path") -> None:
    suffix = PurePosixPath(relative_path).suffix
    if suffix not in allowed_extensions:
        raise PathPolicyError(f"{label} extension must be one of {allowed_extensions}: {relative_path}")
