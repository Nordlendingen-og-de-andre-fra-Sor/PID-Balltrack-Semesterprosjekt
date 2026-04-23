# Semesterprosjekt
Undervisningsverktøy: PID Regulator med touchdisplay


21.10.25 
Bjørnar var ikke til stedet når vi hadde README undervisning, så han har gjort masse greier. Som å gi et forslag til GUI som er kjørbart, i tillegg, under er både main, pid og servo kode som simulerer PID i GUIen.


BALLTRACK PID-PROSJEKT
=========================

20:39 21.10.2025

Bjørnar Vatne

FORMÅL
-------
Dette prosjektet utvikles som en PID-reguleringsplattform for Balltrack-systemet —
en oppgave hvor en ball balanseres på en bevegelig bane ved hjelp av en servo.

Prosjektet skal gi mulighet til å:
- Justere P, I og D-parametere i sanntid via GUI
- Observere systemets respons (simulert eller reell)
- Til slutt kjøre på Raspberry Pi med fysisk servo og sensor

------------------------------------------

PROSJEKTSTRUKTUR
----------------
balltrack/
├─ app/
│  ├─ main.py           - Programstart (entry point)
│  ├─ config.py         - Innstillinger og valg av backend
│  └─ factory.py        - Lager riktige objektinstanser (servo, sim, osv.)
│
├─ gui/
│  └─ pid_gui.py        - Tkinter-basert GUI med slidere for Kp, Ki, Kd
│
├─ control/
│  └─ pid.py            - Selve PID-algoritmen (u = Kp*e + Ki*∫e + Kd*de/dt)
│
├─ drivers/
│  ├─ servo_base.py     - Felles grensesnitt (IServo)
│  ├─ servo_mock.py     - Simulert servo for PC-testing
│  ├─ servo_pigpio.py   - Servo-driver for Raspberry Pi (pigpio)
│  └─ servo_pca9685.py  - I2C-driver (Adafruit PCA9685)
│
├─ sim/
│  └─ ballbeam.py       - Fysisk modell av ball-på-bjelke-systemet
│
├─ logs/                - Automatisk loggmappe fra run_balltrack.bat
├─ requirements.txt     - Avhengigheter (pigpio/PCA9685 kommentert ut foreløpig)
├─ run_balltrack.bat    - Launcher som starter GUI og logger konsoll-output
└─ README.txt           - Denne filen

------------------------------------------

STATUS OG FUNKSJONER
--------------------
 Oppsatt/ikke testet GUI
- Tkinter-grensesnitt med slidere for Kp, Ki, Kd
- Setpunkt-inndata
- Sanntidsvisning av PV (målt verdi)
- Start/Stop-knapp
- Enkel grafisk visning av ballens posisjon (Canvas)

Oppsatt/ikke testet PID-logikk
- Egen modul (control/pid.py) med anti-windup og metning
- Kan brukes både i simulasjon og mot ekte maskinvare

Oppsatt/ikke testet Simulator (SimBallBeam)
- Numerisk modell som gir realistisk oppførsel av ball-på-bjelke
- Kobles automatisk inn når SIMULATION = True

Oppsatt/ikke testet Modulært design
- Eget grensesnitt for servo (drivers/servo_base.py)
- Lett å bytte mellom mock, pigpio eller PCA9685

Oppsatt/ikke testet Launcher med logging
- run_balltrack.bat aktiverer .venv og logger output til logs/
- Holder terminalvinduet åpent for feilsøk og varsler

------------------------------------------

VALG OG PRINSIPPER
------------------
- Prosjektet skal kunne kjøres både på Windows (simulasjon) og Raspberry Pi (reell regulering)
- Maskinvareavhengigheter installeres ikke automatisk — aktiveres via requirements.txt
- Lazy-import brukes for å unngå feil i simulasjon
- Mappe 'io/' ble endret til 'drivers/' for å unngå konflikt med standardbiblioteket 'io'

------------------------------------------

BRUK
----
Første gang (PC-test):
    setup_env.bat     - Lager virtuell environment og installerer krav
    run_balltrack.bat  - Starter GUI med simulering
