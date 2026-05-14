const GAME = {
    id: "001",
    title: "Esimese aasta kordamismäng",
};

export function renderMenu(root, onSelect) {
    root.innerHTML = `
        <section class="hero-card" aria-labelledby="hero-title">
            <div class="hero-copy">
                <p class="eyebrow">15 küsimust. 3 raskusastet. Üks mäng.</p>
                <h2 id="hero-title">Korda olulisemaid teemasid.</h2>
                <p>
                    Küsimused põhinevad õppeainetel nagu: agiilne arendus,
                    andmebaasid, dokumentatsioon, JavaScript, märgendikeeled, SQL,
                    testimine, klient-server rakendused ja veebiteenused. Iga mäng
                    valib küsimused juhuslikult 150 küsimuse pangast.
                </p>
            </div>
            <div class="start-panel" aria-label="Mängu kokkuvõte">
                <div class="stat-row"><span>Lihtsad</span><strong>50 varianti</strong></div>
                <div class="stat-row"><span>Keskmised</span><strong>50 varianti</strong></div>
                <div class="stat-row"><span>Rasked</span><strong>50 varianti</strong></div>
                <button class="btn primary" id="start-game" type="button">Alusta mängu</button>
            </div>
        </section>
        <section class="rules-card" aria-labelledby="rules-title">
            <h3 id="rules-title">Mängu reeglid</h3>
            <div class="rule-grid">
                <p><strong>15 küsimust</strong><span>5 küsimust igast raskusastmest</span></p>
                <p><strong>4 vastusevarianti</strong><span>ainult üks vastus on õige</span></p>
                <p><strong>3 õlekõrt</strong><span>50:50, vihje ja küsimuse vahetamine</span></p>
                <p><strong>Turvatasemed</strong><span>1 000, 32 000 ja 1 000 000 punkti</span></p>
            </div>
        </section>`;

    root.querySelector("#start-game").addEventListener("click", () => onSelect(GAME));
}
