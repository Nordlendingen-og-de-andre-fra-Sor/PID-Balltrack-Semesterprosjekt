# tools/grovehat_adc_fallback.py

def install_grovehat_fallback():
    """
    Patch'er hardware.adc.ads1015.ADS1015 slik at den faller tilbake til Grove Base HAT ADC
    dersom ADS1015 ikke kan initialiseres.
    """
    try:
        from V8_BALLTRACK.hardware.adc.ads1015 import ADS1015 as _ADS1015_Original
        import V8_BALLTRACK.hardware.adc.ads1015 as ads1015_module
    except Exception as e:
        raise RuntimeError(f"Kunne ikke importere hardware.adc.ads1015.ADS1015: {e!r}")

    class ADS1015(_ADS1015_Original):
        def __init__(self, *args, **kwargs):
            try:
                super().__init__(*args, **kwargs)
                self._backend = "ads1015"
            except Exception as e_ads:
                # Fallback til Grove ADC
                try:
                    from grove.adc import ADC  # Seeed grove.py
                except Exception as e_grove:
                    raise RuntimeError(
                        "ADS1015 init feilet og Grove ADC er ikke tilgjengelig.\n"
                        f"- ADS1015-feil: {e_ads!r}\n"
                        f"- Grove-feil:  {e_grove!r}\n"
                        "Tiltak:\n"
                        "  1) Sjekk i2cdetect -y 1 (ADS1015 ofte 0x48)\n"
                        "  2) Installer grove.py / seeed grove libs hvis du bruker Grove Base HAT\n"
                    )

                self._grove_adc = ADC()
                self._backend = "grove"
                # velg standard kanal hvis din kode forventer det
                self.default_channel = kwargs.get("default_channel", 0)

        def read_raw(self, channel=None):
            if getattr(self, "_backend", None) == "ads1015":
                return super().read_raw(channel)

            if channel is None:
                channel = getattr(self, "default_channel", 0)

            raw = int(self._grove_adc.read_raw(channel))

            # normaliser til 12-bit (0..4095) hvis grove gir 10-bit (0..1023)
            if raw <= 1023:
                raw = int(round(raw * (4095.0 / 1023.0)))

            return max(0, min(4095, raw))

    # Patch inn i modulen som resten av koden importerer fra
    ads1015_module.ADS1015 = ADS1015
