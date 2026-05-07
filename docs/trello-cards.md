# Trello kaardid — kopeerimiseks

See fail sisaldab kõiki Trello kaarte valmis vormingus. Iga kaart on jaotatud
selgete sektsioonidega: **pealkiri**, **kirjeldus**, **vastuvõtutingimused** (kui
on), **sildid** ja **veerg**, kuhu kaart kuulub algselt.

## Kuidas kaardid Trellosse panna

1. Loo Trellos uus tahvel **„Miljonimäng"**
2. Loo veerud: **Backlog**, **Todo**, **In progress**, **Review/Test**, **Done**
3. Loo igale alljärgnevale kaardile uus Trello kaart:
   - Pealkiri = `Pealkiri:` rida
   - Kirjeldus = kaardi kogu sisu (kirjeldus + AC + sildid)
   - Sildid = lisa Trellos värvilised sildid (`feature` = roheline,
     `bug` = punane, `docs` = sinine, `ai` = lilla, `frontend` = kollane,
     `backend` = oranž)
4. Kaart algse veergu vastavalt rea **Veerg:** väärtusele
5. Iteratsioon = lisa Trellos kaardile sama nimega silt (`iter-0`, `iter-1`, jne)

---

## Kasutajalood (Epic-tüüpi kaardid)

### Kaart 1

**Pealkiri:** [US1] Õppijana tahan näha ülesannete nimekirja

**Kirjeldus:**
Õppijana tahan näha ülesannete nimekirja, et saaksin valida, millise ülesande
kohta mängu mängida.

**Vastuvõtutingimused:**
- Avalehel kuvatakse kõik `input/`-kausta numbrilised alamkaustad
- Iga ülesande kohta on näha number ja pealkiri (`assignment.md` H1-st)
- Kui pealkirja ei ole, kuvatakse vaikepealkirjana kausta number
- Nimekiri uueneb pärast brauseri värskendamist ilma serveri taaskäivitamiseta
- Mittenumbrilised kaustad ignoreeritakse

**Sildid:** feature, frontend, backend, iter-1
**Veerg:** Backlog

---

### Kaart 2

**Pealkiri:** [US2] Õppijana tahan vastata valikvastustega küsimustele

**Kirjeldus:**
Õppijana tahan vastata valikvastustega küsimustele, et kontrollida, kas saan
lahendusest aru.

**Vastuvõtutingimused:**
- Pärast ülesande valikut käivitub mäng 15 küsimusega
- Igal küsimusel on täpselt 4 vastusevarianti, üks neist õige
- Küsimused lähevad järjest keerulisemaks (5 lihtsat + 5 keskmist + 5 rasket)
- Hetkeseis (küsimuse number ja punktid) on alati ekraanil näha
- Vale vastusega mäng lõpeb ja punktid kukuvad turvatasemele
- Õige vastusega liigutakse järgmisele küsimusele

**Sildid:** feature, frontend, backend, iter-1, iter-2
**Veerg:** Backlog

---

### Kaart 3

**Pealkiri:** [US3] Õppijana tahan näha selgitust pärast vastamist

**Kirjeldus:**
Õppijana tahan näha pärast vastamist selgitust, et mõista, miks vastus oli õige
või vale.

**Vastuvõtutingimused:**
- Pärast iga vastust kuvatakse lühike selgitus (1–2 lauset)
- Selgitus tuleb AI vastusest (`explanation` väli)
- Mängu lõpus kuvatakse koondvaade vastatud küsimustest selgitustega

**Sildid:** feature, frontend, iter-1, iter-4
**Veerg:** Backlog

---

### Kaart 4

**Pealkiri:** [US4] Õpetajana tahan lisada uusi ülesandeid input/-kausta

**Kirjeldus:**
Õpetajana tahan lisada uusi ülesandeid `input/`-kausta, et sama rakendust saaks
kasutada erinevate ülesannete valideerimiseks.

