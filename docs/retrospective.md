# Retrospektiiv

> Vahetagasivaade pärast iteratsiooni 6 (issue'd #1–#8). Täiendatakse projekti
> lõpus ja iga järgmise iteratsiooni järel.

## Mis õnnestus

- **Iteratiivne arendus** — 7 iteratsiooni, igaüks suletud ühe PR-iga
  squash-merge'iga. Funktsionaalsuse evolutsioon (fallback → AI per game →
  küsimusepank → static demo) toimus järk-järgult, mitte ühe suure
  rewrite'iga.
- **Arhitektuuri kihtide selge eraldatus** — kui issue #4 muutis mängu
  loogika küsimusepanga-põhiseks ja issue #6 viis mängu loogika brauserisse,
  oli tänu Pydantic-skeemidele ja `api.js`-i façade'ile muutus väike ja
  mõjus tehniliselt elegantne. Frontend ei tea, kas mängu loogika jookseb
  backend'is või brauseris.
- **Definition of Done** hoidis kvaliteedi ühtlase — iga PR sisaldas testid,
  vastuvõtutestid, dokumentatsiooni-uuendused.
- **Tasuta AI free tier** (Gemini 2.5 Flash) sobis õppeotstarbeks ideaalselt,
  ei vajanud arvelduse seadistamist.
- **GitHub Pages deploy** tegi projekti reaalselt jagatavaks — õpilane saab
  lingi ja proovib kohe, mitte „klooni repo ja installi Python".
- **Kahekordne loogika (engine.js + game_logic.py)** võiks tunduda topelttöö,
  kuid see hoiab kaks režiimi ühilduvana ja annab võimaluse Python-poolt
  pytestidega kindlustada.

## Mis oli keeruline

- **AI-küsimuste kvaliteet** — esimesed Gemini päringud tagastasid liiga
  triviaalseid küsimusi („Mis on fail nimi?"). Lahendus: prompti kohendati
  kahel-kolmel iteratsioonil. Pikem küsimuste stiil (miljonimängu
  kontekstilausetega) + lühikesed vastusevariandid (1–3 sõna) — see oli
  reegel, mida Gemini vajas konkreetsete näidetega.
- **JSON-skeemi peensused** Gemini API-s — `enum` ja `type` ei saa olla
  korraga, `min_items`/`max_items` peavad olema all-lowercase. Iter-3 algas
  väikese bugfixiga (#3).
- **Kõmusõnastus „backend"** ja sellised vahepealsed olemine eesti UI-s.
  Sõnastuse lihv (#8) võttis aega kaalukate sõnade valimisega
  („Punktisumma" vs „Sinu skoor" vs „Hetkeseis").
- **GitHub Pages aktiveerimine privaatses reposes** — `GITHUB_TOKEN`-il
  pole õigust Pages-i lubada. Vaja oli kasutaja PAT-i kaudu API kutset.
  Lahendus: `enablement: true` workflow-is + esmane manuaalne aktiveerimine.
- **Algse plaani „pause and resume" (US7)** — selgus, et päris miljonimängus
  saab lihtsalt walk away. Implementeerisime selle vastavalt, mitte algse
  plaani järgi. Plaan tuleb tihti mängu enda käigus üle vaadata.

## Mida järgmises iteratsioonis parandada

- **Mänguajalugu** (`localStorage`) — kasutaja tahaks näha varasemate mängude
  punktisummasid. Suhteliselt väike töö, kasutaja jaoks suur väärtus (US14).
- **Markdown + koodivärvimine** (US8) — `assignment.md` praegu mainimist
  ei saa; kui kasutaja vajutaks „vaata ülesannet", oleks loetav markdown
  hea lisand.
- **Hetkel kasutamata `backend/app/routes/game.py`** — peale iter-5 ei kutsu
  frontend enam server-poolset mängu loogikat. Kood jääb, kuid lisab
  kontekstilist „mis-on-mis" küsimust. Otsustada: kustutada või
  dokumenteerida selgemalt.
- **Test coverage Node smoke-testidele** — praegu on `/tmp/`-is mitu
  smoke-test skripti, mis pole versionihalduses. Vaja need viia
  `frontend/tests/`-i (pole prioriteet, aga aitaks regressioonide vältimisel).
- **Õpetaja vaade** (US15) — õpilaste statistikat, küsimuste muutmist
  ilma kogu panka uuesti generaerimata.

## Vastuvõtutingimused — kokkuvõte

Nõudefaili miinimumnõuded arvestuseks:

| Nõue | Olek | Märkused |
|------|------|----------|
| `input/`-kaustas saab olla mitu ülesannet | ✅ | 3 olemas; numbriline alamkaust |
| Iga ülesanne eraldi numbrilises alamkaustas | ✅ | `001`, `002`, `003` |
| Rakendus kuvab ülesannete valiku | ✅ | Avalehe grid + manifest |
| Rakendus loeb `assignment.md` faili | ✅ | Uue teema loomisel — Gemini-le saadetakse |
| Rakendus loeb vähemalt ühe lahenduse faili | ✅ | `assignment_loader.py` kogub kõik |
| Rakendus genereerib ≥ 15 küsimust | ✅ | 50 küsimusega pank, mängu valitakse 15 |
| Mängus on 4 vastusevarianti | ✅ | Skeem valideerib |
| Mäng kontrollib õiget ja valet vastust | ✅ | `engine.submitAnswer` |
| Vale vastuse korral mäng lõpeb | ✅ | Status „lost", skoor turvatasemele |
| Tulemus kuvatakse kasutajale | ✅ | Tulemus­vaade selgitustega |
| README sisaldab käivitamise juhiseid | ✅ | „Käivitamise juhend" peatükk |

## Lisafunktsioonid

| Funktsioon | Olek | Märkused |
|------------|------|----------|
| Päris AI API ühendus | ✅ | Gemini 2.5 Flash (free tier) |
| Küsimuste salvestamine vahemällu | ✅ | `input/<id>/questions.json` panga­põhine |
| Võimalus küsimused uuesti genereerida | ✅ | „Proovi sama ülesannet uuesti" valib uue komplekti pangast |
| Tulemuste salvestamine | ⬜ | Plaanis US14 |
| Mänguajalugu | ⬜ | Plaanis US14 |
| Õpetaja vaade | ⬜ | Plaanis US15 |
| Markdown ilus kuvamine | ⬜ | Plaanis US8 |
| Süntaksivärvimine | ⬜ | Plaanis US8 |
| Õlekõrred | ✅ | 50:50, Vihje, Vaheta küsimus |
| Selgituse kuvamine pärast vastamist | ✅ (lõpus) | Iga küsimuse järel — võiks lisada iteratsioonis 7+ |
| Avalik demo | ✅ | <https://urmasrehkalt.github.io/millionaire/> |
