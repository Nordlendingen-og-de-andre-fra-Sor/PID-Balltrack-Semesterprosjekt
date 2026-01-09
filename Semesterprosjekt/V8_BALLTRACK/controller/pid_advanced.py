# controller/pid_advanced.py
# Denne pakken er startet på menn ikke fullført. og ikke implementert i GUI ennå.
# Den er ment å tilby avanserte PID-funksjoner som anti-windup,
"""
Avanserte PID-funksjoner for Balltrack V8.

Dette er IKKE en del av klassisk PID.
Alt her kan aktiveres/deaktiveres fra GUI.
"""

from dataclasses import dataclass


@dataclass
class AdvancedConfig:
    anti_windup: bool = False
    derivative_filter: bool = False
    setpoint_weighting: bool = False
    feed_forward: bool = False

    # anti-windup parameter
    Tt: float = 0.1

    # derivative filtering
    N: float = 10.0   # filter ratio

    # setpoint weights
    beta: float = 1.0
    gamma: float = 1.0

    # feed-forward gain
    Kff: float = 0.0


class AdvancedPID:
    """
    Wrapper rundt klassisk PID med valgbar «industrilogikk».
    """
    def __init__(self, pid, cfg: AdvancedConfig):
        self.pid = pid
        self.cfg = cfg
        self.last_Df = 0.0   # filtered derivative

    def update(self, e, r, y, dt):
        """
        e = error = r - y
        r = setpoint
        y = measurement
        """

        # -------- Setpoint weighting --------
        if self.cfg.setpoint_weighting:
            eP = self.cfg.beta * r - y
            eD = self.cfg.gamma * r - y
        else:
            eP = e
            eD = e

        # -------- Kjør klassisk PID (parallel/ideal/series) --------
        u_pid = self.pid.update(eP, dt)

        # -------- Anti-windup --------
        if self.cfg.anti_windup:
            if u_pid > self.pid.cfg.umax:
                self.pid.integral -= (u_pid - self.pid.cfg.umax) * self.cfg.Tt
            elif u_pid < self.pid.cfg.umin:
                self.pid.integral -= (u_pid - self.pid.cfg.umin) * self.cfg.Tt

        # -------- Derivative filtering --------
        if self.cfg.derivative_filter:
            Td = self.pid.cfg.Td
            N = self.cfg.N
            alpha = Td / (Td + N * dt)

            D_raw = self.pid.last_D
            self.last_Df = alpha * self.last_Df + (1 - alpha) * D_raw

            u_pid = self.pid.last_P + self.pid.last_I + self.last_Df

        # -------- Feed-forward --------
        if self.cfg.feed_forward:
            u_pid += self.cfg.Kff * r

        return u_pid
