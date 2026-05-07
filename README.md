# Miljonimäng

AI-põhine ülesande valideerimise rakendus „Kes tahab saada miljonäriks?" formaadis.
TAK25 grupi õppeprojekt.

## Projekti kirjeldus

Õppevahend, mis aitab kontrollida, kas õppija saab aru enda või kellegi teise tehtud
tarkvaraülesande lahendusest. Rakendus loeb `input/<NNN>/` kaustadest ülesandeid
ja nende lahendusi ning palub OpenAI API-l genereerida 15 raskenevat valikvastusega
küsimust. Õppija mängib küsimused läbi nagu „Kes tahab saada miljonäriks?" mängus —
3 turvataset (1 000 / 32 000 / 1 000 000 punkti) ja 3 õlekõrt (50:50, AI vihje,
publiku küsitlus).

## Kasutatud tehnoloogiad

- **Backend:** Python 3.11+ ja [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** vanilla HTML/CSS/JS (ilma raamistikuta)
- **AI:** [OpenAI API](https://platform.openai.com/) (mudel `gpt-4o-mini` vaikimisi)
- **Markdown ja koodivärvimine:** `marked` ja `highlight.js` CDN-ist
- **Versioonihaldus:** Git + GitHub
- **Projektihaldus:** Trello (`Backlog → Todo → In progress → Review/Test → Done`)

## Käivitamise juhend

### Eeldused

- Python 3.11 või uuem
- OpenAI API võti (vajalik AI-küsimuste genereerimiseks; ilma võtmeta töötab fallback)

### Käivitamine

```bash
# 1. Klooni repo
git clone https://github.com/urmasrehkalt/millionaire.git
cd millionaire

# 2. Loo virtuaalne keskkond ja installi sõltuvused
python3 -m venv .venv
source .venv/bin/activate          # Windowsis: .venv\Scripts\activate
pip install -e ".[dev]"

# 3. Seadista .env
cp .env.example .env
# Ava .env ja lisa OPENAI_API_KEY=sk-... (valikuline; ilma selleta töötab fallback)

# 4. Käivita server
uvicorn backend.app.main:app --reload

# 5. Ava brauseris
# http://localhost:8000
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

Uue ülesande lisamiseks loo lihtsalt uus numbriline kaust ja värskenda brauserit —
rakendust ei pea taaskäivitama.

## AI küsimuste genereerimise loogika

Iga mängu alguses koondab rakendus valitud ülesande failid (assignment.md +
lahendusfailid) ühte konteksti ja saadab OpenAI API-le. Prompt asub failis
[`prompts/question-generation.md`](prompts/question-generation.md) ja palub AI-l
genereerida 15 valikvastusega küsimust JSON-formaadis: 5 lihtsat, 5 keskmist ja
5 rasket. Iga küsimusega kaasneb 4 vastusevarianti, õige vastuse indeks ja lühike
selgitus.

Kui `OPENAI_API_KEY` puudub või API-päring ebaõnnestub, kasutatakse fallback-küsimusi
failist `backend/app/services/fallback_questions.json`.

## Mängu reeglid

- 15 küsimust, igal 4 vastusevarianti
- Punktiastmed: 100 → 200 → 300 → 500 → 1 000 → 2 000 → 4 000 → 8 000 → 16 000 →
  32 000 → 64 000 → 125 000 → 250 000 → 500 000 → 1 000 000
- Turvatasemed: **1 000**, **32 000**, **1 000 000** punkti
- Vale vastusega kukub punktisumma viimasele saavutatud turvatasemele
- 3 õlekõrt, igaüks kasutatav 1 kord:
  - **50:50** — eemaldab kaks valet vastust
  - **AI vihje** — annab lühikese suunava vihje
  - **Küsi publikult** — simuleeritud hääletustulemus
- Mängu saab pooleli jätta, hetkeseis salvestub `localStorage`-isse

## Teadaolevad piirangud

- Mängusessioonid hoitakse mälusiseses dictionary'is — serveri taaskäivitamisel kaovad
- Suuremate kui ~32 KB lahendusfailide korral kärbib rakendus konteksti, et hoida
  promptide pikkust kontrolli all
- Binaarfaile (pildid, PDF jne) ei saadeta AI-le

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
