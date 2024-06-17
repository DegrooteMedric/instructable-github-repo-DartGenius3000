from smbus import SMBus
import time

class MPU6050:
    def __init__(self, i2c_address):
        self.i2c_address = i2c_address
        self.i2c_bus = 1
        self.i2c = SMBus(self.i2c_bus)

    def setup(self):
        # Initialize the MPU6050
        self.i2c.write_byte_data(self.i2c_address, 0x6B, 0x00)  # Power management register
        self.i2c.write_byte_data(self.i2c_address, 0x1C, 0x00)  # 2g accelerometer
        self.i2c.write_byte_data(self.i2c_address, 0x1B, 0x18)  # Setting up gyroscope

    def read_components(self):
        # Read 14 bytes of data from the MPU6050
        return self.i2c.read_i2c_block_data(self.i2c_address, 0x3B, 14)

    def combine_bytes(self, high_byte, low_byte):
        # Combine two bytes into a single value interpreting as 2's complement
        value = (high_byte << 8) | low_byte
        if value >> 15 == 1:
            value = (value - (2 ** 16)) - 1
        return value

    def read_acceleration(self, data):
        # Read acceleration data from the sensor data
        acceleration_x = self.combine_bytes(data[0], data[1]) / 16384.0
        acceleration_y = self.combine_bytes(data[2], data[3]) / 16384.0
        acceleration_z = self.combine_bytes(data[4], data[5]) / 16384.0
        return acceleration_x, acceleration_y, acceleration_z

    def read_temperature(self, data):
        # Read temperature data from the sensor data
        temperature = (self.combine_bytes(data[6], data[7]) / 340) + 30.53
        return temperature

    def read_gyroscope(self, data):
        # Read gyroscope data from the sensor data
        gyro_x = self.combine_bytes(data[8], data[9]) / 131
        gyro_y = self.combine_bytes(data[10], data[11]) / 131
        gyro_z = self.combine_bytes(data[12], data[13]) / 131
        return gyro_x, gyro_y, gyro_z
    
    def read_temperatureself(self):
        self.setup()
        data = self.read_components()
        # print(str(data) + "temperatuur")
        return str(round(self.read_temperature(data),2))

 

if __name__ == "__main__":
    try:
        mpu_sensor = MPU6050(0x68)  # Initialize the MPU6050 with the specified address
        mpu_sensor.setup()  # Call the setup function to initialize the sensor
        
        while True:
            sensor_data = mpu_sensor.read_components()

            acceleration = mpu_sensor.read_acceleration(sensor_data)
            print("Acceleration: X:{:.2f} Y:{:.2f} Z:{:.2f}".format(*acceleration))

            temperature = mpu_sensor.read_temperature(sensor_data)
            print("Temperature: {:.2f} C".format(temperature))

            gyroscope = mpu_sensor.read_gyroscope(sensor_data)
            print("Gyroscope: X:{:.2f} Y:{:.2f} Z:{:.2f}".format(*gyroscope))

            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        # Close the I2C bus
        mpu_sensor.i2c.close()
