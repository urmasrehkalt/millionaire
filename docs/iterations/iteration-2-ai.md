# Iteratsioon 2 — AI integratsioon (Gemini 2.5 Flash)

**Periood:** 2026-05-14 — (1 päev)
**Eesmärk:** küsimused genereeritakse iga mängu alguses päris AI abil ülesande
sisu põhjal. Fallback-küsimused jäävad varuvariandiks.

## Muudatus võrreldes algse plaaniga

Iteratsiooni 0 plaan rääkis OpenAI API-st (`gpt-4o-mini`). Kasutaja valis 2026-05-14
ümber **Google Gemini 2.5 Flash** (free tier AI Studio kaudu). Põhjus: tasuta
piisava kvaliteediga mudel, ei vaja arvelduse seadistamist.

Mõju koodile:
- Sõltuvus: `openai` → `google-genai`
- Env muutuja: `OPENAI_API_KEY` → `GEMINI_API_KEY`, `OPENAI_MODEL` → `GEMINI_MODEL`
- Mudel: `gpt-4o-mini` → `gemini-2.5-flash`
- API kutse: `chat.completions.create(response_format=...)` → `client.models.generate_content(config=...)`
- JSON-skeem: Gemini toetab `response_mime_type="application/json"` + `response_schema`

## Skoop (urmas-agiilne-tracker kaardid)

- **T12** — `prompts/question-generation.md` täielik prompt (eesti keeles, kirjeldab
  raskusastmeid, JSON-formaati, selgituse nõuet)
- **T13** — `question_generator.py` reaalne versioon Gemini API-ga
- **T14** — `pydantic-settings` config täiendus (`GEMINI_API_KEY`, hoiatus puudumisel)
- **US5** vastuvõtutingimused: kahe järjestikuse mängu küsimustest osa erinev

## Tehnilised otsused

- **SDK:** `google-genai` (uus ühendatud SDK, mitte vana `google-generativeai`)
- **Mudel:** `gemini-2.5-flash` (vahetatav `GEMINI_MODEL` kaudu)
- **JSON-output:** `response_mime_type="application/json"` + Pydantic-põhine skeem
- **Temperatuur:** `temperature=0.9` mitmekesisuse jaoks (US5)
- **Muutus iga päringu vahel:** lisame promptisse timestampi/nonce'i, et Gemini
  ei tagastaks vahemällu salvestatud vastust
- **Fallback:** kui `GEMINI_API_KEY` puudub või API tagastab vea / vigase JSON-i,
  langeme `fallback_questions.json`-i peale (kuvame hoiatuse logis)
- **Vea käitlemine:** `try/except` ümber Gemini päringu, log hoiatus, fallback
- **Rate-limit:** free tier on 15 RPM / 1500 RPD — piisab koolikasutuseks. Cache
  lisame iteratsioonis 5

## Definition of Done (iteratsioon 2)

- [ ] `pyproject.toml`-s `google-genai` (mitte `openai`)
- [ ] `.env.example` ja `config.py` viitavad `GEMINI_API_KEY`-le
- [ ] `prompts/question-generation.md` sisaldab täielikku prompti
- [ ] `question_generator.py` kasutab Gemini API-d kui võti on seatud
- [ ] Päringu vea / puuduva võtme korral kasutatakse fallback'i
- [ ] Vastuvõtutest US5: 2 järjestikuse mängu küsimustest vähemalt mõni erineb
- [ ] `pytest` läbib (sh uued generator-testid mock'idega)
- [ ] README peatükk „AI küsimuste genereerimise loogika" uuendatud Gemini jaoks

## Plaan tunnipiketi-tasandil

1. Loo iteratsiooni dokument (see fail)
2. Uuenda `pyproject.toml`: eemalda `openai`, lisa `google-genai`
3. Uuenda `.env.example`: `GEMINI_API_KEY=`, `GEMINI_MODEL=gemini-2.5-flash`
4. Uuenda `backend/app/config.py`
5. Kirjuta täielik prompt `prompts/question-generation.md`-sse
6. Kirjuta `question_generator.py` reaalne implementatsioon Gemini API-ga
7. Kirjuta üksusetestid mock'iga (Gemini client mockitakse `unittest.mock`-iga)
8. Uuenda README
9. Käivita `pytest` ja smoke-test
10. Test brauseris, kui kasutaja annab oma API-võtme

## Iteratsiooni tagasivaade

(Täidetakse iteratsiooni lõpus.)
