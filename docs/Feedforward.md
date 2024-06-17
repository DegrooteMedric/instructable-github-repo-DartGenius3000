# Projectgegevens

**VOORNAAM NAAM:** Degroote Medric

**Sparringpartner:** Andreas Adam

**Projectsamenvatting in max 10 woorden:** Dartbord(vogelpiek) inlezen a.d.h.v lasersensoren op draaiend wiel.

**Projecttitel:** Dart Genius 3000

# Tips voor feedbackgesprekken

## Voorbereiding

> Bepaal voor jezelf waar je graag feedback op wil. Schrijf op voorhand een aantal punten op waar je zeker feedback over wil krijgen. Op die manier zal het feedbackgesprek gerichter verlopen en zullen vragen, die je zeker beantwoord wil hebben, aan bod komen.

## Tijdens het gesprek:

> **Luister actief:** Schiet niet onmiddellijk in de verdediging maar probeer goed te luisteren. Laat verbaal en non-verbaal ook zien dat je aandacht hebt voor de feedback door een open houding (oogcontact, rechte houding), door het maken van aantekeningen, knikken...

> **Maak notities:** Schrijf de feedback op zo heb je ze nog nadien. Noteer de kernwoorden en zoek naar een snelle noteer methode voor jezelf. Als je goed noteert,kan je op het einde van het gesprek je belangrijkste feedback punten kort overlopen.

> **Vat samen:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.

