import { listAssignments } from "../api.js";

export async function renderMenu(root, onSelect) {
    root.innerHTML = `<div class="loading">Laen ülesandeid…</div>`;

    let assignments;
    try {
        assignments = await listAssignments();
    } catch (err) {
        root.innerHTML = `<div class="error-state">Ülesannete laadimine ebaõnnestus: ${err.message}</div>`;
        return;
    }

    if (assignments.length === 0) {
        root.innerHTML = `
            <div class="empty-state">
                <p>Ühtegi ülesannet ei leitud.</p>
                <p>Loo <code>input/001/</code> kausta <code>assignment.md</code>-fail ja värskenda lehte.</p>
            </div>`;
        return;
    }

    root.innerHTML = `
        <p class="menu-intro">Vali ülesanne, mille kohta tahad mängu mängida.</p>
        <div class="assignment-grid" id="grid"></div>`;

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