**Vastuvõtutingimused:**
- Uue numbrilise alamkausta loomine teeb ülesande mängitavaks
- Kausta sisus peab olema vähemalt `assignment.md`
- Lahendusfailid suvalises struktuuris, sh alamkaustades
- Rakenduse koodi muutmist ega taaskäivitamist ei nõuta
- `node_modules/`, `.git/`, `vendor/` jäetakse vahele
- Üle 32 KB suurused failid kärbitakse promptis

**Sildid:** feature, backend, iter-1
**Veerg:** Backlog

---

### Kaart 5

**Pealkiri:** [US5] Õpetajana tahan, et küsimused oleksid iga kord erinevad

**Kirjeldus:**
Õpetajana tahan, et küsimused oleksid iga kord erinevad, et õppija ei saaks
lihtsalt vastuseid pähe õppida.

**Vastuvõtutingimused:**
- Kahe järjestikuse mängu küsimustest on vähemalt osa erinev
- AI päringus kasutatakse `temperature >= 0.7` ja muutuvat seed/nonce'i
- Dubleeritud küsimuste korral korratakse päringut

**Sildid:** feature, backend, ai, iter-2
**Veerg:** Backlog

---

### Kaart 6

**Pealkiri:** [US6] Õppijana tahan kasutada õlekõrri

**Kirjeldus:**
Õppijana tahan kasutada õlekõrri, et saaksin raskete küsimuste juures abi.

**Vastuvõtutingimused:**
- 3 õlekõrt: 50:50, AI vihje, küsi publikult
- Iga õlekõrs kasutatav 1 kord mängu kohta
- 50:50 jätab alles 2 vastust, millest üks on õige
- AI vihje annab suunise, ei ütle vastust otse
- Publiku tulemus on kallutatud nii, et õigel vastusel on suurem tõenäosus saada
  rohkem hääli (eriti lihtsamatel küsimustel)

**Sildid:** feature, frontend, backend, ai, iter-3
**Veerg:** Backlog

---

### Kaart 7

**Pealkiri:** [US7] Õppijana tahan mängu pooleli jätta

**Kirjeldus:**
Õppijana tahan saada mängu pooleli jätta, et saaksin sellega hiljem jätkata ja
oma punktid säiliksid.

**Vastuvõtutingimused:**
- Nupp „Lõpeta mäng" säilitab saavutatud punktid
- Mänguajalugu salvestub `localStorage`-isse
- Mänguajalugu kuvatakse avalehel

**Sildid:** feature, frontend, iter-4
**Veerg:** Backlog

---

### Kaart 8

**Pealkiri:** [US8] Markdown ja koodivärvimine

**Kirjeldus:**
Õppijana tahan, et `assignment.md` ja küsimustes esinev kood oleksid loetavalt
kuvatud.

**Vastuvõtutingimused:**
- `assignment.md` renderdatakse markdownina
- Küsimustes ja vastustes esinev kood saab süntaksivärvimise

**Sildid:** feature, frontend, iter-4
**Veerg:** Backlog

---

### Kaart 9

**Pealkiri:** [US9] Küsimuste regenereerimine

**Kirjeldus:**
Õppijana tahan saada nupuga genereerida samale ülesandele uued küsimused, et
saaksin uuesti proovida ilma teist ülesannet valimata.

**Vastuvõtutingimused:**
- Mängu lõpus on nupp „Mängi uuesti uute küsimustega"
- Nupp käivitab uue AI-päringu ja alustab mängu nullist

**Sildid:** feature, frontend, backend, iter-4
**Veerg:** Backlog

---

## Arendusülesanded (Tasks)

### Kaart T01

**Pealkiri:** [T01] Projekti skelett, .gitignore, pyproject.toml, README

**Kirjeldus:**
Loo projekti algfailid: `.gitignore`, `.env.example`, `pyproject.toml`, `README.md`
skelett, `docs/` kataloog dokumentidega.

