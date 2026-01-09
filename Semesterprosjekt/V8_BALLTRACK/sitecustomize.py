# sitecustomize.py
import os

# Sett USE_GROVEHAT_ADC=1 for å aktivere fallback
if os.environ.get("USE_GROVEHAT_ADC", "0") == "1":
    try:
        from V8_BALLTRACK.tools.grovehat_adc_fallback import install_grovehat_fallback
        install_grovehat_fallback()
        print("[sitecustomize] GroveHAT ADC fallback: ENABLED")
    except Exception as e:
        print(f"[sitecustomize] GroveHAT ADC fallback: FAILED ({e!r})")
