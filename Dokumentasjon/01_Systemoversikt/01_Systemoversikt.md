# Systemoversikt

BallTrack er et 1D reguleringssystem der posisjonen til en ball på en
bevegelig bane styres ved hjelp av en PID-regulator. Systemet er bygget som
en lukket reguleringssløyfe med sensorbasert tilbakekobling.

---

## Hovedfunksjon
Systemets hovedfunksjon er å holde ballen i ønsket posisjon langs banen ved
å justere banens helningsvinkel via en servomotor.

---

## Systemoppbygning
Systemet består av følgende hoveddeler:
- Målesystem (posisjonssensor)
- Regulator (PID)
- Aktuator (servomotor)
- Prosess (ball og bane)
- Brukergrensesnitt (GUI)

---

## Signal- og dataflyt
Reguleringssløyfen fungerer som følger:
1. Bruker angir ønsket posisjon (setpunkt) via GUI
2. Posisjonssensor måler ballens faktiske posisjon
3. Reguleringsfeil beregnes i programvaren
4. PID-regulatoren beregner pådrag
5. Servomotoren justerer banens helning
6. Ballens posisjon endres og måles på nytt

---

## Systemgrenser
Systemoversikten beskriver den overordnede strukturen og samspillet mellom
systemets hoveddeler.

Detaljert informasjon om reguleringsteori, hardwarekoblinger og kode finnes
i egne dokumentasjonskapitler.
