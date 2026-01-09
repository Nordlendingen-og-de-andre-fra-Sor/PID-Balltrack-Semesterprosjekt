# Reguleringsstrukturer
BallTrack-systemet er implementert som en énsløyfe, tilbakekoblet posisjonsregulering. Den regulerte størrelsen er ballens posisjon langs bjelken, mens pådraget er servomotorens vinkel som bestemmer bjelkens helning.
# Blokkskjema

<img width="1222" height="886" alt="image" src="https://github.com/user-attachments/assets/4f9504bc-2db3-4e8d-a8bd-f03c0e1d1c5a" />

# Setpunkt – r(t) 
Setpunktet r(t) representerer ønsket posisjon for kulen langs bjelken. Setpunktet angis av brukeren via LCD touch-skjermen og GUI-et, og er normalisert til en prosentverdi. Setpunktet fungerer som referanseverdien regulatoren forsøker å oppnå ved å justere pådraget til prosessen.

<img width="316" height="252" alt="image" src="https://github.com/user-attachments/assets/40c93811-81cf-4b53-b84f-ca8c4a4685bd" />

# Summeringsledd – Avvik e(t)

<img width="558" height="330" alt="image" src="https://github.com/user-attachments/assets/3cd7c1eb-ed19-4bd1-97ce-6ee797611e7a" />

Summeringsleddet beregner reguleringsfeilen: e(t)=r(t)−y(t).
der:
o	r(t) er ønsket posisjon (setpunkt)
o	y(t) er målt posisjon fra sensoren
Denne feilen uttrykker hvor langt systemet er fra ønsket tilstand og brukes som inngang til PID-regulatoren.

# PID-regulator (Kp, Ti, Td)

<img width="606" height="296" alt="image" src="https://github.com/user-attachments/assets/3c2f3841-5e81-48f1-85fe-6185cbcf0c9a" />

PID-regulatoren er gjennomført i programvaren på Raspberry Pi og beregner pådraget basert på feilen. Regulatoren består av tre ledd:
o	Proporsjonalledd (P): Gir en respons proporsjonal med feilen og sørger for rask korreksjon.
o	Integralledd (I): Summerer feilen over tid og fjerner stasjonære avvik.
o	Derivasjonsledd (D): Reagerer på endring i feilen og demper raske bevegelser og oversving.

Regulatoren kan matematisk uttrykkes som:

<img width="680" height="154" alt="image" src="https://github.com/user-attachments/assets/173b255e-a2b2-4290-87c9-b6a7567280d6" />

PID-regulatoren er implementert diskret i koden som en parallell PID, der P-, I- og D-leddene beregnes separat og summeres.

# Pådrag – u(t)

<img width="532" height="196" alt="image" src="https://github.com/user-attachments/assets/7abcd0ac-ca3a-461f-b6a3-c0d9b73cdba1" />

Pådraget  er regulatorens utgangssignal og representerer kommandoen som sendes til aktuatoren. I BallTrack-systemet kode er pådraget normalisert til intervallet:
 
Dette signalet oversettes direkte til servomotorens pulsbredde:
 
Pådraget bestemmer dermed bjelkens vinkel.

<img width="1208" height="230" alt="image" src="https://github.com/user-attachments/assets/7436d420-8f1e-45af-8f5e-9a17ee2c1191" />

# Aktuator 
Aktuatoren er en servomotor som fysisk justerer bjelkens helning. Servomotoren mottar PWM-signal fra PCA9685-driveren og omsetter dette til en mekanisk rotasjon. Servomotorens oppgave er å endre vinkelen på bjelken slik at kulen beveger seg mot ønsket posisjon.

<img width="412" height="412" alt="image" src="https://github.com/user-attachments/assets/d38ec82d-bec9-42a7-b58b-7a2163f02aba" />

# Forstyrrelse – d(t)
Forstyrrelsen d(t) representerer ytre påvirkninger som ikke kontrolleres direkte av systemet, for eksempel:
o	friksjonsvariasjoner
o	små vibrasjoner
o	ujevnheter i bjelken
o	støt på kulen
PID-regulatoren kompenserer for disse forstyrrelsene ved hjelp av tilbakekoblingen.

<img width="376" height="538" alt="image" src="https://github.com/user-attachments/assets/68718c48-e80d-48bd-9844-bcede7fd76b5" />

# Prosess og Prosessvariabel

<img width="910" height="410" alt="image" src="https://github.com/user-attachments/assets/7f861524-4f0b-43f8-b2e1-cee631fec92b" />

Prosessen består av den mekaniske sammenhengen mellom bjelkens vinkel og kulens bevegelse. Når bjelken vippes, vil kulen akselerere som følge av tyngdekraften.Ball–bjelke-systemet er i utgangspunktet ustabilt uten regulering, og krever kontinuerlig justering av vinkelen for å holde kulen i ønsket posisjon.
Prosessvariabelen y(t) er kulens faktiske posisjon langs bjelken. Denne verdien er systemets utgang og det som reguleres. Verdien sendes videre til målesystemet og tilbakekobles til regulatoren.

# Måling – SoftPot




