"""Game session endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.config import settings
from backend.app.models.schemas import (
    AnswerRequest,
    AnswerResponse,
    LifelineRequest,
    LifelineResponse,
    StartGameRequest,
    StartGameResponse,
)
from backend.app.services.assignment_loader import AssignmentLoader, AssignmentNotFoundError
from backend.app.services.game_logic import SessionNotFoundError, create_session, submit_answer, use_lifeline
from backend.app.services.question_bank import QuestionBankError, load_question_bank, select_game_questions

router = APIRouter(prefix="/api/game", tags=["game"])


@router.post("/start", response_model=StartGameResponse)
def start_game(req: StartGameRequest) -> StartGameResponse:
    loader = AssignmentLoader(settings.input_dir)
    try:
        assignment = loader.load_assignment(req.assignment_id)
    except AssignmentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        question_bank = load_question_bank(settings.input_dir, assignment.id)
    except QuestionBankError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    questions, reserves = select_game_questions(question_bank)
    return create_session(req.assignment_id, questions, reserves)


@router.post("/answer", response_model=AnswerResponse)
def answer(req: AnswerRequest) -> AnswerResponse:
    try:
        return submit_answer(req.session_id, req.answer_index)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/lifeline", response_model=LifelineResponse)
def lifeline(req: LifelineRequest) -> LifelineResponse:
    try:
        return use_lifeline(req.session_id, req.lifeline)
    except SessionNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