Sørg for at SIMULATION = True i app/config.py

Ved overgang til Raspberry Pi:
1. Sett SIMULATION = False
2. Fjern kommentaren foran riktig driver i requirements.txt
   f.eks. 'pigpio; platform_system == "Linux"'
3. Kjør setup_env.bat på Pi for å installere pigpio
4. Start run_balltrack.bat (eller .sh senere)

------------------------------------------

PLANLAGTE VIDERE STEG
----------------------
- Fullføre logging av regulatorparametre til CSV
- Lage enkel feilhåndtering/varsling i terminal
- Implementere sensorgrensesnitt (kamera/analog sensor)
- Portere launcher til Linux (.sh)
- Teste fysisk PID-regulering på Raspberry Pi

------------------------------------------

PROSJEKTSTATUS
---------------
| Komponent | Status | Kommentar |
|------------|:------:|-----------|
| GUI | Oppsatt/ikke testet | Kjører stabilt i sim-modus |
| PID | Oppsatt/ikke testet | Ferdig testet med simulering |
| Simulator | Oppsatt/ikke testet | Realistisk respons |
| Servo-mock | Oppsatt/ikke testet | Brukes på PC |
| Pigpio-driver | Satt på pause | Venter på fysisk oppsett |
| Logging / Launcher | OK | Fungerer på Windows |
| Raspberry Pi-oppstart | Satt på pause | Tas ved neste holdepunkt |

