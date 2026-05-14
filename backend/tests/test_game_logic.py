"""Tests for game_logic — scoring ladder, safety levels, session flow."""

from __future__ import annotations

import pytest

from backend.app.models.schemas import Question, QuestionLevel
from backend.app.services.game_logic import (
    SCORE_LADDER,
    SessionNotFoundError,
    clear_sessions_for_tests,
    create_session,
    submit_answer,
)


@pytest.fixture(autouse=True)
def _clean_sessions() -> None:
    clear_sessions_for_tests()


def _make_questions() -> list[Question]:
    return [
        Question(
            level=QuestionLevel.EASY if i < 5 else QuestionLevel.MEDIUM if i < 10 else QuestionLevel.HARD,
            question=f"Q{i + 1}",
            options=["A", "B", "C", "D"],
            correctIndex=0,
            explanation=f"Explanation {i + 1}",
        )
        for i in range(15)
    ]


def test_create_session_returns_first_question() -> None:
    response = create_session("001", _make_questions())

    assert response.question_number == 1
    assert response.total_questions == 15
    assert response.score == 0
    assert response.question.question == "Q1"
    assert len(response.question.options) == 4


def test_create_session_rejects_wrong_question_count() -> None:
    with pytest.raises(ValueError):
        create_session("001", _make_questions()[:10])


def test_correct_answer_advances_and_updates_score() -> None:
    start = create_session("001", _make_questions())

    answer = submit_answer(start.session_id, 0)

    assert answer.correct is True
    assert answer.status == "in_progress"
    assert answer.score == SCORE_LADDER[0]  # 100 after Q1
    assert answer.next_question is not None
    assert answer.next_question.question == "Q2"
    assert answer.question_number == 2


def test_wrong_answer_first_question_drops_to_zero() -> None:
    start = create_session("001", _make_questions())

    answer = submit_answer(start.session_id, 1)  # wrong

    assert answer.correct is False
    assert answer.status == "lost"
    assert answer.score == 0
    assert answer.answered_questions is not None and len(answer.answered_questions) == 1


def test_wrong_answer_after_first_safety_drops_to_1000() -> None:
    """Pass Q1–Q5 (which awards 1000 pts after Q5), miss Q6 → score = 1000."""
    session_id = create_session("001", _make_questions()).session_id

    for _ in range(5):
        submit_answer(session_id, 0)
    answer = submit_answer(session_id, 2)  # wrong on Q6

    assert answer.status == "lost"
    assert answer.score == 1_000


def test_wrong_answer_after_second_safety_drops_to_32000() -> None:
    session_id = create_session("001", _make_questions()).session_id

    for _ in range(10):
        submit_answer(session_id, 0)
    answer = submit_answer(session_id, 2)  # wrong on Q11

    assert answer.status == "lost"
    assert answer.score == 32_000


def test_winning_all_15_returns_million() -> None:
    session_id = create_session("001", _make_questions()).session_id

    final = None
    for _ in range(15):
        final = submit_answer(session_id, 0)

    assert final is not None
    assert final.status == "won"
    assert final.score == 1_000_000
    assert final.answered_questions is not None and len(final.answered_questions) == 15


def test_cannot_answer_after_game_ended() -> None:
    session_id = create_session("001", _make_questions()).session_id
    submit_answer(session_id, 1)  # wrong → game over

    with pytest.raises(ValueError):
        submit_answer(session_id, 0)


def test_unknown_session_raises() -> None:
    with pytest.raises(SessionNotFoundError):
        submit_answer("bogus-uuid", 0)
