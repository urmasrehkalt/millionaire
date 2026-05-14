# Esimese aasta miljonimäng

AI-põhise ülesande valideerimise ideest lähtuv õppeprojekt „Kes tahab saada
miljonäriks?” formaadis. Rakendus aitab korrata esimese õppeaasta lõpuks kogunenud
tarkvaraarenduse teadmisi ning kontrollib mõistmist, mitte päheõppimist.

**Mängi otse brauseris:** <https://urmasrehkalt.github.io/millionaire/>

## Projekti kirjeldus

Õppevahend aitab kontrollida arusaamist, mitte failinimede või vastuste
päheõppimist. Avalehel on üks mäng: **Tarkvaraarendaja miljonimäng**. Enne
alustamist saab valida režiimi **Lihtne** või **Keerulisem**. Iga käivitus valib
juhuslikult 15 küsimust valitud 150 küsimusega pangast: 5 lihtsat, 5 keskmist ja
5 rasket.

Küsimusepank on koostatud Tahvlis nähtavate Henno Tähe õppeainete põhjal:
agiilne tarkvaraarendus, agiilse tarkvaraarenduse projekt, andmebaaside alused,
andmebaaside projekteerimine, dokumentatsiooni koostamine, JavaScript,
märgendikeeled, SQL keele alused, sissejuhatus programmeerimisse, testimise
alused, testimise tüübid ja automatiseerimine, klient-server veebirakendused ning
veebiteenused. Küsimused on eesti keeles ning igal küsimusel on 4 vastusevarianti,
üks õige vastus, vihje ja lühike selgitus. Keerulisem režiim kasutab tehnilisemaid
küsimusi ja usutavamaid valesid vastuseid.

## Kasutatud tehnoloogiad

- **Backend:** Python 3.12+ ja [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend:** vanilla HTML/CSS/JS (ilma raamistikuta)
- **AI:** küsimuste loomise prompt on dokumenteeritud; praegune mäng kasutab salvestatud küsimusepanka
- **Versioonihaldus:** Git + GitHub
- **Projektihaldus:** Trello (`Backlog → Todo → In progress → Review/Test → Done`)

## Käivitamise juhend

### Eeldused

- Python 3.12 või uuem
- Lisateenuste võtmeid pole mängimiseks vaja

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
# Vaikimisi töötab mäng ilma production saladusteta

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

Praegune kasutajavoog kasutab ühte mängu kaustas `input/001/`. Kaust sisaldab
ülesande kirjeldust ja küsimusepanka. Struktuur jätab alles võimaluse mängu
hiljem laiendada, kuid UI ei paku enam eraldi teema valikut.

```
input/
  001/
    assignment.md              # teadmiste kontrolli kirjeldus
    learning-outcomes.md       # õpiväljundid ja rõhuasetused
    questions.json             # Lihtne režiim: 50 lihtsat, 50 keskmist, 50 rasket
    questions-hard.json        # Keerulisem režiim: 50 lihtsat, 50 keskmist, 50 rasket
```

Küsimusepank on JSON-kujul. Iga kirje sisaldab `level`, `question`, `options`,
`correctIndex`, `explanation` ja `hint` välju.

## Küsimuste ja AI loogika

Mäng ei kutsu AI-d iga mängu alguses. Lihtne režiim loeb küsimused failist
[`input/001/questions.json`](input/001/questions.json), keerulisem režiim failist
[`input/001/questions-hard.json`](input/001/questions-hard.json). Mängumootor jagab
valitud panga raskusastmete järgi kolmeks, segab iga taseme küsimused ja valib
mänguks 5 lihtsat, 5 keskmist ning 5 rasket küsimust. Ülejäänud sama raskusastme
küsimused jäävad küsimuse vahetamise õlekõrre jaoks varuks.

AI kasutamise loogika ja prompt on dokumenteeritud failis
[`prompts/question-generation.md`](prompts/question-generation.md). Prompt kirjeldab,
et küsimused peavad kontrollima arusaamist, põhinema nõuetel ja lahenduse loogikal,
omama nelja vastusevarianti, üht õiget vastust, raskusastet, vihjet ja selgitust.

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

Rakendus töötab GitHub Pages'is täielikult kliendipoolselt. Mängu loogika
(skoor, turvatasemed, õlekõrred ja küsimuste valik küsimusepangast) asub failis
[`frontend/js/engine.js`](frontend/js/engine.js). Backend'i
[`backend/app/services/game_logic.py`](backend/app/services/game_logic.py) hoiab sama
reeglistiku testitava serveripoolse vastena.

Iga `main`-i push käivitab [`.github/workflows/pages.yml`](.github/workflows/pages.yml),
mis kogub `frontend/` + numbrilised `input/<id>/` kaustad ühte `dist/`-i,
  genereerib `assignments.json`-i `input/`-i põhjal ja deploy-b GitHub Pages-isse.

## Teadaolevad piirangud

- Küsimused on salvestatud staatilises küsimusepangas; mängu alguses uut AI päringut ei tehta
- GitHub Pages demo ei salvesta mänguajalugu ega kasutajapõhiseid tulemusi
- Backend'i mälusisesed sessioonid ei püsi serveri taaskäivituse üle

## Edasiarenduse võimalused

- Õpetaja vaade küsimusepanga haldamiseks veebist
- Kasutajate süsteem ja mänguajalugu
- Küsimuste AI abil uuesti genereerimine ja kvaliteedikontroll
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
