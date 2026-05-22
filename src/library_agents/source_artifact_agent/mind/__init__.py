"""Mind step for the Source Artifact Agent."""

from __future__ import annotations

from pathlib import PurePosixPath
import re
from typing import Any

from library_agents.common.providers import PromptPacket, ProviderResponse, SourceArtifactProvider
from library_agents.source_artifact_agent.common.types import CandidateValidationError, SourceObservation


SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*")


def source_slug_from_path(source_path: str) -> str:
    stem = PurePosixPath(source_path).stem.lower()
    slug = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug or "source"


def build_prompt_packet(observation: SourceObservation) -> PromptPacket:
    return PromptPacket(
        workflow_id=observation.workflow.workflow_id,
        source_path=observation.source_path,
        source_slug=source_slug_from_path(observation.source_path),
        source_sha256=observation.source_sha256,
        source_text=observation.source_text,
        prompt_text=observation.prompt_text,
        existing_artifact_paths=observation.existing_artifact_paths,
    )


def generate_candidate(observation: SourceObservation, provider: SourceArtifactProvider) -> ProviderResponse:
    packet = build_prompt_packet(observation)
    return provider.generate_source_artifact(packet)


def validate_payload(payload: dict[str, Any], *, source_path: str, source_sha256: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise CandidateValidationError("candidate payload must be a mapping")

    source_slug = source_slug_from_path(source_path)
    source_card = _required_mapping(payload.get("source_card"), "source_card")
    _require_equal(source_card.get("source_slug"), source_slug, "source_card.source_slug")
    _require_equal(source_card.get("source_path"), source_path, "source_card.source_path")
    _require_equal(source_card.get("source_sha256"), source_sha256, "source_card.source_sha256")
    _required_string(source_card.get("source_title"), "source_card.source_title")
    _required_string(source_card.get("source_type"), "source_card.source_type")
    _require_equal(source_card.get("artifact_status"), "draft", "source_card.artifact_status")
    if not SLUG_PATTERN.fullmatch(str(source_card.get("source_slug"))):
        raise CandidateValidationError("source_card.source_slug must be lowercase snake_case")

    source_summary = _required_mapping(payload.get("source_summary"), "source_summary")
    _required_string(source_summary.get("title"), "source_summary.title")
    _required_string(source_summary.get("summary"), "source_summary.summary")
    _string_list(source_summary.get("notable_points"), "source_summary.notable_points", min_items=1)

    evidence_ledger = _required_mapping(payload.get("evidence_ledger"), "evidence_ledger")
    _require_equal(evidence_ledger.get("source_path"), source_path, "evidence_ledger.source_path")
    _require_equal(evidence_ledger.get("source_sha256"), source_sha256, "evidence_ledger.source_sha256")
    excerpts = evidence_ledger.get("excerpts")
    if not isinstance(excerpts, list):
        raise CandidateValidationError("evidence_ledger.excerpts must be a list")
    for index, excerpt in enumerate(excerpts):
        if not isinstance(excerpt, dict):
            raise CandidateValidationError(f"evidence_ledger.excerpts[{index}] must be a mapping")
        if not isinstance(excerpt.get("line"), int) or excerpt["line"] < 1:
            raise CandidateValidationError(f"evidence_ledger.excerpts[{index}].line must be a positive integer")
        _required_string(excerpt.get("text"), f"evidence_ledger.excerpts[{index}].text")

    _string_list(payload.get("questions"), "questions", min_items=1)
    _string_list(payload.get("candidate_tags"), "candidate_tags", min_items=1)
    return payload


def _required_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CandidateValidationError(f"{label} must be a mapping")
    return value


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateValidationError(f"{label} must be a non-empty string")
    return value.strip()


def _string_list(value: Any, label: str, min_items: int) -> list[str]:
    if not isinstance(value, list) or len(value) < min_items:
        raise CandidateValidationError(f"{label} must be a list with at least {min_items} item(s)")
    values = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise CandidateValidationError(f"{label}[{index}] must be a non-empty string")
        values.append(item.strip())
    return values


def _require_equal(value: Any, expected: str, label: str) -> None:
    if value != expected:
        raise CandidateValidationError(f"{label} must be {expected!r}")
