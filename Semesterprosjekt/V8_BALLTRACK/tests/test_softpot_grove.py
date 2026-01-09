import time
import os

# Aktiver Grove Base HAT ADC fallback
os.environ["USE_GROVEHAT_ADC"] = "1"

from V8_BALLTRACK.hardware.adc.ads1015 import ADS1015

def main():
    print("=== Softpot test – Grove A0 ===")
    print("Forventet område: 0–4095")
    print("Trykk CTRL+C for å stoppe\n")

    adc = ADS1015(
        bus=1,
        address=0x48,        # ignoreres ved Grove fallback
        default_channel=0,   # A0
        debug=False
    )

    while True:
        raw = adc.read_raw(0)
        print(f"RAW = {raw:4d}")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
