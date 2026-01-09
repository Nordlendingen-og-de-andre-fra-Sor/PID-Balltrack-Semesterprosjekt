# controller/position_controller.py

from V8_BALLTRACK.config import settings
from V8_BALLTRACK.controller.pid import PID, PIDConfig, PIDType



class PositionControllerV8:
    def __init__(self, adc, pwm):
        self.adc = adc
        self.pwm = pwm

        # PID-konfig
        cfg = PIDConfig(
            pid_type=PIDType.PARALLEL,
            Kp=settings.PID_KP,
            Ki=settings.PID_KI,
            Kd=settings.PID_KD,
            umin=settings.PID_MIN,
            umax=settings.PID_MAX,
        )
        self.pid = PID(cfg)

        self.setpoint = settings.DEFAULT_SETPOINT

        self.last_raw = 0
        self.last_pos = 0.0
        self.last_u = 0.0
        self.last_pulse_us = 1500
        self.last_servo_saturated = False

        self._enabled = False
        self._manual_mode = False

        # GUI leser denne: "HW" eller "DUMMY"
        self.mode = "HW"

    # ---------------------------------------------------------
    # Les posisjon fra ADC
    # ---------------------------------------------------------
    def read_position(self) -> float:
        raw = self.adc.read_raw(settings.ADC_CHANNEL)
        self.last_raw = raw

        pos = raw / settings.ADC_RESOLUTION
        pos = max(0.0, min(1.0, pos))
        self.last_pos = pos
        return pos

    # ---------------------------------------------------------
    # HOVED UPDATE LOOP
    # ---------------------------------------------------------
    def update(self, dt: float):
        if not self._enabled:
            return
        if self._manual_mode:
            return

        pos = self.read_position()
        e = self.setpoint - pos

        u = self.pid.update(e, dt)
        self.last_u = u

        # u → puls
        mid = (settings.SERVO_MIN_US + settings.SERVO_MAX_US) / 2.0
        span = (settings.SERVO_MAX_US - settings.SERVO_MIN_US) / 2.0
        pulse = mid + (u * span)

        pulse = max(settings.SERVO_MIN_US, min(settings.SERVO_MAX_US, pulse))
        
        # registrer metning (for logging / plotting)
        self.last_servo_saturated = (
            pulse == settings.SERVO_MIN_US
            or pulse == settings.SERVO_MAX_US
        )

        pulse = int(round(pulse))

        self.last_pulse_us = pulse
        self.pwm.set_servo_us(settings.SERVO_CHANNEL, pulse)

    # ---------------------------------------------------------
    # API: start/stop
    # ---------------------------------------------------------
    def start(self):
        self._enabled = True

    def stop(self):
        self._enabled = False
        self.servo_off()

    # ---------------------------------------------------------
    # Servo av
    # ---------------------------------------------------------
    def servo_off(self):
        self.pwm.servo_off(settings.SERVO_CHANNEL)

    # ---------------------------------------------------------
    # SETPOINT
    # ---------------------------------------------------------
    def set_setpoint(self, sp):
        self.setpoint = max(0.0, min(1.0, sp))

    def get_setpoint(self):
        return self.setpoint

    # ---------------------------------------------------------
    # MANUELL SERVO
    # ---------------------------------------------------------
    def enable_manual_servo(self, flag):
        self._manual_mode = flag
        if flag:
            self._enabled = False

    def set_servo_manual(self, pos_norm):
        if not self._manual_mode:
            return

        # robust clamp av input
        pos_norm = max(0.0, min(1.0, float(pos_norm)))

        # map 0..1 → SERVO_MIN..SERVO_MAX
        pulse = settings.SERVO_MIN_US + pos_norm * (settings.SERVO_MAX_US - settings.SERVO_MIN_US)

        # clamp + metning (for logging/plot)
        pulse = max(settings.SERVO_MIN_US, min(settings.SERVO_MAX_US, pulse))
        self.last_servo_saturated = (
            pulse == settings.SERVO_MIN_US
            or pulse == settings.SERVO_MAX_US
        )

        # servo forventer heltall µs
        pulse = int(round(pulse))

        self.last_pulse_us = pulse
        self.pwm.set_servo_us(settings.SERVO_CHANNEL, pulse)


    # ---------------------------------------------------------
    # PID API (GUI forventer disse)
    # ---------------------------------------------------------
    def get_pid(self):
        cfg = self.pid.cfg
        return cfg.Kp, cfg.Ki, cfg.Kd

    def set_pid(self, kp, ki, kd):
        cfg = self.pid.cfg
        cfg.Kp = kp
        cfg.Ki = ki
        cfg.Kd = kd
        self.pid.reset()

    def disable_integral(self, flag: bool):
        self.pid.cfg.Ki = 0.0 if flag else settings.PID_KI
        self.pid.reset()

    def disable_derivative(self, flag: bool):
        self.pid.cfg.Kd = 0.0 if flag else settings.PID_KD
        self.pid.reset()

    # ---------------------------------------------------------
    # Status for GUI
    # ---------------------------------------------------------
    def get_status(self):
        return {
            "raw": self.last_raw,
            "pos": self.last_pos,
            "setpoint": self.setpoint,
            "u": self.last_u,
            "pulse_us": self.last_pulse_us,
            "P": self.pid.last_P,
            "I": self.pid.last_I,
            "D": self.pid.last_D,
            "mode": self.mode,
        }

    def get_servo_position(self) -> float:
        # map last_pulse_us -> 0..1
        span = (settings.SERVO_MAX_US - settings.SERVO_MIN_US)
        if span <= 0:
            return 0.5
        pos = (self.last_pulse_us - settings.SERVO_MIN_US) / span
        return max(0.0, min(1.0, pos))
