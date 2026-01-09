# controller/dummy_controller.py
# ------------------------------------------------------------
# DummyController V8
# Brukes når hardware ikke finnes.
#
# Gir GUI realistiske data uten å gjøre ekte regulering.
# ------------------------------------------------------------

import math
import time


class DummyController:
    def __init__(self):
        # Interne variabler
        self.setpoint = 0.5
        self.pos = 0.5
        self.u = 0.0
        self.last_pulse_us = 1500
        self.manual_mode = False
        self._enabled = False

        # Oscillasjon for "visuell realisme"
        self._t0 = time.time()

    # ---------------------------------------------------------
    # API: start/stop
    # ---------------------------------------------------------
    def start(self):
        self._enabled = True

    def stop(self):
        self._enabled = False

    # ---------------------------------------------------------
    # API: Setpoint
    # ---------------------------------------------------------
    def set_setpoint(self, sp_norm: float):
        self.setpoint = max(0.0, min(1.0, sp_norm))
        # gjør dummy-visning mer responsiv
        self.pos = self.setpoint

    # ---------------------------------------------------------
    # API: Manuell servo
    # ---------------------------------------------------------
    def enable_manual_servo(self, flag: bool):
        self.manual_mode = flag

    def set_servo_manual(self, pos_norm: float):
        """I dummy-modus gjør vi ingenting med hardware — men GUI ser pos."""
        self.pos = max(0.0, min(1.0, pos_norm))
        self.last_pulse_us = 1000 + int(self.pos * 1000)

    # ---------------------------------------------------------
    # Dummy update-loop
    # ---------------------------------------------------------
    def update(self, dt: float):
        """
        Simulerer en sakte oscillerende posisjon, så GUI-plottet ser levende ut.
        """
        t = time.time() - self._t0

        if not self.manual_mode:
            # dummy oscillasjon rundt settpunkt
            self.pos = self.setpoint + 0.02 * math.sin(2 * math.pi * 0.2 * t)
            self.pos = max(0.0, min(1.0, self.pos))

            # dummy "reguleringssignal"
            self.u = math.sin(2 * math.pi * 0.2 * t)

            # dummy servo puls
            self.last_pulse_us = 1500 + int(self.u * 200)
        else:
            # i manuell modus endrer GUI pos direkte via set_servo_manual()
            pass

    # ---------------------------------------------------------
    # API: status til GUI
    # ---------------------------------------------------------
    def get_status(self) -> dict:
        raw = int(self.pos * 4095)

        return {
            "raw": raw,
            "pos": self.pos,
            "setpoint": self.setpoint,
            "u": self.u,
            "pulse_us": self.last_pulse_us,
            "P": self.u * 0.6,   # dummy komponenter for GUI
            "I": self.u * 0.3,
            "D": self.u * 0.1,
        }
