# Pådragsorgan - Servomotor
![alt text](09_images/servomotor.png)

Som pådragsorgan i BallTrack-systemet er det benyttet en servomotor. En servomotor er en elektrisk motor som muliggjør presis styring av vinkelposisjon ved hjelp av pulsbredde-modulasjon (PWM). Servomotorer benyttes ofte i reguleringstekniske applikasjoner innen robotikk, automatisering og mekatronikk.

Servomotoren mottar et PWM-signal med fast frekvens (50 Hz), der pulsbredde mellom ca. 1,0 ms og 2,0 ms tilsvarer henholdsvis minimums- og maksimumsposisjon. I BallTrack-systemet brukes servomotoren til å justere helningsvinkelen på bjelken, og dermed styre ballens posisjon langs banen.

Servoen drives av ekstern 5 V strømforsyning for å sikre tilstrekkelig moment og for å unngå spenningsfall i styreelektronikken. PWM-signalet genereres av en PCA9685 PWM-modul, som gir høy oppløsning og stabil signalgenerering.

Det er valgte en Savox SC-1267SG servomotor. Den har en rotasjonsgrense på 200° ±10°. Dette er innenfor vår
 rotasjon som gir til å maks 180°. Spenningskilden vår leverer 5 volt som gir et dreiemoment på 130 oz/in eller 9,36 kg/cm. Radiusen fra senter av aksling til feste på hjulet hvor belastningen vil være er 4cm. Da vil motoren være i
 stand til å løfte:

![alt text](09_images/servomotor_formel.png)
# Servo driver - PCA9685 PWM-modul


![alt text](09_images/servo_driver.jpg)

PCA9685 er en spesialisert I²C-basert PWM-generator. Den genererer stabile, presise PWM-signaler uten å belaste hovedprosessoren.
Dette er spesielt viktig i realtidssystemer der servosignaler må holdes eksakte.

## Funksjon
-	Kobles til Raspberry Pi via I²C .
-	Har intern 25 MHz oscillator.
-	Bruker 12-bit oppløsning - 4096 steg per periode.
-	Kan generere 16 uavhengige PWM-signaler (brukes her til servo-kanal 0).

## PWM-prinsipp
![alt text](09_images/pwm_prinsipp.png)

PWM (Pulse Width Modulation), eller pulssbredde-modulasjon, er en metode for å styre effekten eller posisjonen til elektriske enheter ved å variere hvor lenge et digitalt signal er “på” i forhold til hvor lenge det er “av”.
Selv om signalet i seg selv bare kan ha to tilstander (høy/lav), kan vi oppnå et analogt resultat ved å justere hvor stor del av tiden signalet holdes høyt i hver periode.

## Grunnpinsipp
Et PWM-signal er et firkantsignal med fast frekvens og variabel duty cycle (arbeidssyklus).
Frekvensen angir hvor ofte signalet gjentar seg per sekund, mens duty cycle angir hvor stor andel av tiden signalet er “på”.

![alt text](09_images/formelgrunnprinsipp.png)

T(on) -tiden signalet er høyt (på)

t(off) -tiden signalet er lavt (av)

Et signal med 50% duty cycle betyr at signalet er høyt halvparten av tiden og lavt resten.

# Bruk i kode
I servo_pca9685.py initialiseres modulen slik:
-	i2c = busio.I2C(board.SCL, board.SDA)
-	pwm = PCA9685(i2c)
-	pwm.frequency = 50
-	channel = pwm.channels[0]
og vinkelen styres med:
-	channel.duty_cycle = int(pulse * 4096 / 20000)

PCA9685-modulen oversetter dette til en digital verdi mellom 0 og 4095 (12-bit oppløsning): 
Modulen genererer en PWM-syklus med fast periode, vanligvis 20 000 mikrosekunder (20 ms), som tilsvarer 50 Hz.
Innenfor hver 20 ms-periode bestemmer pulsbreddeverdien hvor lenge signalet er “høyt” (på 3.3 V eller 5 V).

Denne varigheten avgjør servoens vinkel:

1.0 ms	0° (minimum)

1.5 ms	90° (midtposisjon)

2.0 ms	180° (maks)

