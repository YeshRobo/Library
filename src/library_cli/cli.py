"""Command line interface for Library validation and draft-only agents."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from library_cli.validator import validate_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="library-cli",
        description="Validate a file-based Library knowledge repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a Library repository")
    validate_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository root to validate (default: current directory)",
    )

    source_artifact_parser = subparsers.add_parser(
        "source-artifact",
        help="create draft source artifacts from a source file",
    )
    source_artifact_parser.add_argument("source_path", help="repo-relative source file path under library/knowledge/01_sources")
    source_artifact_parser.add_argument("--repo-root", default=".", help="repository root (default: current directory)")
    source_artifact_parser.add_argument("--write", action="store_true", help="write draft artifacts and a run record")
    source_artifact_parser.add_argument("--overwrite", action="store_true", help="replace an existing draft artifact set")
    source_artifact_parser.add_argument("--provider", default="mock", help="provider name (default: mock)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        result = validate_repository(Path(args.path))
        if result.ok:
            print("Library validation passed.")
            return 0

        for finding in result.findings:
            print(f"{finding.level}: {finding.path}: {finding.message}")
        return 1

    if args.command == "source-artifact":
        from library_agents.source_artifact_agent.cli import run as run_source_artifact_cli

        return run_source_artifact_cli(args)

    parser.error(f"unknown command: {args.command}")
    return 2
