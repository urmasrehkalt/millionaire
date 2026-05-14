// Client-side game engine — mirrors backend/app/services/game_logic.py and
// backend/app/services/question_bank.py so the game runs in the browser
// without a backend (needed for the GitHub Pages build).
//
// If you change the scoring rules or lifelines here, update the Python side
// to match and vice versa. The pytest suite is the canonical source of truth.

export const SCORE_LADDER = [
    100, 200, 300, 500, 1_000,
    2_000, 4_000, 8_000, 16_000, 32_000,
    64_000, 125_000, 250_000, 500_000, 1_000_000,
];

// After passing question 5 you keep 1 000; after passing question 10 you
// keep 32 000; winning question 15 gives you the million. Index 4, 9, 14
// in the ladder above.
const SAFETY_LEVEL_INDICES = [-1, 4, 9, 14];

const QUESTIONS_PER_LEVEL = 5;

const sessions = new Map();

export class QuestionBankError extends Error {}

function uuid() {
    if (crypto.randomUUID) return crypto.randomUUID();
    // Fallback for older browsers
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
    });
}

function shuffle(arr) {
    // Fisher–Yates in place
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
}

function groupByLevel(questions) {
    const groups = { 1: [], 2: [], 3: [] };
    for (const q of questions) {
        if (!groups[q.level]) {
            throw new QuestionBankError(`Unknown level ${q.level} in question bank`);
        }
        groups[q.level].push(q);
    }
    return groups;
}

function selectGameQuestions(bank) {
    const groups = groupByLevel(bank);
    const selected = [];
    const reserves = { 1: [], 2: [], 3: [] };

    for (const level of [1, 2, 3]) {
        const pool = groups[level];
        if (pool.length < QUESTIONS_PER_LEVEL) {
            throw new QuestionBankError(
                `Need at least ${QUESTIONS_PER_LEVEL} level ${level} questions, got ${pool.length}`,
            );
        }
        shuffle(pool);
        selected.push(...pool.slice(0, QUESTIONS_PER_LEVEL));
        reserves[level] = pool.slice(QUESTIONS_PER_LEVEL);
    }
    return { selected, reserves };
}

function publicQuestion(q) {
    return { level: q.level, question: q.question, options: q.options };
}

function lifelineState(session) {
    return {
        fifty_fifty: session.usedLifelines.has("fifty_fifty"),
        hint: session.usedLifelines.has("hint"),
        swap: session.usedLifelines.has("swap"),
    };
}

function safetyScoreFor(currentIndex) {
    let lastPassed = -1;
    for (const safety of SAFETY_LEVEL_INDICES) {
        if (safety < currentIndex) lastPassed = safety;
    }
    return lastPassed < 0 ? 0 : SCORE_LADDER[lastPassed];
}

export function createSession(assignmentId, questions, reserves) {
    if (questions.length !== SCORE_LADDER.length) {
        throw new Error(`Expected ${SCORE_LADDER.length} questions, got ${questions.length}`);
    }
    const session = {
        sessionId: uuid(),
        assignmentId,
        questions,
        reserves: reserves || { 1: [], 2: [], 3: [] },
        currentIndex: 0,
        answered: [],
        usedLifelines: new Set(),
        finished: false,
    };
    sessions.set(session.sessionId, session);
    return {
        session_id: session.sessionId,
        question_number: 1,
        total_questions: questions.length,
        score: 0,
        question: publicQuestion(questions[0]),
        lifelines: lifelineState(session),
    };
}

export function submitAnswer(sessionId, answerIndex) {
    const session = sessions.get(sessionId);
    if (!session) throw new Error(`Session not found: ${sessionId}`);
    if (session.finished) throw new Error("Game already finished");

    const current = session.questions[session.currentIndex];
    const correct = answerIndex === current.correctIndex;

    session.answered.push({
        question: current.question,
        options: current.options,
        correct_index: current.correctIndex,
        user_answer_index: answerIndex,
        explanation: current.explanation,
    });

    if (!correct) {
        session.finished = true;
        const finalScore = safetyScoreFor(session.currentIndex);
        return {
            correct: false,
            correct_index: current.correctIndex,
            explanation: current.explanation,
            status: "lost",
            score: finalScore,
            answered_questions: session.answered,
        };
    }

    const newScore = SCORE_LADDER[session.currentIndex];
    session.currentIndex += 1;

    if (session.currentIndex >= session.questions.length) {
        session.finished = true;
        return {
            correct: true,
            correct_index: current.correctIndex,
            explanation: current.explanation,
            status: "won",
            score: SCORE_LADDER[SCORE_LADDER.length - 1],
            answered_questions: session.answered,
        };
    }

    const next = session.questions[session.currentIndex];
    return {
        correct: true,
        correct_index: current.correctIndex,
        explanation: current.explanation,
        status: "in_progress",
        score: newScore,
        next_question: publicQuestion(next),
        question_number: session.currentIndex + 1,
    };
}

export function useLifeline(sessionId, lifeline) {
    const session = sessions.get(sessionId);
    if (!session) throw new Error(`Session not found: ${sessionId}`);
    if (session.finished) throw new Error("Game already finished");
    if (session.usedLifelines.has(lifeline)) throw new Error("Lifeline already used");

    const current = session.questions[session.currentIndex];

    if (lifeline === "fifty_fifty") {
        session.usedLifelines.add(lifeline);
        const wrongIdx = [0, 1, 2, 3].filter((i) => i !== current.correctIndex);
        shuffle(wrongIdx);
        const disabled = wrongIdx.slice(0, 2).sort((a, b) => a - b);
        return {
            lifeline: "fifty_fifty",
            lifelines: lifelineState(session),
            disabled_options: disabled,
        };
    }

    if (lifeline === "hint") {
        session.usedLifelines.add(lifeline);
        return {
            lifeline: "hint",
            lifelines: lifelineState(session),
            hint: current.hint || fallbackHint(current),
        };
    }

    if (lifeline === "swap") {
        const reserves = session.reserves[current.level] || [];
        if (reserves.length === 0) throw new Error("No replacement question available");
        session.usedLifelines.add(lifeline);
        const replacement = reserves.shift();
        session.questions[session.currentIndex] = replacement;
        return {
            lifeline: "swap",
            lifelines: lifelineState(session),
            question: publicQuestion(replacement),
        };
    }

    throw new Error(`Unknown lifeline: ${lifeline}`);
}

function fallbackHint(question) {
    return `Vihje: keskendu raskusastme ${question.level} põhiteemale ja välista vastused, mis ei sobi ülesande nõuetega.`;
}

export async function loadQuestionBank(assignmentId) {
    const response = await fetch(`input/${assignmentId}/questions.json`);
    if (!response.ok) {
        throw new QuestionBankError(`Question bank not found for ${assignmentId}`);
    }
    const payload = await response.json();
    if (!Array.isArray(payload.questions)) {
        throw new QuestionBankError(`Invalid question bank for ${assignmentId}`);
    }
    return payload.questions;
}

export async function startGameFor(assignmentId) {
    const bank = await loadQuestionBank(assignmentId);
    const { selected, reserves } = selectGameQuestions(bank);
    return createSession(assignmentId, selected, reserves);
}

export function clearSessionsForTests() {
    sessions.clear();
}
