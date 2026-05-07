# Arhitektuur

## Komponentide ülevaade

```
┌──────────────────────────────────────────────────────────────────┐
│                         BRAUSER                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Frontend (vanilla JS)                                     │  │
│  │                                                            │  │
│  │  index.html ──► main.js ──► api.js ──► fetch()             │  │
│  │                    │                                       │  │
│  │            ┌───────┼─────────┐                             │  │
│  │            ▼       ▼         ▼                             │  │
│  │         menu.js  game.js  result.js                        │  │
│  │                     │                                      │  │
│  │                  lifelines.js                              │  │
│  │                                                            │  │
│  │  marked + highlight.js (CDN)                               │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────┬───────────────────────────┘
                                       │ HTTP (JSON)
                                       ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FastAPI (uvicorn)                            │
│                                                                   │
│  routes/                                                          │
│    assignments.py ──► services/assignment_loader.py ──► input/    │
│    game.py ──► services/game_logic.py (in-memory dict)            │
│             ──► services/question_generator.py ──► OpenAI API     │
│             ──► services/lifelines.py            ──► OpenAI API   │
│                                                                   │
│  config.py (pydantic-settings, .env)                              │
│  models/schemas.py (Pydantic v2)                                  │
└──────────────────────────────────────────┬───────────────────────┘
                                           │
                                           ▼
                                    ┌────────────────┐
                                    │  OpenAI API    │
                                    │  (gpt-4o-mini) │
                                    └────────────────┘
```

## Andmevoog: mängu alustamine

1. Kasutaja klikib avalehel ülesande peal
2. Frontend: `POST /api/game/start { assignment_id: "001" }`
3. Backend:
   - `assignment_loader.load_assignment("001")` loeb assignment.md + lahendusfailid
   - `question_generator.generate(...)` saadab kõik OpenAI-le, valideerib JSON-vastuse
   - Kui API on kättesaamatu → fallback JSON-ist
   - `game_logic.create_session(questions)` loob sessiooni (UUID + GameSession-objekt)
   - Tagastab `{ session_id, question: {level, question, options}, score: 0 }`
4. Frontend: salvestab session_id, renderdab esimese küsimuse

## Andmevoog: vastuse esitamine

1. Frontend: `POST /api/game/answer { session_id, answer_index: 1 }`
2. Backend:
   - `game_logic.submit_answer(session_id, 1)` võrdleb õige vastusega
   - Õige → `current_question_idx += 1`, score uuendub, tagastab järgmise küsimuse
   - Vale → mäng lõppeb, score kukub turvatasemele
   - Tagastab `{ correct: bool, correct_index, explanation, next_question?, final_score? }`
3. Frontend: kuvab tulemuse, animeerib üleminekut

## Failisüsteem (input/-kausta lugemine)

`assignment_loader` reeglid:

- Numbriline alamkaust = ülesande ID (`001`, `002`, …)
- `assignment.md` on kohustuslik — selle puudumisel ülesannet ei laadita
- Kõik ülejäänud failid on lahenduse osa
- **Skip**:
  - kataloogid: `node_modules`, `.git`, `vendor`, `__pycache__`, `.venv`
  - failid: laiend pildiformaatides (.png, .jpg, .gif, .svg, .ico), .pdf, .zip, .tar
  - failid suurusega > 32 KB: kärbitakse 32 KB-ni promptis ja lisatakse märge
- Path traversal kaitse: `os.path.realpath` kontroll, et fail on `input/<id>/`-i sees

## Sessioonihaldus (MVP)

`game_logic` hoiab `_sessions: dict[str, GameSession]`-it mälus:

- UUID4 võti
- Sessioon kustutatakse automaatselt 1 tund pärast viimast tegevust (background task)
- Server taaskäivituse korral kaovad → kasutaja peab uue mängu alustama

Iteratsiooni 5 plaanis: SQLite migratsioon püsivuseks.

## Ohutus ja saladused

- `OPENAI_API_KEY` ainult serveripoolel (.env)
- Frontend ei näe kunagi API-võtit
- CORS lubab arenduses kõik (`*`), tootmises kitsendatav `ENVIRONMENT=production` kaudu
- Path traversal `input/`-i lugemisel: kontrollime, et lahendatud reaal-tee jääb
  `input/<numeric_id>/`-i sisse
