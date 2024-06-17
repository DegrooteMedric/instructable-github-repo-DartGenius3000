from RPi import GPIO
try:
    GPIO.cleanup()
except Exception as e:
    print("An error occurred while cleaning up GPIO pins:", e)
