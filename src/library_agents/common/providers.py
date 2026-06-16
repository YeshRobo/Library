"""Provider interfaces and deterministic local providers for Library agents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Protocol


@dataclass(frozen=True)
class PromptPacket:
    workflow_id: str
    source_path: str
    source_slug: str
    source_sha256: str
    source_text: str
    prompt_text: str
    existing_artifact_paths: list[str]


@dataclass(frozen=True)
class ProviderResponse:
    payload: dict[str, Any]
    usage: dict[str, int] | None = None


class SourceArtifactProvider(Protocol):
    name: str
    model: str

    def generate_source_artifact(self, packet: PromptPacket) -> ProviderResponse:
        """Generate a candidate source artifact payload."""


class MockSourceArtifactProvider:
    name = "mock"
    model = "mock-local"

    def generate_source_artifact(self, packet: PromptPacket) -> ProviderResponse:
        lines = _source_lines(packet.source_text)
        title = _source_title(packet.source_path, lines)
        excerpt_entries = [
            {"line": line_number, "text": text[:320]}
            for line_number, text in lines[:8]
        ]
        questions = [text for _, text in lines if text.endswith("?")][:6]
        if not questions:
            questions = ["No explicit questions found in this source."]

        tags = _candidate_tags(packet.source_slug, lines)
        summary_lines = [text for _, text in lines[:4]]
        summary = " ".join(summary_lines) if summary_lines else "This source has no extractable body text."

        payload = {
            "source_card": {
                "source_slug": packet.source_slug,
                "source_title": title,
                "source_path": packet.source_path,
                "source_type": Path(packet.source_path).suffix.lstrip(".") or "text",
                "artifact_status": "draft",
                "source_sha256": packet.source_sha256,
            },
            "source_summary": {
                "title": title,
                "summary": summary,
                "notable_points": [text for _, text in lines[:5]] or ["No summary basis lines extracted."],
            },
            "evidence_ledger": {
                "source_path": packet.source_path,
                "source_sha256": packet.source_sha256,
                "excerpts": excerpt_entries,
            },
            "questions": questions,
            "candidate_tags": tags,
        }
        usage = {
            "source_characters": len(packet.source_text),
            "excerpts": len(excerpt_entries),
        }
        return ProviderResponse(payload=payload, usage=usage)


def get_source_artifact_provider(name: str) -> SourceArtifactProvider:
    if name == "mock":
        return MockSourceArtifactProvider()
    raise ValueError(f"unknown source artifact provider: {name}")


def _source_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    for index, raw_line in enumerate(text.splitlines(), start=1):
        cleaned = raw_line.strip().lstrip("# ").strip()
        if cleaned:
            lines.append((index, cleaned))
    return lines


def _source_title(source_path: str, lines: list[tuple[int, str]]) -> str:
    for _, text in lines:
        if text and len(text.split()) <= 12:
            return text
    return Path(source_path).stem.replace("_", " ").replace("-", " ").title()


def _candidate_tags(source_slug: str, lines: list[tuple[int, str]]) -> list[str]:
    words = re.findall(r"[a-z0-9]+", source_slug.lower())
    for _, text in lines[:6]:
        words.extend(re.findall(r"[a-z0-9]{4,}", text.lower()))
    ignored = {"source", "this", "that", "with", "from", "into", "notes", "should", "would"}
    tags: list[str] = []
    for word in words:
        if word in ignored or word in tags:
            continue
        tags.append(word)
        if len(tags) == 8:
            break
    return tags or ["source"]
