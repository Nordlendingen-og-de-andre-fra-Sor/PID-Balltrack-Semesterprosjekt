# V8_BALLTRACK/hardware/adc/ads1015.py
from smbus2 import SMBus
import time

class ADS1015:
    REG_CONVERSION = 0x00
    REG_CONFIG = 0x01

    # OS=1 (start), MODE=1 (single-shot), PGA=±4.096V, DR=1600SPS, comparator disabled
    BASE_CONFIG = (
        (1 << 15) |      # OS
        (1 << 8)  |      # MODE (single-shot)
        (0b001 << 9) |   # PGA ±4.096V
        (0b100 << 5) |   # DR 1600 SPS
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
        """Returnerer 12-bit raw (0..4095) fra valgt channel (0..3)."""
        if channel is None:
            channel = self.default_channel
        if channel not in self.MUX_SINGLE:
            raise ValueError(f"Ugyldig ADC channel {channel}. Gyldig: 0..3")

        mux = self.MUX_SINGLE[channel]
        config = (self.BASE_CONFIG & ~(0b111 << 12)) | (mux << 12)

        # skriv config (big-endian)
        self.bus.write_i2c_block_data(
            self.address,
            self.REG_CONFIG,
            [(config >> 8) & 0xFF, config & 0xFF]
        )

        time.sleep(0.002)  # ~2ms holder for 1600SPS

        hi, lo = self.bus.read_i2c_block_data(self.address, self.REG_CONVERSION, 2)

        # ADS1015 gir 12-bit venstrejustert i 16-bit ord
        raw = (hi << 4) | (lo >> 4)

        if self.debug:
            print(f"[ADS1015] addr=0x{self.address:02X} ch={channel} raw={raw}")

        return raw

    def close(self):
        try:
            self.bus.close()
        except Exception:
            pass

    def __del__(self):
        self.close()
