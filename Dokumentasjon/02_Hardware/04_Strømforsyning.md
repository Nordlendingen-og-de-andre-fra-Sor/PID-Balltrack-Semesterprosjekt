# PSU - Strømforsyning

Strømforsyningen som benyttes i BallTrack-systemet er en ATX-strømforsyning av typen Tagan TG330-U01. Dette er en standard datamaskinstrømforsyning som leverer flere spenningsnivåer, blant annet +3,3 V, +5 V og ±12 V.

+5 V benyttes til drift av servomotoren, mens Raspberry Pi forsynes via 5 V-inngangen. Logikknivåer på 3,3 V benyttes for I²C-kommunikasjon mellom Raspberry Pi og PWM-modulen.

Ved å forsyne servomotoren separat fra måle- og styreelektronikken reduseres risikoen for spenningsstøy og forstyrrelser i sensorsignalene. Dette gir mer stabile målinger og bedre reguleringsytelse.