"""Generates AI question banks for newly-created topics.

Existing topics use stored `questions.json` banks during gameplay. This module
is kept for creating a new topic bank through Google Gemini and for the legacy
fallback helper used by tests.

The prompt itself lives in `prompts/question-generation.md` (documentation
requirement from the assignment). This module parses that file at load time
so prose docs and runtime prompt stay in sync.
"""

from __future__ import annotations

import json
import logging
import re
import secrets
from pathlib import Path

from backend.app.config import settings
from backend.app.models.schemas import Assignment, Question

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
FALLBACK_PATH = Path(__file__).parent / "fallback_questions.json"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "question-generation.md"


def load_fallback_questions() -> list[Question]:
    """Read and parse the bundled fallback question set."""
    raw = json.loads(FALLBACK_PATH.read_text(encoding="utf-8"))
    return [Question.model_validate(q) for q in raw["questions"]]


def _load_prompt_parts() -> tuple[str, str]:
    """Return (system_instruction, user_template) parsed from the markdown doc.

    The doc has the system instruction as the first ```text fenced block and
    the user template as the second.
    """
    text = PROMPT_PATH.read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)```", text, re.DOTALL)
    if len(blocks) < 2:
        raise RuntimeError(
            f"Expected two ```text blocks in {PROMPT_PATH}, found {len(blocks)}"
        )
    return blocks[0].strip(), blocks[1].strip()


def _build_user_prompt(assignment: Assignment, template: str, nonce: str) -> str:
    files_block = "\n\n".join(
        f"=== Fail: {f.path} ===\n{f.content}"
        + ("\n[FAILI SISU LÕIGATUD — failist näete ainult algust]" if f.truncated else "")
        for f in assignment.solution_files
    )
    if not files_block:
        files_block = "(Lahendusfaile ei leitud.)"

    # Replace the templated placeholders with literal values. We do simple
    # string substitution; Mustache-style `{{...}}` markers in the doc are
    # illustrative, not a real template engine.
    return (
        template
        .replace("{{assignment.title}}", assignment.title)
        .replace("{{assignment.id}}", assignment.id)
        .replace("{{assignment.description_md}}", assignment.description_md)
        .replace(
            "{{#each solution_files}}\n=== Fail: {{path}} ===\n{{content}}\n{{/each}}",
            files_block,
        )
        .replace("{{nonce}}", nonce)
    )


def generate_questions(assignment: Assignment) -> list[Question]:
    """Return 15 questions for the given assignment.

    Tries Gemini first; falls back to bundled questions on any error.
    """
    if not settings.gemini_api_key:
        logger.warning("GEMINI_API_KEY not set — using fallback questions.")
        return _sorted(load_fallback_questions())

    try:
        questions = _generate_via_gemini(assignment)
    except Exception as exc:  # noqa: BLE001 — any AI failure must not break the game
        logger.warning("Gemini request failed (%s) — using fallback questions.", exc)
        return _sorted(load_fallback_questions())

    return _sorted(questions)


def generate_question_bank(assignment: Assignment, question_count: int = 50) -> list[Question]:
    """Generate and validate a stored question bank for a new topic."""
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY not set — cannot generate a new question bank")
    return _sorted(_generate_via_gemini(assignment, question_count=question_count))


def _generate_via_gemini(assignment: Assignment, question_count: int = 15) -> list[Question]:
    """Make the actual Gemini call and validate the response."""
    # Imported lazily so tests and the fallback path don't require the SDK.
    from google import genai
    from google.genai import types

    system_instruction, user_template = _load_prompt_parts()
    user_prompt = _build_user_prompt(
        assignment, user_template, nonce=secrets.token_hex(4)
    )
    if question_count != 15:
        user_prompt += (
            f"\n\nOLULINE ÜLEKIRJUTUS: loo täpselt {question_count} küsimust. "
            "Jaota need võimalikult võrdselt raskusastmete 1, 2 ja 3 vahel."
        )

    client = genai.Client(api_key=settings.gemini_api_key)
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.9,
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "questions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "level": {"type": "integer", "minimum": 1, "maximum": 3},
                                "question": {"type": "string"},
                                "options": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "min_items": 4,
                                    "max_items": 4,
                                },
                                "correctIndex": {
                                    "type": "integer",
                                    "minimum": 0,
                                    "maximum": 3,
                                },
                                "explanation": {"type": "string"},
                                "hint": {"type": "string"},
                            },
                            "required": [
                                "level",
                                "question",
                                "options",
                                "correctIndex",
                                "explanation",
                                "hint",
                            ],
                        },
                    }
                },
                "required": ["questions"],
            },
        ),
    )

    return _parse_response(response.text, expected_count=question_count)


def _parse_response(raw_text: str | None, expected_count: int = 15) -> list[Question]:
    if not raw_text:
        raise ValueError("Empty Gemini response")

    payload = json.loads(raw_text)
    if "questions" not in payload:
        raise ValueError("Response missing 'questions' field")

    questions = [Question.model_validate(q) for q in payload["questions"]]

    if len(questions) != expected_count:
        raise ValueError(f"Expected {expected_count} questions, got {len(questions)}")

    return questions


def _sorted(questions: list[Question]) -> list[Question]:
    return sorted(questions, key=lambda q: q.level)
