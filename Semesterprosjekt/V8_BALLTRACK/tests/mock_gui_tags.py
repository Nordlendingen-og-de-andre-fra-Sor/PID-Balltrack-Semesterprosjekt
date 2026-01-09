# V8_BALLTRACK/tests/mock_gui_tags.py
import time
import math

class MockGuiTags:
    """
    Minimal mock av GuiTags-kontrakten.
    Widgets binder mot denne via .bind(tags)
    """

    def __init__(self):
        self._running = False
        self._sp = 0.50
        self._kp, self._ki, self._kd = 1.0, 0.0, 0.0
        self._disable_i = False
        self._disable_d = False
        self._manual = False
        self._manual_u = 0.0

        self._t0 = time.time()
        self._pos = 0.5
        self._u = 0.0

    # ---- Control ----
    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    # ---- Setpoint ----
    def get_setpoint(self):
        return self._sp

    def set_setpoint(self, sp):
        self._sp = float(sp)

    # ---- PID ----
    def get_pid(self):
        return (self._kp, self._ki, self._kd)

    def set_pid(self, kp, ki, kd):
        self._kp, self._ki, self._kd = float(kp), float(ki), float(kd)

    def disable_integral(self, flag: bool):
        self._disable_i = bool(flag)

    def disable_derivative(self, flag: bool):
        self._disable_d = bool(flag)

    # ---- Servo/manual ----
    def enable_manual_servo(self, flag: bool):
        self._manual = bool(flag)

    def set_servo_manual(self, value):
        self._manual_u = float(value)

    def get_servo_position(self):
        # Bruk pos som "ballposisjon" (for visual-widget)
        return self._pos

    # ---- Status ----
    def get_status(self):
        # enkel "dynamikk": pos varierer litt over tid når running=True
        t = time.time() - self._t0
        if self._running:
            base = 0.5 + 0.35 * math.sin(t * 0.6)
            self._pos = max(0.0, min(1.0, base))
            self._u = (self._sp - self._pos) * self._kp
        else:
            self._u = 0.0

        return {
            "mode": "MOCK",
            "pos": self._pos,
            "u": self._u,
            "sp": self._sp,
            "kp": self._kp,
            "ki": self._ki,
            "kd": self._kd,
            "running": self._running,
            "manual": self._manual,
        }
