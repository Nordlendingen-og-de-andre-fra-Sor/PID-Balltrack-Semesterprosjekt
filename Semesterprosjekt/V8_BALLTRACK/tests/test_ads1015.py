from hardware.adc.ads1015 import ADS1015
import time

adc = ADS1015(debug=True)

print("Starter ADS1015 AIN0 test. CTRL+C for å stoppe.\n")

try:
    while True:
        raw = adc.read_raw()
        percent = adc.read_percent()
        print(f"RAW={raw:4d}   POS={percent:6.2f}%")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nAvslutter test.")
