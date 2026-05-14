// Frontend façade kept stable so menu/game/result UI modules don't need to
// know whether the backend is reachable. The game itself runs entirely
// client-side via engine.js — both locally and on GitHub Pages.
//
// `createTopic` still goes through the FastAPI backend (it needs the Gemini
// API key, which can't live in the browser). On a backend-less deploy it
// throws and the UI surfaces a friendly message.

import {
    quitGame as engineQuitGame,
    startGameFor,
    submitAnswer as engineSubmitAnswer,
    useLifeline as engineUseLifeline,
} from "./engine.js";

const BACKEND_API_BASE = "/api";

let backendAvailableCache = null;

export async function isBackendAvailable() {
    if (backendAvailableCache !== null) return backendAvailableCache;
    try {
        const response = await fetch(`${BACKEND_API_BASE}/health`, { method: "GET" });
        backendAvailableCache = response.ok;
    } catch {
        backendAvailableCache = false;
    }
    return backendAvailableCache;
}

export async function listAssignments() {
    const response = await fetch("assignments.json");
    if (!response.ok) {
        throw new Error(`Manifesti laadimine ebaõnnestus (HTTP ${response.status})`);
    }
    const payload = await response.json();
    return payload.assignments ?? [];
}

export async function createTopic(title, descriptionMd) {
    const available = await isBackendAvailable();
    if (!available) {
        throw new Error(
            "Uue teema loomine vajab töötavat backendi (Gemini API kutse). " +
            "GitHub Pages versioonis see ei tööta — käivita rakendus lokaalselt: ./start.sh",
        );
    }
    const response = await fetch(`${BACKEND_API_BASE}/assignments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description_md: descriptionMd }),
    });
    if (!response.ok) {
        const detail = await response.text().catch(() => "");
        throw new Error(`HTTP ${response.status}: ${detail || response.statusText}`);
    }
    return response.json();
}

export async function startGame(assignmentId) {
    return startGameFor(assignmentId);
}

export async function submitAnswer(sessionId, answerIndex) {
    return engineSubmitAnswer(sessionId, answerIndex);
}

export async function useLifeline(sessionId, lifeline) {
    return engineUseLifeline(sessionId, lifeline);
}

export async function quitGame(sessionId) {
    return engineQuitGame(sessionId);
}
