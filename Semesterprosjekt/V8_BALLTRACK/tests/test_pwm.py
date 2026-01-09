# test_pwm.py – V8 trygg versjon
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from hardware.pwm.pca9685 import PCA9685
from config import settings
import time

def main():
    print("Starter PWM/Servo-test...")
    print("Trykk CTRL+C for å stoppe.\n")

    try:
        pwm = PCA9685(
            address=settings.PCA9685_I2C_ADDR,
            bus=settings.PCA9685_I2C_BUS,
            freq_hz=settings.PCA9685_FREQ_HZ,
        )
    except Exception as e:
        print("❌ Klarte ikke å initialisere PCA9685:", e)
        return

    ch = settings.SERVO_CHANNEL

    try:
        for pulse in (1000, 1500, 2000, 1500):
            print(f"Setter servo[{ch}] = {pulse} us")
            pwm.set_servo_us(ch, pulse)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStoppet av bruker.")

    finally:
        print("Slår av servo...")
        try:
            pwm.servo_off(ch)
        except:
            pwm.set_servo_us(ch, 0)
        print("Servo av. Test ferdig.")

if __name__ == "__main__":
    main()
