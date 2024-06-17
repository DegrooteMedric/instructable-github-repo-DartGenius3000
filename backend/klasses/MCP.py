import spidev
import time

class Mcp:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 10 ** 5

    def read_channel(self, ch):
        adc = self.spi.xfer2([1, (8 | ch) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]
        return data

    def close_spi(self):
        self.spi.close()

if __name__ == "__main__":
    mcp = Mcp(bus=0, device=0)  # Using SPI0 and CE0
    try:
        while True:
            # lichtweerstand
            # channel = 0  # Read from channel 0
            # value = mcp.read_channel(channel)
            # value = 100 - ((value /1023) * 100)
            # print(f"Channel {channel} value: {value}")
            # time.sleep(0.1)

            # magneetsensor
            channel = 1  # Read from channel 0
            value = mcp.read_channel(channel)
            # value = 100 - ((value /1023) * 100)
            print(f"Channel {channel} value: {value} ==== magneetsensor")
            time.sleep(1)
    finally:
        mcp.close_spi()


