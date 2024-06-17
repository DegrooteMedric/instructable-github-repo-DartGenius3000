import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, step_sequence, stepmotorA, stepmotorB, stepmotorC, stepmotorD):
        self.step_sequence = step_sequence
        self.stepmotorA = stepmotorA
        self.stepmotorB = stepmotorB
        self.stepmotorC = stepmotorC
        self.stepmotorD = stepmotorD
        self.position = 0

        # Set up GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepmotorA, GPIO.OUT)
        GPIO.setup(self.stepmotorB, GPIO.OUT)
        GPIO.setup(self.stepmotorC, GPIO.OUT)
        GPIO.setup(self.stepmotorD, GPIO.OUT)

    def move_motor(self, direction, steps):
        current_step = 0
        step_sequence = self.step_sequence if direction == "kloksgewijs" else list(reversed(self.step_sequence))
        
        for _ in range(steps):
            for step in step_sequence:
                GPIO.output(self.stepmotorA, step[3])
                GPIO.output(self.stepmotorB, step[2])
                GPIO.output(self.stepmotorC, step[1])
                GPIO.output(self.stepmotorD, step[0])
                current_step = (current_step + 1) % 8
                time.sleep(0.001)
                dart_angle = current_step / len(self.step_sequence)
                self.position += dart_angle

    def cleanup(self):
        GPIO.cleanup()

# Test loop implementation
if __name__ == "__main__":
    # Define the step sequence for the stepper motor
    step_sequence = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]
    
    # Define GPIO pins connected to the stepper motor
    # stepmotorA = 17
    # stepmotorB = 18
    # stepmotorC = 27
    # stepmotorD = 22
    stepmotorA=4
    stepmotorB=17
    stepmotorC=27
    stepmotorD=22
    # Create a StepperMotor instance
    motor = StepperMotor(step_sequence, stepmotorA, stepmotorB, stepmotorC, stepmotorD)

    try:
        steps = 520 * 5

        # Turn 10 times to the right (5200 steps)
        motor.move_motor("kloksgewijs", 2 * steps)

        # Turn 5 times to the left (2600 steps)
        motor.move_motor("tegen", steps)
        

    finally:
        # Clean up GPIO pins
        motor.cleanup()
