# Iteratsioon 3 — Küsimusepank teema kohta (#3 + #4)

**Periood:** 2026-05-14
**Eesmärk:** Mäng ei kutsu enam AI-d iga alustamisel. Iga teema saab
salvestatud 50 küsimusega panga, millest mäng valib juhuslikult 5+5+5
(lihtne+keskmine+raske). AI roll kitsendub uue teema loomiseks.

## Põhjus

Iteratsioonis 2 valmis Gemini API-päring iga mängu alguses. Probleemid:

- Iga mängu start võttis 4–8 s
- Free tier 15 RPM piirang muudaks klassikomplekti raskeks
- Õpilane sai uue küsimustekomplekti igal proovikorral — ja võis raporteerida,
  et küsimused „pole järjepidevad" õpetajaga
- Sama küsimus võis kahel järjestikusel mängul olla peaaegu identne

Lahendus: **küsimusepank** ülesande kausta.

## Skoop

**Issue #3** (väike bugfix):
- `min_items` / `max_items` Gemini JSON-skeemis tagastas „Cannot set both
  `enum` and `type`" — eemaldati `enum`, lisati `minimum`/`maximum` korrektne kuju

**Issue #4** (peapaljudus):
- Uus mudel `Question.hint` (õlekõrre jaoks)
- Uus teenus `backend/app/services/question_bank.py`:
  - `load_question_bank(input_root, assignment_id)`
  - `select_game_questions(bank)` — Fisher-Yates 5+5+5 valik
  - Valideerib, et igas tasemes on vähemalt 5 küsimust
- `game_logic.py`-i lisandus `reserve_questions` ja `swap` lifeline
- API muudatused:
  - `POST /api/assignments` — uue teema loomine AI abil
  - `POST /api/game/lifeline` — laienenud 3 õlekõrrega
  - `POST /api/game/start` loeb panga (mitte ei kutsu AI-d)
- 50-küsimusega `questions.json` failid `input/001`, `input/002`, `input/003`
- Õlekõrred frontendis: 50:50, Vihje, Vaheta
- Uue teema vorm avalehel
- Prompt-fail uuendatud: kõik küsimused saavad `hint`-välja, pikem küsimuste
  stiil (miljonimängu kontekstilausetega)

## Tehnilised otsused

- **Pangad on JSON-failid, mitte SQLite:** lihtsam diff'ida ja git'iga jälgida
- **Reserve hoitakse mälusiseses sessioonis:** vahetus võtab esimese vaba sama
  taseme küsimuse
- **Õlekõrre asendus:** algselt plaanitud „Küsi publikult" (audience poll)
  asendus „Vaheta küsimusega" — kuna meil on juba 50 küsimust ja AI-päringut
  ei taha lifeline-i jaoks teha

## Definition of Done

- ✅ Iga `input/<id>/` sisaldab `questions.json` 50 küsimusega
- ✅ `select_game_questions` valib korrektselt 5+5+5
- ✅ Õlekõrred töötavad (50:50, vihje, vaheta)
- ✅ Uus teema veebivormis loodav
- ✅ Backend pytest läbib (lisandusid `test_question_bank.py`)
- ✅ Brauseritest: mängitud läbi 3 teemat, õlekõrred kasutatud

## Iteratsiooni tagasivaade

**Õnnestus:** küsimusepanga JSON-formaat on lihtne ja git-sõbralik.
Pre-generated küsimused lasevad rakendust kasutada ka ilma jooksva
AI-ühenduseta.

**Keeruline:** Gemini JSON-skeemi süntaks oli kapriisne (`enum` + `type`
konflikt → #3 bugfix). Pikemate küsimuste prompt nõudis paar iteratsiooni,
et AI ei tagastaks „Mis fail" tüüpi triviaalseid küsimusi.

**Edasi:** mänguajalugu `localStorage`-isse (US14).
