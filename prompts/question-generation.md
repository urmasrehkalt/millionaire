# Küsimuste genereerimise prompt

> **Märkus:** Selle faili täielik prompt valmib **iteratsioonis 2** (AI integratsioon).
> Praegune sisu on iteratsiooni 0 platshoidja, mis kirjeldab nõuded prompti
> sisule.

## Prompti nõuded (nõudefaili järgi)

Prompt peab kirjeldama:

1. Et küsimused tuleb koostada `assignment.md` ja lahendusfailide põhjal
2. Et küsimused peavad kontrollima **arusaamist**, mitte ainult mälu
3. Et igal küsimusel peab olema **4 vastusevarianti**
4. Et **ainult üks** vastus tohib olla õige
5. Et küsimustel peab olema **raskusaste** (1–3, kus 1=lihtne, 2=keskmine, 3=raske)
6. Et vastusega peab kaasas olema **lühike selgitus**
7. Et küsimusi tuleb kokku **15** (5 lihtsat + 5 keskmist + 5 rasket)
8. Et keel on **eesti keel**

## Oodatav vastuse formaat

Vastus on JSON-objekt järgmise kujuga:

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
      "explanation": "JavaScripti kasutatakse siin kasutaja tegevustele reageerimiseks ja lehe sisu muutmiseks."
    }
  ]
}
```

## Tulevased iteratsiooni 2 ülesanded

- Lisada täielik süsteemi-prompt (system message), mis kirjeldab AI rolli
- Lisada näiteid (few-shot) lihtsate, keskmiste ja raskete küsimuste kohta
- Defineerida raskusastmete erinevused konkreetselt
- Lisada juhised koodinäidete formaadi kohta (markdown code blocks)
- Veaolukordade prompt: kui ülesanne on liiga väike või segane

---

**Allikas:** Nõudefaili (ülesande_valideerimine.md) sektsioon „AI kasutamise nõuded".
