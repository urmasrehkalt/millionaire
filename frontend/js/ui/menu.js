import { createTopic, isBackendAvailable, listAssignments } from "../api.js";

export async function renderMenu(root, onSelect) {
    root.innerHTML = `<div class="loading">Laen ülesandeid…</div>`;

    let assignments;
    let backendOnline = false;
    try {
        [assignments, backendOnline] = await Promise.all([
            listAssignments(),
            isBackendAvailable(),
        ]);
    } catch (err) {
        root.innerHTML = `<div class="error-state">Ülesannete laadimine ebaõnnestus: ${err.message}</div>`;
        return;
    }

    if (assignments.length === 0) {
        root.innerHTML = `
            <div class="empty-state">
                <p>Ühtegi ülesannet ei leitud.</p>
                <p>Lisa kausta <code>input/001/</code> fail <code>assignment.md</code> ja värskenda lehte.</p>
            </div>`;
        return;
    }

    const newTopicSection = backendOnline ? `
        <section class="new-topic-card">
            <h2>Lisa uus teema</h2>
            <p>AI koostab teema kirjelduse põhjal 50 küsimusega panga, mis salvestub ülesande kausta.</p>
            <form id="new-topic-form">
                <input id="topic-title" name="title" type="text" minlength="3" maxlength="120" placeholder="Teema pealkiri" required>
                <textarea id="topic-description" name="description" minlength="10" maxlength="8000" rows="5" placeholder="Kirjelda teemat, õpieesmärke ja olulisi nõudeid" required></textarea>
                <button class="btn" type="submit">Loo teema AI abiga</button>
                <div class="form-status" id="topic-status" aria-live="polite"></div>
            </form>
        </section>` : `
        <p class="static-note">
            See on GitHub Pages demo — uute teemade lisamiseks tuleb rakendus
            <a href="https://github.com/urmasrehkalt/millionaire#k%C3%A4ivitamise-juhend">lokaalselt käivitada</a>.
            Olemasolevaid teemasid saad demos ikka mängida.
        </p>`;

    root.innerHTML = `
        <p class="menu-intro">Vali ülesanne, mille üle soovid end proovile panna.</p>
        <div class="assignment-grid" id="grid"></div>
        ${newTopicSection}`;

    const grid = root.querySelector("#grid");
    for (const a of assignments) {
        const card = document.createElement("button");
        card.type = "button";
        card.className = "assignment-card";
        card.innerHTML = `
            <span class="num">${a.id}</span>
            <span class="title">${escapeHtml(a.title)}</span>`;
        card.addEventListener("click", () => onSelect(a));
        grid.appendChild(card);
    }

    const newTopicForm = root.querySelector("#new-topic-form");
    if (!newTopicForm) return;

    newTopicForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const status = root.querySelector("#topic-status");
        const button = form.querySelector("button");
        const title = form.querySelector("#topic-title").value.trim();
        const description = form.querySelector("#topic-description").value.trim();

        button.disabled = true;
        status.textContent = "Loon teemat ja genereerin 50 küsimust…";
        try {
            const created = await createTopic(title, description);
            status.textContent = `Teema „${created.assignment.title}” loodud. Pangas on ${created.question_count} küsimust.`;
            form.reset();
            renderMenu(root, onSelect);
        } catch (err) {
            status.textContent = `Teema loomine ebaõnnestus: ${err.message}`;
        } finally {
            button.disabled = false;
        }
    });
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
