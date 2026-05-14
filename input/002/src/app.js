const userList = document.getElementById("userList");
const filterInput = document.getElementById("filter");

let allUsers = [];

async function loadUsers() {
    try {
        const response = await fetch("src/data.json");
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        allUsers = await response.json();
        render(allUsers);
    } catch (err) {
        userList.innerHTML = `<li class="error">Andmete laadimine ebaõnnestus: ${err.message}</li>`;
    }
}

function render(users) {
    if (users.length === 0) {
        userList.innerHTML = "<li>Ühtegi kasutajat ei leitud.</li>";
        return;
    }
    userList.innerHTML = users
        .map((u) => `<li><strong>${u.nimi}</strong> — ${u.vanus} a, ${u.linn}</li>`)
        .join("");
}

filterInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase();
    const filtered = allUsers.filter((u) => u.nimi.toLowerCase().includes(query));
    render(filtered);
});

loadUsers();
