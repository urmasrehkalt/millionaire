"""Generates the 15-question set for a game.

In iteration 1 we always return the fallback set bundled in
fallback_questions.json. The real OpenAI integration arrives in iteration 2
behind the same generate_questions() interface.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from backend.app.models.schemas import Assignment, Question

FALLBACK_PATH = Path(__file__).parent / "fallback_questions.json"


def load_fallback_questions() -> list[Question]:
    """Read and parse the fallback question set from disk."""
    raw = json.loads(FALLBACK_PATH.read_text(encoding="utf-8"))
    return [Question.model_validate(q) for q in raw["questions"]]


def generate_questions(assignment: Assignment, rng: random.Random | None = None) -> list[Question]:
    """Return 15 questions for the given assignment.

    The assignment argument is accepted now so the function signature stays
    stable when we plug in the real OpenAI call in iteration 2.
    """
    del assignment  # unused in fallback mode
    questions = load_fallback_questions()
    # Sort by difficulty so the game stays easy → medium → hard.
    questions.sort(key=lambda q: q.level)
    return questions
