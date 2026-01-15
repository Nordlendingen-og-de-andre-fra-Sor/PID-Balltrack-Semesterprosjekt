# gui_tags.py
class GuiTags:
    """
    PLC/TIA-tankegang:
    - Dette er HMI-tags/UDT-laget.
    - Eksponerer et stabilt 'tag-API' som widgets binder mot.
    - Videresender til ekte controller, men tåler manglende metoder.
    """

    def __init__(self, controller):
        self._c = controller

    # -------------------------
    # Control tags
    # -------------------------
    def start(self):
        if hasattr(self._c, "start"):
            return self._c.start()

    def stop(self):
        if hasattr(self._c, "stop"):
            return self._c.stop()

    # -------------------------
    # Setpoint tags
    # -------------------------
    def get_setpoint(self):
        if hasattr(self._c, "get_setpoint"):
            return self._c.get_setpoint()
        return 0.0

    def set_setpoint(self, sp):
        if hasattr(self._c, "set_setpoint"):
            return self._c.set_setpoint(sp)

    # -------------------------
    # PID tags
    # -------------------------
    def get_pid(self):
        if hasattr(self._c, "get_pid"):
            return self._c.get_pid()
        # fallback
        return (0.0, 0.0, 0.0)

    def set_pid(self, kp, ki, kd):
        if hasattr(self._c, "set_pid"):
            return self._c.set_pid(kp, ki, kd)

    def disable_integral(self, flag: bool):
        if hasattr(self._c, "disable_integral"):
            return self._c.disable_integral(flag)

    def disable_derivative(self, flag: bool):
        if hasattr(self._c, "disable_derivative"):
            return self._c.disable_derivative(flag)

    # -------------------------
    # Servo/manual tags
    # -------------------------
    def enable_manual_servo(self, flag: bool):
        print("[GuiTags] enable_manual_servo:", flag)
        if hasattr(self._c, "enable_manual_servo"):
            self._c.enable_manual_servo(flag)
        else:
            print("[GuiTags] underliggende controller mangler enable_manual_servo")

    def set_servo_manual(self, pos_norm: float):
        print("[GuiTags] set_servo_manual:", pos_norm)
        if hasattr(self._c, "set_servo_manual"):
            self._c.set_servo_manual(pos_norm)
        else:
            print("[GuiTags] underliggende controller mangler set_servo_manual")

    def get_servo_position(self):
        if hasattr(self._c, "get_servo_position"):
            return self._c.get_servo_position()
        return 0.5


    # -------------------------
    # Status (for skjerm/plot)
    # -------------------------
    def get_status(self):
        if hasattr(self._c, "get_status"):
            return self._c.get_status()
        return {}
