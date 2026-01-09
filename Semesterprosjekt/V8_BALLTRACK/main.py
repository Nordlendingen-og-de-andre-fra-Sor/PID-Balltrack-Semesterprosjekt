# V8_BALLTRACK/main.py
import sys
import time

from V8_BALLTRACK.config import settings

from V8_BALLTRACK.controller.position_controller import PositionControllerV8
from V8_BALLTRACK.controller.dummy_controller import DummyController

from V8_BALLTRACK.hardware.adc.ads1015 import ADS1015
from V8_BALLTRACK.hardware.pwm.pca9685 import PCA9685

from V8_BALLTRACK.gui.gui_tags import GuiTags
from V8_BALLTRACK.gui.app_screen import run_app


# ----------------------------------------------------------
# HARDWARE DETECTION
# ----------------------------------------------------------
def create_controller():
    print("\n=== Balltrack V8 – Hardware Detection ===")

    try:
        # Test ADC
        adc = ADS1015(
            bus=settings.ADC_I2C_BUS,
            address=settings.ADC_I2C_ADDR,
            default_channel=settings.ADC_CHANNEL,
        )
        _ = adc.read_raw(settings.ADC_CHANNEL)

        # Test PWM
        pwm = PCA9685(
            address=settings.PCA9685_I2C_ADDR,
            bus=settings.PCA9685_I2C_BUS,
            freq_hz=settings.PCA9685_FREQ_HZ,
        )

        ctrl = PositionControllerV8(adc, pwm)
        ctrl.mode = "HW"
        print("✓ Hardware OK – bruker PID-regulering.\n")
        return ctrl

    except Exception as e:
        print("⚠️ Hardware IKKE funnet – bytter til DummyController")
        print("Feilmelding:", e)
        ctrl = DummyController()
        ctrl.mode = "DUMMY"
        return ctrl


# ----------------------------------------------------------
# CLI RUN
# ----------------------------------------------------------
def run_cli():
    ctrl = create_controller()
    ctrl.set_setpoint(settings.DEFAULT_SETPOINT)
    ctrl.start()

    dt = settings.PID_TS
    print("Trykk CTRL+C for å stoppe.")
    try:
        while True:
            ctrl.update(dt)
            s = ctrl.get_status()
            print(f"[{s.get('mode','?')}] pos={s.get('pos',0):.3f}, u={s.get('u',0):.3f}")
            time.sleep(dt)
    except KeyboardInterrupt:
        ctrl.stop()
        print("\nStoppet.")


# ----------------------------------------------------------
# GUI RUN
# ----------------------------------------------------------
def run_gui():
    ctrl = create_controller()
    tags = GuiTags(ctrl)     # <-- nøkkelen: HMI binder mot tags
    run_app(tags)            # <-- app_screen starter Tkinter


def main():
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()


if __name__ == "__main__":
    main()
