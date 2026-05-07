# Product Backlog — Miljonimäng

See dokument on Trello tahvli **allikas**: kasutajalood ja arendusülesanded
hoitakse koodirepos failina, et need oleksid versionihalduses ja mitte ainult
Trellos. Trello tahvel peegeldab seda dokumenti — kaardid kopeeritakse
[`trello-cards.md`](trello-cards.md) failist.

Töövoog: **Backlog → Todo → In progress → Review/Test → Done**

---

## Kasutajalood

### US1 — Ülesannete nimekirja kuvamine

> Õppijana tahan näha ülesannete nimekirja, et saaksin valida, millise ülesande
> kohta mängu mängida.

**Vastuvõtutingimused:**

- Avalehel kuvatakse kõik `input/`-kausta numbrilised alamkaustad (001, 002, …)
- Iga ülesande kohta on näha number ja pealkiri (`assignment.md` H1-st)
- Kui pealkirja ei ole, kuvatakse vaikepealkirjana kausta number
- Nimekiri uueneb pärast brauseri värskendamist ilma serveri taaskäivitamiseta
- Mittenumbrilised kaustad (`.git`, `node_modules` jne) ignoreeritakse

**Iteratsioon:** 1 · **Sildid:** `feature`, `frontend`, `backend`

---

### US2 — Mängu mängimine

> Õppijana tahan vastata valikvastustega küsimustele, et kontrollida, kas saan
> lahendusest aru.

**Vastuvõtutingimused:**

- Pärast ülesande valikut käivitub mäng 15 küsimusega
- Igal küsimusel on täpselt 4 vastusevarianti
- Ainult üks vastus on õige
- Küsimused lähevad järjest keerulisemaks (5 lihtsat + 5 keskmist + 5 rasket)
- Hetkeseis (küsimuse number ja punktid) on alati ekraanil näha
- Vale vastusega mäng lõpeb ja punktid kukuvad turvatasemele
- Õige vastusega liigutakse järgmisele küsimusele

**Iteratsioon:** 1–2 · **Sildid:** `feature`, `frontend`, `backend`

---

### US3 — Selgituse kuvamine

> Õppijana tahan näha pärast vastamist selgitust, et mõista, miks vastus oli õige
> või vale.

**Vastuvõtutingimused:**

- Pärast iga vastust kuvatakse lühike selgitus (1–2 lauset)
- Selgitus tuleb AI vastusest (väli `explanation`)
- Mängu lõpus kuvatakse koondvaade vastatud küsimustest koos selgitustega

**Iteratsioon:** 1 (lõpus), 4 (iga küsimuse järel) · **Sildid:** `feature`, `frontend`

---

### US4 — Uue ülesande lisamine

> Õpetajana tahan lisada uusi ülesandeid `input/`-kausta, et sama rakendust saaks
> kasutada erinevate ülesannete valideerimiseks.

**Vastuvõtutingimused:**

- Uue numbrilise alamkausta loomine `input/`-i alla teeb ülesande mängitavaks
- Kausta sisus peab olema vähemalt `assignment.md`
- Lahendusfailid võivad olla suvalises struktuuris (sh alamkaustades)
- Rakenduse koodi muutmist ega taaskäivitamist ei nõuta
- Alamkaustad nagu `node_modules/`, `.git/`, `vendor/` jäetakse vaikimisi vahele
- Üle 32 KB suurused failid kärbitakse promptis

**Iteratsioon:** 1 · **Sildid:** `feature`, `backend`

---

### US5 — Igal mängul uued küsimused

> Õpetajana tahan, et küsimused oleksid iga kord erinevad, et õppija ei saaks
> lihtsalt vastuseid pähe õppida.

**Vastuvõtutingimused:**

- Kahe järjestikuse mängu küsimustest on vähemalt osa erinev
- AI päringus kasutatakse `temperature >= 0.7` ja muutuvat seed/nonce'i
- Kui AI tagastab dubleeritud küsimusi, korratakse päringut

**Iteratsioon:** 2 · **Sildid:** `feature`, `backend`, `ai`

---

## Lisafunktsioonid (parem hinne)

### US6 — Õlekõrred

> Õppijana tahan kasutada õlekõrri, et saaksin raskete küsimuste juures abi.

**Vastuvõtutingimused:**

