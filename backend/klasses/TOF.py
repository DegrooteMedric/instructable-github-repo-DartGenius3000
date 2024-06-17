# import smbus2

# # Define the I²C address of your sensor
# address = 0x29

# # Create an SMBus object for communication
# bus = smbus2.SMBus(1)  # Use the appropriate bus number

# # Example write operation
# try:
#     # Write data (e.g., 0x55) to register 0x52
#     bus.write_byte_data(address, 0x52, 0x55)
#     print("Write operation successful.")
# except Exception as e:
#     print(f"Error writing data: {e}")

# # Example read operation
# try:
#     # Read data from register 0x53
#     data = bus.read_byte_data(address, 0x53)
#     print(f"Read data: {data}")
# except Exception as e:
#     print(f"Error reading data: {e}")

from knop import knopke
import time
from RPi import GPIO

def button_pressed(channel):
    print("Button pressed!")

def button_released(channel):
    print("Button released!")

if __name__ == "__main__":
    button = knopke(20)
    button.on_press(button_pressed)
    button.on_release(button_released)

    try:
        while True:
            time.sleep(1)  # Wait for 1 second
    except KeyboardInterrupt:
        print("Exiting gracefully")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
