import RPi.GPIO as GPIO


class knopke:
    def __init__(self, pin, bouncetime=200):
        self.pin = pin
        self.bouncetime = bouncetime
        GPIO.cleanup(pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def pressed(self):
        ingedrukt = GPIO.input(self.pin)
        return not ingedrukt

    def on_press(self, call_method):
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.FALLING,
                              call_method, bouncetime=self.bouncetime)

    def on_release(self, call_method):
        GPIO.remove_event_detect(self.pin)
        GPIO.add_event_detect(self.pin, GPIO.RISING,
                              call_method, bouncetime=self.bouncetime)
