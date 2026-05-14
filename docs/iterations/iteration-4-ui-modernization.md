# Iteratsioon 4 — UI moderniseerimine (#5)

**Periood:** 2026-05-14
**Eesmärk:** mänguliides peab näima ja tundma nagu päris miljonimäng — mitte
nagu funktsionaalne MVP.

## Skoop

- Uus tumesinine-kuldne värvilahendus (CSS muutujad `--bg`, `--accent` jne)
- Punktiastmete tabel klassikalises miljonimängu stiilis (kuldne ääris,
  turvatasemete eristamine)
- Mängu vaate küsimuspaneel pehmete pööratud servadega ja gradient-glow
- Õlekõrte nupud ümar-kuldsed, hover- ja disabled-olekud
- „Järgmine küsimus" CTA ere kuldne, kontrastne kuldsete õlekõrrenuppudega
- Vastusenupud:
  - hover-state kuldse äärisega
  - vale vastus animatsiooniga „lärm"
  - õige vastus rohelise highlight'iga
- Tulemus­vaade keskel, prominentne skoor, ülesande pealkiri allpool
- Responsive: vaade töötab ka mobiilis (ladder läheb alla, vastused
  ühe veeruga)

## Mis ei muutunud

Mängu loogika, õlekõrred, sessioonid, API — kõik samad. Puhas
CSS-uuendus ühe `index.html` muudatusega (klassinimed kohendatud).

## Definition of Done

- ✅ Lehel on miljonimängu „tunne" (must-kuld, animatsioonid)
- ✅ Mobiili viewport töötab (ülesannete kaardid grid-laotud, mängu vaate
  ladder läheb alla)
- ✅ Hover/disabled olekud korrektsed
- ✅ Toimub puhas refresh — kasutaja saab F5-ga restartida

## Iteratsiooni tagasivaade

**Õnnestus:** CSS muutujad muudavad teemavahetuse triviaalseks. Põhi-
mehaanika oli juba paigas, joonistamine oli puhas frontend-töö.

**Keeruline:** kuldse aktsentvärvi tasakaal — liiga eredalt häirib silmi,
liiga tumedalt ei eristu fonist. Lõppvarriant kasutab gradientidel kahte
kuldse­tooni.

**Edasi:** demo URL (US12 / iter-5).
