# Pythoni käsurea To-Do nimekiri

## Ülesande kirjeldus

Loo Pythoni programm, mis võimaldab kasutajal hallata oma ülesandeid (to-do
nimekirja) käsurealt. Andmed peavad **säilima** ka pärast programmi sulgemist —
kasuta selleks JSON-faili.

## Nõuded

1. Programm pakub kasutajale **menüü**:
   - 1 — Vaata ülesandeid
   - 2 — Lisa uus ülesanne
   - 3 — Märgi ülesanne tehtuks
   - 4 — Kustuta ülesanne
   - 0 — Välju
2. Iga ülesanne sisaldab vähemalt:
   - `id` (täisarv)
   - `text` (ülesande tekst)
   - `done` (Boolean — kas valmis)
3. Ülesanded salvestatakse faili `todos.json` ja loetakse sealt
   programmi käivitumisel
4. Kui faili ei ole, alustatakse tühja nimekirjaga
5. Programm kasutab vähemalt **kolme funktsiooni** (näiteks `load_todos()`,
   `save_todos()`, `add_todo()`)
6. Sisendi valideerimine: kui kasutaja sisestab kehtetu menüüvaliku,
   kuvatakse veateade ja kuvatakse menüü uuesti
7. Kustutamisel/lõpetamisel kontrollitakse, et antud id eksisteerib

## Hindamiskriteeriumid

- Andmed püsivad pärast programmi taaskäivitamist
- Programm ei jookse kokku kehtetu sisendi korral
- Kood on jagatud funktsioonideks (mitte üks suur main-funktsioon)
- Kasutatakse Pythoni standardteeki: `json`, `os.path`
- JSON-fail loetakse ja kirjutatakse UTF-8 kodeeringuga
