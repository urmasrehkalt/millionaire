"""Loads stored question banks and selects game questions."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

from backend.app.models.schemas import Question, QuestionLevel

QUESTION_BANK_FILENAME = "questions.json"
QUESTIONS_PER_LEVEL = 5


class QuestionBankError(Exception):
    """Raised when a stored question bank is missing or invalid."""


def load_question_bank(input_root: Path, assignment_id: str) -> list[Question]:
    path = input_root / assignment_id / QUESTION_BANK_FILENAME
    if not path.exists():
        raise QuestionBankError(f"Question bank not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QuestionBankError(f"Invalid question bank: {path}") from exc

    try:
        questions = [Question.model_validate(q) for q in payload["questions"]]
    except (KeyError, TypeError, ValueError) as exc:
        raise QuestionBankError(f"Invalid question bank schema: {path}") from exc

    _validate_question_bank(questions)
    return questions


def select_game_questions(question_bank: list[Question]) -> tuple[list[Question], dict[QuestionLevel, list[Question]]]:
    """Pick 15 questions: 5 random questions for each difficulty level."""
    by_level = _group_by_level(question_bank)
    selected: list[Question] = []
    reserves: dict[QuestionLevel, list[Question]] = {}

    for level in (QuestionLevel.EASY, QuestionLevel.MEDIUM, QuestionLevel.HARD):
        level_questions = by_level[level]
        random.shuffle(level_questions)
        selected.extend(level_questions[:QUESTIONS_PER_LEVEL])
        reserves[level] = level_questions[QUESTIONS_PER_LEVEL:]

    return selected, reserves


def question_bank_payload(questions: list[Question]) -> dict[str, list[dict]]:
    return {
        "questions": [
            q.model_dump(mode="json", by_alias=True, exclude_none=True)
            for q in questions
        ]
    }


def _validate_question_bank(questions: list[Question]) -> None:
    by_level = _group_by_level(questions)
    for level in (QuestionLevel.EASY, QuestionLevel.MEDIUM, QuestionLevel.HARD):
        count = len(by_level[level])
        if count < QUESTIONS_PER_LEVEL:
            raise QuestionBankError(
                f"Question bank needs at least {QUESTIONS_PER_LEVEL} level {int(level)} questions, got {count}"
            )


def _group_by_level(questions: list[Question]) -> dict[QuestionLevel, list[Question]]:
    by_level: dict[QuestionLevel, list[Question]] = defaultdict(list)
    for question in questions:
        by_level[question.level].append(question)
    return by_level
