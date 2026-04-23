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

Dette prosjektet bruker en Raspberry Pi 5 med microSD-kort som oppstartsdisk. Kortet inneholder operativsystemet og er nødvendig for at systemet skal fungere.


## Installere Raspberry Pi OS

1. Last ned og åpne **Raspberry Pi Imager**  
   https://www.raspberrypi.com/software/

2. Velg følgende:
   - **Device** → Raspberry Pi 5  
   - **OS** → Raspberry Pi OS (64-bit)  
   - **Storage** → ditt SD-kort  

3. (Valgfritt) Customisation kan brukes, men er ikke nødvendig for dette prosjektet.

4. Trykk **Write** og vent til prosessen er ferdig.

5. Sett SD-kortet inn i Raspberry Pi og start den.

6. Følg standard oppstartsprosess.

---

## Oppsett av prosjekt

Åpne terminal og kjør:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install prerequisites
sudo apt install -y git bash

# Clone repository
git clone https://github.com/Nordlendingen-og-de-andre-fra-Sor/PID-Balltrack-Semesterprosjekt

# Enter project directory
cd PID-Balltrack-Semesterprosjekt/Semesterprosjekt

# Make installer executable
chmod +x BalltrackInstaller

# Run installer
bash BalltrackInstaller

# Start application
./Balltrack
```

---

## Forventet oppførsel

```text
Hardware connected    -> Full tracking + PID control
No hardware detected  -> DummyController (simulation)
```

---

## Senere oppstart

```bash
cd ~/PID-Balltrack-Semesterprosjekt/Semesterprosjekt
./Balltrack
```

---

## Notater

- Ingen manuell konfigurasjon er nødvendig  
- Alle avhengigheter installeres automatisk  
- Systemet fungerer uten hardware (simulering)  

Etterpå kan man forvente:
Hardware connected    -> Full tracking + PID control
No hardware detected  -> DummyController (simulation)

# For senere bruk husk:
cd ~/PID-Balltrack-Semesterprosjekt/Semesterprosjekt
./Balltrack
+ Update repository
git pull

