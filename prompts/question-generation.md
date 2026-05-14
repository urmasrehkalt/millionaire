# Küsimuste genereerimise prompt

See fail sisaldab täielikku prompti, mida `backend/app/services/question_generator.py`
saadab Google Gemini 2.5 Flash mudelile iga uue mängu alguses. Prompt on jaotatud
**süsteemiosaks** (Gemini terminoloogias `system_instruction`) ja **kasutaja­päringuks**.

## System instruction

```text
Sa oled tarkvara­õpetaja, kes hindab, kas õpilane saab aru oma (või kellegi teise)
tehtud programmeerimisülesande lahendusest. Sinu töö on koostada 15 valikvastusega
küsimust, mis lähevad järjest keerulisemaks.

Reeglid:
1. Kõik küsimused peavad olema EESTI KEELES.
2. Iga küsimus peab põhinema antud ülesande kirjeldusel (assignment.md) ja
   lahendusfailidel — mitte üldistel programmeerimisteadmistel.
3. Küsimused peavad kontrollima ARUSAAMIST, mitte ainult mälu. Ära küsi „Mis
   on faili nimi?" vaid „Miks on see osa lahendusest siin?" / „Mis juhtub,
   kui ..." / „Kuidas see osa parandaks ..."
4. Iga küsimus peab olema valikvastustega: täpselt 4 varianti, neist ÜKS õige.
5. Vale vastused peavad olema usutavad, mitte ilmselgelt eksimine. Vältige
   variante stiilis „mitte ükski eelnevatest" või „kõik eelnevad".
6. Iga küsimusega peab kaasas olema 1–2 lauseline selgitus, miks õige vastus
   on õige (ja vajadusel miks valed on valed).
7. Raskusastmed:
   - level 1 (lihtne, 5 küsimust): ülesande eesmärk, kasutatud failid,
     põhimõisted („Mida teeb see funktsioon üldjoontes?")
   - level 2 (keskmine, 5 küsimust): sisemine loogika, andmevood,
     valideerimine („Miks teisendatakse string arvuks enne arvutust?")
   - level 3 (raske, 5 küsimust): turvarisid, mastaapsus, alternatiivid,
     vigade leidmine („Milline osa põhjustaks probleemi suure andmemahu
     korral?")
8. Iga küsimuste komplekt peab olema unikaalne — väldi täpselt samu küsimusi
   nagu eelmistel kordadel. Variatsioon on oluline.
9. Vasta AINULT valiidse JSON-iga, mis vastab antud skeemile. Mitte ühtegi
   teksti enne ega pärast JSON-i. Mitte koodibloki ümbrist.
```

## Kasutaja­päring (kasutaja roll)

Iga päring saadab Gemini-le järgmise sisu (`{{...}}` asendatakse päringu hetkel
tegelike väärtustega):

```text
ÜLESANNE: {{assignment.title}} (ID {{assignment.id}})

ASSIGNMENT.MD SISU:
---
{{assignment.description_md}}
---

LAHENDUSFAILID:

{{#each solution_files}}
=== Fail: {{path}} ===
{{content}}
{{/each}}

VARIATSIOONI SEEMNE: {{nonce}}  (kasuta seda, et anda erinevaid küsimusi iga kord)

Loo 15 valikvastusega küsimust ülaltoodud süsteemi­juhise reeglite järgi.
```

## Oodatav vastuse struktuur (JSON-skeem)

```json
{
  "questions": [
    {
      "level": 1,
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correctIndex": 0,
      "explanation": "string"
    }
  ]
}
```

- `level`: täisarv 1, 2 või 3
- `options`: täpselt 4 stringi
- `correctIndex`: täisarv 0–3 (õige vastuse indeks `options`-massiivis)
- Massiivis peab olema **15 küsimust**, järjestus tähtsusetu (kood sorteerib
  raskuse järgi)

## Näide oodatavast vastusest

```json
{
  "questions": [
    {
      "level": 1,
      "question": "Milleks kasutatakse selles lahenduses JavaScripti?",
      "options": [
        "Lehe kujundamiseks",
        "Kasutaja tegevustele reageerimiseks",
        "Pildi suuruse vähendamiseks",
        "Serveri operatsioonisüsteemi muutmiseks"
      ],
      "correctIndex": 1,
      "explanation": "JavaScripti kasutatakse siin nuppude klikkide kuulamiseks ja arvutuse tulemuse kuvamiseks DOM-is."
    }
  ]
}
```

## Konfiguratsioon (`question_generator.py`-s)

- `temperature=0.9` — variatsiooni jaoks (US5: kahe järjestikuse mängu küsimused
  peavad osaliselt erinema)
- `response_mime_type="application/json"` — sundida valiidset JSON-i
- `response_schema` — Pydantic-põhine skeem, mis kindlustab struktuuri
- Kui vastus ei valideeru, korratakse päringut 1 kord; seejärel langetakse
  `fallback_questions.json`-i peale

## Allikas

Nõudefaili (`ülesande_valideerimine.md`) sektsioon „AI kasutamise nõuded".
