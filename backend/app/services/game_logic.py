"""In-memory game session manager.

Implements the Millionaire-style scoring ladder and safety levels. Sessions are
keyed by UUID and live in process memory — they vanish on server restart, which
is fine for iteration 1.
"""

from __future__ import annotations

import uuid
import random
from dataclasses import dataclass, field
from typing import Final

from backend.app.models.schemas import (
    AnsweredQuestion,
    AnswerResponse,
    LifelineResponse,
    PublicQuestion,
    Question,
    QuestionLevel,
    StartGameResponse,
)

# Index = question number (1-based -1). 15 levels.
SCORE_LADDER: Final[list[int]] = [
    100, 200, 300, 500, 1_000,
    2_000, 4_000, 8_000, 16_000, 32_000,
    64_000, 125_000, 250_000, 500_000, 1_000_000,
]

# Safety levels are the points the player keeps after passing question 5 and 10.
# Index 4 = question 5 = 1 000 pts; index 9 = question 10 = 32 000 pts.
SAFETY_LEVEL_INDICES: Final[tuple[int, ...]] = (-1, 4, 9, 14)


class SessionNotFoundError(Exception):
    pass


@dataclass
class GameSession:
    session_id: str
    assignment_id: str
    questions: list[Question]
    reserve_questions: dict[QuestionLevel, list[Question]] = field(default_factory=dict)
    current_index: int = 0
    answered: list[AnsweredQuestion] = field(default_factory=list)
    used_lifelines: set[str] = field(default_factory=set)
    finished: bool = False
    final_score: int | None = None


_sessions: dict[str, GameSession] = {}


def create_session(
    assignment_id: str,
    questions: list[Question],
    reserve_questions: dict[QuestionLevel, list[Question]] | None = None,
) -> StartGameResponse:
    if len(questions) != len(SCORE_LADDER):
        raise ValueError(f"Expected {len(SCORE_LADDER)} questions, got {len(questions)}")

    session_id = str(uuid.uuid4())
    session = GameSession(
        session_id=session_id,
        assignment_id=assignment_id,
        questions=questions,
        reserve_questions=reserve_questions or {},
    )
    _sessions[session_id] = session

    return StartGameResponse(
        session_id=session_id,
        question_number=1,
        total_questions=len(questions),
        score=0,
        question=_public(questions[0]),
        lifelines=_lifeline_state(session),
    )


def get_session(session_id: str) -> GameSession:
    session = _sessions.get(session_id)
    if session is None:
        raise SessionNotFoundError(f"Session not found: {session_id}")
    return session


def submit_answer(session_id: str, answer_index: int) -> AnswerResponse:
    session = get_session(session_id)
    if session.finished:
        raise ValueError("Game already finished")

    current = session.questions[session.current_index]
    correct = answer_index == current.correct_index

    session.answered.append(
        AnsweredQuestion(
            question=current.question,
            options=current.options,
            correct_index=current.correct_index,
            user_answer_index=answer_index,
            explanation=current.explanation,
        )
    )

    if not correct:
        session.finished = True
        session.final_score = _safety_score_for(session.current_index)
        return AnswerResponse(
            correct=False,
            correct_index=current.correct_index,
            explanation=current.explanation,
            status="lost",
            score=session.final_score,
            answered_questions=session.answered,
        )

    # Correct answer — advance.
    new_score = SCORE_LADDER[session.current_index]
    session.current_index += 1

    if session.current_index >= len(session.questions):
        session.finished = True
        session.final_score = SCORE_LADDER[-1]
        return AnswerResponse(
            correct=True,
            correct_index=current.correct_index,
            explanation=current.explanation,
            status="won",
            score=session.final_score,
            answered_questions=session.answered,
        )

    next_q = session.questions[session.current_index]
    return AnswerResponse(
        correct=True,
        correct_index=current.correct_index,
        explanation=current.explanation,
        status="in_progress",
        score=new_score,
        next_question=_public(next_q),
        question_number=session.current_index + 1,
    )


def use_lifeline(session_id: str, lifeline: str) -> LifelineResponse:
    session = get_session(session_id)
    if session.finished:
        raise ValueError("Game already finished")
    if lifeline in session.used_lifelines:
        raise ValueError("Lifeline already used")

    current = session.questions[session.current_index]
    if lifeline == "fifty_fifty":
        session.used_lifelines.add(lifeline)
        wrong_indices = [idx for idx in range(4) if idx != current.correct_index]
        disabled = sorted(random.sample(wrong_indices, 2))
        return LifelineResponse(
            lifeline="fifty_fifty",
            lifelines=_lifeline_state(session),
            disabled_options=disabled,
        )

    if lifeline == "hint":
        session.used_lifelines.add(lifeline)
        return LifelineResponse(
            lifeline="hint",
            lifelines=_lifeline_state(session),
            hint=current.hint or _fallback_hint(current),
        )

    if lifeline == "swap":
        reserves = session.reserve_questions.get(current.level, [])
        if not reserves:
            raise ValueError("No replacement question available")
        session.used_lifelines.add(lifeline)
        replacement = reserves.pop(0)
        session.questions[session.current_index] = replacement
        return LifelineResponse(
            lifeline="swap",
            lifelines=_lifeline_state(session),
            question=_public(replacement),
        )

    raise ValueError("Unknown lifeline")


def _safety_score_for(current_index: int) -> int:
    """Return the score the player drops to after answering wrong on question
    `current_index` (0-based)."""
    # Find the highest safety index that was passed (strictly less than current).
    last_passed = -1
    for safety in SAFETY_LEVEL_INDICES:
        if safety < current_index:
            last_passed = safety
    if last_passed < 0:
        return 0
    return SCORE_LADDER[last_passed]


def _public(question: Question) -> PublicQuestion:
    return PublicQuestion(
        level=question.level,
        question=question.question,
        options=question.options,
    )


def _lifeline_state(session: GameSession) -> dict[str, bool]:
    return {
        "fifty_fifty": "fifty_fifty" in session.used_lifelines,
        "hint": "hint" in session.used_lifelines,
        "swap": "swap" in session.used_lifelines,
    }


def _fallback_hint(question: Question) -> str:
    return f"Vihje: keskendu raskusastme {int(question.level)} põhiteemale ja välista vastused, mis ei sobi ülesande nõuetega."


def clear_sessions_for_tests() -> None:
    """Reset session state — only used by tests."""
    _sessions.clear()
