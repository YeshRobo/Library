"""Types for the Source Artifact Agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from library_agents.common.workflows import WorkflowDefinition


@dataclass(frozen=True)
class SourceArtifactRequest:
    repo_root: Path
    source_path: str
    dry_run: bool = True
    overwrite: bool = False
    provider_name: str = "mock"


@dataclass(frozen=True)
class SourceObservation:
    repo_root: Path
    workflow: WorkflowDefinition
    source_path: str
    source_text: str
    source_sha256: str
    prompt_text: str
    existing_artifact_paths: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SourceArtifactOutcome:
    status: str
    run_id: str
    dry_run: bool
    read_paths: list[str]
    draft_paths: list[str]
    run_record_path: str | None
    payload: dict[str, Any]
    usage: dict[str, int] | None = None


class SourceArtifactAgentError(ValueError):
    """Raised when the Source Artifact Agent cannot complete a request."""


class CandidateValidationError(SourceArtifactAgentError):
    """Raised when a provider returns an invalid source artifact payload."""


class ActionError(SourceArtifactAgentError):
    """Raised when a draft artifact cannot be written safely."""
