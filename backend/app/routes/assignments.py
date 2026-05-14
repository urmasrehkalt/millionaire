"""Assignment listing endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.config import settings
from backend.app.models.schemas import Assignment, AssignmentSummary
from backend.app.services.assignment_loader import AssignmentLoader, AssignmentNotFoundError

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


def _loader() -> AssignmentLoader:
    return AssignmentLoader(settings.input_dir)


@router.get("", response_model=list[AssignmentSummary])
def list_assignments() -> list[AssignmentSummary]:
    return _loader().list_assignments()


@router.get("/{assignment_id}", response_model=Assignment)
def get_assignment(assignment_id: str) -> Assignment:
    try:
        return _loader().load_assignment(assignment_id)
    except AssignmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
