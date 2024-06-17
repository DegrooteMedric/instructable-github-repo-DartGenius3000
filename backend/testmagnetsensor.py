import time
from Dartboardcontroller import DartboardController
from RPi import GPIO
def test_stepper_motor_calibration():
    # Initialize DartboardController with mock GPIO pins
    controller = DartboardController(laser=12, sensor1=20, sensor2=21, steps=520, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22)

    try:
        # Start the calibration process
        controller.setstepmotorstart()

        # Simulate the behavior of the magnet sensor
        while controller.position > 300:
            # Move the stepper motor one step at a time
            controller.oneturn("kloksgewijs")

            # Simulate the delay between steps
            time.sleep(0.1)

        # Output the final position of the stepper motor
        print("Stepper motor calibrated to position:", controller.position)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up GPIO pins
        GPIO.cleanup()

# Run the test
if __name__ == "__main__":
    test_stepper_motor_calibration()
