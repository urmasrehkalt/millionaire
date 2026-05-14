# Definition of Done

Kasutajalood ja arendusülesanded loetakse valmis (Done), kui **kõik** alljärgnevad
tingimused on täidetud.

## Kasutajaloo DoD

- [ ] Kõik kasutajaloo vastuvõtutingimused on käsitsi testitud ja töötavad
- [ ] Testimise tulemus on lisatud faili `docs/testing-notes.md`
- [ ] Vastav tracker-kaart on liigutatud veergu **Done**
- [ ] Funktsionaalsus on käivitatav `main`-harul (squash-merge tehtud)
- [ ] Vastav osa README-st ja/või [`docs/backlog.md`](backlog.md)-st (kui asjakohane) on uuendatud

## Arendusülesande (technical task) DoD

- [ ] Kood on kirjutatud ja töötab
- [ ] Kus võimalik, on lisatud üksuse- või integratsioonitestid (`pytest` või Node-poolne smoke-test)
- [ ] Kõik olemasolevad testid läbivad (`pytest` ilma vigadeta)
- [ ] JS-failid `node --check`-iga puhtad
- [ ] Linter on puhas (`ruff check .`)
- [ ] Pull request on tehtud feature-harust ja review'tud
- [ ] Squash-merge on tehtud `main`-harule
- [ ] Commit-sõnumid järgivad konventsiooni `#<issue-number>: <imperative summary>`
- [ ] Tracker-kaart on **Done**-veerus

## Iteratsiooni DoD

- [ ] Kõik selle iteratsiooni kaardid on **Done**-veerus
- [ ] Iteratsiooni dokument `docs/iterations/iteration-N-*.md` on uuendatud kokkuvõttega
- [ ] Käivitusjuhend töötab värskel kloonil (`./start.sh` viib serveri pordile 8005)
- [ ] GitHub Pages deploy on edukas (vt Actions vahekaarti)
- [ ] Kasutaja on iteratsiooni läbi vaadanud ja kinnitanud

## Projekti DoD

- [ ] README sisaldab kõiki nõudefailis loetletud peatükke
- [ ] `prompts/question-generation.md` on dokumenteeritud
- [ ] Vähemalt 3 näidisülesannet `input/`-kaustas, igaüks koos `questions.json`-iga
- [ ] `docs/retrospective.md` on täidetud (mis õnnestus, mis oli keeruline)
- [ ] Lõppdemo on saadaval avaliku URL-i kaudu (<https://urmasrehkalt.github.io/millionaire/>)
- [ ] Tracker-tahvel ja koodirepo on sünkroonis

## Üldised reeglid

- **Mitte kunagi** ei pushi otse `main`-harule. Iga muudatus tuleb feature-harust
  pull request'iga
- Iga commit tuleb siduda issue/kaardi numbriga (`#4: ...`, `#7: ...`) commit-sõnumis
- Saladusi (`GEMINI_API_KEY`) ei tohi commit'ida — kasuta `.env` (`.gitignore`-is)
- Scope control: ühe kaardi raames ei refaktoreerita teemaväliseid faile
