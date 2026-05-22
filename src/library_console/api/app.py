"""FastAPI app assembly for the read-only Library console."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from library_console.repository import ConsoleRepositoryError, LibraryRepository


app = FastAPI(title="Library Console", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/console/health")
def health() -> dict[str, str]:
    return _repository().health()


@app.get("/api/library/summary")
def summary() -> dict[str, Any]:
    return _repository().summary()


@app.get("/api/library/validation")
def validation() -> dict[str, Any]:
    return _repository().validation_status()


@app.get("/api/library/knowledge")
def targets() -> list[dict[str, Any]]:
    return _repository().list_targets()


@app.get("/api/library/knowledge/{target_slug}")
def target_detail(target_slug: str) -> dict[str, Any]:
    try:
        return _repository().target_detail(target_slug)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="target not found") from exc
    except ConsoleRepositoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _repository() -> LibraryRepository:
    root = Path(os.environ.get("LIBRARY_REPO_ROOT", "."))
    return LibraryRepository(root)
