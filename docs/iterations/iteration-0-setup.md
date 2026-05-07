# Iteratsioon 0 — Setup

**Periood:** 2026-05-07 — 2026-05-07 (1 päev)
**Eesmärk:** projekti elustamine, dokumentide ja Trello tahvli ettevalmistus.

## Sprindi sisu

Selle iteratsiooni jooksul ei kirjutatud rakenduse koodi — keskendusime
arendusprotsessi alusele. Hindamiskriteeriumide järgi peab olema enne arendust
„koostatud vähemalt üks planeerimise dokument", olema „nähtav ja arusaadav
product backlog" ja kirjeldatud Definition of Done.

## Tegevused

| Kaart | Tegevus | Olek |
|-------|---------|------|
| T01 | Git-repo initsialiseerimine, GitHubi private remote loomine | Done |
| T01 | `.gitignore`, `.env.example`, `pyproject.toml` | Done |
| T01 | README.md skelett kõigi nõudefailis nõutud peatükkidega | Done |
| T01 | `docs/backlog.md` — 9 kasutajalugu + 20 arendusülesannet | Done |
| T01 | `docs/trello-cards.md` — kopeerimisvalmis Trello kaardid | Done |
| T01 | `docs/definition-of-done.md` | Done |
| T01 | `docs/architecture.md` — komponendiskeem ja andmevoog | Done |
| T01 | `docs/iterations/iteration-0-setup.md` (see fail) | Done |
| T01 | Näidisülesanne `input/001/` (JS-kalkulaator) | Done |
| T01 | Tühjad backend/, frontend/, prompts/ kataloogid | Done |

## Otsused

1. **Tehnoloogia:** Python 3.11+ FastAPI backend, vanilla JS frontend, OpenAI API
   AI osaks. Põhjus: Pythoni ökosüsteem AI-osaks parem, vanilla JS hoiab projekti
   lihtsana ja õpetlikuna ilma ehitustööriistade keerukuseta.

2. **AI mudel:** `gpt-4o-mini` vaikimisi. Põhjus: odav, kiire, eesti keeles
   piisav kvaliteet. Vahetatav `.env` muutuja `OPENAI_MODEL` kaudu.

3. **Sessioonihaldus:** mälusisene `dict` MVP-s. Põhjus: lihtsus. SQLite
   iteratsioonis 5 kui aega jääb.

4. **Projektihaldus:** Trello tahvel + paralleelne `docs/backlog.md` koodirepos.
   Põhjus: kasutajalood ja AC peavad olema ka koodirepoga seotud, et
   versionihaldus näitaks nõuete arengut.

## Iteratsiooni DoD

- [x] Git repo initsialiseeritud, GitHub remote olemas
- [x] Kõik docs/-failid loodud
- [x] Trello kaartide tekst kopeerimisvalmis failis
- [x] README sisaldab kõiki nõutud peatükke (skeletina)
- [x] Vähemalt 1 näidisülesanne `input/`-kaustas

## Järgmine iteratsioon

Iteratsioon 1 — MVP ilma AI-ta. Vt
[`iteration-1-mvp.md`](iteration-1-mvp.md) (loomata, koostatakse iteratsiooni
alguses).
