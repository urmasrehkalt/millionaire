# Arhitektuur

> Viimati uuendatud: 2026-05-14 (peegeldab kuni issue'd #8 main-haru seisuga).

## Lühikokkuvõte

Miljonimäng töötab **kahes režiimis** sama koodibaasi alusel:

- **Lokaalne arendus** — FastAPI server jookseb pordil 8005, serveerib frontendi
  ja `/input` faile, ning vajab Gemini API-võtit ainult **uue teema loomiseks**.
- **GitHub Pages demo** — staatiline `dist/` assembleeritud failidest, mängu
  loogika jookseb kliendipoolselt. Uue teema loomine pole võimalik (vajab
  serveripoolset API-võtit), kuid kõik olemasolevad teemad mängitavad.

Mängu loogika (skoor, turvatasemed, õlekõrred, sessiooniseis) elab
**brauseris** `frontend/js/engine.js`-is. Backend mängu mängimisel rolli ei
mängi — ta on olemas vaid AI-uue-teema-loomise jaoks.

## Komponendid

```text
┌──────────────────────────────────────────────────────────────────┐
│                              BRAUSER                              │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Frontend (vanilla JS, ESM-moodulid)                       │  │
│  │                                                            │  │
│  │  index.html ──► js/main.js                                 │  │
│  │                    │                                       │  │
│  │              ┌─────┴─────┐                                 │  │
│  │              ▼           ▼                                 │  │
│  │           ui/menu.js  ui/game.js  ui/result.js             │  │
│  │              │           │                                 │  │
│  │              └───────────┴──► js/api.js                    │  │
│  │                                  │                         │  │
│  │                        ┌─────────┴───────┐                 │  │
│  │                        ▼                 ▼                 │  │
│  │                  js/engine.js      fetch staatika          │  │
│  │  (mängu olek)                       /assignments.json       │  │
│  │  (skoor, sessioonid)                /input/<id>/questions.json│
│  │  (õlekõrred)                                               │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│                  HTTP (ainult uue teema vorm)                     │
└───────────────────────────────────────┬───────────────────────────┘
                                        │ POST /api/assignments
                                        ▼  (ainult lokaalses dev'is)
┌──────────────────────────────────────────────────────────────────┐
│                       FastAPI (uvicorn :8005)                     │
│                                                                   │
│  routes/assignments.py ─► services/assignment_loader.py           │
│                       ─► services/question_generator.py           │
│                                       │                           │
│  StaticFiles mount /input             │ google-genai SDK          │
│  StaticFiles mount /        services/question_bank.py             │
│                                       │                           │
└───────────────────────────────────────┼───────────────────────────┘
                                        │
                                        ▼
                            ┌──────────────────────┐
                            │  Google Gemini API   │
                            │  (gemini-2.5-flash)  │
                            └──────────────────────┘
```

## Failipuu

```text
millionaire/
├── frontend/                      # Staatiliselt serveeritav frontend
│   ├── index.html
│   ├── assignments.json           # Manifest (CI regenereerib deploy-l)
│   ├── css/style.css
│   └── js/
│       ├── main.js                # Vaate-routing
│       ├── api.js                 # Façade: engine + static fetches + backend probe
│       ├── engine.js              # Kliendipoolne mängu loogika
│       └── ui/
│           ├── menu.js
│           ├── game.js
│           └── result.js
├── backend/                       # FastAPI server (ainult lokaalseks devis ja uue teema loomiseks)
│   └── app/
│       ├── main.py                # FastAPI app + StaticFiles mountid
│       ├── config.py              # pydantic-settings .env-st
│       ├── routes/
│       │   ├── assignments.py     # GET, POST /api/assignments
│       │   └── game.py            # /api/game/* (säilitatud, kuid frontend ei kutsu)
│       └── services/
│           ├── assignment_loader.py
│           ├── question_generator.py  # Gemini call
│           ├── question_bank.py       # Pangast 5+5+5 valik
│           ├── game_logic.py          # Pythoni mängu loogika (vananeb, vt allpool)
│           └── fallback_questions.json
├── input/                         # Iga teema omas numbrilises kaustas
│   └── 001/
│       ├── assignment.md
│       ├── questions.json         # 50 küsimusega pank
│       └── (lahendusfailid)
├── prompts/
│   └── question-generation.md     # Lugemisväärne prompt; runtime parsib siit
└── .github/workflows/pages.yml    # Build + deploy GitHub Pages-isse
```

## Andmevoog: mängu mängimine (mõlemas režiimis ühtemoodi)

1. Kasutaja avab avalehe
2. `menu.js` kutsub `api.listAssignments()` → `fetch("assignments.json")`
3. `api.isBackendAvailable()` kontrollib `/api/health` (paralleelselt)
   - **online** → kuvab „Lisa uus teema" vormi
   - **offline** → kuvab GitHub Pages märkuse
4. Kasutaja klikib ülesannet → `game.startNewGame(assignment)`
5. `api.startGame(id)` kutsub `engine.startGameFor(id)`:
   - `engine.loadQuestionBank(id)` → `fetch("input/<id>/questions.json")`
   - `engine.selectGameQuestions(bank)` valib juhuslikult 5 lihtsat + 5 keskmist + 5 rasket; ülejäänud läheb reserve'i (vahetuse õlekõrre jaoks)
   - `engine.createSession(...)` loob `Map`-is sessiooni, UUID võti
6. Kasutaja vastab → `api.submitAnswer(...)` → `engine.submitAnswer(...)`:
   - Õige → skoor `SCORE_LADDER[currentIndex]`-st, järgmine küsimus
   - Vale → status="lost", skoor turvatasemele, vastatud küsimused tagastatakse
7. Lõpus `result.js` kuvab verdiktit ja kõik vastatud küsimused selgitustega

Backend mängu kulu ei näe — keskandmevoog on täielikult brauseris.

## Andmevoog: uue teema loomine (ainult lokaalne arendus)

1. Kasutaja täidab „Lisa uus teema" vormi
2. `api.createTopic(title, descriptionMd)` saadab `POST /api/assignments`
3. `routes/assignments.py` :
   - Genereerib uue numbrilise ID (`004`, `005`, ...)
   - Loob `input/<id>/assignment.md` pealkirja ja kirjeldusega
   - Kutsub `question_generator.generate_question_bank(...)` ⇒ Gemini API
   - Salvestab tulemuse `input/<id>/questions.json`-i
4. Frontend värskendab menüü; uus teema kuvatakse kohe (nii dev-is kui ka pärast push'i + GitHub Pages deploy'd)

Kui `GEMINI_API_KEY` puudub, tagastab endpoint 400-vea ja vorm näitab teadet.

## Sessioonihaldus

Kliendipoolne. `engine.js`-s on `sessions = new Map()` UUID → session.
Sessioonid kaovad lehe sulgemisel — see on teadlik valik:

- Mäng kestab 5–10 minutit; lehe sulgemisel jätkamine pole vajalik
- Pole vaja persistence-kihti (SQLite ega localStorage)
- GitHub Pages ei pakuks niikuinii püsiseanssi

Tulevikus, kui lisame mänguajaloo, salvestame **lõpetatud** mängu kokkuvõtted
`localStorage`-isse.

## Õlekõrred

`engine.useLifeline(sessionId, lifeline)` — 3 õlekõrt, igaüks kasutatav 1 kord
mängu kohta:

| Õlekõrs | Käitumine |
|---------|-----------|
| `fifty_fifty` | Eemaldab juhuslikult 2 valet vastust (3-st valesti vastusest) |
| `hint` | Tagastab küsimuse `hint`-välja (kui puudub, genereerib raskustase­põhise üldvihje) |
| `swap` | Asendab praeguse küsimuse sama raskustaseme reservküsimusega |

Pyhne logikasamut: `lifelines` ja `audience_poll` ideed (originaalsest kava'st)
asendati `swap`-iga, kuna stored bank model teeb selle loomulikult võimalikuks
ilma uue AI-päringuta.

## Failisüsteem (input/-kausta lugemine)

`backend/app/services/assignment_loader.py` reeglid (kehtivad ainult uue teema
loomisel — mängu kulus loeb kõike kliendipool):

- Numbriline alamkaust = teema ID (`001`, `002`, …)
- `assignment.md` kohustuslik
- Lahendusfailid loetakse kontekstina, **kui** ülesannet uuesti generaeritakse
- Skip: `node_modules`, `.git`, `vendor`, `__pycache__`, `.venv`, binaarfailid
- Üle 32 KB suurused failid kärbitakse
- Path traversal kaitse: lahendatud reaal-tee peab jääma `input/<id>/`-i sisse

## Deploy-voog (GitHub Actions)

`.github/workflows/pages.yml` käivitub iga `main`-i push'iga:

1. `actions/checkout@v4`
2. **Assemble dist/**:
   - `cp -r frontend/. dist/`
   - Iga numbrilise `input/<id>/` kausta `dist/input/`-isse
3. **Regenerate `dist/assignments.json`** — Pythoni skript skannib
   `dist/input/`-i ja võtab pealkirjad `assignment.md` H1-st
4. `actions/configure-pages@v5` (enablement: true)
5. `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`
6. URL: <https://urmasrehkalt.github.io/millionaire/>

## Ohutus ja saladused

- `GEMINI_API_KEY` ainult `.env`-is, mis on `.gitignore`-i sisse pandud
- Frontend ei näe API-võtit kunagi
- CORS arenduses `*`, tootmises kitsendatav `ENVIRONMENT=production`-iga
- Path traversal kaitse `assignment_loader.py`-s
- GitHub Pages serveerib ainult staatilist sisu; secrets pole brauseris kättesaadavad

## Hetkel kasutamata backend-kood

Frontend pärast issue #6 ei kutsu enam `/api/game/*` endpoint'e
(`game.py`, `game_logic.py`, `question_bank.py` server-poolne select). Kood
jääb alles, kuna:

- `pytest` testid katsetavad need radasid (32 testi)
- Tulevikus võiks lisada „multiplayer" režiimi (server-poolne mängu olek)
- Eemaldamine pole prioriteet; selguselt eraldatud kihid

Vajadusel võiks need iteratsioonis 7+ kustutada.
