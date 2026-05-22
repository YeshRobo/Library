"""CLI for the Source Artifact Agent."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from library_agents.source_artifact_agent.common.types import SourceArtifactAgentError, SourceArtifactRequest
from library_agents.source_artifact_agent.orchestrator import run_source_artifact_agent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="library-cli source-artifact",
        description="Create draft source artifacts from a Library source file.",
    )
    parser.add_argument("source_path", help="repo-relative source file path under library/knowledge/01_sources")
    parser.add_argument("--repo-root", default=".", help="repository root (default: current directory)")
    parser.add_argument("--write", action="store_true", help="write draft artifacts and a run record")
    parser.add_argument("--overwrite", action="store_true", help="replace an existing draft artifact set")
    parser.add_argument("--provider", default="mock", help="provider name (default: mock)")
    return parser


def run(args: argparse.Namespace) -> int:
    request = SourceArtifactRequest(
        repo_root=Path(args.repo_root),
        source_path=args.source_path,
        dry_run=not args.write,
        overwrite=args.overwrite,
        provider_name=args.provider,
    )
    try:
        outcome = run_source_artifact_agent(request)
    except (SourceArtifactAgentError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Workflow: Source Artifact Agent")
    print(f"Mode: {'dry-run' if outcome.dry_run else 'draft-only write'}")
    print("Reads:")
    for path in outcome.read_paths:
        print(f"  - {path}")
    print("Draft paths:")
    for path in outcome.draft_paths:
        print(f"  - {path}")
    if outcome.run_record_path:
        print(f"Run record: {outcome.run_record_path}")
    else:
        print("Run record: not written during dry-run")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    return run(parser.parse_args(argv))
