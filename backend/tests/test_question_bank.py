"""Tests for stored question banks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from backend.app.models.schemas import Question, QuestionLevel
from backend.app.services.question_bank import (
    QuestionBankError,
    load_question_bank,
    question_bank_payload,
    select_game_questions,
)


def _questions() -> list[Question]:
    return [
        Question(
            level=QuestionLevel.EASY if i < 8 else QuestionLevel.MEDIUM if i < 16 else QuestionLevel.HARD,
            question=f"Q{i + 1}",
            options=["A", "B", "C", "D"],
            correctIndex=0,
            explanation=f"Explanation {i + 1}",
        )
        for i in range(24)
    ]


def test_load_question_bank_validates_and_parses(tmp_path: Path) -> None:
    topic = tmp_path / "001"
    topic.mkdir()
    (topic / "questions.json").write_text(
        json.dumps(question_bank_payload(_questions())),
        encoding="utf-8",
    )

    loaded = load_question_bank(tmp_path, "001")

    assert len(loaded) == 24
    assert loaded[0].question == "Q1"


def test_load_question_bank_rejects_missing_level_volume(tmp_path: Path) -> None:
    topic = tmp_path / "001"
    topic.mkdir()
    sparse = [q for q in _questions() if q.level != QuestionLevel.HARD]
    (topic / "questions.json").write_text(
        json.dumps(question_bank_payload(sparse)),
        encoding="utf-8",
    )

    with pytest.raises(QuestionBankError):
        load_question_bank(tmp_path, "001")


def test_select_game_questions_picks_five_per_level_with_reserves() -> None:
    selected, reserves = select_game_questions(_questions())

    assert len(selected) == 15
    assert [q.level for q in selected].count(QuestionLevel.EASY) == 5
    assert [q.level for q in selected].count(QuestionLevel.MEDIUM) == 5
    assert [q.level for q in selected].count(QuestionLevel.HARD) == 5
    assert len(reserves[QuestionLevel.EASY]) == 3
