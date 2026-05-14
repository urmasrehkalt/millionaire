# Testimise märkmed

Iga iteratsiooni lõpus täidame siin tabeli vastuvõtutestide tulemustega.

## Iteratsioon 0 — Setup

| Test | Tulemus | Märkused |
|------|---------|----------|
| `git status` näitab puhast tööruumi pärast esmast commit'i | ✅ | |
| GitHubi remote `origin` viitab privaatsele repole | ✅ | https://github.com/urmasrehkalt/millionaire |
| `docs/backlog.md` sisaldab 9 kasutajalugu | ✅ | US1–US9 |
| `docs/trello-cards.md` sisaldab kopeeritavat kaartide teksti | ✅ | 9 user story + 20 task |
| README sisaldab kõiki nõutud peatükke | ✅ | Projekti kirjeldus, tehnoloogiad, käivitamise juhend, input-struktuur, AI loogika, mängu reeglid, piirangud, edasiarendus |
| Näidisülesanne `input/001/` on olemas | ✅ | JavaScripti kalkulaator |

## Iteratsioon 1 — MVP

Testitud 2026-05-14 (`feature/iter1-mvp` branch, port 8005, `gpt-4o-mini` veel
ei ole liidestatud — kasutati fallback-küsimusi).

| Test | Tulemus | Märkused |
|------|---------|----------|
| **US1** Avaleht kuvab kõik input/-i ülesanded | ✅ | `GET /api/assignments` → 001, 002, 003 |
| **US1** Pealkiri tuleb assignment.md H1-st | ✅ | „JavaScripti kalkulaator", „JSON-andmete kuvamine", „Pythoni komandoreal käivituv To-Do nimekiri" |
| **US1** Mittenumbrilised kaustad ignoreeritakse | ✅ | Üksusetestiga `test_lists_only_numeric_dirs_with_assignment_md` kaetud |
| **US2** Mäng käivitub ja kuvab 15 küsimust | ✅ | Smoke-test: 15 küsimust voogesitatud, õigete vastustega võit 1 000 000 punkti |
| **US2** Igal küsimusel on 4 vastusevarianti | ✅ | Pydantic skeema valideerib `options` pikkust 4-ks |
| **US2** Hetkeseis on alati näha | ✅ | Mänguvaates `Hetkeseis: X p` ja punktiastmete tabel |
| **US2** Vale vastus lõpetab mängu | ✅ | Smoke-test: Q1 vale → score=0, status=lost; Q6 vale pärast 5 õiget → score=1000 |
| **US3** Vastatud küsimused kuvatakse selgitustega | ✅ | Tulemusvaade kuvab kõik 15 (või vähem) küsimust koos õige vastuse ja selgitusega |
| **US4** Uue ülesande lisamine teeb selle mängitavaks ilma serveri restartita | ✅ | Lisasin jooksva serveri ajal `input/002` ja `input/003`, kuvatakse kohe peale lehe värskendust |
| Üksusetestid (`pytest`) läbivad | ✅ | 17/17 passed |
| HTTP smoke-test | ✅ | 17/17 checks passed (frontend serving + API + game flow + error handling) |

### Iteratsiooni 1 hetkeseis vastuvõtukriteeriumide vastu

Miinimumnõuded arvestuseks (nõudefailist):

- ✅ input/-kaustas saab olla mitu ülesannet (3 olemas)
- ✅ Iga ülesanne eraldi numbrilises alamkaustas
- ✅ Rakendus kuvab ülesannete valiku
- ✅ Rakendus loeb assignment.md faili
- ✅ Rakendus loeb vähemalt ühe lahenduse faili
- ✅ Rakendus simuleerib 15 küsimust (fallback-failist)
- ✅ Mängus on 4 vastusevarianti
- ✅ Mäng kontrollib õiget ja valet vastust
- ✅ Vale vastuse korral mäng lõpeb
- ✅ Tulemus kuvatakse kasutajale
- ✅ README sisaldab käivitamise juhiseid

**Jäänud iteratsiooniks 2:** päris AI API ühendus (praegu fallback-küsimused).

## Iteratsioon 2 — AI (Gemini 2.5 Flash)

Testitud 2026-05-14 (`feature/iter2-gemini` branch). AI pakkujaks valiti
Gemini Flash (free tier) OpenAI asemel — vt
[iteration-2-ai.md](iterations/iteration-2-ai.md) põhjenduse jaoks.

| Test | Tulemus | Märkused |
|------|---------|----------|
| `pyproject.toml`-s on `google-genai` (mitte `openai`) | ✅ | |
| `.env.example` viitab `GEMINI_API_KEY`-le | ✅ | |
| `prompts/question-generation.md` sisaldab täielikku prompti | ✅ | System instruction + user template, raskusastmed dokumenteeritud |
| Päris Gemini API-ühendus tagastab valiidse JSON-i | ✅ | Mockitud testiga `test_generate_via_gemini_returns_parsed_questions` |
| **US5** Kahe järjestikuse mängu prompid erinevad | ✅ | Mockitud testiga `test_two_calls_send_different_nonces` — iga päring saab uue nonce |
| Puuduva API-võtme korral kasutatakse fallback'i | ✅ | `test_fallback_when_api_key_missing` + logitakse hoiatus |
| API-vea korral langetakse fallback'ile | ✅ | `test_fallback_when_gemini_raises` |
| Vigane vastus (vale küsimuste arv, puuduvad väljad) lükatakse tagasi | ✅ | `_parse_response` testid |
| Üksusetestid (`pytest`) läbivad | ✅ | 25/25 (17 vana + 8 uut) |
| HTTP smoke-test läbib | ✅ | 17/17 kontrolli; mäng töötab fallback'iga ilma API-võtmeta |

