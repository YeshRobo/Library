"""Perception step for the Source Artifact Agent."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from library_agents.common.path_policy import ensure_under_allowed_roots, repo_relative_path, resolve_repo_path
from library_agents.common.workflows import WorkflowDefinition
from library_agents.source_artifact_agent.common.types import SourceArtifactAgentError, SourceObservation
from library_agents.source_artifact_agent.mind import source_slug_from_path


def observe_source(repo_root: Path, workflow: WorkflowDefinition, source_path: str) -> SourceObservation:
    source = resolve_repo_path(repo_root, source_path, "source_path")
    source_rel = repo_relative_path(repo_root, source)
    ensure_under_allowed_roots(source_rel, workflow.allowed_read_roots, "source_path")
    if source_rel == workflow.draft_root or source_rel.startswith(f"{workflow.draft_root.rstrip('/')}/"):
        raise SourceArtifactAgentError("source_path must be a source file, not an existing source artifact")
    if not source.is_file():
        raise SourceArtifactAgentError(f"source_path does not exist or is not a file: {source_path}")

    prompt = resolve_repo_path(repo_root, workflow.prompt_path, "prompt_path")
    source_text = source.read_text(encoding="utf-8")
    artifact_dir = resolve_repo_path(repo_root, f"{workflow.draft_root}/{source_slug_from_path(source_rel)}", "draft root")
    existing_artifact_paths = []
    if artifact_dir.is_dir():
        existing_artifact_paths = [
            repo_relative_path(repo_root, path)
            for path in sorted(artifact_dir.iterdir())
            if path.is_file()
        ]

    return SourceObservation(
        repo_root=repo_root,
        workflow=workflow,
        source_path=source_rel,
        source_text=source_text,
        source_sha256=sha256(source.read_bytes()).hexdigest(),
        prompt_text=prompt.read_text(encoding="utf-8"),
        existing_artifact_paths=existing_artifact_paths,
    )
