# Miljonimäng

AI-põhine ülesande valideerimise rakendus „Kes tahab saada miljonäriks?" formaadis.
TAK25 grupi õppeprojekt.

🎮 **Mängi otse brauseris:** <https://urmasrehkalt.github.io/millionaire/>
(staatiline GitHub Pages demo — uue teema loomise vorm on aktiivne ainult lokaalses arendusrežiimis)

## Projekti kirjeldus

Õppevahend, mis aitab kontrollida, kas õppija saab aru enda või kellegi teise tehtud
tarkvaraülesande lahendusest. Rakendus loeb `input/<NNN>/` kaustadest ülesandeid
ja salvestatud küsimusepanku. Õppija mängib küsimused läbi nagu „Kes tahab saada
miljonäriks?" mängus — 3 turvataset (1 000 / 32 000 / 1 000 000 punkti) ja 3
õlekõrt (50:50, vihje, küsimuse vahetamine).

## Kasutatud tehnoloogiad

- **Backend:** Python 3.12+ ja [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** vanilla HTML/CSS/JS (ilma raamistikuta)
- **AI:** [Google Gemini API](https://ai.google.dev/) (mudel `gemini-2.5-flash` vaikimisi, free tier)
- **Markdown ja koodivärvimine:** `marked` ja `highlight.js` CDN-ist
- **Versioonihaldus:** Git + GitHub
- **Projektihaldus:** Trello (`Backlog → Todo → In progress → Review/Test → Done`)

## Käivitamise juhend

### Eeldused

- Python 3.12 või uuem
- Gemini API võti uue teema loomiseks (tasuta saab [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey); olemasolevad teemad töötavad ilma võtmeta)

### Käivitamine

```bash
# 1. Klooni repo
git clone https://github.com/urmasrehkalt/millionaire.git
cd millionaire

# 2. Loo virtuaalne keskkond ja installi sõltuvused
python3.12 -m venv .venv
source .venv/bin/activate          # Windowsis: .venv\Scripts\activate
python -m pip install -e ".[dev]"

# 3. Seadista .env
cp .env.example .env
# Ava .env ja lisa GEMINI_API_KEY=... (vajalik ainult uue teema AI-loomiseks)

# 4. Käivita server
uvicorn backend.app.main:app --reload --port 8005

# 5. Ava brauseris
# http://localhost:8005
```

### Testid

```bash
pytest
```

## Input-kausta struktuur

Iga ülesanne on eraldi numbrilises alamkaustas `input/`-i all. Kaust peab sisaldama
faili `assignment.md` (ülesande püstitus, nõuded, hindamiskriteeriumid). Lahendusfailid
võivad olla suvalises vormis ja struktuuris.

```
input/
  001/
    assignment.md
    index.html
    style.css
    script.js
  002/
    assignment.md
    src/
      app.js
      data.json
  003/
    assignment.md
    README.md
    solution/
      main.py
```

Ülesande pealkiri võetakse `assignment.md` esimesest H1-pealkirjast (näiteks
`# JavaScripti kalkulaator`).

Olemasolevatel teemadel on samas kaustas `questions.json` küsimusepank. Uue teema
saab lisada ka veebivormist: AI loob siis teema jaoks salvestatud küsimusepanga.

## Küsimuste ja AI loogika

Mäng ei kutsu AI-d iga mängu alguses. Olemasolevate teemade puhul loetakse
küsimused `input/<id>/questions.json` failist. Igas pangas on umbes 50 küsimust,
tasemetega 1-3. Mäng valib igal alustamisel juhuslikult 5 lihtsat, 5 keskmist ja
5 rasket küsimust ning hoiab ülejäänud sama taseme küsimused vahetamise õlekõrre
jaoks varus.

AI-d kasutatakse ainult uue teema loomisel. Veebivorm saadab teema pealkirja ja
kirjelduse backendile, mis palub Google Gemini API-l (`gemini-2.5-flash`) luua
50 küsimusega `questions.json` panga. Prompt asub failis
[`prompts/question-generation.md`](prompts/question-generation.md). Kui
`GEMINI_API_KEY` puudub või päring ebaõnnestub, uut teemat ei looda.

## Mängu reeglid

- 15 küsimust, igal 4 vastusevarianti
- Punktiastmed: 100 → 200 → 300 → 500 → 1 000 → 2 000 → 4 000 → 8 000 → 16 000 →
  32 000 → 64 000 → 125 000 → 250 000 → 500 000 → 1 000 000
- Turvatasemed: **1 000**, **32 000**, **1 000 000** punkti
- Vale vastusega kukub punktisumma viimasele saavutatud turvatasemele
- 3 õlekõrt, igaüks kasutatav 1 kord:
  - **50:50** — eemaldab kaks valet vastust
  - **Vihje** — kuvab küsimusepangas salvestatud suunava vihje
  - **Vaheta küsimus** — asendab küsimuse sama raskusastme varuküsimusega

## Demo (GitHub Pages)

Rakendus on saadaval kahes režiimis:

| Režiim | URL | Mängu mängimine | Uue teema loomine AI abil |
|--------|-----|------------------|---------------------------|
| **GitHub Pages demo** | <https://urmasrehkalt.github.io/millionaire/> | ✅ töötab kliendipoolselt | ❌ vajab backendi |
| **Lokaalne arendus** | `http://localhost:8005` | ✅ töötab kliendipoolselt | ✅ vajab `GEMINI_API_KEY`-d |

Mängu loogika (skoor, turvatasemed, õlekõrred, küsimuste valik küsimusepangast)
elab failis [`frontend/js/engine.js`](frontend/js/engine.js) ja jookseb täielikult
brauseris. Backend ([`backend/app/services/game_logic.py`](backend/app/services/game_logic.py))
peegeldab sama loogikat ja teenindab uue teema AI-genereerimist. Mõlemal poolel
on `pytest` / käsitsi smoke-testid samale käitumisele.

Iga `main`-i push käivitab [`.github/workflows/pages.yml`](.github/workflows/pages.yml),
mis kogub `frontend/` + numbrilised `input/<id>/` kaustad ühte `dist/`-i,
genereerib värske `assignments.json`-i `input/`-i põhjal ja deploy-b GitHub
Pages-isse.

## Teadaolevad piirangud

- Mängusessioonid hoitakse mälusiseses dictionary'is — serveri taaskäivitamisel kaovad
- Uue teema loomine nõuab töötavat `GEMINI_API_KEY` väärtust
- Mängusessioonid ei püsi serveri taaskäivituse üle

## Edasiarenduse võimalused

- Õpetaja vaade — ülesannete haldus veebist
- Kasutajate süsteem ja mänguajalugu
- Küsimuste vahemällu salvestamine (sama ülesande korduvkasutusel)
- Mitme AI pakkuja tugi (Anthropic, kohalik mudel)
- SQLite mängusessioonide püsivaks salvestamiseks

## Projekti dokumentatsioon

Detailsem info arenduse kohta:

- [`docs/backlog.md`](docs/backlog.md) — kasutajalood ja vastuvõtutingimused
- [`docs/trello-cards.md`](docs/trello-cards.md) — Trellosse kopeeritavad kaardid
- [`docs/definition-of-done.md`](docs/definition-of-done.md) — DoD
- [`docs/architecture.md`](docs/architecture.md) — komponendiskeem
- [`docs/iterations/`](docs/iterations/) — iteratsioonide kirjeldused
- [`docs/testing-notes.md`](docs/testing-notes.md) — vastuvõtutestide tulemused
- [`docs/retrospective.md`](docs/retrospective.md) — projekti tagasivaade
