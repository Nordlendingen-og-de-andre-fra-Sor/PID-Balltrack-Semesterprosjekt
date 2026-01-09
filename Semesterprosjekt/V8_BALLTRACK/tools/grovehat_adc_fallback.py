# tools/grovehat_adc_fallback.py

def install_grovehat_fallback():
    """
    Patch'er V8_BALLTRACK.hardware.adc.ads1015.ADS1015 slik at den faller tilbake til
    Grove Base HAT ADC dersom ADS1015 ikke kan initialiseres.
    """
    try:
        from V8_BALLTRACK.hardware.adc.ads1015 import ADS1015 as _ADS1015_Original
        import V8_BALLTRACK.hardware.adc.ads1015 as ads1015_module
    except Exception as e:
        raise RuntimeError(f"Kunne ikke importere V8_BALLTRACK.hardware.adc.ads1015.ADS1015: {e!r}")

    class ADS1015(_ADS1015_Original):
        def __init__(self, *args, **kwargs):
            try:
                super().__init__(*args, **kwargs)
                self._backend = "ads1015"
            except Exception as e_ads:
                try:
                    from grove.adc import ADC
                except Exception as e_grove:
                    raise RuntimeError(
                        "ADS1015 init feilet og Grove ADC er ikke tilgjengelig.\n"
                        f"- ADS1015-feil: {e_ads!r}\n"
                        f"- Grove-feil:  {e_grove!r}\n"
                    )

                self._grove_adc = ADC()
                self._backend = "grove"
                self.default_channel = kwargs.get("default_channel", 0)

        def read_raw(self, channel=None):
            if getattr(self, "_backend", None) == "ads1015":
                return super().read_raw(channel)

            if channel is None:
                channel = getattr(self, "default_channel", 0)

            raw = int(self._grove_adc.read_raw(channel))

            # Skaler 10-bit (0..1023) -> 12-bit (0..4095)
            if raw <= 1023:
                raw = int(round(raw * (4095.0 / 1023.0)))

            return max(0, min(4095, raw))

    # ✅ Patch må skje HER (inne i funksjonen), ellers er ADS1015/ads1015_module ute av scope
    ads1015_module.ADS1015 = ADS1015

    # Valgfritt, men nyttig for test
    return ADS1015
