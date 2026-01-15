import time
from V8_BALLTRACK.config import settings
from V8_BALLTRACK.hardware.pwm.pca9685 import PCA9685

p = PCA9685(address=settings.PCA9685_I2C_ADDR, bus=settings.PCA9685_I2C_BUS, freq_hz=settings.PCA9685_FREQ_HZ)
ch = settings.SERVO_CHANNEL

for us in (1000, 1500, 2000, 1500):
    print("pulse_us =", us)
    p.set_servo_us(ch, us)
    time.sleep(1)

p.servo_off(ch)
print("done")