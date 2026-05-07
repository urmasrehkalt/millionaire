# JavaScripti kalkulaator

## Ülesande kirjeldus

Loo lihtne veebipõhine kalkulaator, mis võimaldab kasutajal teostada nelja
põhilist aritmeetilist tehet (liitmine, lahutamine, korrutamine, jagamine)
kahe arvuga.

## Nõuded

1. Lehel on **kaks sisendvälja** kahe arvu sisestamiseks
2. Lehel on **neli nuppu**: `+`, `−`, `×`, `÷`
3. Pärast nupule vajutamist kuvatakse tulemus eraldi alal
4. Sisestust tuleb teisendada arvuks (`Number()` või `parseFloat()`)
5. Kui sisend ei ole arv, kuvatakse veateade
6. Nulliga jagamise korral kuvatakse veateade „Nulliga jagada ei saa"
7. Lahendus peab koosnema **kolmest failist**: `index.html`, `style.css`, `script.js`
8. JavaScript peab kasutama `addEventListener`-it (mitte inline `onclick`)

## Hindamiskriteeriumid

- Kõik neli tehet töötavad korrektselt
- Sisendi valideerimine on olemas
- Nulliga jagamine on käsitletud
- Kood on jaotatud kolme eraldi faili
- Kasutajaliides on selge ja loetav
- Veateated on eestikeelsed ja kasutajasõbralikud

## Näide

```
Sisend 1: 10
Sisend 2: 3
Vajuta nuppu „+"
→ Tulemus: 13

Sisend 1: 7
Sisend 2: 0
Vajuta nuppu „÷"
→ Veateade: Nulliga jagada ei saa
```
