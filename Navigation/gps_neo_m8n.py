import serial
import pynmea2

gps_serial = serial.Serial(
    port="/dev/serial0",
    baudrate=9600,
    timeout=1
)

def get_gps_data():
    while True:
        line = gps_serial.readline().decode("utf-8", errors="ignore")
        if line.startswith("$GPGGA"):
            msg = pynmea2.parse(line)
            return {
                "lat": msg.latitude,
                "lon": msg.longitude,
                "alt": msg.altitude,
                "satellites": msg.num_sats
            }

if __name__ == "__main__":
    while True:
        print(get_gps_data())
