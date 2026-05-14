# Iteratsioon 1 — MVP ilma AI-ta

**Periood:** 2026-05-14 — (kestus ~2 päeva)
**Eesmärk:** mängu täielik kasutusvoog töötab fikseeritud (fallback) küsimustega.
Miinimumnõuded arvestuseks on täidetud.

## Skoop (Trello-kaardid)

- **T02** — FastAPI rakendus + staatilise frontendi serveerimine (port 8005)
- **T03** — `assignment_loader.py` (input/-i lugemine, H1 parsing, path-traversal kaitse)
- **T04** — API: `GET /api/assignments`, `GET /api/assignments/{id}`
- **T05** — Pydantic skeemid
- **T06** — `game_logic.py` (punktiastmed, turvatasemed, sessioonid)
- **T07** — API: `POST /api/game/start`, `POST /api/game/answer`
- **T08** — `fallback_questions.json` (15 küsimust ülesande 001 jaoks)
- **T09** — Frontend: avalehe ülesannete nimekiri
- **T10** — Frontend: mänguvaade
- **T11** — Frontend: tulemusvaade selgitustega

Katavad kasutajalood: **US1, US2, US3 (lõpus), US4**.

## Töövoog

1. Branch: `feature/iter1-mvp` (loodud `main`-st)
2. Implementeerimisjärjekord (sõltuvuste põhjal):
   - T05 (skeemid) → T03 (loader) → T08 (fallback) → T06 (loogika)
   - T02 (FastAPI skelett) → T04 (assignments routes) → T07 (game routes)
   - Üksusetestid T03 ja T06 jaoks (`pytest`)
   - T09 → T10 → T11 (frontend ülevalt alla)
3. Otsast lõpuni test brauseris (port 8005)
4. `docs/testing-notes.md` täiendamine vastuvõtutestide tulemustega
5. Pull request `main`-i vastu → kasutaja review → squash-merge (alles pärast
   kasutaja kinnitust!)

## Tehnilised otsused

- **Port:** 8005 (8000 on kasutaja agiilse trackeri jaoks)
- **Python:** 3.12+
- **Sessioonid:** mälusisene `dict[uuid, GameSession]`, ei vaja serialiseerimist
- **Failide kärpimine:** lahendusfailid >32 KB kärbitakse 32 KB-ni
- **CORS:** lubatud arenduses kõigile (`allow_origins=["*"]`)
- **Fallback:** kasutame alati seda iteratsioonis 1, isegi kui `OPENAI_API_KEY`
  on seatud — AI integratsioon tuleb iteratsioonis 2
- **Frontend marsruutimine:** lihtne `state.view` muutuja (`menu`/`game`/`result`),
  ilma SPA-raamistikuta

## Definition of Done (iteratsioon 1)

- [ ] Kasutaja saab valida `input/001/` ülesande avalehel
- [ ] Mäng algab ja kuvab esimese küsimuse 4 vastusega
- [ ] Õige vastus liigub järgmisele küsimusele, punktid suurenevad
- [ ] Vale vastus lõpetab mängu, punktid kukuvad turvatasemele
- [ ] Lõppekraan kuvab punktid + vastatud küsimused selgitustega
- [ ] Uue `input/00X/` lisamine teeb selle mängitavaks ilma serveri restartita
- [ ] `pytest` läbib edukalt
- [ ] PR review tehtud ja kasutaja kinnitanud merge'imiseks

## Iteratsiooni tagasivaade

(Täidetakse iteratsiooni lõpus.)
