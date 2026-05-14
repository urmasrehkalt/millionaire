"""Tests for question_generator — covers prompt parsing, fallback path and
Gemini integration (mocked)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from backend.app.config import settings
from backend.app.models.schemas import Assignment, AssignmentFile
from backend.app.services import question_generator


def _make_assignment() -> Assignment:
    return Assignment(
        id="001",
        title="Test ülesanne",
        description_md="# Test\n\nMidagi.",
        solution_files=[AssignmentFile(path="app.js", content="console.log(1);")],
    )


def _fake_gemini_payload() -> dict:
    return {
        "questions": [
            {
                "level": (i // 5) + 1,
                "question": f"AI küsimus {i + 1}",
                "options": ["A", "B", "C", "D"],
                "correctIndex": i % 4,
                "explanation": f"Selgitus {i + 1}",
            }
            for i in range(15)
        ]
    }


# ----- Fallback path -----

def test_fallback_when_api_key_missing(monkeypatch) -> None:
    monkeypatch.setattr(settings, "gemini_api_key", "")
    questions = question_generator.generate_questions(_make_assignment())
    assert len(questions) == 15
    # Sorted by level
    assert [q.level for q in questions] == sorted(q.level for q in questions)


def test_fallback_when_gemini_raises(monkeypatch) -> None:
    monkeypatch.setattr(settings, "gemini_api_key", "fake-key")
    with patch(
        "backend.app.services.question_generator._generate_via_gemini",
        side_effect=RuntimeError("network down"),
    ):
        questions = question_generator.generate_questions(_make_assignment())
    assert len(questions) == 15
    # Came from the fallback file
    assert questions[0].question.startswith("Mis on selle")


# ----- Successful Gemini call -----

def test_generate_via_gemini_returns_parsed_questions(monkeypatch) -> None:
    monkeypatch.setattr(settings, "gemini_api_key", "fake-key")

    fake_response = MagicMock()
    fake_response.text = json.dumps(_fake_gemini_payload())

    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = fake_response

    with patch("google.genai.Client", return_value=fake_client) as client_ctor:
        questions = question_generator.generate_questions(_make_assignment())

    client_ctor.assert_called_once_with(api_key="fake-key")
    assert fake_client.models.generate_content.called

    # Inspect the call to confirm the right model, JSON mode and prompt content.
    call = fake_client.models.generate_content.call_args
    assert call.kwargs["model"] == settings.gemini_model
    cfg = call.kwargs["config"]
    assert cfg.response_mime_type == "application/json"
    assert "Sa oled tarkvara" in cfg.system_instruction
    assert "Test ülesanne" in call.kwargs["contents"]
    assert "console.log(1);" in call.kwargs["contents"]

    assert len(questions) == 15
    assert questions[0].question == "AI küsimus 1"


# ----- Variation across calls (US5) -----

def test_two_calls_send_different_nonces(monkeypatch) -> None:
    monkeypatch.setattr(settings, "gemini_api_key", "fake-key")

    fake_client = MagicMock()
    fake_client.models.generate_content.return_value = MagicMock(
        text=json.dumps(_fake_gemini_payload())
    )

    with patch("google.genai.Client", return_value=fake_client):
        question_generator.generate_questions(_make_assignment())
        question_generator.generate_questions(_make_assignment())

    prompt_a = fake_client.models.generate_content.call_args_list[0].kwargs["contents"]
    prompt_b = fake_client.models.generate_content.call_args_list[1].kwargs["contents"]
    assert prompt_a != prompt_b, "Each call should send a different nonce"


# ----- Prompt-doc parsing -----

def test_load_prompt_parts_extracts_two_blocks() -> None:
    system_instruction, user_template = question_generator._load_prompt_parts()
    assert "Sa oled tarkvara" in system_instruction
    assert "{{assignment.title}}" in user_template


# ----- Response validation -----

def test_parse_response_rejects_wrong_count() -> None:
    bad_payload = json.dumps({"questions": _fake_gemini_payload()["questions"][:10]})
    with pytest.raises(ValueError, match="Expected 15"):
        question_generator._parse_response(bad_payload)


def test_parse_response_rejects_missing_field() -> None:
    with pytest.raises(ValueError, match="missing 'questions'"):
        question_generator._parse_response('{"items": []}')


def test_parse_response_rejects_empty() -> None:
    with pytest.raises(ValueError, match="Empty"):
        question_generator._parse_response(None)
