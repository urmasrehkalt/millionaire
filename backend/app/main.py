"""FastAPI entry point. Serves the API and the static frontend."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import settings
from backend.app.routes import assignments, game

app = FastAPI(title="Miljonimäng", version="0.1.0")

if settings.environment == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(assignments.router)
app.include_router(game.router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Mount input/ so the client-side game engine can fetch
# input/<id>/questions.json the same way it does on GitHub Pages.
app.mount(
    "/input",
    StaticFiles(directory=str(settings.input_dir)),
    name="input",
)

# Serve the frontend last so /api/* and /input/* mounts win.
app.mount(
    "/",
    StaticFiles(directory=str(settings.frontend_dir), html=True),
    name="frontend",
)
