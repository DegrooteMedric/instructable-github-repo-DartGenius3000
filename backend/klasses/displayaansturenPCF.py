import time
from smbus import SMBus
import lgpio

class displayi2c:
    def __init__(self, max_width=16, rspin=23, enable_pin=24, i2c_bus=1):
        self.max_width = max_width
        self.rspin = rspin
        self.enable_pin = enable_pin
        self.i2c_bus = i2c_bus
        self.i2c = SMBus(self.i2c_bus)
        self.chip = lgpio.gpiochip_open(0)  # Open gpiochip 0
        self.pins_claimed = False
        self.setup()

    def setup(self):
        self.cleanup()  # Ensure any previous configuration is cleaned up
        lgpio.gpio_claim_output(self.chip, self.rspin)
        lgpio.gpio_claim_output(self.chip, self.enable_pin)
        self.pins_claimed = True
        time.sleep(0.1)  # Delay after setting up each pin

    def stuur_instructie(self, byte):
        lgpio.gpio_write(self.chip, self.enable_pin, 1)
        lgpio.gpio_write(self.chip, self.rspin, 0)

        self.i2c.write_byte(0x38, byte)  # Assuming the I2C address is 0x3c
        lgpio.gpio_write(self.chip, self.enable_pin, 0)
        time.sleep(0.1)

    def stuur_data(self, text):
        for char in text:
            # print("char" + str(char))
            lgpio.gpio_write(self.chip, self.enable_pin, 1)
            lgpio.gpio_write(self.chip, self.rspin, 1)

            self.i2c.write_byte(0x38, ord(char))  # Assuming the I2C address is 0x3c
            lgpio.gpio_write(self.chip, self.enable_pin, 0)
            time.sleep(0.01)

    def cleanup(self):
        if self.pins_claimed:
            lgpio.gpio_free(self.chip, self.rspin)
            lgpio.gpio_free(self.chip, self.enable_pin)
            lgpio.gpiochip_close(self.chip)
            self.pins_claimed = False

if __name__ == "__main__":
    display = displayi2c()
    try:

        while True:
            display.stuur_instructie(0x3F)  # Send some initialization instruction
            display.stuur_instructie(0x0F)  # Another initialization instruction
            display.stuur_instructie(0x01)  # Clear display instruction
            display.stuur_data("hello ruben")  # Display some text
            print("text sent")
            time.sleep(5)
    finally:
        display.cleanup()  # Clean up GPIO settings
        print("GPIO cleaned up")
