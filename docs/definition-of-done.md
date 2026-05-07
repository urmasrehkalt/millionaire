# Definition of Done

Kasutajalood ja arendusülesanded loetakse valmis (Done), kui **kõik** alljärgnevad
tingimused on täidetud.

## Kasutajaloo DoD

- [ ] Kõik kasutajaloo vastuvõtutingimused on käsitsi testitud ja töötavad
- [ ] Testimise tulemus on lisatud faili `docs/testing-notes.md`
- [ ] Trello kaart on liigutatud veergu **Done**
- [ ] Funktsionaalsus on käivitatav `main`-harul (squash-merge tehtud)
- [ ] Vastav osa README-st (kui asjakohane) on uuendatud

## Arendusülesande (technical task) DoD

- [ ] Kood on kirjutatud ja töötab
- [ ] Kus võimalik, on lisatud üksuse- või integratsioonitestid (`pytest`)
- [ ] Kõik olemasolevad testid läbivad (`pytest` ilma vigadeta)
- [ ] Linter on puhas (`ruff check .`)
- [ ] Pull request on tehtud feature-harust ja review'tud
- [ ] Squash-merge on tehtud `main`-harule
- [ ] Commit-sõnumid järgivad konventsiooni `T<number>: <imperative summary>` või
      `US<number>: <imperative summary>`
- [ ] Trello kaart on **Done**-veerus

## Iteratsiooni DoD

- [ ] Kõik selle iteratsiooni kaardid on **Done**-veerus
- [ ] Iteratsiooni dokument `docs/iterations/iteration-N-*.md` on uuendatud kokkuvõttega
- [ ] Käivitusjuhend töötab värskel kloonil (`git clone`-st kuni `uvicorn`-ini)
- [ ] Kasutaja on iteratsiooni läbi vaadanud ja kinnitanud

## Projekti DoD

- [ ] README sisaldab kõiki nõudefailis loetletud peatükke
- [ ] `prompts/question-generation.md` on dokumenteeritud
- [ ] Vähemalt 3 näidisülesannet `input/`-kaustas
- [ ] `docs/retrospective.md` on täidetud (mis õnnestus, mis oli keeruline)
- [ ] Lõppdemo on salvestatud või dokumenteeritud
- [ ] Trello tahvel ja koodirepo on sünkroonis

## Üldised reeglid

- **Mitte kunagi** ei pushi otse `main`-harule. Iga muudatus tuleb feature-harust
  pull request'iga
- Iga commit tuleb siduda kaardi ID-ga (`T03`, `US2`, jne) commit-sõnumis
- Saladusi (`OPENAI_API_KEY`) ei tohi commit'ida — kasuta `.env`
- Scope control: ühe kaardi raames ei refaktoreerita teemaväliseid faile
