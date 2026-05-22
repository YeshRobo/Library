"""Stable facade for the Source Artifact Agent."""

from __future__ import annotations

from library_agents.source_artifact_agent.cli import main
from library_agents.source_artifact_agent.orchestrator import run_source_artifact_agent

__all__ = ["main", "run_source_artifact_agent"]


if __name__ == "__main__":
    raise SystemExit(main())
