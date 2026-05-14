# Iteratsioon 6 — „Lõpeta mäng" ja eesti keele lihv (#7 + #8)

**Periood:** 2026-05-14
**Eesmärk:** lõpetada miljonimängu walk-away funktsioon ja viimistleda UI
sõnastust nii, et õpetaja saaks lehte ette näidata ilma piinlikkuseta.

## #7 — „Lõpeta mäng" walk-away

**Skoop:**

- `engine.js` saab `quitGame(sessionId)` — lõpetab sessiooni staatusega
  „quit" ja punktidega `SCORE_LADDER[currentIndex - 1]` (klassikaline
  miljonimängu reegel: oma teenitud raha jätta, mitte turvatasemele kukkuda)
- `api.js` re-eksporib `quitGame`
- `game.js` lisab „Lõpeta mäng" nupu question-actions ribale
- Klikk → `window.confirm` näitab summat („Lahkud 1 000 punktiga.") → kinnitusel
  tulemusvaate
- `result.js` toetas juba „quit" staatust (verdict: „Lahkusid mängust")
- CSS: sekundaarne vaikne nupustiil, mobiil-vaates täislaius

**Testid:**

- 9/9 Node smoke-test: lahkumine Q1-l = 0 p; Q3 järel = 300 p; Q5 järel =
  1 000 p (mitte turvatase!); throw kui sessioon juba lõppes / tundmatu

## #8 — Eesti keele lihv

**Põhilised parandused:**

| Asukoht | Enne | Pärast |
|---------|------|--------|
| Päise loosung | Kes tahab tõestada, et lahendusest aru saab? | Tõesta, et mõistad oma lahendust. |
| Menüü intro | ...mille kohta tahad mängu mängida. | ...mille üle soovid end proovile panna. |
| Mängu meta | Küsimus 1/15 • Raskus 1/3 | Küsimus 1 / 15 • Raskusaste 1 / 3 |
| Mängu skoor | Hetkeseis: 100 p | Punktisumma: 100 |
| Õlekõrs | Vaheta | Vaheta küsimus |
| Tulemus „lost" | 💥 Mäng läbi | 💥 Mäng on läbi |
| Tulemus „quit" | 👋 Mäng katkestatud | 👋 Lahkusid mängust |
| Skoor tulemus­vaates | 1 000 000 p | 1 000 000 punkti |
| Nupp | Mängi sama ülesannet uuesti | Proovi sama ülesannet uuesti |
| Nupp | Tagasi ülesannete juurde | Vali teine ülesanne |
| Sektsioon | Vastatud küsimused | Sinu vastused |
| Ülesanne 003 | ...komandoreal käivituv... | Pythoni käsurea To-Do nimekiri |

Lisaks:

- Tühja oleku, uue teema vormi ja quit-dialoogi sõnastus loetavamaks
- Ülesande 003 sisus „komandorea" → „käsurea" (3 esinemist ka
  `questions.json`-is)
- `assignments.json` manifest uuendatud (CI taastoodab sama tulemuse
  H1-pealkirjast)

## Definition of Done

- ✅ Walk-away nupp töötab kõikides olukordades (smoke-test 9/9)
- ✅ Iga visiibel string käsitsi üle loetud
- ✅ Pytest 32/32 ei regresseeru
- ✅ JS süntaks puhas (`node --check`)
- ✅ Demo deploy edukas (commit 1791290 läbis Pages workflow'i)

## Iteratsiooni tagasivaade

**Õnnestus:** quit-feature passis kena teemana iter-2-st 4-ni
„sessioonid client-poolel" arhitektuuri. Üks engine-funktsioon + üks
nupp + üks dialoog — terve feature alla 80 rea koodi.

**Keeruline:** keele-lihv võttis aega, kuna eesti keele „loomulik
toon" ei ole otseses tõlkes kättesaadav. Mõned otsused (nt
„Punktisumma" vs „Sinu skoor") nõudsid valimist 3 ekvivalendi vahel.

**Edasi:** mänguajalugu (US14) ja/või markdown-render (US8).
