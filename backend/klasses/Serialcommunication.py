import serial
import time
from RPi import GPIO

class SerialCommunication:
    def __init__(self, serial_port='/dev/ttyS0', baud_rate=9600, button_pin=26):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.button_pin = button_pin
        self.serial_connection = None
        self.setup_gpio()

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.button_pin, GPIO.FALLING, callback=self.button_callback, bouncetime=300)

    def start_serial(self):
        self.serial_connection = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        time.sleep(2)  # Allow some time for Arduino to initialize

    def send_data(self, data):
        self.serial_connection.write(data.encode())

    def get_line(self):
        line = self.serial_connection.readline().decode().strip()
        if line:
            return line

    def close_serial(self):
        self.serial_connection.close()

    def button_callback(self, pin):
        if pin == self.button_pin:
            print("Button pressed. Sending 'test' command to Arduino.")
            self.send_data("test\n")

    def distanceTOF(self):
        try:
            readings = []
            # self.send_data("start\n")
            print("Sent 'start' command to Arduino. Receiving distance measurements...")

            while len(readings) < 10:
                self.send_data("start\n")
                if self.serial_connection.in_waiting > 0:
                    line = self.get_line()
                    print(f"Distance: {line} mm")

                    try:
                        distance = int(line)
                        readings.append(distance)
                    except ValueError:
                        print(f"Invalid reading: {line}")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("Interrupted by user.")

        finally:
            self.send_data("stop\n")
            print("Sent 'stop' command to Arduino. Stopping distance measurements.")

        if readings:
            return min(readings)
        else:
            return None

    def cleanup(self):
        GPIO.cleanup()
        self.close_serial()

    def run(self):
        self.start_serial()
        # try:
        #     while True:
        #         response = self.get_line()
        #         if response:
        #             print(response)
        # except KeyboardInterrupt:
        #     print("Program interrupted by user.")
        # finally:
        #     self.cleanup()
        #     print("Program stopped.")

if __name__ == '__main__':
    print("Starting program")
    serial_comm = SerialCommunication(serial_port='/dev/ttyS0', baud_rate=9600, button_pin=26)
    serial_comm.start_serial()
    serial_comm.distanceTOF()
