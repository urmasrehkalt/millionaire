export function renderResult(root, result, callbacks) {
    const verdictText = {
        won: "🏆 Sa võitsid!",
        lost: "💥 Mäng läbi",
        quit: "👋 Mäng katkestatud",
    }[result.status] || "Mäng lõppes";

    const cardClass = result.status === "won" ? "won" : result.status === "lost" ? "lost" : "";

    root.innerHTML = `
        <div class="result-card ${cardClass}">
            <div class="verdict">${verdictText}</div>
            <div class="score">${formatScore(result.score)} p</div>
            <p>${escapeHtml(result.assignment.title)}</p>
            <div class="actions">
                <button class="btn" id="play-again">Mängi sama ülesannet uuesti</button>
                <button class="btn secondary" id="back-to-menu">Tagasi ülesannete juurde</button>
            </div>
        </div>
        <section class="review">
            <h2>Vastatud küsimused</h2>
            <div id="review-list"></div>
        </section>`;

    const list = root.querySelector("#review-list");
    result.answered.forEach((item, idx) => {
        const userOption = item.user_answer_index != null ? item.options[item.user_answer_index] : "—";
        const correctOption = item.options[item.correct_index];
        const isCorrect = item.user_answer_index === item.correct_index;

        const block = document.createElement("div");
        block.className = "review-item";
        block.innerHTML = `
            <div class="q">${idx + 1}. ${escapeHtml(item.question)}</div>
            <div class="ans user ${isCorrect ? "correct" : "wrong"}">
                Sinu vastus: ${escapeHtml(userOption)}
            </div>
            ${isCorrect ? "" : `<div class="ans">Õige vastus: ${escapeHtml(correctOption)}</div>`}
            <div class="explanation">${escapeHtml(item.explanation)}</div>`;
        list.appendChild(block);
    });

    root.querySelector("#play-again").addEventListener("click", () => callbacks.onPlayAgain(result.assignment));
    root.querySelector("#back-to-menu").addEventListener("click", () => callbacks.onBackToMenu());
}

function formatScore(n) {
    return n.toLocaleString("et-EE").replace(/,/g, " ");
}

function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }[ch]));
}
