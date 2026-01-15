# V8_BALLTRACK/hardware/adc/ads1115.py
from smbus2 import SMBus
import time

class ADS1115:
    REG_CONVERSION = 0x00
    REG_CONFIG = 0x01

    # MODE=1 (single-shot), PGA=±4.096V, DR=128SPS, comparator disabled
    # OS-biten settes ved hver måling for å starte konvertering
    BASE_CONFIG = (
        (1 << 8)  |      # MODE (single-shot)
        (0b001 << 9) |   # PGA ±4.096V
        (0b100 << 5) |   # DR 128 SPS
        0b11             # COMP_QUE disable
    )

    # MUX for single-ended AINx vs GND
    MUX_SINGLE = {0: 0b100, 1: 0b101, 2: 0b110, 3: 0b111}

    def __init__(self, bus=1, address=0x48, default_channel=0, debug=False):
        self.bus_num = bus
        self.address = address
        self.default_channel = default_channel
        self.debug = debug
        self.bus = SMBus(bus)

    def read_raw(self, channel=None) -> int:
        """
        Returnerer signed 16-bit råverdi fra ADS1115.
        For single-ended forventes normalt 0..32767.
        """
        if channel is None:
            channel = self.default_channel
        if channel not in self.MUX_SINGLE:
            raise ValueError(f"Ugyldig ADC channel {channel}. Gyldig: 0..3")

        mux = self.MUX_SINGLE[channel]

        # Sett OS=1 for å starte konvertering (bit 15)
        config = (1 << 15) | (self.BASE_CONFIG & ~(0b111 << 12)) | (mux << 12)

        # skriv config (big-endian)
        self.bus.write_i2c_block_data(
            self.address,
            self.REG_CONFIG,
            [(config >> 8) & 0xFF, config & 0xFF]
        )

        # 128 SPS -> ~7.8ms per konvertering. 10ms er trygt.
        time.sleep(0.01)

        hi, lo = self.bus.read_i2c_block_data(self.address, self.REG_CONVERSION, 2)
        raw = (hi << 8) | lo

        # signed 16-bit
        if raw & 0x8000:
            raw -= 65536

        if self.debug:
            print(f"[ADS1115] addr=0x{self.address:02X} ch={channel} raw={raw}")

        return raw

    def close(self):
        try:
            self.bus.close()
        except Exception:
            pass

    def __del__(self):
        self.close()
