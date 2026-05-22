"""Run record helpers for Library agents."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from library_agents.common.path_policy import ensure_under_allowed_roots, repo_relative_path, resolve_repo_path


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def make_run_id(workflow_id: str, slug: str, started_at: datetime) -> str:
    stamp = started_at.astimezone(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{workflow_id}_{stamp}_{slug}"


def write_run_record(repo_root: Path | str, run_root: str, workflow_id: str, record: dict[str, Any]) -> str:
    run_id = str(record.get("run_id", "")).strip()
    if not run_id:
        raise ValueError("run record requires run_id")
    relative_path = f"{run_root.rstrip('/')}/{workflow_id}/{run_id}.yaml"
    ensure_under_allowed_roots(relative_path, [run_root], "run record path")
    path = resolve_repo_path(repo_root, relative_path, "run record path")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    return repo_relative_path(repo_root, path)
