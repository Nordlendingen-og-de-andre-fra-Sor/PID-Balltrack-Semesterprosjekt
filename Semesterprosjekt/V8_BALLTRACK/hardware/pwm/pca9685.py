# -------------------------------------------------------------------
# hardware/pwm/pca9685.py
#
# PCA9685-driver for Balltrack V8 – fokus på forståelse og enkel bruk.
#
# Hvis du kommer fra Arduino-verden:
#   - Arduino har egen servo-funksjonalitet innebygd.
#   - Raspberry Pi har ingen slik funksjon, så vi bruker PCA9685
#     som en ekstern PWM-generator.
#
# PCA9685 lager stabile servo-signaler uten at Raspberry Pi trenger
# å generere PWM selv. Det gir et mer robust system under regulering.
# -------------------------------------------------------------------

from smbus2 import SMBus
import time


class PCA9685:
    """
    Driverklasse for PCA9685, en 16-kanalers PWM-kontroller.
    Brikken brukes her til å styre én servo på Balltrack.

    PWM-signalet defineres som:
        - Frekvens (50 Hz for servo)
        - Pulsbredde (1000–2000 µs typisk)
    På Arduino gjør servo-biblioteket dette for oss.
    Her gjør vi det manuelt slik at vi har full kontroll.
    """

    # Vanlige registeradresser (fra databladet)
    MODE1       = 0x00
    MODE2       = 0x01
    PRESCALE    = 0xFE

    LED0_ON_L   = 0x06
    LED0_ON_H   = 0x07
    LED0_OFF_L  = 0x08
    LED0_OFF_H  = 0x09

    # MODE1 flagg
    RESTART = 0x80
    SLEEP   = 0x10
    ALLCALL = 0x01

    # MODE2 flagg
    OUTDRV = 0x04

    # ----------------------------------------------------------------------
    def __init__(self, address=0x40, bus=1, freq_hz=50):
        """
        Initialiserer PCA9685.

        address: I2C-adressen til modulen
        bus:     Raspberry Pi sin I2C-bus (1 på Pi 4/5)
        freq_hz: PWM-frekvens. Servor bruker alltid ~50 Hz.

        Tilsvarer Arduino:
            servo.attach(pin);
        """

        self.address = address
        self.bus = SMBus(bus)

        # Aktiver I2C-kommunikasjon
        self._write(self.MODE1, self.ALLCALL)
        time.sleep(0.005)

        # Vekk brikken fra SLEEP-modus
        mode1 = self._read(self.MODE1) & ~self.SLEEP
        self._write(self.MODE1, mode1)
        time.sleep(0.005)

        # Sett PWM-frekvens
        self.set_pwm_freq(freq_hz)

    # ----------------------------------------------------------------------
    # Lavnivå I2C-funksjoner
    # (Samme rolle som Wire.write()/Wire.read() på Arduino)
    def _write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def _read(self, reg):
        return self.bus.read_byte_data(self.address, reg)

    # ----------------------------------------------------------------------
    def set_pwm_freq(self, freq_hz):
        """
        Setter PWM-frekvensen til brikken.

        Servo = 50 Hz → periode = 20 ms.
        Pulsbredde innenfor denne perioden avgjør servoens posisjon.

        Formelen kommer fra PCA9685-databladet, og brukes for å oversette
        ønsket frekvens til brikkens interne prescaler-verdi.
        """

        prescale_val = int(round(25000000.0 / (4096 * freq_hz) - 1))

        # Brikken må settes i "sleep" for å endre prescale
        old_mode = self._read(self.MODE1)
        new_mode = (old_mode & 0x7F) | self.SLEEP
        self._write(self.MODE1, new_mode)

        # Skriv prescaler
        self._write(self.PRESCALE, prescale_val)

        # Start igjen
        self._write(self.MODE1, old_mode)
        time.sleep(0.005)
        self._write(self.MODE1, old_mode | self.RESTART)

        # Verdier som brukes videre når vi setter puls i mikrosekunder
        self.freq_hz = freq_hz
        self.period_us = 1_000_000.0 / freq_hz       # f.eks 20000 µs
        self.ticks_per_us = 4096.0 / self.period_us  # ticks per mikrosekund

    # ----------------------------------------------------------------------
    def set_pulse_us(self, channel, pulse_us):
        """
        Setter en puls i mikrosekunder på en gitt kanal.

        Arduino:
            servo.writeMicroseconds(1500);
        Her:
            pca.set_pulse_us(0, 1500)

        PCA9685 bruker 0–4095 ticks per periode, så vi må oversette
        pulsbredden fra µs → ticks.
        """

        if pulse_us < 0:
            pulse_us = 0  # sikkerhetsmargin

        ticks = int(pulse_us * self.ticks_per_us)
        ticks &= 0x0FFF  # begrens til 12-bit

        # Hver kanal har 4 registre som må fylles
        reg_base = self.LED0_ON_L + 4 * channel

        # Puls starter på 0
        self._write(reg_base + 0, 0)
        self._write(reg_base + 1, 0)

        # Puls slutter på "ticks"
        self._write(reg_base + 2, ticks & 0xFF)
        self._write(reg_base + 3, ticks >> 8)

    # ----------------------------------------------------------------------
    def set_servo_us(self, channel, pulse_us):

        self.set_pulse_us(channel, pulse_us)

    # ----------------------------------------------------------------------
    def servo_off(self, channel):
        """
        Slår PWM helt av på denne kanalen.
        Tilsvarer servo.detach() på Arduino.
        """
        reg_base = self.LED0_ON_L + 4 * channel
        self._write(reg_base + 0, 0)
        self._write(reg_base + 1, 0)
        self._write(reg_base + 2, 0)
        self._write(reg_base + 3, 0)
