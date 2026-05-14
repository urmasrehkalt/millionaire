"""Reads assignments from the input/ directory.

Each assignment is a numerically-named subfolder of input/ that must contain
at least an assignment.md file. All other files (including those in nested
folders) are treated as the solution.
"""

from __future__ import annotations

import re
from pathlib import Path

from backend.app.models.schemas import Assignment, AssignmentFile, AssignmentSummary

# Folders we never descend into when collecting solution files.
SKIP_DIRS = {
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "vendor",
    "dist",
    "build",
    ".idea",
    ".vscode",
}

# File extensions we never include (binary or media — not useful as text context).
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".ico", ".svg",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".mp3", ".mp4", ".mov", ".wav", ".ogg",
    ".woff", ".woff2", ".ttf", ".eot",
    ".pyc", ".class", ".o", ".so", ".dll", ".exe",
}

# Files larger than this are truncated.
MAX_FILE_BYTES = 32 * 1024

H1_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
NUMERIC_DIR_PATTERN = re.compile(r"^\d+$")


class AssignmentNotFoundError(Exception):
    """Raised when an assignment id does not exist or has no assignment.md."""


class AssignmentLoader:
    """Loads assignments from a given input root directory."""

    def __init__(self, input_root: Path):
        self.input_root = input_root.resolve()

    def list_assignments(self) -> list[AssignmentSummary]:
        """Return all numerically-named assignment folders with their titles."""
        if not self.input_root.exists():
            return []

        summaries: list[AssignmentSummary] = []
        for entry in sorted(self.input_root.iterdir()):
            if not entry.is_dir() or not NUMERIC_DIR_PATTERN.match(entry.name):
                continue

            assignment_md = entry / "assignment.md"
            if not assignment_md.exists():
                continue

            title = self._extract_title(assignment_md) or f"Ülesanne {entry.name}"
            summaries.append(AssignmentSummary(id=entry.name, title=title))

        return summaries

    def load_assignment(self, assignment_id: str) -> Assignment:
        """Load a single assignment with its description and solution files."""
        assignment_dir = self._resolve_assignment_dir(assignment_id)
        assignment_md = assignment_dir / "assignment.md"

        description = assignment_md.read_text(encoding="utf-8", errors="replace")
        title = self._extract_title_from_text(description) or f"Ülesanne {assignment_id}"

        solution_files = self._collect_solution_files(assignment_dir)

        return Assignment(
            id=assignment_id,
            title=title,
            description_md=description,
            solution_files=solution_files,
        )

    def _resolve_assignment_dir(self, assignment_id: str) -> Path:
        # Path traversal protection: only accept purely numeric ids and verify
        # the resolved path stays inside input_root.
        if not NUMERIC_DIR_PATTERN.match(assignment_id):
            raise AssignmentNotFoundError(f"Invalid assignment id: {assignment_id}")

        candidate = (self.input_root / assignment_id).resolve()
        if not _is_relative_to(candidate, self.input_root):
            raise AssignmentNotFoundError(f"Assignment path escapes input root: {assignment_id}")

        if not candidate.is_dir() or not (candidate / "assignment.md").exists():
            raise AssignmentNotFoundError(f"Assignment not found: {assignment_id}")

        return candidate

    def _collect_solution_files(self, assignment_dir: Path) -> list[AssignmentFile]:
        files: list[AssignmentFile] = []
        for path in sorted(assignment_dir.rglob("*")):
            if path.is_dir():
                continue
            if path.name == "assignment.md":
                continue
            if any(part in SKIP_DIRS for part in path.relative_to(assignment_dir).parts):
                continue
            if path.suffix.lower() in SKIP_EXTENSIONS:
                continue

            try:
                size = path.stat().st_size
            except OSError:
                continue

            try:
                raw = path.read_bytes()
            except OSError:
                continue

            truncated = size > MAX_FILE_BYTES
            content_bytes = raw[:MAX_FILE_BYTES] if truncated else raw

            try:
                content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                # Skip files that aren't valid UTF-8 (likely binary we didn't catch).
                continue

            files.append(
                AssignmentFile(
                    path=str(path.relative_to(assignment_dir)),
                    content=content,
                    truncated=truncated,
                )
            )

        return files

    @staticmethod
    def _extract_title(assignment_md: Path) -> str | None:
        try:
            text = assignment_md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        return AssignmentLoader._extract_title_from_text(text)

    @staticmethod
    def _extract_title_from_text(text: str) -> str | None:
        match = H1_PATTERN.search(text)
        return match.group(1).strip() if match else None


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True
