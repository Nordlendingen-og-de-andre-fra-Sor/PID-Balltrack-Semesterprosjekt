# V8_BALLTRACK/dummy_controller.py
# -----------------------------------------------------------
# DummyController (Debug/Feilsøking)
# -----------------------------------------------------------
# Formål:
#  - Gjøre GUI-feilsøking enkel uten hardware
#  - Vise tydelig hvilke knapper/kommandoer som blir brukt
#  - Oppføre seg "som en ekte kontroller" med intern tilstand
#
# Hva du får:
#  - start/stop regulering
#  - setpoint-endringer
#  - PID-apply + P/I/D toggles
#  - manuell servo (ON/OFF + slider)
#  - status-verdier som oppdateres over tid (pos, u, pulse_us, raw)
#  - event-logg (ringbuffer) slik at du kan vise i LogWidget
# -----------------------------------------------------------

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import time


def _clamp(x: float, lo: float, hi: float) -> float:
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


@dataclass
class PIDGains:
    kp: float = 2.0
    ki: float = 0.0
    kd: float = 0.0


class DummyController:
    """
    DummyController er laget for GUI-feilsøking:

    - Når GUI trykker "Start", "Stop", endrer SP, Apply PID, eller bruker manuell servo,
      logges dette med en tydelig tekst.
    - Controlleren simulerer en "posisjon" (0..1) og en servo-puls (us).
    - get_status() returnerer samme type struktur som HW-controlleren typisk gjør.
    """

    def __init__(
        self,
        adc_resolution: int = 4095,
        servo_min_us: int = 1000,
        servo_max_us: int = 2000,
        default_setpoint: float = 0.5,
        u_min: float = -1.0,
        u_max: float = 1.0,
        gui_tag_name: str = "SIM",
        events_max: int = 40,
    ) -> None:
        # "Hardware-lik" konfigurering
        self.adc_resolution = int(adc_resolution)
        self.servo_min_us = int(servo_min_us)
        self.servo_max_us = int(servo_max_us)
        self.u_min = float(u_min)
        self.u_max = float(u_max)

        # Tilstand
        self.setpoint: float = float(default_setpoint)
        self.pos: float = 0.5  # 0..1
        self.raw: int = int(self.pos * self.adc_resolution)
        self.u: float = 0.0
        self.pulse_us: int = int((self.servo_min_us + self.servo_max_us) / 2)

        # "Regulator"-tilstand
        self._enabled: bool = False
        self._manual_mode: bool = False
        self._manual_servo_pos: float = 0.5  # 0..1
        self._disable_i: bool = False
        self._disable_d: bool = False

        self.pid = PIDGains()
        self._i_acc: float = 0.0
        self._prev_e: Optional[float] = None

        # For feilsøking / logging
        self._tag = str(gui_tag_name)
        self._events: List[str] = []
        self._events_max = int(events_max)
        self._last_action: str = "INIT"
        self._t0 = time.monotonic()
        self._last_tick = time.monotonic()

        self._log("INIT: DummyController opprettet")

    # -------------------------
    # Intern logging / events
    # -------------------------
    def _log(self, msg: str) -> None:
        t = time.monotonic() - self._t0
        line = f"{t:8.3f}s | {msg}"
        self._events.append(line)
        if len(self._events) > self._events_max:
            self._events = self._events[-self._events_max :]
        self._last_action = msg

    def get_events(self) -> List[str]:
        return list(self._events)

    def clear_events(self) -> None:
        self._events.clear()
        self._log("EVENTS cleared")

    # -------------------------
    # API: Start/Stop regulering
    # -------------------------
    def start_regulation(self) -> None:
        self._enabled = True
        self._log("START pressed → enabled=True")

    def stop_regulation(self) -> None:
        self._enabled = False
        self.u = 0.0
        self._i_acc = 0.0
        self._prev_e = None
        self._log("STOP pressed → enabled=False (u=0, I reset)")

    # Alias (i tilfelle GUI bruker andre navn)
    def start(self) -> None:
        self.start_regulation()

    def stop(self) -> None:
        self.stop_regulation()

    # -------------------------
    # API: Setpoint
    # -------------------------
    def set_setpoint(self, sp: float) -> None:
        sp = _clamp(float(sp), 0.0, 1.0)
        self.setpoint = sp
        self._log(f"Setpoint changed → {sp:.3f}")

    def get_setpoint(self) -> float:
        return float(self.setpoint)

    # -------------------------
    # API: PID-parametre
    # -------------------------
    def set_pid(self, kp: float, ki: float, kd: float) -> None:
        self.pid.kp = float(kp)
        self.pid.ki = float(ki)
        self.pid.kd = float(kd)
        self._log(f"PID Apply → Kp={self.pid.kp:.3f}, Ki={self.pid.ki:.3f}, Kd={self.pid.kd:.3f}")

    def get_pid(self) -> Dict[str, float]:
        return {"kp": float(self.pid.kp), "ki": float(self.pid.ki), "kd": float(self.pid.kd)}

    def disable_integral(self, flag: bool) -> None:
        self._disable_i = bool(flag)
        if self._disable_i:
            self._i_acc = 0.0
        self._log(f"I {'DISABLED' if self._disable_i else 'ENABLED'}")

    def disable_derivative(self, flag: bool) -> None:
        self._disable_d = bool(flag)
        self._log(f"D {'DISABLED' if self._disable_d else 'ENABLED'}")

    # -------------------------
    # API: Manuell servo
    # -------------------------
    def enable_manual_servo(self, flag: bool) -> None:
        self._manual_mode = bool(flag)
        self._log(f"Manual servo {'ON' if self._manual_mode else 'OFF'}")

    def set_servo_manual(self, pos_norm: float) -> None:
        # Dette skal kunne kalles fra slider i GUI
        p = _clamp(float(pos_norm), 0.0, 1.0)
        self._manual_servo_pos = p
        self._log(f"Manual slider → pos={p:.3f}")
        # Oppdater pulse direkte slik HW normalt ville gjort
        self.pulse_us = int(self.servo_min_us + p * (self.servo_max_us - self.servo_min_us))

    def get_servo_position(self) -> float:
        # Normalisert 0..1 (nyttig for GUI)
        if self.servo_max_us == self.servo_min_us:
            return 0.5
        return (self.pulse_us - self.servo_min_us) / (self.servo_max_us - self.servo_min_us)

    # -------------------------
    # "Kontrollsyklus" (GUI/CLI kan kalle denne periodisk)
    # -------------------------
    def tick(self, dt: Optional[float] = None) -> None:
        force_dt = dt is not None
        now = time.monotonic()
        if dt is None:
            dt = now - self._last_tick
        self._last_tick = now

        # For sikkerhet: unngå rare dt
        dt = float(_clamp(float(dt), 0.0, 0.2))

        # 1) Manual: servo følger slider, pos driver sakte mot "servoeffekt"
        if self._manual_mode:
            # Map servo-pos til en "helling" effekt: -1..+1
            servo_eff = (self._manual_servo_pos - 0.5) * 2.0
            # ball-pos integrerer litt av servo_eff
            self.pos = _clamp(self.pos + servo_eff * 0.35 * dt, 0.0, 1.0)
            self.u = 0.0  # i manual viser vi gjerne u=0
        else:
            # 2) Auto: hvis enabled, kjør en enkel PID-lignende beregning
            if self._enabled:
                e = self.setpoint - self.pos

                # P
                P = self.pid.kp * e

                # I
                if self._disable_i or self.pid.ki == 0.0:
                    I = 0.0
                else:
                    self._i_acc += e * dt
                    I = self.pid.ki * self._i_acc

                # D
                if self._disable_d or self.pid.kd == 0.0:
                    D = 0.0
                else:
                    if self._prev_e is None or dt <= 0.0:
                        D = 0.0
                    else:
                        D = self.pid.kd * ((e - self._prev_e) / dt)

                self._prev_e = e

                u = P + I + D
                self.u = _clamp(u, self.u_min, self.u_max)

                # Map u (-1..1) til servo-puls og pos-endring
                u_norm = (self.u + 1.0) / 2.0  # 0..1
                self.pulse_us = int(self.servo_min_us + u_norm * (self.servo_max_us - self.servo_min_us))

                # Simuler at ballen følger u (dynamikk)
                # (Dette er kun en enkel "plant" for at GUI skal ha liv)
                self.pos = _clamp(self.pos + self.u * 0.30 * dt, 0.0, 1.0)

            else:
                # Ikke enabled: behold pos, sett u=0 og hold servo midt
                self.u = 0.0
                self.pulse_us = int((self.servo_min_us + self.servo_max_us) / 2)

        # Oppdater raw fra pos
        self.raw = int(_clamp(self.pos, 0.0, 1.0) * self.adc_resolution)

        # Hvis tick blir kalt, kan vi logge "heartbeat" sjeldent (valgfritt)
        # Unngå spam; logg bare hvis dt ble tvunget (f.eks. fra GUI)
        if force_dt and int((time.monotonic() - self._t0) * 10) % 50 == 0:
            self._log(f"TICK dt={dt:.3f} (heartbeat)")

    # Alias: i tilfelle noe i koden forventer update()
    def update(self, dt: float) -> None:
        # Behold for kompatibilitet, men GUI bør bruke tick()
        self.tick(dt)

    # -------------------------
    # Status til GUI
    # -------------------------
    def get_status(self) -> Dict[str, Any]:
        # Mode-feltet er ofte synlig i footer; vi legger inn siste handling der.
        run_state = "RUN" if self._enabled else "STOP"
        man_state = "MAN" if self._manual_mode else "AUTO"
        mode = f"{self._tag}:{run_state}:{man_state} | last={self._last_action}"

        # P/I/D komponenter for plotting (bruk de faktiske bidragene der det gir mening)
        # Her gir vi "sist beregnet" komponenter basert på nåværende e.
        e = self.setpoint - self.pos
        P = self.pid.kp * e
        I = 0.0 if self._disable_i else (self.pid.ki * self._i_acc)
        D = 0.0  # vi lagrer ikke siste D separat her, men GUI kan fortsatt plotte u

        return {
            "raw": int(self.raw),
            "pos": float(self.pos),
            "setpoint": float(self.setpoint),
            "u": float(self.u),
            "pulse_us": int(self.pulse_us),
            "P": float(P),
            "I": float(I),
            "D": float(D),
            "mode": mode,
            "events": list(self._events),  # valgfritt: kan vises i logg-widget
        }
