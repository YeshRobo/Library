"""Command line interface for Library validation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from library_cli.validator import validate_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="section-library",
        description="Validate a file-based Library section-library repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate a Library repository")
    validate_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository root to validate (default: current directory)",
    )
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

    parser.error(f"unknown command: {args.command}")
    return 2
