"""Tests for assignment_loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from backend.app.services.assignment_loader import AssignmentLoader, AssignmentNotFoundError


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def input_root(tmp_path: Path) -> Path:
    return tmp_path


def test_lists_only_numeric_dirs_with_assignment_md(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "# Esimene\n")
    _write(input_root / "002" / "assignment.md", "# Teine\n")
    # Non-numeric and missing assignment.md — both must be skipped.
    _write(input_root / "abc" / "assignment.md", "# Skip me\n")
    (input_root / "003").mkdir()  # numeric but no assignment.md

    summaries = AssignmentLoader(input_root).list_assignments()

    assert [s.id for s in summaries] == ["001", "002"]
    assert [s.title for s in summaries] == ["Esimene", "Teine"]


def test_falls_back_to_id_when_no_h1(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "no heading here")

    summaries = AssignmentLoader(input_root).list_assignments()

    assert summaries[0].title == "Ülesanne 001"


def test_load_assignment_collects_solution_files(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "# Kalkulaator\n")
    _write(input_root / "001" / "index.html", "<html></html>")
    _write(input_root / "001" / "src" / "app.js", "console.log(1);")

    assignment = AssignmentLoader(input_root).load_assignment("001")

    assert assignment.title == "Kalkulaator"
    paths = {f.path for f in assignment.solution_files}
    assert "index.html" in paths
    assert str(Path("src") / "app.js") in paths


def test_skip_dirs_are_ignored(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "# X\n")
    _write(input_root / "001" / "node_modules" / "foo.js", "skip me")
    _write(input_root / "001" / ".git" / "config", "skip me too")
    _write(input_root / "001" / "app.js", "keep me")

    assignment = AssignmentLoader(input_root).load_assignment("001")
    paths = {f.path for f in assignment.solution_files}

    assert paths == {"app.js"}


def test_binary_extensions_are_skipped(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "# X\n")
    _write(input_root / "001" / "image.png", "binary garbage")
    _write(input_root / "001" / "app.js", "keep")

    assignment = AssignmentLoader(input_root).load_assignment("001")
    paths = {f.path for f in assignment.solution_files}

    assert paths == {"app.js"}


def test_large_file_is_truncated(input_root: Path) -> None:
    _write(input_root / "001" / "assignment.md", "# X\n")
    big = "a" * (40 * 1024)
    _write(input_root / "001" / "big.txt", big)

    assignment = AssignmentLoader(input_root).load_assignment("001")
    big_file = next(f for f in assignment.solution_files if f.path == "big.txt")

    assert big_file.truncated is True
    assert len(big_file.content) == 32 * 1024


def test_path_traversal_rejected(input_root: Path) -> None:
    loader = AssignmentLoader(input_root)
    with pytest.raises(AssignmentNotFoundError):
        loader.load_assignment("../etc")
    with pytest.raises(AssignmentNotFoundError):
        loader.load_assignment("001/../002")


def test_missing_assignment_raises(input_root: Path) -> None:
    with pytest.raises(AssignmentNotFoundError):
        AssignmentLoader(input_root).load_assignment("999")