**Sildid:** docs, iter-0
**Veerg:** Done (Iteratsioon 0 lõpetuseks)

---

### Kaart T02

**Pealkiri:** [T02] FastAPI rakendus + staatilise frontendi serveerimine

**Kirjeldus:**
Loo `backend/app/main.py` FastAPI rakendusega, mis serveerib ka
`frontend/`-kausta staatiliste failidena `StaticFiles` kaudu.

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T03

**Pealkiri:** [T03] assignment_loader.py — input/-kausta lugemine

**Kirjeldus:**
Loo teenus, mis loeb `input/`-i numbrilisi alamkaustu, parsib `assignment.md`
H1-pealkirja, koondab kõik failid (sh alamkaustades) tekstiks. Ignoreerib
`node_modules/`, `.git/`, `vendor/` ja binaarfaile suurusega >32 KB.

**Vastuvõtutingimused:**
- Funktsioon `list_assignments()` tagastab kõigi ülesannete metaandmed
- Funktsioon `load_assignment(id)` tagastab konkreetse ülesande sisu (assignment.md
  + lahendusfailid)
- Mittenumbrilised alamkaustad jäetakse vahele
- Kataloogiraja-libisemise rünnakud (path traversal) on välistatud

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T04

**Pealkiri:** [T04] API: assignments endpoint'id

**Kirjeldus:**
Loo FastAPI marsruudid:
- `GET /api/assignments` — kõigi ülesannete nimekiri
- `GET /api/assignments/{id}` — konkreetne ülesanne sisuga

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T05

**Pealkiri:** [T05] Pydantic skeemid

**Kirjeldus:**
Loo `backend/app/models/schemas.py` järgmiste mudelitega:
- `Assignment`, `AssignmentSummary`
- `Question`, `QuestionLevel`
- `GameSession`, `GameStatus`
- `AnswerRequest`, `AnswerResponse`

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T06

**Pealkiri:** [T06] game_logic.py — punktiastmed, turvatasemed, sessioonid

**Kirjeldus:**
Mängu olek hoitakse mälusiseses `dict[session_id, GameSession]`-is. Punktiastmed
on hardcode'itud massiivina, turvatasemed indekseeritakse (4, 9, 14).

**Vastuvõtutingimused:**
- Vale vastusega kukub punktid eelmisele turvatasemele
- 15. küsimuse õige vastus annab 1 000 000 punkti

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T07

**Pealkiri:** [T07] API: game endpoint'id

**Kirjeldus:**
- `POST /api/game/start` — alustab mängu, tagastab session_id ja esimese küsimuse
- `POST /api/game/answer` — kontrollib vastust, tagastab tulemuse + järgmise küsimuse

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T08

**Pealkiri:** [T08] Fallback-küsimused JSON-failis

**Kirjeldus:**
Loo `backend/app/services/fallback_questions.json` 15 staatilise küsimusega
ülesande 001 (JS-kalkulaator) kohta. Kasutatakse, kui `OPENAI_API_KEY` puudub
või API-päring ebaõnnestub.

**Sildid:** backend, iter-1
**Veerg:** Todo

---

### Kaart T09

**Pealkiri:** [T09] Frontend: avalehe ülesannete nimekiri

**Kirjeldus:**
HTML + CSS + JS, mis küsib `GET /api/assignments` ja kuvab nimekirja klikkitavate
kaartidena.

**Sildid:** frontend, iter-1
**Veerg:** Todo

---

### Kaart T10

**Pealkiri:** [T10] Frontend: mänguvaade

