# Product Backlog — Miljonimäng

> Viimati uuendatud: 2026-05-14 (issue'd #1–#8 main-il).

See dokument on projekti backlogi **allikas**. Töötahvel
(`urmas-agiilne-tracker`, localhost:8000) peegeldab seda — kaardid kopeeriti
algselt [`trello-cards.md`](trello-cards.md)-st ja on edaspidi sünkroonis
issue-numbritega (`#1`, `#2`, …).

Töövoog: **Backlog → Todo → In progress → Review/Test → Done**

## Olek lühidalt

| ID | Lugu | Olek | PR / Issue |
|----|------|------|------------|
| US1 | Ülesannete nimekiri | ✅ Done | #1 (iter-1) |
| US2 | Mängu mängimine 15 küsimusega | ✅ Done | #1, #2, #4 |
| US3 | Selgituse kuvamine | ✅ Done (tulemusvaates) | #1 |
| US4 | Uue ülesande lisamine `input/`-i | ✅ Done | #1 |
| US5 | Igal mängul (osaliselt) uued küsimused | ✅ Done | #4 (juhuslik valik pangast) |
| US6 | Õlekõrred (50:50, vihje, vaheta) | ✅ Done | #4, #5 |
| US7 | Mängu pooleli jätmine („walk away") | ✅ Done | #7 |
| US8 | Markdown ja koodivärvimine | ⬜ Backlog | — |
| US9 | Mängu uuesti alustamine | ✅ Done (lihtne play-again nupp) | #5 |
| US10 | AI-genereeritud küsimusepank teema kohta | ✅ Done | #4 |
| US11 | Veebist uue teema loomine AI abil | ✅ Done | #4 |
| US12 | Avalik demo (GitHub Pages) | ✅ Done | #6 |
| US13 | Eestikeelne UI lihv | ✅ Done | #8 |
| US14 | Mänguajalugu (localStorage) | ⬜ Backlog | — |
| US15 | Õpetaja vaade | ⬜ Backlog | — |

## Kasutajalood

### US1 — Ülesannete nimekirja kuvamine ✅

> Õppijana tahan näha ülesannete nimekirja, et saaksin valida, millise ülesande
> kohta mängu mängida.

**Vastuvõtutingimused:**

- Avalehel kuvatakse kõik teemad `assignments.json` manifesti põhjal
- Iga teema kohta on näha ID ja pealkiri (`assignment.md` H1-st)
- CI regenereerib manifesti igal `main`-i push'iga
- Mittenumbrilised kaustad ignoreeritakse

### US2 — Mängu mängimine ✅

> Õppijana tahan vastata valikvastustega küsimustele, et kontrollida, kas saan
> lahendusest aru.

**Vastuvõtutingimused:**

- Pärast ülesande valikut käivitub mäng 15 küsimusega
- Igal küsimusel on täpselt 4 vastusevarianti, üks õige
- Küsimused on jaotatud 5 lihtsat + 5 keskmist + 5 rasket (raskenev järjekord)
- Hetkeseis (küsimuse number ja punktid) on alati ekraanil näha
- Vale vastusega mäng lõpeb ja punktid kukuvad turvatasemele
- Õige vastusega liigutakse järgmisele küsimusele

### US3 — Selgituse kuvamine ✅

> Õppijana tahan näha pärast vastamist selgitust, et mõista, miks vastus oli
> õige või vale.

**Vastuvõtutingimused:**

- Pärast iga vastust kuvatakse lühike selgitus (1–2 lauset)
- Selgitus tuleb küsimuse `explanation`-väljast
- Mängu lõpus kuvatakse koondvaade vastatud küsimustest selgitustega

### US4 — Uue ülesande lisamine ✅

> Õpetajana tahan lisada uusi ülesandeid `input/`-kausta, et sama rakendust
> saaks kasutada erinevate ülesannete valideerimiseks.

**Vastuvõtutingimused:**

- Uue numbrilise alamkausta loomine teeb ülesande mängitavaks
- Kausta sisus peab olema vähemalt `assignment.md` ja `questions.json`
- Veebivormi kaudu (lokaalses dev'is) saab kogu sammu automaatselt teha — vt
  [US11](#us11--ai-abil-uue-teema-loomine-veebist-)

### US5 — Igal mängul (osaliselt) uued küsimused ✅

> Õpetajana tahan, et küsimused oleksid iga kord (vähemalt osaliselt) erinevad,
> et õppija ei saaks lihtsalt vastuseid pähe õppida.

**Vastuvõtutingimused:**

- Iga mängu alguses valitakse 50 küsimusega pangast juhuslikult 5+5+5
- Sama teemat järjest mängides on tõenäosus, et osad küsimused korduvad,
  vähene (50/15 ≈ 30% kattuvus)

### US6 — Õlekõrred ✅

> Õppijana tahan kasutada õlekõrri, et saaksin raskete küsimuste juures abi.

**Vastuvõtutingimused:**

- 3 õlekõrt: **50 : 50**, **Vihje**, **Vaheta küsimus**
- Iga õlekõrs kasutatav 1 kord mängu kohta
- 50 : 50 jätab alles 2 vastust, üks õige
- Vihje tagastab küsimuse `hint`-välja sisu (ilma vastust ütlemata)
- Vaheta küsimus asendab praeguse küsimuse sama raskustaseme reservküsimusega

> **Märkus:** algses plaanis oli kolmas õlekõrs „Küsi publikult". Asendati
> „Vaheta küsimusega" — see sobib küsimusepanga mudeliga paremini ega vaja
> jooksvalt AI-d.

### US7 — Mängu lõpetamine (walk-away) ✅

> Õppijana tahan saada mängu igal hetkel lõpetada ja teenitud punktidega
> lahkuda.

**Vastuvõtutingimused:**

- „Lõpeta mäng" nupp on alati nähtaval mängu vaates
- Klikk kuvab kinnitusdialoogi punktisummaga
- Kinnitusel suunatakse tulemusvaatesse staatuse „quit" ja viimase teenitud
  skooriga (mitte turvatase)

### US8 — Markdown ja koodivärvimine ⬜

> Õppijana tahan, et `assignment.md` ja küsimustes esinev kood oleksid
> loetavalt kuvatud.

**Vastuvõtutingimused:**

- `assignment.md` renderdatakse markdownina enne mängu algust
- Küsimustes esinev kood saab süntaksivärvimise (`highlight.js`)

### US9 — Mängu uuesti alustamine ✅

> Õppijana tahan mängu lõpus saada sama ülesannet kohe uuesti proovida.

**Vastuvõtutingimused:**

- Tulemusvaates on nupp „Proovi sama ülesannet uuesti"
- Klikk käivitab uue mängu (uus küsimuste valik pangast)

### US10 — Küsimusepank teema kohta ✅

> Õpetajana tahan, et iga teema küsimused oleksid eelnevalt salvestatud, et
> mäng ei nõuaks iga alustamisel AI-päringut.

**Vastuvõtutingimused:**

- Iga teema kaustas on `questions.json` (50 küsimusega)
- Pangas on vähemalt 5 küsimust iga raskustaseme kohta (valideeritud
  laadimisel)
- Mängu alguses ei tehta AI-päringut

### US11 — AI abil uue teema loomine veebist ✅

> Õpetajana tahan luua uue teema otse rakendusest, et ma ei peaks
> JSON-i käsitsi koostama.

**Vastuvõtutingimused:**

- Avalehel on vorm „Lisa uus teema" (pealkiri + kirjeldus)
- Vajab töötavat `GEMINI_API_KEY`-d (lokaalne arendus)
- Loob `input/<id>/assignment.md` ja `input/<id>/questions.json` 50 küsimusega
- Pärast loomist kuvatakse uus teema kohe menüüs
- GitHub Pages režiimis vorm peidetakse

### US12 — Avalik demo ✅

> Õpetajana tahan jagada lihtsalt linki, et õppijad ja kaaslased saaksid
> rakendust proovida ilma keskkonda seadistamata.

**Vastuvõtutingimused:**

- `main`-i push deploy-b GitHub Pages-isse
- URL: <https://urmasrehkalt.github.io/millionaire/>
- Mäng töötab täielikult ilma serverita
- AI-uue-teema vorm peidetakse (selge selgitus, kuidas seda saaks)

### US13 — Eestikeelne UI lihv ✅

> Õppijana tahan, et UI sõnastus oleks loomulik ja eestikeelne, mitte
> kohmakate suhtelausetega.

**Vastuvõtutingimused:**

- Iga visiibel string käsitsi üle loetud
- „komandorida" → „käsurida" (modernne eesti keel)
- Verdiktid kasutavad korrektset eesti grammatikat („Mäng on läbi", mitte
  „Mäng läbi")

### US14 — Mänguajalugu ⬜

> Õppijana tahan näha varasemate mängude tulemusi, et jälgida edusamme.

### US15 — Õpetaja vaade ⬜

> Õpetajana tahan hallata teemasid ja näha õppijate tulemusi (sh statistikat).

## Arendusülesanded — ajalooline kokkuvõte

Algselt kavandatud T01–T20 enamus realiseeriti, kuid arhitektuuri muutused
(`#4` küsimusepank ja `#6` GitHub Pages) muutsid mõned ülesanded mittevajalikuks
ja tõid uued juurde. Allpool on lihtsustatud kaardistus PR-ide kaupa —
detailne lugu igast iteratsioonist on failis [`iterations/`](iterations/).

| Issue | Mis tehti | Iteratsiooni dokument |
|-------|-----------|----------------------|
| #1 | FastAPI MVP, mänguvoog fallback-küsimustega, 3 näidisülesannet | [iter-1](iterations/iteration-1-mvp.md) |
| #2 | Gemini API integratsioon (T12–T14) | [iter-2](iterations/iteration-2-ai.md) |
| #3 | Gemini JSON-skeemi `min/max_items` parandus | (väike bugfix, vt git log) |
| #4 | Küsimusepank, 50-küsimusega `questions.json`, vaheta-õlekõrs | [iter-3](iterations/iteration-3-question-banks.md) |
| #5 | UI moderniseerimine (must-kuld teema, animatsioonid) | [iter-4](iterations/iteration-4-ui-modernization.md) |
| #6 | Client-side engine, GitHub Pages deploy | [iter-5](iterations/iteration-5-github-pages.md) |
| #7 | „Lõpeta mäng" walk-away nupp | [iter-6](iterations/iteration-6-quit-and-polish.md) |
| #8 | Eesti keele lihv kogu UI-s | [iter-6](iterations/iteration-6-quit-and-polish.md) |

## Testimine ja vastuvõtt

Vt [`testing-notes.md`](testing-notes.md) — iga iteratsiooni lõpus käime selle
iteratsiooni vastuvõtutingimused läbi ja märgime tulemuse.
