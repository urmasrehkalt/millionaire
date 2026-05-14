# JSON-andmete kuvamine

## Ülesande kirjeldus

Loo veebileht, mis loeb JSON-faili kasutajate kohta ja kuvab need nimekirjas.

## Nõuded

1. Loo fail `src/data.json`, milles on **vähemalt 3 kasutajat**
   järgmise struktuuriga:
   ```json
   [
     { "nimi": "Mari", "vanus": 28, "linn": "Tartu" },
     { "nimi": "Jüri", "vanus": 35, "linn": "Tallinn" }
   ]
   ```
2. Loo fail `src/app.js`, mis:
   - laadib `data.json`-i kasutades `fetch()`-i
   - parsib JSON-i `response.json()` abil
   - kuvab iga kasutaja andmed lehel olevas `<ul>`-loetelus
3. Käsitle ka **veaolukorda** (kui `data.json` puudub või on vigane), kuvades
   kasutajale veateate
4. Kasuta `async/await` süntaksit, mitte `.then()` ahelat
5. Lehel on **filtreerimisväli**, kuhu kirjutatud tekstiga saab loendit
   nime järgi filtreerida

## Hindamiskriteeriumid

- Andmed laaditakse ja kuvatakse korrektselt
- Veaolukorraga on arvestatud
- Filter töötab (case-insensitive)
- Kood kasutab modernset JS-i (async/await, const/let, template literalid)
- HTML-i struktuur on semantiline (`<ul>`, `<li>`, mitte ainult `<div>`-id)
