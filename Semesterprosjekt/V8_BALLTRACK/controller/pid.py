# controller/pid.py
# -------------------------------------------------------------
# PID-regulator i tre klassiske varianter:
#   - Parallel (u = Kp*e + Ki*∫e dt + Kd*de/dt)
#   - Ideal   (u = K(e + (1/Ti)*∫e dt + Td*de/dt))
#   - Series  (u = Kp(e + (1/Ti)*∫e dt) + Kp*Td*de/dt)
#
# Koden er skrevet slik at formeluttrykket er direkte gjenkjennbart.
# Ingen filtrering, ingen glatting, ingen automatikk — helt ren PID.
# -------------------------------------------------------------

from dataclasses import dataclass
from enum import Enum


class PIDType(Enum):
    PARALLEL = "parallel"
    IDEAL    = "ideal"
    SERIES   = "series"


@dataclass
class PIDConfig:
    pid_type: PIDType = PIDType.PARALLEL

    # Parallel form
    Kp: float = 1.0
    Ki: float = 0.0
    Kd: float = 0.0

    # Ideal/ISA form
    K:  float = 1.0
    Ti: float = 1.0
    Td: float = 0.0

    # Serieform
    # (Bruker samme Kp, Ti, Td mapping)

    # Output-begrensninger
    umin: float = -1.0
    umax: float = 1.0


class PID:
    def __init__(self, cfg: PIDConfig):
        self.cfg = cfg

        self.integral = 0.0
        self.last_error = 0.0

        # For visning i GUI
        self.last_P = 0.0
        self.last_I = 0.0
        self.last_D = 0.0

    # ----------------------------------------------------------
    def reset(self):
        self.integral = 0.0
        self.last_error = 0.0
        self.last_P = 0.0
        self.last_I = 0.0
        self.last_D = 0.0

    # ----------------------------------------------------------
    def update(self, e: float, dt: float) -> float:
        """
        Utfører ett PID-steg basert på valgt PID-type.
        e = feil = settpunkt - målt verdi
        """

        if self.cfg.pid_type == PIDType.PARALLEL:
            return self._parallel(e, dt)

        elif self.cfg.pid_type == PIDType.IDEAL:
            return self._ideal(e, dt)

        elif self.cfg.pid_type == PIDType.SERIES:
            return self._series(e, dt)

        else:
            raise ValueError("Ukjent PID-type")

    # ==========================================================
    # 1. PARALLEL PID
    # u(t) = Kp*e(t) + Ki*∫e(t) dt + Kd*de/dt
    # ==========================================================
    def _parallel(self, e, dt):
        cfg = self.cfg

        # Integral
        self.integral += e * dt

        # Derivert
        de_dt = (e - self.last_error) / dt if dt > 0 else 0.0

        # Matematisk formel — 1:1
        P = cfg.Kp * e
        I = cfg.Ki * self.integral
        D = cfg.Kd * de_dt

        u = P + I + D

        # logging
        self.last_P, self.last_I, self.last_D = P, I, D
        self.last_error = e

        return self._saturate(u)

    # ==========================================================
    # 2. IDEAL PID / ISA PID
    # u(t) = K(e(t) + (1/Ti)*∫e dt + Td*de/dt)
    # ==========================================================
    def _ideal(self, e, dt):
        cfg = self.cfg

        self.integral += e * dt
        de_dt = (e - self.last_error) / dt if dt > 0 else 0.0

        # Matematisk formel — 1:1
        P = cfg.K * e
        I = cfg.K * (self.integral / cfg.Ti if cfg.Ti != 0 else 0)
        D = cfg.K * (cfg.Td * de_dt)

        u = P + I + D

        self.last_P, self.last_I, self.last_D = P, I, D
        self.last_error = e

        return self._saturate(u)

    # ==========================================================
    # 3. SERIES / INTERACTING PID
    # u(t) = Kp(e + (1/Ti)*∫e dt) + Kp*Td*de/dt
    # ==========================================================
    def _series(self, e, dt):
        cfg = self.cfg

        self.integral += e * dt
        de_dt = (e - self.last_error) / dt if dt > 0 else 0.0

        # Matematisk formel — 1:1
        P = cfg.Kp * e
        I = cfg.Kp * (self.integral / cfg.Ti if cfg.Ti != 0 else 0)
        D = cfg.Kp * (cfg.Td * de_dt)

        u = P + I + D

        self.last_P, self.last_I, self.last_D = P, I, D
        self.last_error = e

        return self._saturate(u)

    # ----------------------------------------------------------
    def _saturate(self, u):
        """Begrenser u uten anti-windup, da dette er ren PID."""
        if u > self.cfg.umax:
            u = self.cfg.umax
        elif u < self.cfg.umin:
            u = self.cfg.umin
        return u
