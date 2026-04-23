
from V8_BALLTRACK.hardware.pwm.pca9685 import PCA9685
from V8_BALLTRACK.config import settings


def main():
    print("=== SERVO TEST (PCA9685) ===")
    print("Skriv inn puls i mikrosekunder (f.eks 1500)")
    print("Skriv 'q' for å avslutte\n")

    try:
        pwm = PCA9685(
            address=settings.PCA9685_I2C_ADDR,
            bus=settings.PCA9685_I2C_BUS,
            freq_hz=settings.PCA9685_FREQ_HZ,
        )
    except Exception as e:
        print("FEIL: Klarte ikke å initialisere PCA9685")
        print(e)
        return

    channel = settings.SERVO_CHANNEL

    print(f"PCA9685 OK på adresse 0x{settings.PCA9685_I2C_ADDR:02X}")
    print(f"Bruker kanal: {channel}\n")

    last_value = 1500
    pwm.set_servo_us(channel, last_value)

    while True:
        try:
            user_input = input("µs > ").strip()

            if user_input.lower() in ("q", "quit", "exit"):
                break

            if user_input == "":
                value = last_value
            else:
                value = int(user_input)

            # sikkerhetsbegrensning
            if value < 500 or value > 2500:
                print("Advarsel: verdi utenfor normalt område (500–2500 µs)")

            pwm.set_servo_us(channel, value)
            last_value = value

            print(f"→ Setter puls: {value} µs")

        except ValueError:
            print("Ugyldig input. Skriv et tall (µs) eller 'q'.")
        except KeyboardInterrupt:
            break

    print("\nSlår av servo...")
    pwm.servo_off(channel)
    print("Ferdig.")


if __name__ == "__main__":
    main()