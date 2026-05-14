# Iteratsioon 5 — GitHub Pages demo (#6)

**Periood:** 2026-05-14
**Eesmärk:** rakendus peab töötama ilma backendita. Mängu loogika kolib
brauserisse, GitHub Actions deploy-b iga `main`-i push'iga.

## Põhjus

- Tunnis ja õpilastega jagamiseks on lihtsam saata link kui paluda
  rakendus käivitada lokaalselt
- Pärast iter-3 küsimusepanga mudelit on AI ainult uue teema loomisel —
  mängu jooksul backendit pole vaja
- GitHub Pages on tasuta, lihtne ja töötab privaatse repo HTTPS-iga

## Skoop

**Frontend muudatused:**

- `frontend/js/engine.js` (uus) — peegeldab `backend/app/services/game_logic.py`
  ja `question_bank.py` käitumist JS-is. SCORE_LADDER, turvatasemed,
  Fisher-Yates 5+5+5 valik, kõik 3 õlekõrt, sessiooni-Map
- `frontend/js/api.js` — sama eksporditud liides, aga staatiline:
  `listAssignments` → fetch `assignments.json`; `startGame/submitAnswer/
  useLifeline` → kutsuvad engine'it
- `isBackendAvailable()` — proovib `GET /api/health`. Frontend kasutab seda
  „uue teema" vormi peitmiseks Pages režiimis
- `createTopic()` jääb backendi sõltuvaks (Gemini API-võti ei tohi
  brauserisse)
- `frontend/assignments.json` (uus) — manifest. CI regenereerib igal deploy-l

**Backend muudatused:**

- `backend/app/main.py` mountib `/input` staatilise teena — lokaalne dev
  käitub Pages-iga samamoodi (frontend fetch'ib `input/<id>/questions.json`)

**Build & deploy:**

- `.github/workflows/pages.yml` (uus):
  - Assemble `dist/`: `cp -r frontend/.` + numbrilised `input/<id>/`
  - Python skript regenereerib `assignments.json` `assignment.md` H1-st
  - `actions/configure-pages@v5` (enablement: true)
  - `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4`

**README:**

- Päises demo-link
- Uus „Demo (GitHub Pages)" peatükk: kahe režiimi võrdlus, kus mis töötab

## Tehnilised otsused

- **Engine.js peegeldab Python-poolt 1:1:** parem järjepidev kasutaja­kogemus
  (lokaalne dev ja Pages käituvad ühtemoodi) kui ühe-poole versioon
- **Skoor server-poolelt eemaldatud — engine on ainus tõde:** Python
  `game_logic.py` jääb alles ainult tegelike pytestide jaoks
- **Manifest CI-s regenereeritav:** uue ülesande lisamine on
  `git add input/004/...` + push; CI võtab pealkirja automaatselt

## Definition of Done

- ✅ Demo URL töötab: <https://urmasrehkalt.github.io/millionaire/>
- ✅ Mäng mängitav ilma backendita (engine.js)
- ✅ Uue teema vorm peidetud Pages režiimis
- ✅ CI workflow edukas
- ✅ JS smoke-test 15/15 (täisvõit, kaotus, õlekõrred)
- ✅ Backend pytest 32/32 ei regresseeru

## Komplikatsioonid

1. **`actions/configure-pages@v5` ebaõnnestus esmasel käivitusel** kuna Pages
   polnud repoi seadetes lubatud. Lahendus: `gh api -X POST
   repos/.../pages -f build_type=workflow` enne workflow käivitamist.
   Hilisem fix: lisasime `enablement: true` configure-pages-i sisse, et
   järgmised repod ei vajaks käsitsi sammu.

2. **GitHub Pages serveerib alamkataloogis** (`/millionaire/`). Lahendus:
   kõik fetch'id kasutavad **relatiivseid** teid (`assignments.json`,
   mitte `/assignments.json`).

## Iteratsiooni tagasivaade

**Õnnestus:** kahe-režiimi-arhitektuur on selge: backend = uue teema
loomine, frontend = mängu mängimine. Frontend ei tea režiimi, ta lihtsalt
fetch'ib relatiivseid teid.

**Keeruline:** Pages-i lubamine privaatses reposes nõuab kõrgemaid
õigusi kui `GITHUB_TOKEN` annab. Vaja oli kasutaja PAT'i kaudu API kutset.

**Edasi:** UX-vea „walk away" nupp (US7 / iter-6).