### Lõpp-otsast-lõpuni test päris võtmega

⚠️ Kasutaja test: lisa `.env`-i `GEMINI_API_KEY=...` ja mängi 1 mäng. Oodatud
tulemus: AI küsimused on uue mängu jaoks erinevad fallback'i küsimustest ja
seotud `input/001` ülesande sisuga (kalkulaator). Logides ei tohi olla
„using fallback questions" hoiatust.

## Iteratsioon 3 — Küsimusepank teema kohta (#3 + #4)

Testitud 2026-05-14 (issue #4 merge'itud `main`-isse).

| Test | Tulemus | Märkused |
|------|---------|----------|
| Iga teema kaustas on `questions.json` 50 küsimusega | ✅ | `jq '.questions \| length'` → 50 kõigil |
| Pangast valitakse 5+5+5 raskustaseme kaupa | ✅ | `test_select_game_questions` |
| Bank-laadimine valideerib min 5 küsimust per tase | ✅ | `test_load_question_bank_rejects_too_few` |
| **US6** 50:50 lifeline eemaldab 2 valet vastust | ✅ | `test_fifty_fifty_disables_two_wrong` + brauserist mängitud |
| **US6** Vihje lifeline tagastab `hint`-välja sisu | ✅ | Brauserist kontrollitud kõigil 3 teemal |
| **US6** Vaheta lifeline asendab sama raskustaseme küsimusega | ✅ | `test_swap_replaces_with_same_level` |
| **US11** Uue teema vorm avalehel | ✅ | Loodi test-teema „Test JS", AI tagastas 50 küsimust ja teema kuvati menüüs |
| Pytest läbib | ✅ | 32/32 |

## Iteratsioon 4 — UI moderniseerimine (#5)

Testitud 2026-05-14. CSS-only iteratsioon; testid keskendusid visuaalsele
inspektsioonile.

| Test | Tulemus | Märkused |
|------|---------|----------|
| Avaleht — must-kuld teema | ✅ | Kontrollitud Chrome desktop + responsive emulator |
| Mängu vaade — punktiastmete tabel paremal | ✅ | Turvatasemed eristuvad kuldselt |
| Õlekõrte nupud — hover/used/disabled | ✅ | Kõik kolm olekut visuaalselt selged |
| Vastusenupud — hover, correct, wrong | ✅ | Värvide tugevus kontrastne, kuid ei pimesta |
| Mobiili viewport — ladder ja vastused ridadeks | ✅ | iPhone SE viewport (375px) |
| Tulemus­vaade — prominentne skoor | ✅ | Suur kollane number keskel |

## Iteratsioon 5 — GitHub Pages demo (#6)

Testitud 2026-05-14 (commit `7cce8c2` ja järgmised deploy'd).

| Test | Tulemus | Märkused |
|------|---------|----------|
| Pages deploy õnnestub | ✅ | Workflow `25859954951` ja kõik järgnevad |
| Demo URL serveerib `index.html`-i (HTTP 200) | ✅ | <https://urmasrehkalt.github.io/millionaire/> |
| `assignments.json` regenereeritakse igal deploy-l | ✅ | CI Pythoni skript võtab H1 pealkirjad |
| `input/<id>/questions.json` kättesaadav | ✅ | `curl` saidiltis töötab kõigil 3 teemal |
| Mängu mängimine staatilises moodis | ✅ | Engine smoke 15/15: täisvõit, kaotus, kõik 3 õlekõrt |
| Uue teema vorm peidetud Pages režiimis | ✅ | `isBackendAvailable()` tagastab false → CSS .static-note kuvatud |
| Lokaalne dev `./start.sh`-iga töötab samuti | ✅ | `/input` static mount töötab |
| Backend pytest ei regresseeru | ✅ | 32/32 |

## Iteratsioon 6 — „Lõpeta mäng" + keele lihv (#7 + #8)

Testitud 2026-05-14 (commit `1791290`).

| Test | Tulemus | Märkused |
|------|---------|----------|
| **US7** Walk-away Q1-l (ilma vastusteta) → 0 p | ✅ | `quit_smoke.mjs` test 1 |
| **US7** Walk-away Q3 järel → 300 p | ✅ | Smoke test 2 |
| **US7** Walk-away Q5 järel → 1 000 p (mitte turvatase) | ✅ | Smoke test 5 — kinnitab walk-away vs lost erinevuse |
| **US7** Quit-confirm dialoog näitab summa | ✅ | Brauserist testitud |
| **US7** Quit-throw kui sessioon juba lõppenud / tundmatu | ✅ | Smoke testid 3, 4 |
| **US13** Iga visiibel string üle loetud | ✅ | Vt iter-6 dok kõigi muudatuste tabel |
| **US13** Ülesanne 003 pealkiri uuendatud (käsurea) | ✅ | Manifestis ja questions.json-is |
| Pytest 32/32 | ✅ | Backend muutmata |
| JS süntaks puhas | ✅ | `node --check` kõigil failidel |
