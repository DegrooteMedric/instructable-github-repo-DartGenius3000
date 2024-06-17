from RPi import GPIO
from subprocess import check_output
from klasses.displayaansturenPCF import displayi2c
from klasses.MCP import Mcp
from klasses.knop import knopke
from klasses.MPU650class import MPU6050
from klasses.rotaryencoder import GPIOHandler
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time
from datetime import datetime
class SensorController:
    def __init__(self, socketio,busmcp=0, devicemcp=0, clk=13, dt=19, sw=26, counter=1, mpuadress=0x68):
        self.socketio = socketio
        self.lcd_display = displayi2c()
        self.lcd_display.stuur_instructie(0x3F)
        self.lcd_display.stuur_instructie(0x0F)
        self.lcd_display.stuur_instructie(0x01)
        self.busmcp = busmcp
        self.devicemcp = devicemcp
        self.clock = clk
        self.dt = dt
        self.sw = sw
        self.mpuadress = mpuadress
        self.mcp = Mcp(self.busmcp, self.devicemcp)
        self.rotary = GPIOHandler(self.clock, self.dt, self.sw, counter)
        self.mpu6050 = MPU6050(self.mpuadress)
        self.score = 0
        self.counter = 1
        self.laststatus = self.counter
        self.firsttime = True
        self.lastvaluelijn2 = "172.30.248.49"

 
    def read_light_sensor(self):
        waarde = 100 - (self.mcp.read_channel(0) / 1023.0 * 100)
        self.socketio.emit("B2F_lichtsensor",{"waarde":waarde})
        # print("reading licht sensor")
        return waarde

    def read_magnet_sensor(self):
        waarde = (self.mcp.read_channel(1))
        # print("reading magnetsensor")
        return str(round(waarde,2))

    def geefwaardeweer(self, status, lijn1, lijn2):
        if status != self.laststatus or self.firsttime == True:
            self.lcd_display.stuur_instructie(0x01)
            self.lcd_display.stuur_data(lijn1)

        if lijn2 != self.lastvaluelijn2 or self.firsttime == True:
            time.sleep(0.01)
            self.lcd_display.stuur_instructie(0xc0)
            time.sleep(0.01)
            # print(lijn2)
            self.lcd_display.stuur_data(lijn2)

        self.firsttime = False
        self.lastvaluelijn2 = lijn2
        self.laststatus = status

    def read_temperature(self):
        # print("reading temp")
        temperature = self.mpu6050.read_temperatureself()
        response = DataRepository.create_historiek("lichtsensor","inserttemp",temperature,"temperatuur") # ,datetime.now()
        self.socketio.emit("B2F_temperatuur",{"waarde":temperature})
        print(temperature)
        return temperature

    def get_rotary_status(self):
        self.counter = self.rotary.counter
        return self.rotary.counter

    def display_value(self, status, label, value):
        print("display is being used to print something")
        self.geefwaardeweer(status, label, str(value))

    def run(self):
        print("sensorcontroller is running")
        while True:
            self.lichtsensor = self.read_light_sensor()
            self.temperatuur = self.read_temperature()
            self.magneetsensor = self.read_magnet_sensor()

            self.counter = self.get_rotary_status()
            if self.counter == 1:
                ips = check_output(["hostname", "--all-ip-addresses"]).decode('utf-8').strip()
                ip_list = ips.split()
                
                # via ssh without cable
                second_ip = ip_list[0]

                # Ensure there's a second IP address(via cable)
                # if len(ip_list) > 1:
                #     second_ip = ip_list[1]
                # else:
                #     second_ip = "No IP found"
                self.display_value(self.counter, "ip:", second_ip)
                # print("writing to lcd")
                time.sleep(0.1)
            elif self.counter == 2:
                self.display_value(self.counter, "SCORE + naam", round(self.lichtsensor, 2))
            elif self.counter == 3:
                self.display_value(self.counter, "magneetsensor", f"{self.magneetsensor} °C")
            elif self.counter > 3:
                self.counter = 1
            time.sleep(2)

if __name__ == "__main__":
    controller = SensorController()
    try:
        while True:
            controller.run()
    finally:
        controller.firsttime = True
        controller.lastvaluelijn2 = "172.30.248.49"
        controller.lcd_display.cleanup()  # Clean up GPIO settings
        print("finished")