------------------------------------------
KOMPONENTBESKRIVELSE
-------------------
## Raspberry Pi
![raspberry_pi](https://github.com/user-attachments/assets/a9ef0a46-1cdf-409d-8d2c-20a40bdc1aa7)

**Hovedprosessor og styringsenhet**
Raspberry Pi fungerer som hovedprosessoren i Balltrack-systemet og kjører all programvare relatert til sanntidskontroll, PID-regulering, kommunikasjon og brukergrensesnitt. 
Maskinvaren består av et ARM-basert mikrodatakort med 3.3 V logikk og et komplett Linux-operativsystem (Raspberry Pi OS). 

**Funksjon i systemet:**
Pi-en fungerer som hjernen i systemet
Leser sensorverdier fra Arduino via seriell-USB-kommunikasjon (UART over USB). 
Beregner reguleringssignalet i PID-algoritmen (Python). 
Sender servo-posisjoner til PCA9685-modulen via I²C-protokollen. 
Kjører GUI (Tkinter) som lar brukeren overvåke systemet, endre PID-verdier og observere responser i sanntid. 

**Kobling:**
3.3 V brukes som logikknivå for kommunikasjon. 
5 V fra Tagan PSU brukes til å forsyne Raspberry Pi via GPIO 5V. 
Felles GND kobles til både Arduino, PCA9685 og servoens jord. 
Introduction to the Raspberry Pi GPIO and Physical Computing - SparkFun  Learn 
Raspberry Pi bruker to kommunikasjonsgrensesnitt parallelt: 
I²C (SDA = GPIO 2, SCL = GPIO 3) for kommunikasjon med PWM-modulen. 
USB-serial (ttyACM0) for kommunikasjon med Arduino, som leverer sensorverdier. 
<img width="912" height="538" alt="kobling_rasperry_pi" src="https://github.com/user-attachments/assets/ddbb9ae7-4aca-4bef-8aff-d9c631ad0f22" />
Pi-en driver ikke servoen direkte, siden PWM-signalene fra Pi har lav oppløsning og er programvarebasert, og dermed for ustabile til presis servo-kontroll. I stedet sendes kommandoer til en ekstern PWM-driver (PCA9685). 

## Arduino Uno Rev 4 WiFi
**ADC-grensesnitt**
<img width="729" height="545" alt="arduino_r4_wifi" src="https://github.com/user-attachments/assets/e8b8d8fd-0258-4210-a5a0-2703b55e21ce" />

Arduino er systemets analog-til-digital-konverter (ADC). 
Grunnen til at Arduino brukes her er at Raspberry Pi ikke har egne analoge innganger, og dermed ikke kan lese et spenningssignal direkte fra softpot-sensoren. 
<img width="600" height="308" alt="analog_digital_converter" src="https://github.com/user-attachments/assets/8bd048f6-6604-4cee-910c-37433917ed8f" />

**Funksjon:** 
Arduino gjør følgende: 
Mates med 5 V fra strømforsyningen. 
Gir 5 V referansespenning til softpot-sensorens VCC-pin. 
Leser sensorens midtpinne (utgangsspenning) som et analogt signal på A0. 
Konverterer denne spenningen (0–5 V) til et tall mellom 0 og 1023 ved hjelp av sin 10-bit ADC. 
Sender verdien fortløpende til Raspberry Pi via USB-seriell-port (115 200 baud). 

**Kommunikasjon:**
Input: analog spenning (0–5 V) 
Output: tekstverdi via Serial (f.eks. “512”) 
Protokoll: enkel UART over USB, 8N1-format 
Oppdateringsfrekvens: ca. 200 Hz (hver 5 ms i koden) 
Dette gjør at Pi kan motta kontinuerlig strøm av data som representerer ballens posisjon på bjelken. 
<img width="780" height="625" alt="kobling_arduino" src="https://github.com/user-attachments/assets/0cde41b1-44f4-424b-9ff8-b5550aed14c5" />

**Virkemåte:**
Arduino sitt ADC-system består av en sample-and-hold-forsterker og en 10-bit suksessiv tilnærming-konverter (SAR). 
ADC-inngangen har høy impedans (>100 MΩ), slik at sensoren ikke belastes merkbart. 
Dette gir en fast datastrøm til Pi-en som Python-koden deretter bruker som målesignal 
y(t)

## Diverse Komponenter

**Posisjonsmåling: SP-L-0400-203-3%-ST**
<img width="702" height="473" alt="softpot-trykk" src="https://github.com/user-attachments/assets/26ca199c-8510-49d1-955d-b3373d5ce198" />

Softpot-sensoren fungerer som en lineær posisjonssensor basert på variabel motstand. 
Den består av en tynn polymerfilm med et resistivt belegg (totalt ca. 20 kΩ) og en toppfilm med ledende spor. Når en metallkule ligger oppå, skapes kontakt mellom de to lagene og gir en bestemt resistans ut fra kontaktpunktet. 

Oppbygning av soft pot: d, mens duty cycle angir hvor stor andel av tiden signalet er “på”. 

SIST OPPDATERT
---------------
21. oktober 2025


--------------------------------------
Bjørnar
13:55 22.10.2025

MÅLINGER PÅ SOFTPOT
Verdier 
MIN = 1,375 kohm
Max = 20 kohm

Modell SP-L-0500-203-3%-ST

Linear motstand
Konkluderte at nytt soft potensiometer er nødvendig grunnet skadet tilkoblingspkt.

Verifiser mot RasPi5 for digital inngang parameter


19:21 22.10.2025



_______________________________________________--
23.10.2025 Ball & Beam PID-treningsrigg

Komponentoversikt

Ball and Beam-modul

     -Består av metallplate med to stenger.
     -En motor (servomotor) justerer vinkelen på stengene.
     -Sensor registrerer ballens posisjon. SoftPot Position Sensor.
	 
Motor og kjøleribbe

      -Montert på venstre side av metallplaten.
	  -Tilkoblet via skruterminal til strømforsyning og kontrollkort.
		
Strømforsyning (Tagan PSU)

     -Leverer 5 V og 12 V til systemet.
     -Kabler ført gjennom koblingslist til breadboard og motor.
	 
Koblingslist / Terminalblokk

     -Samler signal- og spenningsledninger.
     -Kobler strømforsyning til breadboard og mikrokontroller.
	 
Breadboard med elektronikk

     -Mikrokontrollerkort Ardouino.
     -RasberryPi
	 
Kommunikasjonskabler

     -USB-kabel til PC (for data og programmering).
     -Signalledninger mellom sensor, forsterker og mikrokontroller.
     @ -194,6 +194,39 @@ Kommunikasjonskabler

     -USB-kabel til PC (for data og programmering).
     -Signalledninger mellom sensor, forsterker og mikrokontroller.

_________________________________________
29.10.2025
Julian Rødal:
<img width="1536" height="1024" alt="Tegning av brett" src="https://github.com/user-attachments/assets/9d8b770d-3fbc-4770-af07-6e1864124b80" />

Petter Kildal:
Blitt enig om komponentplassering på hovedbrett.

Endelig plassering av komponenter er bestemt med følgende layout:

### Venstre seksjon
- Balltrack-softpot montert langs venstre kant
- Øverst tilkobling til softpot
- Servomotor installert ved basis av balltrack
- Nederst integrert med eksisterende servotilkobling

### Høyre øvre seksjon
- Kombinert Rasperry Pi og touchskjerm
- Arduino for softpot måling og analog/digital omforming

### Midtre seksjon
- Motordriver for servo (i beskyttende plastemballasje)
- Tilkoblingspunkt for Raspberry Pi og touchskjerm
- Breadboard for elektronikk og signalruting

### Høyre nedre seksjon
- Strømforsyningsenhet
- Rekkeklemmer for spenningsfordeling:
  - 5V + og - distribusjon
  - 12V + og - distribusjon
  - Signallinjer

Denne layouten optimaliserer:
- Kort kabellengde mellom servo og driver
- Enkel tilgang til strømfordeling
- Oversiktlig signalruting mellom komponenter


------------------------------------------------------
30.10.2025
Bjørnar Vatne

Små endringer for å kunne kjøre testing av programmet simulert før integrering av reel versjon beregnet for hardware

Aslak Aarsland:
Montert opp arduino og ledninger fra strømforsyning og skiftet softpot på balanseskinnen. Loddet tilkoblinger servodriver. 

Isak Abdulkadir Isak:
Valg av servomotor;
Det er valgt en Savox SC-1267SG som pådragsorgan. Servomotoren styres via PWM-signal (Pulsbreddemodulasjon) fra komponenten PCA9685, ettersom Raspberry Pi ikke håndterer analoge signaler.

Motoren har en rotasjonsgrense på 200° ±10°, som dekker prosjektets behov på maks 180°. Den drives med 5 V og yter et dreiemoment på 9,36 kg/cm (130 oz/in).

Servo modul av typen PCA9685 er ting vi kan se nermere 

------------------------------------------------------
06.11.2025
Tester Arduino om den leser Softpot verdi.
Topp verdi, 961
Middel verdi, 458
Bunn verdi, 45

Deretter tester 10V supply fra PSU:
Visuelt ser alt bra ut, styrke på LED er lik som 5V USB C fra en pc.
Ved berøring har temperaturen ikke endret seg heller. Samt å la den stå på over tid er det ingen endringer.

I tillegg, skal man teste kommunikasjon mellom Arduino og Rasperry Pi:

12.11.2025
P og B
Hafrun kom med et forslag om å bytte arduinoen med en rasperry pi hatt. Den skal kunne også lese analoge signaler, derfor fjernet vi arduinoen for å slippe å ha den som et mellomledd. (Arduinoen kan også være mer ustabil enn Rasperry Pi)
![image](https://github.com/user-attachments/assets/37f5a272-ad07-43a2-af6d-e6de9ffc86a4)

13.11.2025
Bjørnar, Julian og Petter:
Etter testing av forskjellige spenningskilder til PSUen for å forsyne Rasperry Pi 4B + touch skjerm + hatt koblet til driver. Har vi konkludert at eksisterende strømforsyning ikke kan forsyne nevnt utstyr.
Fant ut med Chatgpt som kilde, at Rasperry Pi kan ha 5V som forsyningsspenning, og skal ikke overstige 5,25V for å unngå overspenning. 
Testet uttak 5,09V som målt, for den var ideel for forsyning. Når vi skrudde på PSUen, så startet selve Rasperry Pi, men touch skjermen lyste ikke opp. Målte uttaket og den droppet frta 5,09V til 4,7V som er underspenning.
Koblet deretter fra skjermen til 5,3V uttaket til PSUen, mens resten ble på allerede brukt 5,09V. Satt spenning på PSUen og ingenting lyste opp. Målte spenning på 5,09V uttaket og den viste 2,0V.
Da som nevnt kan strømforsyningen ikke levere til utstyret vårt og blir nødt til å finne alternativ PSU.

Koblet etterpå Bjørnars laptop lader som er USB-C 5V 65W. Den leverte mer en nok til utstyret.

Bjørnar do software:
Tester analog lesing av softpot med bruk av Rasperry Pi istedenfor Arduino. Etter litt frem og tilbake med terminal trykking og diskutering med Chatgpt begynner vi med read_softpot.py
Lager et test program for å sjekke om alle bibliotek er oppdatert og installert. Møtte på mye problemer med HAT-en grunnet den er egnet for Rasperry Pi 2 og 3.


Oppdatert versjon av komponent plassering:

Venstre seksjon
- Balltrack-softpot montert langs venstre kant
- Øverst tilkobling til softpot
- Servomotor installert ved basis av balltrack
- Nederst integrert med eksisterende servotilkobling

Høyre øvre seksjon
- Kombinert Rasperry Pi og touchskjerm
- I tillegg HAT for måling og analoglesing av softpot

Midtre seksjon
- Motordriver for servo (i beskyttende plastemballasje)
- Tilkoblingspunkt for Raspberry Pi og touchskjerm
- Breadboard for elektronikk og signalruting

Høyre nedre seksjon
- Strømforsyningsenhet
- Rekkeklemmer for spenningsfordeling:
  - 5V + og - distribusjon
  - 12V + og - distribusjon
  - Signallinjer

Denne layouten optimaliserer:
- Kort kabellengde mellom servo og driver
- Enkel tilgang til strømfordeling
- Oversiktlig signalruting mellom komponenter

19.11.2025

Konkret loggføring av hele prossesen for HAT-en til Rasperry pi 4:

1. Mål
Mål: Lese verdien fra en SoftPot koblet til Grove Base HAT for Raspberry Pi på A0, direkte i terminal.
Plattform: Raspberry Pi 4B + Grove Base HAT + SoftPot + PCA9685 (servo-driver).

2. Første forsøk – bibliotek og I²C
- Bibliotek-installasjon
Forsøk: pip3 install --upgrade seeed-python-grove
Resultat: Feil – pakken finnes ikke på PyPI.
Tiltak: Gikk over til grove.py (Seeed sitt nyere Python-bibliotek).

- Installere grove.py
Kommando: sudo pip3 install grove.py
Etterpå: from grove.adc import ADC fungerte i Python.

- Aktivering av I²C og brukerrettigheter
sudo raspi-config → aktiverte I²C.
sudo usermod -aG i2c <bruker> og sudo usermod -aG gpio <bruker>
Reboot.
Verifisering: i2cdetect -y 1 viste:
0x08 – ADC / MCU på Grove HAT
0x40 – PCA9685
0x63, 0x70 – andre HAT-funksjoner

3. Problem 1 – grove.adc nekter å lese ADC
- Første SoftPot-skript via grove.adc
Enkelt skript med ADC() og adc.read(0).
Feil:
“Check whether I2C enabled and Grove Base HAT RPi is inserted”

- Forsøk på å fikse adresse i adc.py
Fant ut via inspect.getsourcefile(grove.adc) at:
koden ligger i /usr/local/lib/python3.9/dist-packages/grove/adc.py
adc.py viste seg å være en tom stub-fil – selve logikken ligger i en kompilert .so-fil.
Konklusjon: Vi kan ikke patche adressen direkte i Python-filen.

- Installere grove fra GitHub
git clone https://github.com/Seeed-Studio/grove.py
sudo pip3 install .
git checkout dev fungerte ikke – ingen dev-branch lenger.
Etter installasjon: fortsatt samme feilmelding i grove.adc.
→ Delkonklusjon: grove.adc-implementasjonen vi hadde, matchet ikke HAT-revisjonen (MM32 / 0x08). Vi trenger en annen tilnærming.

4. Problem 2 – Direkte I²C-lesing gir bare 0
- Bytte til lavnivå I²C-lesing (smbus2)
Installerte:
sudo apt-get install python3-smbus i2c-tools
sudo pip3 install smbus2
Lagde softpot_i2c_raw.py som:
leste 2 byte fra adresse 0x08, register 0x10 (A0).
Resultat: raw=0 hele tiden, selv når kula ble flyttet.
- Utvidet skanning – adc_scan.py
Lagde skanner som leste alle 8 kanaler (0x10–0x17).
Resultat: alle kanaler viste 0 hele tiden.
→ Delkonklusjon:
I²C-kommunikasjon fungerer (ingen feil).
Men ADC-en rapporterer bare 0 → enten leser vi feil format/registre, eller det kommer ingen spenning inn på ADC-kanalen.

5. Sjekk av kobling og hardware
- Verifisering av kobling
Grove A0-port:
GND (sort), 3V3 (rød), ADC-signal (gul), NC (hvit).
SoftPot:
+V → 3V3 (rød)
GND → GND (sort)
Wiper → Signal (gul)
Hvit fra Grove-kabel ikke tilkoblet
Bekreftet at plugg sitter i A0-porten på HAT-en.
→ Koblingsoppsettet er korrekt i teorien.

6. Løsningen – bruke grove.adc korrekt med adresse 0x08
- Ny tilnærming: bruke grove.adc med eksplisitt adresse
Vi erstattet egen I²C-kode med dette i adc_scan.py:
 
from grove.adc import ADC
adc = ADC(address=0x08)
 
print("HAT-navn :", adc.name)
print("FW-versjon:", adc.version)
 
while True:
    raws  = [adc.read_raw(ch)     for ch in range(8)]
    volts = [adc.read_voltage(ch) for ch in range(8)]
    ...

- Kjøring av nye adc_scan.py
Programmet startet uten feilmelding.
Viste:
HAT-navn
Firmware-versjon
Løpende oversikt over 8 råverdier og spenning per kanal.
Når kula ble flyttet på SoftPot:
Én av kanalene begynte å endre seg → SoftPot-verdien ble korrekt lest.
→ Hovedkonklusjon:
Det var mulig å bruke grove.adc, men vi måtte:
Sørge for at riktig versjon av grove.py var installert, og
Konstruere ADC-objektet med address=0x08 (ny HAT-revisjon).

7. Læringspunkter 
- I²C-feil vs. ADC-feil
i2cdetect med flere adresser (0x08, 0x63, 0x70, 0x40) viste at bussen var OK tidlig.
Feilen lå i driver/konfig, ikke i maskinvare eller I²C-setting.
- HAT-revisjoner og adresser
Grove Base HAT har minst to varianter:
Gammel: ADC på 0x04 (STM32)
Ny: ADC på 0x08 (MM32)
Dokumentasjon og bibliotek må matche revisjonen.
- Bibliotek fra PyPI vs. GitHub
PyPI-versjonen av grove.py var ikke tilstrekkelig for vår HAT.
Installasjon fra GitHub kombinert med eksplisitt adresse ga fungerende løsning.
- Systematisk feilsøking
Aktivere I²C + brukerrettigheter (usermod).
Verifisere med i2cdetect.
Forsøke eksisterende high-level-driver (grove.adc).
Falle tilbake til lavnivå (smbus2) for å sjekke om verdier i det hele tatt endres.
Til slutt tilbake til high-level-driver med riktig konfigurasjon.

8. Loggføring – Testing av servo med Raspberry Pi og PWM-driver

Under første test kjørte vi servoen via Raspberry Pi gjennom PWM-driveren, men kun med signalledningen tilkoblet. Dette førte naturlig nok til feil funksjon. Servoen var fortsatt forsynt direkte fra Tagan-strømforsyningen med 5 V og GND, noe som innebar at PWM-driveren og Raspberry Pi manglet en felles referanse mot servoens GND. Uten denne delte referansen blir PWM-signalet i praksis meningsløst for servoen.

For å løse dette ble strømoppsettet endret: Tagans 5 V og GND føres nå inn i PWM-driveren, som videre distribuerer både spenning og referanse til servoen. Henrik produserte samtidig en base for servotest, men denne manglet inngangsverdier fra programmet. Etter at disse verdiene ble implementert, fungerte oppsettet som forventet.

Med alle komponenter på felles referanse responderte servoen korrekt på ønskede vinkelkommandoer.



-------20.11.2025--------- Bjørnar Vatne----------
Omstrukturering av gamle versjoner og merke disse med versjonsnummer. Nytt oppsett i V4 bruker det vi har lært under testing og identifisering av adresser i i2c protokoll. Legger inn de biblioteker som vi trenger å bruke etter funn under testing. Nytt oppsett i V4 er enkelt for å kunne starte opp på raspi. Legger og in lazy setup og launch for å kunne starte opp enkelt på raspi.

20.11.2025
Aslak Aarsland
Ferdigstilte 3D printet case til PWN driver kortet. Montert på brettet. ble veldig smooth. 

-------21.11.2025---------Petter Kildal-----------
Balltrack Pi – Systemoppsett, Feilrettinger og Endringer

Dette dokumentet oppsummerer arbeidet med å rydde opp i installasjonsfeil, forbedre kodebasen og sikre stabil oppstart av Balltrack-systemet på Raspberry Pi. Det fungerer som teknisk logg og systemoversikt.

1. Fjerning av ugyldig APT-repository (Seeed Stretch)

Under første kjøring av setup.sh stoppet installasjonen på grunn av et gammelt, usignert Seeed-depot:
https://seeed-studio.github.io/pi_repo stretch

Dette depotet stammer fra et tidligere oppsett og førte til GPG-feil under apt update.

Løsning:
Filen ble identifisert og slettet;
sudo rm /etc/apt/sources.list.d/seeed.list

Deretter fungerte sudo apt update uten problemer.

2. Fullføring av setup-skript

Etter opprydding kjørte:
sudo ./setup.sh
Skriptet utførte:  
- installasjon av nødvendige Python- og systempakker
- aktivering av I²C
- opprettelse av venv
- installasjon av Adafruit-biblioteker
- kloning og installasjon av grove.py
- deteksjon av I²C-enheter: 0x08, 0x40, 0x70

3. Programmet hang ved oppstart (PCA9685-driveren)

Ved kjøring av launch.sh stoppet programmet på:
Initialiserer PCA9685 (addr=0x40, servo-kanal=0)...

Årsaken lå i en blokkering i I²C-låserutinen i pca9685_driver.py:
while not self.i2c.try_lock():
    time.sleep(0.001)
Dette kan føre til deadlock på enkelte Pi-systemer.

Løsning: enklere og stabil I²C-initialisering

Hele låserutinen ble fjernet. __init__ bruker nå Adafruit Blinka til å håndtere låsing automatisk.

Endret kode
# Opprett I2C-buss (Blika håndterer locking selv)
self.i2c = i2c or busio.I2C(board.SCL, board.SDA)

# Sett opp PCA9685-modulen
self.pca = PCA9685(self.i2c, address=i2c_addr)
self.set_pwm_freq(freq_hz)

print(f"[PCA9685Driver] Init OK (addr=0x{i2c_addr:X}, freq={freq_hz} Hz)")

Resultat:
- programmet går videre uten heng
- GUI lastes inn
- servo og ADC initialiseres riktig

4. Rettet syntaksfeil i __init__

Manglende : etter funksjonsdefinisjon førte til Python-feil.
Signaturen ble rettet til:
def __init__(
    self,
    i2c_addr: int = 0x40,
    freq_hz: int = 50,
    i2c: Optional["busio.I2C"] = None
):

5. Systemstatus etter retting

Alt fungerer nå som forventet:

- launch.sh starter programmet korrekt
- PCA9685 initialiseres uten heng
- Tkinter-GUI vises som det skal
- ADC-verdier og servoer fungerer
- PID-løkka er klar for videre tuning

10.12.2025
Aslak Aarsland
Etter en del klatt med 3Dprinterens oppsett, så har vi endelig ett deksel til R pie skjermen, som kan festes til brettet. 