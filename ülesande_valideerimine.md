„Miljonimäng” – AI-põhine ülesande valideerimise rakendus
 Grupp: TAK25

Ülesande eesmärk
Luua veebirakendus, mis aitab kontrollida, kas õppija saab aru enda või kellegi teise tehtud ülesande lahendusest.

Rakendus töötab miljonimängu põhimõttel: kasutajale esitatakse järjest valikvastustega küsimusi. Küsimused genereeritakse AI abil konkreetse ülesande kirjelduse ja lahenduse põhjal.

Rakendus ei kontrolli ainult seda, kas failid on olemas või kood töötab, vaid püüab kontrollida, kas kasutaja mõistab lahenduses kasutatud kontseptsioone, loogikat ja lähteülesande nõudeid.

Rakenduse üldine kirjeldus
Rakendusel on input/ kaust, kus asuvad valideeritavad ülesanded.

Rakendus peab toetama rohkem kui ühte ülesannet. Seetõttu asuvad ülesanded numbriliste alamkaustadena.

Näidisstruktuur:

input/
  001/
    assignment.md
    index.html
    style.css
    script.js

  002/
    assignment.md
    src/
      app.js
      data.json

  003/
    assignment.md
    README.md
    solution/
      main.py
Igas ülesande kaustas peab olema vähemalt fail:

assignment.md
Selles failis on ülesande püstitus, nõuded ja hindamiskriteeriumid.

Samas kaustas võivad olla ülesande lahenduse failid ükskõik millisel kujul, vastavalt ülesande olemusele.

Rakenduse põhifunktsioonid
1. Ülesannete nimekirja kuvamine
Rakendus loeb input/ kaustast kõik numbrilised alamkaustad ja kuvab kasutajale menüü.

Näiteks:

Vali ülesanne:

001 - JavaScripti kalkulaator
002 - JSON-andmete kuvamine
003 - To-do list localStorage'iga
Kui võimalik, võetakse ülesande nimi assignment.md faili esimesest pealkirjast.

Näiteks:

# JavaScripti kalkulaator
2. Ülesande valimine
Kasutaja valib ülesande.

Pärast valikut loeb rakendus:

assignment.md faili sisu;
kõik sama ülesande kaustas olevad lahenduse failid;
vajadusel ka alamkaustades olevad failid.
Rakendus peab suutma anda AI-le piisavalt konteksti, et AI saaks koostada sisulised küsimused.

3. AI-ga küsimuste genereerimine
Rakendus genereerib iga mängu alguses uued küsimused.

Küsimused peavad põhinema:

lähteülesande nõuetel;
lahenduse failidel;
lahenduses kasutatud tehnoloogiatel;
kasutatud loogikal;
võimalikel vigadel või erijuhtudel;
sellel, kas lahendus tegelikult vastab ülesande eesmärgile.
Küsimused ei tohi olla ainult stiilis:

Mis faili nimi oli lahenduses?
Eelistatud on küsimused, mis kontrollivad arusaamist:

Miks kasutatakse selles lahenduses addEventListener meetodit?

A) Et HTML-faili automaatselt salvestada  
B) Et reageerida kasutaja tegevusele, näiteks nupuvajutusele  
C) Et muuta JavaScripti fail CSS-failiks  
D) Et laadida brauserisse uus font
Miljonimängu reeglid
Rakendus peab järgima miljonimängu-laadset loogikat.

Nõuded mängule
Mängus on 15 küsimust.
Igal küsimusel on 4 vastusevarianti.
Ainult üks vastus on õige.
Küsimused lähevad järjest keerulisemaks.
Vale vastuse korral mäng lõpeb.
Kasutaja näeb oma hetkeseisu.
Kasutaja saab mängu pooleli jätta.
Küsimused peavad olema iga kord vähemalt osaliselt uued.
Rahaastmed / punktid
Raha võib asendada punktidega, aga mängu loogika võiks jääda samaks.

Näiteks:

1. küsimus - 100 punkti
2. küsimus - 200 punkti
3. küsimus - 300 punkti
4. küsimus - 500 punkti
5. küsimus - 1 000 punkti
6. küsimus - 2 000 punkti
7. küsimus - 4 000 punkti
8. küsimus - 8 000 punkti
9. küsimus - 16 000 punkti
10. küsimus - 32 000 punkti
11. küsimus - 64 000 punkti
12. küsimus - 125 000 punkti
13. küsimus - 250 000 punkti
14. küsimus - 500 000 punkti
15. küsimus - 1 000 000 punkti
Turvatasemed:

