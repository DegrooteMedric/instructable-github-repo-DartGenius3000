import RPi.GPIO as GPIO
import time

class knopke:
    def __init__(self, pin, bouncetime=200):
        self.pin = pin
        self.bouncetime = bouncetime

        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def pressed(self):
        ingedrukt = GPIO.input(self.pin)
        return not ingedrukt

    def on_press(self, call_method):
        GPIO.remove_event_detect(self.pin)  # Clear any existing edge detection
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=call_method, bouncetime=self.bouncetime)

    def on_release(self, call_method):
        GPIO.remove_event_detect(self.pin)  # Clear any existing edge detection
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=call_method, bouncetime=self.bouncetime)

def button_pressed(channel):
    print("Button pressed!")

def button_released(channel):
    print("Button released!")

if __name__ == "__main__":
    button = knopke(6)
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
