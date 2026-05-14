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