küsimus: 1 000 punkti
küsimus: 32 000 punkti
küsimus: 1 000 000 punkti
Kui kasutaja vastab valesti, langeb tulemus viimasele saavutatud turvatasemele.

Õlekõrred
Rakenduses võiks olla vähemalt 2 õlekõrt.

Näiteks:

50:50
Eemaldatakse kaks valet vastusevarianti.

Küsi AI-lt vihjet
AI annab lühikese vihje, kuid ei ütle otsest vastust.

Näide:

Vihje: mõtle sellele, milline meetod seob JavaScripti kasutaja tegevusega.
Küsi publikult
Rakendus kuvab simuleeritud publikuhääletuse tulemuse.

Näiteks:

A - 12%
B - 68%
C - 9%
D - 11%
Publiku tulemus ei pea alati olema 100% õige, aga lihtsamate küsimuste puhul võiks õige vastus saada suurema tõenäosusega rohkem hääli.

Küsimuste raskusastmed
AI peab genereerima küsimused erineva raskusastmega.

Küsimused 1–5
Lihtsad küsimused.

Kontrollivad põhimõisteid ja ülesande üldist arusaamist.

Näiteks:

Mis on selle ülesande eesmärk?
Millist faili kasutatakse põhilise JavaScripti loogika jaoks?
Mida teeb vormi submit-sündmus?
Milleks kasutatakse JSON-faili?
Küsimused 6–10
Keskmise raskusega küsimused.

Kontrollivad lahenduse sisemist loogikat.

Näiteks:

Miks tuleb kasutaja sisend enne arvutamist teisendada arvuks?
Mis juhtub, kui vajalik HTML-element puudub?
Kuidas liigub info ühest funktsioonist teise?
Milline osa lahendusest kontrollib kasutaja sisestust?
Küsimused 11–15
Rasked küsimused.

Kontrollivad sügavamat arusaamist, vigade leidmist ja alternatiivseid lahendusi.

Näiteks:

Milline lahenduse osa võib põhjustada probleemi, kui andmeid tuleb juurde palju?
Kuidas muuta lahendust nii, et see töötaks mitme ülesande puhul?
Milline turvarisk tekib, kui kasutaja sisend lisatakse otse innerHTML abil?
Kuidas parandada lahenduse struktuuri, et seda oleks lihtsam edasi arendada?
Tehnilised nõuded
Rakendus võib olla tehtud vabalt valitud tehnoloogiaga.

Sobivad näiteks:

Node.js + Express
PHP
Python + Flask/FastAPI
ainult frontend + lokaalne JSON, kui AI osa on eraldi simuleeritud
muu õpetajaga kooskõlastatud lahendus
Rakendus peab sisaldama vähemalt:

ülesannete nimekirja;
ülesande valikut;
valitud ülesande failide lugemist;
AI küsimuste genereerimist või vähemalt selgelt eraldatud kohta, kuhu AI ühendus hiljem lisada;
mänguvaadet;
vastuste kontrollimist;
tulemuse kuvamist.
AI kasutamise nõuded
AI-le saadetav prompt peab olema projektis nähtav või dokumenteeritud.

Näiteks failis:

prompts/question-generation.md
Prompt peab kirjeldama:

et küsimused tuleb koostada assignment.md ja lahendusfailide põhjal;
et küsimused peavad kontrollima arusaamist, mitte ainult mälu;
et igal küsimusel peab olema 4 vastusevarianti;
et ainult üks vastus tohib olla õige;
et küsimustel peab olema raskusaste;
et vastusega peab kaasas olema lühike selgitus.
AI vastus võiks olla JSON-kujul.

Näide:

