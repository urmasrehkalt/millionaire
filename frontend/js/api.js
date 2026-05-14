const API_BASE = "/api";

async function request(path, options = {}) {
    const response = await fetch(API_BASE + path, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    if (!response.ok) {
        const detail = await response.text().catch(() => "");
        throw new Error(`HTTP ${response.status}: ${detail || response.statusText}`);
    }
    return response.json();
}

export function listAssignments() {
    return request("/assignments");
}

export function createTopic(title, descriptionMd) {
    return request("/assignments", {
        method: "POST",
        body: JSON.stringify({ title, description_md: descriptionMd }),
    });
}

export function startGame(assignmentId) {
    return request("/game/start", {
        method: "POST",
        body: JSON.stringify({ assignment_id: assignmentId }),
    });
}

export function submitAnswer(sessionId, answerIndex) {
    return request("/game/answer", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, answer_index: answerIndex }),
    });
}

export function useLifeline(sessionId, lifeline) {
    return request("/game/lifeline", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, lifeline }),
    });
}
