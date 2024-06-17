import RPi.GPIO as GPIO

class GPIOHandler:
    def __init__(self, clk=13, dt=19, sw=26,counter=1):
        self.dt = dt
        self.clk = clk
        self.sw = sw
        self.counter = counter

        self.setup_pins()
        

    def setup_pins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.dt, GPIO.FALLING, bouncetime=1)
        GPIO.add_event_callback(self.dt, self.callback_links)

        GPIO.add_event_detect(self.clk, GPIO.FALLING, bouncetime=1)
        GPIO.add_event_callback(self.clk, self.callback_rechts)

        GPIO.add_event_detect(self.sw, GPIO.FALLING, bouncetime=200)
        GPIO.add_event_callback(self.sw, self.callback_button)


    def callback_links(self, pin):
        waarderechts = GPIO.input(self.clk)
        waardelinks = GPIO.input(self.dt)

        if waardelinks == 0 and waarderechts == 1:
            if self.counter == 1:
                self.counter = 3
            else:
                self.counter -= 1
            print(f"links ({self.counter})")

    def callback_rechts(self, pin):
        waardelinks = GPIO.input(self.dt)
        waarderechts = GPIO.input(self.clk)

        if waarderechts == 0 and waardelinks == 1:
            if self.counter == 3:
                self.counter = 1
            else:
                self.counter += 1
            print(f"rechts ({self.counter})")
            

    def callback_button(self, pin):
        print("ingedrukt")

    def cleanup(self):
        GPIO.cleanup()

    

if __name__ == "__main__":
    try:
        gpio_handler = GPIOHandler()
     
    except KeyboardInterrupt:
        GPIO.cleanup()
