"""Assignment listing endpoints."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException

from backend.app.config import settings
from backend.app.models.schemas import Assignment, AssignmentFile, AssignmentSummary, CreateTopicRequest, CreateTopicResponse
from backend.app.services.assignment_loader import AssignmentLoader, AssignmentNotFoundError
from backend.app.services.question_bank import QUESTION_BANK_FILENAME, question_bank_payload
from backend.app.services.question_generator import generate_question_bank

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


@router.post("", response_model=CreateTopicResponse, status_code=201)
def create_topic(req: CreateTopicRequest) -> CreateTopicResponse:
    assignment_id = _next_assignment_id()
    assignment_dir = settings.input_dir / assignment_id

    assignment_md = f"# {req.title.strip()}\n\n{req.description_md.strip()}\n"
    assignment = Assignment(
        id=assignment_id,
        title=req.title.strip(),
        description_md=assignment_md,
        solution_files=[AssignmentFile(path="assignment.md", content=assignment_md)],
    )

    try:
        questions = generate_question_bank(assignment, question_count=50)
    except Exception as exc:  # noqa: BLE001 - API must return a clear creation failure
        raise HTTPException(status_code=502, detail=f"Question bank generation failed: {exc}") from exc

    assignment_dir.mkdir(parents=True, exist_ok=False)
    (assignment_dir / "assignment.md").write_text(assignment_md, encoding="utf-8")
    (assignment_dir / QUESTION_BANK_FILENAME).write_text(
        json.dumps(question_bank_payload(questions), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return CreateTopicResponse(
        assignment=AssignmentSummary(id=assignment_id, title=req.title.strip()),
        question_count=len(questions),
    )


def _next_assignment_id() -> str:
    settings.input_dir.mkdir(parents=True, exist_ok=True)
    numeric_ids = [
        int(path.name)
        for path in settings.input_dir.iterdir()
        if path.is_dir() and path.name.isdigit()
    ]
    return f"{max(numeric_ids, default=0) + 1:03d}"
