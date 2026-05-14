#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

PYTHON_BIN="${PYTHON_BIN:-python3.12}"
PORT="${PORT:-8005}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Viga: $PYTHON_BIN ei ole leitav. Installi Python 3.12 või sea PYTHON_BIN." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "==> Loon virtuaalse keskkonna (.venv) — $($PYTHON_BIN --version)"
  "$PYTHON_BIN" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installin sõltuvused"
pip install --quiet --upgrade pip
pip install --quiet -e ".[dev]"

if [ ! -f .env ]; then
  echo "==> Loon .env (.env.example põhjal)"
  cp .env.example .env
  echo "    Lisa .env-i OPENAI_API_KEY=sk-... (valikuline)"
fi

echo "==> Käivitan serveri: http://localhost:$PORT"
exec uvicorn backend.app.main:app --reload --port "$PORT"
