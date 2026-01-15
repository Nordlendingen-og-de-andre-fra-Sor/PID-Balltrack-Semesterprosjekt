# config/settings.py
# -----------------------------------------------------------
# Konfigurasjonsfil for V8 Balltrack-systemet
# Samler ALLE justerbare parametre ett sted.
# Endringer her påvirker både controller, hardware og GUI.
# -----------------------------------------------------------

# ===========================
# HARDWARE – PWM / PCA9685
# ===========================
PCA9685_I2C_ADDR = 0x40        # Standard adresse
PCA9685_I2C_BUS = 1            # /dev/i2c-1
PCA9685_FREQ_HZ = 50           # Servo-frekvens

# Servo pulsgrenser (kan kalibreres senere)
SERVO_MIN_US = 1000
SERVO_MAX_US = 2000
SERVO_CHANNEL = 0              # PCA9685 utgang vi bruker


# ===========================
# HARDWARE – ADC (ADS1115)
# ===========================
# ADC (ADS1115)
ADC_I2C_BUS = 1
ADC_I2C_ADDR = 0x48      # ADS1115 standardadresse (kan være 0x48–0x4B)
ADC_CHANNEL = 0          # 0..3 (AIN0..AIN3) single-ended
ADC_RESOLUTION = 32767    # 16-bit single-ended positiv range



# ===========================
# PID – standardverdier
# ===========================
PID_KP = 2.0
PID_KI = 0.0
PID_KD = 0.0

# PID begrensninger
PID_MIN = -1.0
PID_MAX = 1.0

# PID sampletid (dt)
PID_TS = 0.02                  # 20 ms → 50 Hz kontrollsløyfe


# ===========================
# CONTROLLER – generelle
# ===========================
DEFAULT_SETPOINT = 0.5         # midt på banen (0..1)
USE_NORMALIZED_UNITS = True


# ===========================
# GUI OPPDATERING
# ===========================
GUI_UPDATE_MS = 20             # 20 ms → 50 Hz GUI oppdatering


# ===========================
# LOGGING
# ===========================
LOG_ENABLED = True
LOG_LEVEL = "INFO"             # DEBUG / INFO / WARNING / ERROR

# LOG_* er forberedt for fremtidig bruk (ikke aktivert i V8 per nå)
