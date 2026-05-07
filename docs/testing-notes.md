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

(Täidetakse iteratsiooni lõpus.)

| Test | Tulemus | Märkused |
|------|---------|----------|
| **US1** Avaleht kuvab kõik input/-i ülesanded | ☐ | |
| **US1** Pealkiri tuleb assignment.md H1-st | ☐ | |
| **US1** Mittenumbrilised kaustad ignoreeritakse | ☐ | |
| **US2** Mäng käivitub ja kuvab 15 küsimust | ☐ | |
| **US2** Igal küsimusel on 4 vastusevarianti | ☐ | |
| **US2** Hetkeseis on alati näha | ☐ | |
| **US2** Vale vastus lõpetab mängu | ☐ | |
| **US3** (lõpus) Vastatud küsimused kuvatakse selgitustega | ☐ | |
| **US4** Uue input/004/ lisamine teeb selle mängitavaks ilma serveri restartita | ☐ | |
| Üksusetestid (`pytest`) läbivad | ☐ | |

## Iteratsioon 2 — AI

(Täidetakse iteratsiooni lõpus.)

| Test | Tulemus | Märkused |
|------|---------|----------|
| Päris OpenAI API-ühendus tagastab valiidse JSON-i | ☐ | |
| Prompt asub failis `prompts/question-generation.md` | ☐ | |
| **US5** Kahe järjestikuse mängu küsimustest on vähemalt osa erinev | ☐ | |
| Puuduva API-võtme korral kasutatakse fallback'i | ☐ | |

## Iteratsioon 3 — Õlekõrred

(Täidetakse iteratsiooni lõpus.)

## Iteratsioon 4 — Poleerimine

(Täidetakse iteratsiooni lõpus.)
