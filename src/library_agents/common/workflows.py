"""Workflow catalog loading and validation for Library agents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from library_agents.common.path_policy import PathPolicyError, resolve_repo_path


class WorkflowCatalogError(ValueError):
    """Raised when a workflow catalog entry is missing or invalid."""


@dataclass(frozen=True)
class WorkflowDefinition:
    workflow_id: str
    name: str
    agent_module: str
    mode: str
    prompt_path: str
    inputs: list[dict[str, Any]]
    read_policy: dict[str, Any]
    write_policy: dict[str, Any]
    run_record: dict[str, Any]
    provider: dict[str, Any]
    expected_output: dict[str, Any]

    @property
    def allowed_read_roots(self) -> list[str]:
        return _string_list(self.read_policy.get("allowed_roots"), "read_policy.allowed_roots")

    @property
    def draft_root(self) -> str:
        return _required_string(self.write_policy.get("draft_root"), "write_policy.draft_root")

    @property
    def allowed_extensions(self) -> list[str]:
        return _string_list(self.write_policy.get("allowed_extensions"), "write_policy.allowed_extensions")

    @property
    def run_record_root(self) -> str:
        return _required_string(self.run_record.get("root"), "run_record.root")

    @property
    def default_provider(self) -> str:
        return _required_string(self.provider.get("default"), "provider.default")


def load_workflow(repo_root: Path | str, workflow_id: str) -> WorkflowDefinition:
    path = Path(repo_root).resolve() / "catalog" / "workflows" / f"{workflow_id}.yaml"
    if not path.is_file():
        raise WorkflowCatalogError(f"workflow is missing: {workflow_id}")

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise WorkflowCatalogError(f"invalid workflow YAML: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise WorkflowCatalogError(f"workflow must be a YAML mapping: {path}")

    workflow = WorkflowDefinition(
        workflow_id=_required_string(data.get("workflow_id"), "workflow_id"),
        name=_required_string(data.get("name"), "name"),
        agent_module=_required_string(data.get("agent_module"), "agent_module"),
        mode=_required_string(data.get("mode"), "mode"),
        prompt_path=_required_string(data.get("prompt_path"), "prompt_path"),
        inputs=_required_list(data.get("inputs"), "inputs"),
        read_policy=_required_mapping(data.get("read_policy"), "read_policy"),
        write_policy=_required_mapping(data.get("write_policy"), "write_policy"),
        run_record=_required_mapping(data.get("run_record"), "run_record"),
        provider=_required_mapping(data.get("provider"), "provider"),
        expected_output=_required_mapping(data.get("expected_output"), "expected_output"),
    )
    validate_workflow(repo_root, workflow)
    return workflow


def validate_workflow(repo_root: Path | str, workflow: WorkflowDefinition) -> None:
    if workflow.mode not in {"draft_only", "read_only"}:
        raise WorkflowCatalogError(f"unsupported workflow mode: {workflow.mode}")
    if workflow.workflow_id != Path(workflow.prompt_path).stem:
        raise WorkflowCatalogError("workflow_id must match prompt file stem")

    for root_value in workflow.allowed_read_roots:
        _resolve_policy_path(repo_root, root_value, "read root")
    _resolve_policy_path(repo_root, workflow.draft_root, "draft root")
    _resolve_policy_path(repo_root, workflow.run_record_root, "run record root")

    prompt = _resolve_policy_path(repo_root, workflow.prompt_path, "prompt path")
    if not prompt.is_file():
        raise WorkflowCatalogError(f"prompt file is missing: {workflow.prompt_path}")

    if not workflow.allowed_extensions:
        raise WorkflowCatalogError("write_policy.allowed_extensions must not be empty")
    for extension in workflow.allowed_extensions:
        if not extension.startswith("."):
            raise WorkflowCatalogError(f"allowed extension must start with '.': {extension}")


def _resolve_policy_path(repo_root: Path | str, value: str, label: str) -> Path:
    try:
        return resolve_repo_path(repo_root, value, label)
    except PathPolicyError as exc:
        raise WorkflowCatalogError(str(exc)) from exc


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkflowCatalogError(f"missing or invalid string field: {label}")
    return value.strip()


def _required_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WorkflowCatalogError(f"missing or invalid mapping field: {label}")
    return value


def _required_list(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise WorkflowCatalogError(f"missing or invalid list field: {label}")
    if not all(isinstance(item, dict) for item in value):
        raise WorkflowCatalogError(f"{label} entries must be mappings")
    return value


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise WorkflowCatalogError(f"missing or invalid list field: {label}")
    values = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    if len(values) != len(value):
        raise WorkflowCatalogError(f"{label} entries must be non-empty strings")
    return values
