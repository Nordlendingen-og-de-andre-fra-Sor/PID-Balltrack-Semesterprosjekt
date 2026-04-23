# PID-Balltrack-Semesterprosjekt

FORMÅL
-------
Dette prosjektet utvikles som en PID-reguleringsplattform for Balltrack-systemet —
en oppgave hvor en ball balanseres på en bevegelig bane ved hjelp av en servo.

Prosjektet skal gi mulighet til å:
- Justere P, I og D-parametere i sanntid via GUI
- Observere systemets respons (simulert eller reell)
- Til slutt kjøre på Raspberry Pi med fysisk servo og sensor
Prosjektet er utviklet som et lærings- og utviklingsprosjekt, og leveres i prototypeform.

KORT BESKRIVELSE

BallTrack-systemet er en én-sløyfe tilbakekoblet reguleringsoppgave der ballens posisjon langs en bane reguleres ved å endre banens helningsvinkel.

PID-regulatoren er implementert i programvare, mens måling og pådrag skjer via fysisk maskinvare. Et grafisk brukergrensesnitt gjør det mulig å overvåke systemet og justere regulatorparametere i sanntid.

Hva prosjektet inneholder:
- 1D PID-regulator (parallell struktur)
- Grafisk brukergrensesnitt (GUI)
- Støtte for sanntidsjustering av regulatorparametere
- Grunnlag for kjøring på Raspberry Pi
- Skript for oppsett og oppstart via terminal
- Dokumentasjon av system, hardware og reguleringsstruktur

DOKUMENSTASJON

Utfyllende dokumentasjon finnes i mappen "Dokumentasjon" og dekker blant annet:
- Systemoversikt og reguleringsstruktur
- Hardwareoppsett og koblinger
- PID-regulator (teori og implementasjon)
- GUI-funksjonalitet
- Raspberry Pi og terminalbruk
- Kjente begrensninger og forslag til videre arbeid

For praktisk overlevering, se HANDOVER.md.

# Quick start
Dette prosjektet tar i bruk en Raspberry Pi 5 og den bruker en microSD som "oppstartsdisk". Den inneholder operativsystemet og er nødvendig for generell funksjon.'

For å sette opp ny OS må man laste ned en Raspberry Pi Imager. Nettside: https://www.raspberrypi.com/software/ 
Her setter man preferanser for OS innstillinger.
Device - Velger din type Raspberry Pi
OS - Velger operativ system, her velger man Raspberry Pi 5.
Storage - Velg ditt SD-kort.
Videre er det opp til bruker om man ønsker å ta i bruk "customisation". Dette er ikke nødvendig for dette prosjektet.
Write - Når du har valgt Device, OS og Storage så er det bare å trykke "Write".

Etter writing av SD-kort er fullført så legger man inn kortet inn i mikrokontrolleren og booter opp.

Følg instrukser under oppstart etter boot er i gang.
Deretter åpne terminal (svart ikon) og følg instrukser under.

Update system:
sudo apt update && sudo apt upgrade -y

Install prerequisites:
sudo apt install -y git bash

Clone repository:
git clone https://github.com/Nordlendingen-og-de-andre-fra-Sor/PID-Balltrack-Semesterprosjekt

Enter project directory:
cd PID-Balltrack-Semesterprosjekt/Semesterprosjekt

Make installer executable:
chmod +x BalltrackInstaller

Run installer:
bash BalltrackInstaller

Start application:
./Balltrack

Etterpå kan man forvente:
Hardware connected    -> Full tracking + PID control
No hardware detected  -> DummyController (simulation)

# For senere bruk husk:
cd ~/PID-Balltrack-Semesterprosjekt/Semesterprosjekt
./Balltrack
+ Update repository
git pull

