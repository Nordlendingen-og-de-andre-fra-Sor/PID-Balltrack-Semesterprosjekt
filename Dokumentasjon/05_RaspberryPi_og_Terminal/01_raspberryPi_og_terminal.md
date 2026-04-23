# Raspberry Pi og terminal (V8 BallTrack)

Dette kapittelet beskriver bruk av Raspberry Pi som kjøremiljø for BallTrack-
prosjektet basert på V8 BallTrack-filene. Fokus er på praktisk kjøring via
terminal, samt erfaringer og begrensninger observert i prosjektets sluttfase.

---

## Rolle i systemet
Raspberry Pi benyttes som hovedplattform for kjøring av:
- PID-regulator
- kommunikasjon mot tilkoblet hardware
- grafisk brukergrensesnitt (GUI)

Målet har vært å kunne kjøre BallTrack-systemet som en selvstendig enhet uten
bruk av ekstern PC eller utviklingsmiljø.

---

## Filstruktur (V8)
V8 BallTrack-versjonen består av et samlet sett filer for regulering, GUI og
hardwarekommunikasjon. Filene er strukturert slik at prosjektet kan startes
direkte fra terminal.

De viktigste filen i denne sammenhengen er:
- V8 BallTrack Python-filer – inneholder PID-logikk, GUI og I/O-håndtering

---


## Oppdatering av kode via Git

Raspberry Pi kan brukes som ren kjøremaskin, der kildekoden holdes oppdatert
via Git.

Før oppstart anbefales det å hente siste versjon av prosjektet:

Sikre at rasperry pi er koblet til internettet.
Skrive inn path for hvor Semesterprosjektet ligger. Da skriver man cd PID-Balltrack-Semesterprosjekt/Semesterprosjekt/
Deretter sjekker man status med "git status" og hvis rasperry pi ikke er oppdatert skriver man "git pull"