> **Sta open voor de feedback:** Wacht niet op een samenvatting door de docenten, dit is jouw taak: Check of je de boodschap goed hebt begrepen door actief te luisteren en samen te vatten in je eigen woorden.`

> **Denk erover na:** Denk na over wat je met de feedback gaat doen en koppel terug. Vind je de opmerkingen terecht of onterecht? Herken je je in de feedback? Op welke manier ga je dit aanpakken?

## NA HET GESPREK

> Herlees je notities en maak actiepunten. Maak keuzes uit alle feedback die je kreeg: Waar kan je mee aan de slag en wat laat je even rusten. Wat waren de prioriteiten? Neem de opdrachtfiche er nog eens bij om je focuspunten te bepalen.Noteer je actiepunten op de feedbackfiche.

# Feedforward gesprekken

## Gesprek 1 (Datum: 24/05/2024) (9.30u)

Lector: Frederik

Vragen voor dit gesprek:

- vraag 1: Is mijn database goed genormaliseerd

ja, wel teveel tabellen

- vraag 2: is mijn "usergame" (tussentabel) een juiste one-to-many relatie

ja, best gamemodes opslaan in list, dan bij game de naam gememode bijhouden. usergamestats is de user geconnecteerd met de game en per game per user dan de stats bijhouden. dan heb je user tabel apart waar de user een account kan aanmaken, en bij het inloggen een dropdown kan gebruiken

- vraag 3: zou ik "3darts average" bijhouden in database of enkel in glob var EN zou ik dat doen voor AVerage in totaal of calculated propertie

ja, je kan dat dan berekenen, is een beetje zoals triple 20s ofzo

- vraag 4: zou ik "Wachtwoord" bijhouden in database, "userscoregame" database of variabele(updatescoregame route)

nee, het doel is geen loginsysteem maken

## Gesprek 2 (Datum: 24/05/2024) (10.45u)

Lector: Christophe

Vragen voor dit gesprek:

- vraag 1: Is mijn UI "schets" een goede start, heb je eventueel nog tips
  -beetje onduidelijk, hier tips:
  Algemeen:

  -contrast zal donkerder moeten
  -borders
  -grafiek, je zal die meer details moeten geven, ook ev de sensoren weergeven op ander tabblad voor te checken of ze werken,...
  -Consistent hoofdlettergebruik
  -duidelijkheid / user experience
  -nuttige dingen

  Dashboard:
  -aantal spelers/users
  -laatst gespeeld

  Lampen:
  -hoe donker is het, wanneer gaan ze uit

  Games:
  -eerst single/team selecteren dan bot(of bot selecteren bij + knop)
  -Pic veranderen in naam
  -start game opvallender zetten

  Livegame:
  -team spiegelen(namen/pics buitenkant)
  -alle worpen/3dats average bijhouden

- vraag 2: Ik heb voorlopig deze routes, Zie je hier nog extras?
  -voorlopig zie ik geen extra updates

## Gesprek 3 (Datum: 27/05/2024) (12.15u)

Lector: Tijn

Vragen voor dit gesprek:

- vraag 1: Hoe zou ik het best mijn servomotor vaststeken
  gaatjes boren

- vraag 2: is het op het algemeen goed geschakeld?-> uitgesteld naar donderdag met geert
- vraag 3: kan ik mijn externe voeding aansluiten aan usb van rasp
  nee, gwn op je raspi steken
  -vraag 4: wat vind je van de average look
  best je bovenkant nog even hercutten, zo past je lcd er perfect in en kan je gaatjes voor bouten voorzien

vraag 5: waar steek ik best mijn lichtsensor
aangezien je achterkant eigenlijk de bovenkant wordt, voorzie je daar best een gaatje

vraag 6: wat doe ik met alle kabels dat ik zal moeten voorzien?
hang alle + en - aan elkaar, zo heb je maximaal 5kabels nodig

vraag 7: heb je anders nog opmerkingen?
je voorziet best nog een soort "lade" waar de cirkelkabels zich op kunnen draaien

## Gesprek 4 (Datum: 28/05/2024) (10u) (MVP01)

lectoren: Christophe, Tijn, Frederik

commentaar:

    Database: Gisteren gechecked : GOED
      - Usermode en gamemode samen steken 0,1,2
      - 3 dart average erbij steken, bijhouden in database niet in python, ook in een nieuwe tabel steken.
          Tabel: Darts
          -     Dart1
          -    Dart2
          -     Dart3
      - Dan kan je het gemiddelde berekenen.
      - Database daarna nog eens indienen bij Frederik
      - DummyData in de database stoppen.

    Fritzing: Weerstand aan de transistor.
        - Aan de Rotary encoder een ground aansluiten op schema.
        - LCD  Verticaal flippen om overlappende datalijnen van pcf8574 te vermijden


    FeedForward: OK

    Toggle: OK (wel sortering toevoegen, zo kan je achteraf makkelijk sorteren)

    Github: Project board to do.

    Foto's: OK

    Schakeling: OK, nog laten checken door Geert

    Figma: OK

algemene tip: begin alvast aan je sensoren inlezen zodat je die kan tonen op je website, want dat is wat je zal moeten tonen volgende week op MVP02

## Gesprek 5 (Datum: 30/05/2024) (13.30u) (Geert)

lector : Geert

vragen:
Zou alles goed geschakeld zijn?
ja, wel 10k weerstand bij LDR

    Zou het lukken zonder breadbordvoeding?
      ja, dat zou moeten lukken

## Gesprek 6 + 7 (Datum: 03/06/2024) (9.30u) (Stijn + Geert)

lector : Stijn, Geert

vragen:
ik heb eens nagedacht, zou het mogelijk zijn om de positie van de dart te bereken door het kruispunt van de "lijnen" die de lasers "zien" als hun signaal onderbroken wordt door de dart? ik zou al die "lijnen" in een map willen steken en dan daaruit de snijpunten berekenen.

    antw:
      dat ziet er heel ingewikkeld uit. Er is een makkelijkere manier

      geert: eventueel is het mogelijk om met één laser dat door het centrum gaat de lijn te berekenen, en dan met een time-of-flight sensor de afstand tot de dart te berekenen.

      (een mct student had ook het voorstel om met 2 lasersensors, eentje door het centrum en de andere net buiten de boule, evenwijdig met elkaar. Je laat ze draaien, de ene ziet de dart, de andere ziet de dart. Zo heb je een kruispunt(x,y), en kan je dan waarschijnlijk met pythagoras de afstand tot het nulpunt berekenen)

## gesprek 8 (datum: 12/06/2024) (2.30u) (tijn)

lector: tijn

vragen:
ik heb mijn cirkel volledig geconnecteerd op mijn arduino aan 5V, dit om de reden omdat de lasertransmitter en TOF perfect op mijn arduino kunnen runnen, MAAR mijn laserreceiver moet wel op een raspi-pin blijven hangen, zou je een manier hebben om dit te kunnen doen?

antw:
aan de hand van een weerstandsdeling (1kohm en 2kohm)

probleem:
laserreceiver leest niet in

oplossing:
weerstandsdeling was te klein, grotere weerstanden gestoken

## \***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***\*\*\*\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***feedbackmoments\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***\*\*\***\*\*\*\*\***\*\*\*\*\***\*\*\*\*\***

**\*\***MVP01**\***

Database: Gisteren gechecked : GOED - Usermode en gamemode samen steken 0,1,2 - 3 dart average erbij steken, bijhouden in database niet in python, ook in een nieuwe tabel steken.
Tabel: Darts - Dart1 - Dart2 - Dart3 - Dan kan je het gemiddelde berekenen. - Database daarna nog eens indienen bij Frederik - DummyData in de database stoppen.

Fritzing: Weerstand aan de transistor. - Aan de Rotary encoder een ground aansluiten. - LCD Verticaal flippen

FeedForward: OK

Toggl: OK

Github: Project board to do.

Foto's: OK

Schakeling: OK

Figma: OK

## MVP 2 (Datum: 04/06/2024) (9.30u) (christophe + tijn)

lector : christophe,tijn

conclusie: gebruik je github en zorg dat je meer op schema zit met alles, je hebt al van alles veel gedaan maar bent nog niet echt klaar met iets. focus ook al meer op je website

## MVP 3 (Datum: 11/06/2024) (9.30u) (Dieter + Geert + Claudia)

lector : Dieter, Geert, Claudia

conclusie: je github, toggle, website(design) zien er redelijk uit, je behuizing is al half af MAAR:

- vul je feedforward aan
- begin al aan je instructables
- doe wat user testing
- UX moet beter
- zorg dat je game al werkt
