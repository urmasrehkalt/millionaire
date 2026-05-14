import { startGame, submitAnswer, useLifeline } from "../api.js";

const SCORE_LADDER = [
    100, 200, 300, 500, 1_000,
    2_000, 4_000, 8_000, 16_000, 32_000,
    64_000, 125_000, 250_000, 500_000, 1_000_000,
];
const SAFETY_INDICES = new Set([4, 9, 14]);

let state = null;
let elements = null;

export async function startNewGame(root, assignment, onFinish) {
    root.innerHTML = `<div class="loading">Alustan mängu…</div>`;

    let start;
    try {
        start = await startGame(assignment.id);
    } catch (err) {
        root.innerHTML = `<div class="error-state">Mängu alustamine ebaõnnestus: ${err.message}</div>`;
        return;
    }

    state = {
        sessionId: start.session_id,
        assignment,
        currentQuestion: start.question,
        questionNumber: start.question_number,
        totalQuestions: start.total_questions,
        score: start.score,
        lifelines: start.lifelines,
        disabledOptions: [],
        locked: false,
        onFinish,
    };

    renderLayout(root);
    paintQuestion();
}

function renderLayout(root) {
    root.innerHTML = `
        <div class="game-layout">
            <div class="question-panel">
                <div class="question-header">
                    <span id="q-meta"></span>
                    <span id="q-score"></span>
                </div>
                <p class="question-text" id="q-text"></p>
                <div class="options" id="q-options"></div>
                <div id="q-feedback" hidden></div>
                <div class="question-actions">
                    <div class="lifelines" id="lifelines" aria-label="Õlekõrred">
                        <button type="button" data-lifeline="fifty_fifty">50:50</button>
                        <button type="button" data-lifeline="hint">Vihje</button>
                        <button type="button" data-lifeline="swap">Vaheta</button>
                    </div>
                    <button class="next-button" id="q-next" hidden>Järgmine küsimus →</button>
                </div>
            </div>
            <aside class="ladder" id="ladder"></aside>
        </div>`;

    elements = {
        meta: root.querySelector("#q-meta"),
        score: root.querySelector("#q-score"),
        text: root.querySelector("#q-text"),
        lifelines: root.querySelector("#lifelines"),
        options: root.querySelector("#q-options"),
        feedback: root.querySelector("#q-feedback"),
        next: root.querySelector("#q-next"),
        ladder: root.querySelector("#ladder"),
    };

    elements.next.addEventListener("click", () => {
        elements.next.hidden = true;
        state.disabledOptions = [];
        paintQuestion();
    });

    elements.lifelines.addEventListener("click", (event) => {
        const button = event.target.closest("button[data-lifeline]");
        if (!button) return;
        handleLifeline(button.dataset.lifeline);
    });

    renderLadder();
}

function paintQuestion() {
    state.locked = false;
    const q = state.currentQuestion;
    elements.meta.textContent = `Küsimus ${state.questionNumber}/${state.totalQuestions} • Raskus ${q.level}/3`;
    elements.score.textContent = `Hetkeseis: ${formatScore(state.score)} p`;
    elements.text.textContent = q.question;

    elements.options.innerHTML = "";
    q.options.forEach((option, idx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "option";
        btn.innerHTML = `<span class="letter">${"ABCD"[idx]}</span><span>${escapeHtml(option)}</span>`;
        if (state.disabledOptions.includes(idx)) {
            btn.disabled = true;
            btn.classList.add("eliminated");
        }
        btn.addEventListener("click", () => handleAnswer(idx, btn));
        elements.options.appendChild(btn);
    });

    elements.feedback.hidden = true;
    elements.feedback.innerHTML = "";
    elements.next.hidden = true;

    renderLadder();
    renderLifelines();
}

async function handleLifeline(lifeline) {
    if (state.locked || state.lifelines[lifeline]) return;

    let response;
    try {
        response = await useLifeline(state.sessionId, lifeline);
    } catch (err) {
        showFeedback(`Õlekõrre kasutamine ebaõnnestus: ${err.message}`, "wrong");
        return;
    }

    state.lifelines = response.lifelines;

    if (response.disabled_options) {
        state.disabledOptions = response.disabled_options;
        paintQuestion();
    }
    if (response.hint) {
        showFeedback(response.hint, "hint");
    }
    if (response.question) {
        state.currentQuestion = response.question;
        state.disabledOptions = [];
        paintQuestion();
    }

    renderLifelines();
}

async function handleAnswer(idx, button) {
    if (state.locked) return;
    state.locked = true;
    renderLifelines();

    const optionButtons = elements.options.querySelectorAll(".option");
    optionButtons.forEach((b) => (b.disabled = true));

    let response;
    try {
        response = await submitAnswer(state.sessionId, idx);
    } catch (err) {
        showFeedback(`Viga: ${err.message}`, "wrong");
        return;
    }

    optionButtons[response.correct_index].classList.add("correct");
    if (!response.correct) {
        button.classList.add("wrong");
    }

    showFeedback(response.explanation, response.correct ? "correct" : "wrong");

    state.score = response.score;
    elements.score.textContent = `Hetkeseis: ${formatScore(state.score)} p`;

    if (response.status === "in_progress") {
        state.currentQuestion = response.next_question;
        state.questionNumber = response.question_number;
        state.disabledOptions = [];
        renderLadder();
        elements.next.hidden = false;
    } else {
        // Game over (won or lost) — show "Vaata tulemust" button.
        elements.next.textContent = "Vaata tulemust →";
        elements.next.hidden = false;
        elements.next.onclick = () => state.onFinish({
            status: response.status,
            score: response.score,
            answered: response.answered_questions ?? [],
            assignment: state.assignment,
        });
    }
}

function renderLifelines() {
    elements.lifelines.querySelectorAll("button[data-lifeline]").forEach((button) => {
        const used = state.lifelines[button.dataset.lifeline];
        button.disabled = used || state.locked;
        button.classList.toggle("used", used);
    });
}

function showFeedback(text, kind) {
    elements.feedback.className = `feedback ${kind}`;
    elements.feedback.textContent = text;
    elements.feedback.hidden = false;
}

function renderLadder() {
    const html = SCORE_LADDER.map((amount, idx) => {
        const stepNumber = idx + 1;
        let cls = "ladder-step";
        if (SAFETY_INDICES.has(idx)) cls += " safety";
        if (idx === state.questionNumber - 1) cls += " current";
        else if (idx < state.questionNumber - 1) cls += " passed";
        return `<div class="${cls}"><span><span class="num">${stepNumber}</span>${formatScore(amount)}</span></div>`;
    }).join("");
    elements.ladder.innerHTML = html;
}

function formatScore(n) {
    return n.toLocaleString("et-EE").replace(/,/g, " ");
}

function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }[ch]));
}
