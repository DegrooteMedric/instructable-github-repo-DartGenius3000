import time
from Serialcommunication import SerialCommunication  # Assuming the class is saved in a file named serial_communication.py

def getdistance():
    # Create an instance of the SerialCommunication class
    serial_comm = SerialCommunication(serial_port='/dev/ttyS0', baud_rate=9600, button_pin=26)

    try:
        # Start the serial communication
        serial_comm.start_serial()

        # Perform distance measurement
        smallest_distance = serial_comm.distanceTOF()
        if smallest_distance is not None:
            print(f"Smallest distance: {smallest_distance} mm")
            return smallest_distance
        else:
            print("No valid readings received.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up GPIO and close serial connection
        serial_comm.cleanup()
        print("Program stopped.")

if __name__ == '__main__':
    print("Starting Serial Communication Test")
    distance = getdistance()
    print("afstand tot dart: " + str(distance))