- 3 õlekõrt: 50:50, AI vihje, küsi publikult
- Iga õlekõrs kasutatav ainult 1 kord mängu kohta
- 50:50 jätab alles 2 vastust, millest üks on õige
- AI vihje annab suunise, kuid ei ütle vastust otse
- Publik kuvab simuleeritud hääletustulemuse, kus õigel vastusel on suurem
  tõenäosus saada rohkem hääli (eriti lihtsamatel küsimustel)

**Iteratsioon:** 3 · **Sildid:** `feature`, `frontend`, `backend`, `ai`

---

### US7 — Mängu poolelijätmine ja jätkamine

> Õppijana tahan saada mängu pooleli jätta, et saaksin sellega hiljem jätkata
> ja oma punktid säiliksid.

**Vastuvõtutingimused:**

- Kasutaja saab nupuga „Lõpeta mäng" mängu lõpetada ja saavutatud punktid säilivad
- Mänguajalugu salvestatakse `localStorage`-isse
- Mänguajalugu kuvatakse avalehel

**Iteratsioon:** 4 · **Sildid:** `feature`, `frontend`

---

### US8 — Markdown ja koodivärvimine

> Õppijana tahan, et `assignment.md` ja küsimustes esinev kood oleksid loetavalt
> kuvatud.

**Vastuvõtutingimused:**

- `assignment.md` renderdatakse markdownina (mitte toorelt tekstina)
- Küsimustes ja vastustes esinev kood saab süntaksivärvimise (`highlight.js`)

**Iteratsioon:** 4 · **Sildid:** `feature`, `frontend`

---

### US9 — Küsimuste regenereerimine

> Õppijana tahan saada nupuga genereerida samale ülesandele uued küsimused, et
> ma saaksin uuesti proovida ilma teist ülesannet valimata.

**Vastuvõtutingimused:**

- Mängu lõpus on nupp „Mängi uuesti uute küsimustega"
- Nupp käivitab uue AI-päringu ja alustab mängu nullist

**Iteratsioon:** 4 · **Sildid:** `feature`, `frontend`, `backend`

---

## Arendusülesanded (technical tasks)

Need ei ole iseseisvad kasutajalood, aga on vajalikud kasutajalugude
realiseerimiseks. Trellos kuvatakse eraldi kaartidena.

| ID | Kirjeldus | Kasutajalugu | Iteratsioon |
|----|-----------|--------------|-------------|
| T01 | Projekti skelett, .gitignore, pyproject.toml, README | — | 0 |
| T02 | FastAPI rakendus + staatilise frontendi serveerimine | US1 | 1 |
| T03 | `assignment_loader.py` — input/-i lugemine | US1, US4 | 1 |
| T04 | API: `GET /api/assignments`, `GET /api/assignments/{id}` | US1 | 1 |
| T05 | Pydantic skeemid (Assignment, Question, GameSession) | US2 | 1 |
| T06 | `game_logic.py` — punktiastmed, turvatasemed, sessioonid | US2 | 1 |
| T07 | API: `POST /api/game/start`, `POST /api/game/answer` | US2 | 1 |
| T08 | Fallback-küsimused JSON-failis | US2 | 1 |
| T09 | Frontend: avalehe ülesannete nimekiri | US1 | 1 |
| T10 | Frontend: mänguvaade (küsimus + 4 vastust) | US2 | 1 |
| T11 | Frontend: tulemusvaade selgitustega | US3 | 1 |
| T12 | Prompt-fail `prompts/question-generation.md` | US2, US5 | 2 |
| T13 | OpenAI integratsioon `question_generator.py`-s | US2, US5 | 2 |
| T14 | `pydantic-settings` config + .env haldus | US2 | 2 |
| T15 | `lifelines.py` — 50:50, AI vihje, publik | US6 | 3 |
| T16 | API: `POST /api/game/lifeline` | US6 | 3 |
| T17 | Frontend: õlekõrte nupud + kasutusloogika | US6 | 3 |
| T18 | Markdown ja koodivärvimine frontendis | US8 | 4 |
| T19 | localStorage mänguajalugu | US7 | 4 |
| T20 | „Mängi uuesti" nupp ja regenereerimine | US9 | 4 |

---

## Testimine ja vastuvõtt

Vt [`testing-notes.md`](testing-notes.md) — iga iteratsiooni lõpus käime kõik
selle iteratsiooni vastuvõtutingimused läbi ja märgime tulemuse.
