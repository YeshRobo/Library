"""Orchestration for the Source Artifact Agent."""

from __future__ import annotations

from pathlib import Path

from library_agents.common.providers import SourceArtifactProvider, get_source_artifact_provider
from library_agents.common.run_records import format_timestamp, make_run_id, utc_now, write_run_record
from library_agents.common.workflows import load_workflow
from library_agents.source_artifact_agent import action, perception
from library_agents.source_artifact_agent.common.types import SourceArtifactOutcome, SourceArtifactRequest
from library_agents.source_artifact_agent.mind import generate_candidate, source_slug_from_path, validate_payload


def run_source_artifact_agent(
    request: SourceArtifactRequest,
    provider: SourceArtifactProvider | None = None,
) -> SourceArtifactOutcome:
    repo_root = Path(request.repo_root).resolve()
    workflow = load_workflow(repo_root, "source_artifact")
    active_provider = provider or get_source_artifact_provider(request.provider_name or workflow.default_provider)
    observation = perception.observe_source(repo_root, workflow, request.source_path)
    response = generate_candidate(observation, active_provider)
    payload = validate_payload(
        response.payload,
        source_path=observation.source_path,
        source_sha256=observation.source_sha256,
    )
    source_slug = source_slug_from_path(observation.source_path)
    started_at = utc_now()
    run_id = make_run_id(workflow.workflow_id, source_slug, started_at)
    planned_paths = action.planned_artifact_paths(workflow, source_slug)
    read_paths = [observation.source_path, workflow.prompt_path, *observation.existing_artifact_paths]

    if request.dry_run:
        return SourceArtifactOutcome(
            status="dry_run",
            run_id=run_id,
            dry_run=True,
            read_paths=dedupe(read_paths),
            draft_paths=planned_paths,
            run_record_path=None,
            payload=payload,
            usage=response.usage,
        )

    draft_paths = action.write_artifacts(
        repo_root,
        workflow,
        source_slug,
        payload,
        run_id=run_id,
        provider=active_provider.name,
        model=active_provider.model,
        overwrite=request.overwrite,
    )
    finished_at = utc_now()
    record = {
        "run_id": run_id,
        "workflow_id": workflow.workflow_id,
        "agent_name": workflow.name,
        "provider": active_provider.name,
        "model": active_provider.model,
        "status": "completed",
        "started_at": format_timestamp(started_at),
        "finished_at": format_timestamp(finished_at),
        "read_paths": dedupe(read_paths),
        "draft_paths": draft_paths,
        "validation": {"ok": True, "findings": []},
        "human_approval": {"required": True, "approved": False},
        "usage": response.usage or {},
    }
    run_record_path = write_run_record(repo_root, workflow.run_record_root, workflow.workflow_id, record)
    return SourceArtifactOutcome(
        status="completed",
        run_id=run_id,
        dry_run=False,
        read_paths=dedupe(read_paths),
        draft_paths=draft_paths,
        run_record_path=run_record_path,
        payload=payload,
        usage=response.usage,
    )


def dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
    return deduped
