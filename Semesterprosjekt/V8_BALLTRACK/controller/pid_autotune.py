# controller/pid_autotune.py
# ------------------------------------------------------------
# Autotune-modul for Balltrack V8
# - Samler data (y(t), u(t), e(t)) i sanntid
# - Utfører step-response eller relay tuning
# - Beregner PID-parametre (ZN, CC, Åström–Hägglund)
# ------------------------------------------------------------

# Denne modulen er ikke tatt i bruk i GUI ennå. Den er under utvikling.
# Modulen er ment å kunne brukes til å auto-tune PID-parametre for systemet.

import time
from dataclasses import dataclass, field


@dataclass
class AutotuneConfig:
    method: str = "zn_relay"          # zn_relay, zn_step, cohen_coon
    amplitude: float = 0.1            # for relay feedback
    sample_time: float = 0.02
    max_duration: float = 10.0        # seconds
    stop_on_divergence: bool = True


@dataclass
class AutotuneResult:
    success: bool
    reason: str
    Kp: float = None
    Ki: float = None
    Kd: float = None
    Ku: float = None
    Pu: float = None
    data: list = field(default_factory=list)


class PIDAutotune:
    def __init__(self, controller, cfg: AutotuneConfig):
        self.ctrl = controller
        self.cfg = cfg
        self.data = []

    # --------------------------------------------------------
    def run(self):
        """Kjører autotune-sesjon."""
        start_time = time.time()
        self.data.clear()

        # Relay-based oscillation (Åström–Hägglund)
        if self.cfg.method == "zn_relay":
            return self._relay_oscillation(start_time)

        # Step response metoder
        elif self.cfg.method == "zn_step":
            return self._step_response(start_time)

        elif self.cfg.method == "cohen_coon":
            return self._cohen_coon(start_time)

        else:
            return AutotuneResult(False, "Ukjent metode")

    # --------------------------------------------------------
    def _relay_oscillation(self, t0):
        """
        Åström–Hägglund relay test:
        - Påfører +- amplitude
        - Måler stabil oscillasjon
        - Beregner Ku og Pu
        """
        print("[Autotune] Starter relay-test...")

        A = self.cfg.amplitude
        last_switch = 0
        u = A
        self.ctrl.set_servo_manual(0.5)  # midtstart
        self.ctrl.enable_manual_servo(True)

        peaks = []
        last_pos = None
        last_sign = None

        while time.time() - t0 < self.cfg.max_duration:
            pos = self.ctrl.read_position()
            now = time.time()

            # Relay switching (u går mellom +A og -A)
            if pos > self.ctrl.setpoint:
                u = -A
            else:
                u = A

            self.ctrl.set_servo_manual(0.5 + u)

            # Peak detection
            sign = pos > self.ctrl.setpoint
            if last_sign is not None and sign != last_sign:
                peaks.append((now, pos))
            last_sign = sign

            self.data.append((now - t0, pos, u))

            if len(peaks) >= 6:
                break

            time.sleep(self.cfg.sample_time)

        self.ctrl.enable_manual_servo(False)

        if len(peaks) < 2:
            return AutotuneResult(False, "Ingen oscillasjoner funnet")

        # Beregn periode Pu
        times = [p[0] for p in peaks]
        Pu = (times[-1] - times[0]) / (len(times) - 1)

        # Relay amplitude → ultimate gain Ku
        Ku = (4 * A) / (3.14159 * (max(p[1] for p in peaks) - min(p[1] for p in peaks)))

        # Ziegler–Nichols PID
        Kp = 0.6 * Ku
        Ki = 2 * Kp / Pu
        Kd = Kp * Pu / 8

        return AutotuneResult(
            True, "OK", Kp, Ki, Kd, Ku=Ku, Pu=Pu, data=self.data
        )
