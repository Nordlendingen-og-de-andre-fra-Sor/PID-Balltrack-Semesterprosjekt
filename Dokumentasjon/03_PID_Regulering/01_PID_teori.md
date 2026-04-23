# PID-Teori
I dette prosjektet benyttes en standard klassiske PID-regulator og parallell PID-regulator.
# Klassisk PID
Dette er den mest brukte regulatorstrukturen i industrielle styringssystemer som PLS, DCS og SCADA. Denne formen er velkjent for både operatører og ingeniører, og de fleste etablerte innstillingsmetoder for PID-regulatorer er basert på denne parameteriseringen.
Regulatoren er bygget opp av tre parallelle ledd: et proporsjonalt ledd (P-ledd), et integrerende ledd (I-ledd) og et deriverende ledd (D-ledd). Styresignalet u(t) beregnes ut fra reguleringsavviket e(t) mellom referanseverdi og målt prosessverdi.

<img width="654" height="324" alt="image" src="https://github.com/user-attachments/assets/67ff0455-b5c2-47aa-a707-32238e7b5157" />

Matematisk uttrykk:

<img width="972" height="198" alt="image" src="https://github.com/user-attachments/assets/86e1836f-d886-4607-92db-a3d76612d430" />

hvor:
o	Kp
er proporsjonalforsterkningen
o	Ti
er integraltiden
o	Td
er derivattiden
Denne strukturen tilhører klassisk lineær reguleringsteori og brukes som standard i industriell regulering på grunn av sin enkle tuning, stabile oppførsel og gode praktiske egenskaper.

# Parallell PID
PID-regulatoren i BallTrack-systemet er implementert som en parallell PID-regulator også, der de proporsjonale, integrerende og deriverende leddene beregnes uavhengig av hverandre og deretter summeres til ett felles pådrag.
Dette er den mest brukte PID-strukturen i digitale reguleringssystemer og er spesielt godt egnet for implementasjon i programvare som Python.
I parallell PID er hver regulatorparameter uavhengig, noe som gir god oversikt og enkel justering av hvert enkelt ledd.
# Matematisk beskrivelse av PID
Den kontinuerlige reguleringsligningen kan skrives som:
Klassisk PID

<img width="614" height="120" alt="image" src="https://github.com/user-attachments/assets/1016c5ad-899c-4e96-bcc8-3cdc7be0ef78" />

o	 er reguleringsfeilen
o	 er proporsjonalforsterkningen
o	  er integraltid
o	 er derivasjonsleddets forsterkning
o	 er regulatorens utgang (pådrag)

#Parrallell PID

<img width="648" height="136" alt="image" src="https://github.com/user-attachments/assets/1c5a7c50-d1a5-42aa-b45b-539408f1bad4" />

der:
o	 er reguleringsfeilen
o	 er proporsjonalforsterkningen
o	 er integralleddets forsterkning
o	 er derivasjonsleddets forsterkning
o	 er regulatorens utgang (pådrag)

Denne formen tilsvarer direkte det som er gjennomført i koden.
 
#Forklaring av hvert ledd

#Klassisk PID 

<img width="1298" height="398" alt="image" src="https://github.com/user-attachments/assets/a909e0fc-5ddc-46ee-8026-5c61bd4d7f28" />

#Parallell PID

<img width="1240" height="414" alt="image" src="https://github.com/user-attachments/assets/88d651c8-52c3-49dc-96ef-5e8536bd065d" />

#Proporsjonalledd (P-ledd)

<img width="274" height="68" alt="image" src="https://github.com/user-attachments/assets/9868684c-3e65-4453-bb60-8bfdb74411b8" />

P-leddet gir et utsignal som er direkte proporsjonalt med feilen. Jo større avvik mellom setpunkt og måleverdi, desto større pådrag.
P-leddet gir rask respons, men kan alene føre til stasjonær feil.

#Integralledd (I-ledd)

<img width="554" height="200" alt="image" src="https://github.com/user-attachments/assets/d7fe2d0d-f666-48c9-a408-a493a15cb897" />

I-leddet summerer feilen over tid og sørger for at systemet når nøyaktig setpunkt. Dette eliminerer stasjonær feil som kan oppstå ved bruk av kun P-ledd.
I BallTrack-koden beregnes integralleddet diskret, og det benyttes metning (anti-windup) for å hindre at integratoren bygger seg opp ukontrollert.
 
#Derivasjonsledd (D-ledd)

<img width="590" height="304" alt="image" src="https://github.com/user-attachments/assets/2320f125-0658-40db-aef1-2723ac3ca870" />

D-leddet reagerer på hvor raskt feilen endrer seg. Dette gir en forutseende effekt som demper raske bevegelser og reduserer oversving i systemet.
I praksis bidrar D-leddet til å stabilisere ballens bevegelse på bjelken.
  
#Sammenheng mellom PID og kode
I BallTrack-koden beregnes PID regulatoren diskret for hvert tidssteg:
o	P-ledd: direkte fra aktuell feil
o	I-ledd: akkumulert feil over tid
o	D-ledd: endring i feil mellom to tidssteg
Deretter summeres leddene og begrenses før signalet brukes videre til servostyring. Dette samsvarer direkte med blokkskjemaet for parallell PID.

