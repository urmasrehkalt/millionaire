// Frontend façade kept stable so game/result UI modules don't need to know
// whether the backend is reachable. The game itself runs entirely client-side
// via engine.js — both locally and on GitHub Pages.

import {
    quitGame as engineQuitGame,
    startGameFor,
    submitAnswer as engineSubmitAnswer,
    useLifeline as engineUseLifeline,
} from "./engine.js";

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
