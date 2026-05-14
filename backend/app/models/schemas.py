"""Pydantic models shared across the API and services."""

from __future__ import annotations

from enum import IntEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class QuestionLevel(IntEnum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


class Question(BaseModel):
    """A single multiple-choice question."""

    level: QuestionLevel
    question: str
    options: list[str]
    correct_index: int = Field(..., alias="correctIndex", ge=0, le=3)
    explanation: str
    hint: str | None = None

    model_config = {"populate_by_name": True}

    @field_validator("options")
    @classmethod
    def _validate_options(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError("Question must have exactly 4 options")
        return v


class AssignmentFile(BaseModel):
    path: str
    content: str
    truncated: bool = False


class AssignmentSummary(BaseModel):
    """Used for the assignments list endpoint."""

    id: str
    title: str


class Assignment(BaseModel):
    """Full assignment with description and solution files."""

    id: str
    title: str
    description_md: str
    solution_files: list[AssignmentFile]


class GameStatus(str):
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"
    QUIT = "quit"


class PublicQuestion(BaseModel):
    """Question variant sent to the frontend — without correct answer."""

    level: QuestionLevel
    question: str
    options: list[str]


class StartGameRequest(BaseModel):
    assignment_id: str


class StartGameResponse(BaseModel):
    session_id: str
    question_number: int
    total_questions: int
    score: int
    question: PublicQuestion
    lifelines: dict[str, bool]


class AnswerRequest(BaseModel):
    session_id: str
    answer_index: int = Field(..., ge=0, le=3)


class AnsweredQuestion(BaseModel):
    """A question after the user has answered it — for the result screen."""

    question: str
    options: list[str]
    correct_index: int
    user_answer_index: int | None
    explanation: str


class AnswerResponse(BaseModel):
    correct: bool
    correct_index: int
    explanation: str
    status: Literal["in_progress", "won", "lost"]
    score: int
    next_question: PublicQuestion | None = None
    question_number: int | None = None
    answered_questions: list[AnsweredQuestion] | None = None


class LifelineRequest(BaseModel):
    session_id: str
    lifeline: Literal["fifty_fifty", "hint", "swap"]


class LifelineResponse(BaseModel):
    lifeline: Literal["fifty_fifty", "hint", "swap"]
    lifelines: dict[str, bool]
    disabled_options: list[int] | None = None
    hint: str | None = None
    question: PublicQuestion | None = None


class CreateTopicRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description_md: str = Field(..., min_length=10, max_length=8000)


class CreateTopicResponse(BaseModel):
    assignment: AssignmentSummary
    question_count: int