**Kirjeldus:**
Küsimuse tekst, 4 nupplikku vastust, hetkene punktisumma, küsimuse number
(„X/15"), punktiastmete tabel paremal serval (klassikaline miljonimängu vaade).

**Sildid:** frontend, iter-1
**Veerg:** Todo

---

### Kaart T11

**Pealkiri:** [T11] Frontend: tulemusvaade selgitustega

**Kirjeldus:**
Mängu lõpus kuvatakse saavutatud punktid, kõik vastatud küsimused koos õige
vastuse ja selgitusega.

**Sildid:** frontend, iter-1
**Veerg:** Todo

---

### Kaart T12

**Pealkiri:** [T12] Prompt-fail prompts/question-generation.md

**Kirjeldus:**
Dokumenteeri AI-prompt eraldi failis (nõudefaili kohustuslik nõue). Prompt
kirjeldab raskusastmeid, JSON-skeemi, selgituse nõuet, eestikeelsust.

**Sildid:** ai, docs, iter-2
**Veerg:** Todo

---

### Kaart T13

**Pealkiri:** [T13] OpenAI integratsioon

**Kirjeldus:**
`question_generator.py` reaalne versioon kasutab `openai.chat.completions.create`
koos `response_format={"type": "json_object"}`. Vastus valideeritakse Pydanticuga,
vea korral langetakse fallback-i.

**Sildid:** ai, backend, iter-2
**Veerg:** Todo

---

### Kaart T14

**Pealkiri:** [T14] pydantic-settings config + .env haldus

**Kirjeldus:**
`backend/app/config.py` loeb `.env` faili ja annab tüübitud Settings-objekti.
Hoiatus, kui `OPENAI_API_KEY` puudub.

**Sildid:** backend, iter-2
**Veerg:** Todo

---

### Kaart T15

**Pealkiri:** [T15] lifelines.py — 50:50, vihje, publik

**Kirjeldus:**
- `fifty_fifty(question)` — eemaldab juhuslikult 2 valet vastust
- `ai_hint(question, assignment)` — eraldi OpenAI päring, mis annab vihje ilma vastust ütlemata
- `audience_poll(question, level)` — kallutatud juhuslik jaotus 4 vastuse vahel

**Sildid:** ai, backend, iter-3
**Veerg:** Todo

---

### Kaart T16

**Pealkiri:** [T16] API: POST /api/game/lifeline

**Kirjeldus:**
Endpoint, mis võtab `session_id` ja `lifeline_type` ning tagastab vastava
õlekõrre tulemuse. Igat õlekõrt saab kasutada 1 kord — kontroll backend'is.

**Sildid:** backend, iter-3
**Veerg:** Todo

---

### Kaart T17

**Pealkiri:** [T17] Frontend: õlekõrte nupud

**Kirjeldus:**
Mänguvaate kõrvale 3 nuppu õlekõrtega. Kasutatud nupp tehakse hallikks. Tulemus
kuvatakse modaal-aknas või sisselülitatud vastusenuppude muutmise kaudu (50:50).

**Sildid:** frontend, iter-3
**Veerg:** Todo

---

### Kaart T18

**Pealkiri:** [T18] Markdown ja koodivärvimine frontendis

**Kirjeldus:**
Lisa `marked` ja `highlight.js` CDN-ist. `assignment.md` renderdatakse markdownina
enne mängu algust. Küsimustes esinev kood saab `<pre><code class="language-...">`
ümbrise.

**Sildid:** frontend, iter-4
**Veerg:** Todo

---

### Kaart T19

**Pealkiri:** [T19] localStorage mänguajalugu

**Kirjeldus:**
Iga mängu lõpus salvestatakse tulemus brauseri `localStorage`-isse. Avalehel on
nupp „Mänguajalugu", mis kuvab varasemate mängude tulemused.

**Sildid:** frontend, iter-4
**Veerg:** Todo

---

### Kaart T20

**Pealkiri:** [T20] „Mängi uuesti" nupp ja regenereerimine

**Kirjeldus:**
Tulemusvaates nupp, mis käivitab uue mängu samale ülesandele. Backend genereerib
uued küsimused (mitte ei kasuta vanu).

**Sildid:** frontend, backend, iter-4
**Veerg:** Todo