[
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
Soovituslikud kasutajalood
Kasutajalugu 1
Õppijana tahan näha ülesannete nimekirja, et saaksin valida, millise ülesande kohta mängu mängida.

Kasutajalugu 2
Õppijana tahan vastata valikvastustega küsimustele, et kontrollida, kas saan lahendusest aru.

Kasutajalugu 3
Õppijana tahan näha pärast vastamist selgitust, et mõista, miks vastus oli õige või vale.

Kasutajalugu 4
Õpetajana tahan lisada uusi ülesandeid input/ kausta, et sama rakendust saaks kasutada erinevate ülesannete valideerimiseks.

Kasutajalugu 5
Õpetajana tahan, et küsimused oleksid iga kord erinevad, et õppija ei saaks lihtsalt vastuseid pähe õppida.

Miinimumnõuded arvestuseks
Töö on arvestatav, kui:

input/ kaustas saab olla mitu ülesannet;
iga ülesanne on eraldi numbrilises alamkaustas;
rakendus kuvab ülesannete valiku;
rakendus loeb valitud ülesande assignment.md faili;
rakendus loeb vähemalt ühe lahenduse faili;
rakendus genereerib või simuleerib vähemalt 15 küsimust;
mängus on 4 vastusevarianti;
mäng kontrollib õiget ja valet vastust;
vale vastuse korral mäng lõpeb;
tulemus kuvatakse kasutajale;
projektis on README, kus on käivitamise juhised.
Lisafunktsioonid parema hinde jaoks
päris AI API ühendus;
küsimuste salvestamine vahemällu;
võimalus küsimused uuesti genereerida;
tulemuste salvestamine;
mänguajalugu;
kasutajate süsteem;
õpetaja vaade;
võimalus ülesandeid veebiliidesest lisada;
automaatne failide ignoreerimine, näiteks node_modules, .git, vendor;
Markdowni ilus kuvamine;
koodi kuvamine süntaksivärvimisega;
õlekõrred;
küsimuse selgituse kuvamine pärast vastamist;
raskusastmete parem jaotus.
README peab sisaldama
# Miljonimäng

## Projekti kirjeldus

## Kasutatud tehnoloogiad

## Käivitamise juhend

## Input-kausta struktuur

## AI küsimuste genereerimise loogika

## Mängu reeglid

## Teadaolevad piirangud

## Edasiarenduse võimalused
Hindamiskriteeriumid
Projekt on arendatud iteratiivselt, mitte ühe korraga valmis kirjutatud tööna.
Projektil on nähtav ja arusaadav product backlog.
Backlog sisaldab kasutajalugusid, mitte ainult tehniliste tööde nimekirja.
Kasutajalood on sõnastatud näiteks kujul: „Kasutajana tahan ..., et ...”
Igal suuremal kasutajalool on kirjas vastuvõtutingimused.
Vastuvõtutingimused kirjeldavad, millal võib ülesande valmis lugeda.
Töö on jaotatud väiksemateks arendusülesanneteks.
Arendusülesanded on hallatud näiteks GitHub Issues, GitLab Issues, Trello, Jira või muu sarnase vahendi abil.
On näha, millised tööd on tegemata, töös ja valmis.
Projektis on kasutatud vähemalt lihtsat agiilset töövoogu: Backlog → Todo → In progress → Review/Test → Done.
Enne arendamist on koostatud vähemalt üks planeerimise dokument või sprinti kirjeldav märge.
Projektis on näha, millised funktsionaalsused valmisid esimeses versioonis ja millised hiljem.
Õpilane oskab selgitada, miks just selline arendusjärjekord valiti.
Iga suurem funktsionaalsus on seotud konkreetse kasutajaloo või issue’ga.
Git commit’id on sisukad ja kirjeldavad tehtud muudatusi.
Projektis ei ole kogu töö tehtud ühe suure commit’ina.
Võimalusel kasutatakse eraldi harusid suuremate funktsioonide arendamiseks.
README sisaldab ülevaadet arendusprotsessist, mitte ainult käivitamise juhendit.
README-s või eraldi dokumendis on kirjas projekti eesmärk, kasutajalood, tööjaotus ja valminud funktsionaalsus.
Projektis on kirjeldatud Definition of Done ehk tingimused, mille alusel töö valmis loetakse.
Valminud rakendust on testitud vastuvõtutingimuste põhjal.
Testimise tulemus on dokumenteeritud vähemalt lühidalt.
Õpilane oskab näidata, millised nõuded said täidetud ja millised jäid tegemata.
Kui mõni nõue jäi täitmata, on põhjus ausalt dokumenteeritud.
Projektis on olemas lõppdemo või selle kirjeldus.
Õpilane oskab demos näidata rakenduse põhikasutusvoogu: ülesande valik, küsimuste genereerimine, mängu mängimine ja tulemuse kuvamine.
Projekti lõpus on tehtud lühike tagasivaade: mis õnnestus, mis oli keeruline ja mida järgmises iteratsioonis parandada.
Lahendus on edasiarendatav: uue ülesande lisamine ei nõua kogu rakenduse ümberkirjutamist.
Koodistruktuur toetab agiilset edasiarendust: küsimuste genereerimine, failide lugemine, mänguloogika ja kasutajaliides ei ole kõik läbisegi ühes failis.
AI kasutamise osa on eraldi kirjeldatud ning õpilane oskab selgitada, kuidas AI aitab ülesande valideerimisel.
Projekt näitab lisaks tehnilisele teostusele ka arendusprotsessi mõistmist.