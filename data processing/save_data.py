import serial
import csv
from datetime import datetime

SERIAL_PORT = "COM5"
BAUD_RATE = 9600
OUTPUT_FILE = "0.csv" 

# aX,aY,aZ,gX,gY,gZ
# -0.163,0.246,2.188,190.918,-218.323,29.785
# -0.180,0.307,2.031,195.618,-178.345,19.592
# -0.276,0.314,1.834,194.031,-150.574,7.019
# -0.354,0.289,1.634,183.594,-134.583,-3.418

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT}")

            with open(OUTPUT_FILE, mode="w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)

                while True:
                    try:

                        line = ser.readline().decode("utf-8").strip()
                        if line:

                            data = line.split(",")
                            if len(data) == 6:

                                csv_writer.writerow(data)
                                print(data)
                    except KeyboardInterrupt:
                        print("\nStopping...")
                        break
    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()