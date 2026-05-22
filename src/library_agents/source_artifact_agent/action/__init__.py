"""Action step for the Source Artifact Agent."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from library_agents.common.path_policy import ensure_extension, ensure_under_allowed_roots, resolve_repo_path
from library_agents.common.workflows import WorkflowDefinition
from library_agents.source_artifact_agent.common.types import ActionError


ARTIFACT_FILES = (
    "source_card.yaml",
    "source_summary.md",
    "evidence_ledger.yaml",
    "questions.md",
    "candidate_tags.yaml",
    "artifact_manifest.yaml",
)


def planned_artifact_paths(workflow: WorkflowDefinition, source_slug: str) -> list[str]:
    return [f"{workflow.draft_root.rstrip('/')}/{source_slug}/{file_name}" for file_name in ARTIFACT_FILES]


def write_artifacts(
    repo_root: Path,
    workflow: WorkflowDefinition,
    source_slug: str,
    payload: dict[str, Any],
    *,
    run_id: str,
    provider: str,
    model: str,
    overwrite: bool,
) -> list[str]:
    relative_paths = planned_artifact_paths(workflow, source_slug)
    for relative_path in relative_paths:
        ensure_under_allowed_roots(relative_path, [workflow.draft_root], "draft path")
        ensure_extension(relative_path, workflow.allowed_extensions, "draft path")

    paths = [resolve_repo_path(repo_root, relative_path, "draft path") for relative_path in relative_paths]
    existing = [path for path in paths if path.exists()]
    if existing and not overwrite:
        existing_rel = ", ".join(path.relative_to(repo_root).as_posix() for path in existing)
        raise ActionError(f"draft artifact already exists; use --overwrite to replace: {existing_rel}")

    manifest = {
        "artifact_status": "draft",
        "run_id": run_id,
        "provider": provider,
        "model": model,
        "source_path": payload["source_card"]["source_path"],
        "source_sha256": payload["source_card"]["source_sha256"],
        "artifact_files": relative_paths[:-1],
        "human_approval": {"required": True, "approved": False},
    }

    rendered = {
        "source_card.yaml": yaml.safe_dump(payload["source_card"], sort_keys=False),
        "source_summary.md": _render_source_summary(payload["source_summary"]),
        "evidence_ledger.yaml": yaml.safe_dump(payload["evidence_ledger"], sort_keys=False),
        "questions.md": _render_list_markdown("Questions", payload["questions"]),
        "candidate_tags.yaml": yaml.safe_dump({"candidate_tags": payload["candidate_tags"]}, sort_keys=False),
        "artifact_manifest.yaml": yaml.safe_dump(manifest, sort_keys=False),
    }

    for path, file_name in zip(paths, ARTIFACT_FILES):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered[file_name], encoding="utf-8")
    return relative_paths


def _render_source_summary(summary: dict[str, Any]) -> str:
    points = "\n".join(f"- {point}" for point in summary["notable_points"])
    return f"# Source Summary: {summary['title']}\n\n## Summary\n\n{summary['summary']}\n\n## Notable Points\n\n{points}\n"


def _render_list_markdown(title: str, values: list[str]) -> str:
    items = "\n".join(f"- {value}" for value in values)
    return f"# {title}\n\n{items}\n"
