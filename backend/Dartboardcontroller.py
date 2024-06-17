import time
import threading
from klasses.MCP import Mcp
from klasses.Serialcommunication import SerialCommunication
from datetime import datetime
import RPi.GPIO as GPIO
from klasses.knop import knopke
from repositories.DataRepository import DataRepository
from sensorcontroller import SensorController

class DartboardController:
    def __init__(self,socketio, laser=12, sensor1=21, sensor2=20, steps=510, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22):
        self.socketio = socketio
        self.laser = laser
        self.sensor1 = sensor1
        self.mcp = Mcp(0, 0)
        self.serial_comm = SerialCommunication(serial_port='/dev/ttyS0', baud_rate=9600, button_pin=26)
        self.position = 10
        self.steps = steps
        self.step_sequence = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 1],
            [1, 0, 0, 1]
        ]
        self.last3throws = []
        self.stepmotorA = stepmotorA
        self.stepmotorB = stepmotorB
        self.stepmotorC = stepmotorC
        self.stepmotorD = stepmotorD
        self.dart_detected1 = False
        self.gamepointuser1 = 310
        self.gamepointuser2 = 310

        self.amountofplayers = 1
        self.usergamestatsidplayer1 = 1
        self.usergamestatsidplayer2 = 2
        self.importantinfogame = {"gameid": 0, "user1_game_stats_id": 0, "user2_game_stats_id": 0}
        self.current_player = 1
        self.amountofthrows = 0
        self.gamefinished = False
        self.gamestopped = False
        self.players = []
        self.laatsterichting = "kloksgewijs"
        # self.stop_event = threading.Event()

        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laser, GPIO.OUT)
        GPIO.setup(self.stepmotorA, GPIO.OUT)
        GPIO.setup(self.stepmotorB, GPIO.OUT)
        GPIO.setup(self.stepmotorC, GPIO.OUT)
        GPIO.setup(self.stepmotorD, GPIO.OUT)
        GPIO.cleanup(self.sensor1)
        GPIO.output(self.laser, 1)

    def button_pressed(self, channel):
        print("Button pressed!")

    def button_released(self, channel):
        self.dart_detected1 = True
        DataRepository.create_historiek("lasersensor1", "log_data", 1, "dartgezienlasersensor1")
        print("Laser 1 detected!")

    def start_buttons(self):
        button = knopke(21)
        button.on_press(self.button_pressed)
        button.on_release(self.button_released)

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

    def movearoundtheworld(self):
        print('move function')
        print(self.dart_detected1)

        while self.dart_detected1 == False and not self.gamestopped:

            print(f"{self.dart_detected1} - Searching for dart")
            waardestapmotor = DataRepository.gethistoriek("stapmotor")
            # while waardestapmotor["waarde"] > 1:

            #     if self.dart_detected1 == True or self.gamestopped == True:
            #         print("stopped")
            #         break
            #     else:
            #         waardestapmotor = DataRepository.gethistoriek("stapmotor")
            if waardestapmotor["waarde"] < 20 and (self.laatsterichting == "kloksgewijs") or waardestapmotor["waarde"] == 1:
                while waardestapmotor["waarde"] < 20:
                    if  self.dart_detected1 == True or self.gamestopped == True:
                        print("stopped")
                        break
                    else:
                        self.oneturn("kloksgewijs")
                        self.laatsterichting = "kloksgewijs"
                    waardestapmotor = DataRepository.gethistoriek("stapmotor")

            elif waardestapmotor["waarde"] == 20 or self.laatsterichting == "tegenkloksgewijs":
                while waardestapmotor["waarde"] > 1:
                    if  self.dart_detected1 == True or self.gamestopped == True:
                        print("stopped")
                        break
                    else:
                        self.oneturn("tegenkloksgewijs")
                        self.laatsterichting = "tegenkloksgewijs"
                    waardestapmotor = DataRepository.gethistoriek("stapmotor")
                self.laatsterichting == "kloksgewijs"
            waardestapmotor = DataRepository.gethistoriek("stapmotor")
            if self.dart_detected1 == True or self.gamestopped == True:
                print("stopped")
                break

        if self.gamestopped == True:
            return "stopped"
        else:
            return "dartdetected"

    def oneturn(self, direction):
        time.sleep(0.1)
        laatstewaardestapmotor = DataRepository.gethistoriek("stapmotor")
        print(str(laatstewaardestapmotor) + "dit is de oude waarde")
        if laatstewaardestapmotor["waarde"] == 20:
            direction = "tegenkloksgewijs"
        elif laatstewaardestapmotor["waarde"] == 1:
            direction = "kloksgewijs"

        if direction == "kloksgewijs":
            waardestapmotor = laatstewaardestapmotor["waarde"] + 1
        else:
            waardestapmotor = laatstewaardestapmotor["waarde"] - 1

        self.socketio.emit("B2F_positionstepmotor", {"waarde": waardestapmotor})
        self.move_motor(direction, 220)



        print('Inserting value' + str(waardestapmotor))
        response = DataRepository.create_historiek("stapmotor", "stepmotorposition", waardestapmotor, f"stapmotor 1 naar {'rechts' if direction == 'kloksgewijs' else 'links'}")
        print(str(response) + "stappenmotor positie gedraaid")
        print(str(DataRepository.gethistoriek("stapmotor")["waarde"]) + "dit is de nieuwe waarde")
        self.position = waardestapmotor

    def setstepmotorstart(self):
        while self.mcp.read_channel(1) > 530:
            print(self.mcp.read_channel(1))
            self.move_motor("kloksgewijs", 50)
            time.sleep(0.1)

        # if DataRepository.gethistoriek("stapmotor")["waarde"] == 10:
        response = DataRepository.create_historiek("stapmotor", "calibrate", 10, "stapmotor gecalibreerd")
        print(str(response) + "gecalibreerd op positie 10")
        self.position = 10

    def startgame(self, data):
        print("in the startgame function")
        # self.stop_event.clear()
        self.gamestopped = False
        # GPIO.cleanup()
        self.serial_comm.start_serial()
        self.start_buttons()

        print("startgame")
        self.setstepmotorstart()
        usergamemode = data["userGameMode"]
        gamemode = int(data["gameMode"])
        finishmode = data["finishMode"]


        self.usergamestats = []

        if usergamemode == "single":
            idusergamemode = 0
            self.players = [{"username": data["username"], "score": gamemode}]
            self.amountofplayers = 1
        elif usergamemode == "team":
            idusergamemode = 1
            self.players = [{"username": player, "score": gamemode} for player in data["usernames"]["team1"]]
            self.players += [{"username": player, "score": gamemode} for player in data["usernames"]["team2"]]
            self.amountofplayers = len(self.players)
        else:
            raise ValueError("Invalid user game mode")
        players = []
        players = [player["username"] for player in self.players]

        gameid = DataRepository.create_game(idusergamemode, self.get_game_mode(gamemode, finishmode))
        print(f"{gameid} - Game ID created")

        for player in self.players:
            user_id = DataRepository.read_user_by_username(player["username"])
            user_game_stats_id = DataRepository.create_usergamestats(user_id["IDuser"], gameid)
            self.usergamestats.append(user_game_stats_id)

        result = {
            "gameid": gameid,
            "user_game_stats_ids": self.usergamestats
        }
        self.importantinfogame = result
        print(str(result) + " dit is het resultaat")
        print("going to livegame")
        threading.Thread(target=self.livegame, daemon=True).start()
        return result

    def get_game_mode(self, gamemode, finishmode):
        if gamemode == 301 and finishmode == "singleout":
            return 0
        elif gamemode == 301 and finishmode == "doubleout":
            return 1
        elif gamemode == 501 and finishmode == "singleout":
            return 2
        elif gamemode == 501 and finishmode == "doubleout":
            return 3
        else:
            raise ValueError("Invalid game mode or finish mode")

    def livegame(self):
        while not self.gamefinished and not self.gamestopped:
            response = "notdartdatected"
            # time.sleep(3)
            response = self.movearoundtheworld()

            if response == "dartdetected":
                self.dart_detected1 = False

                print("Dart detected! Converting position to score and updating database.")
                waardeworp = self.changepositionintonumber(int(self.position))
                print(f"Score: {waardeworp}")

                # Ensure self.usergamestats is populated correctly and has the right indices
                if self.current_player <= len(self.usergamestats):
                    current_player_stats_id = self.usergamestats[self.current_player - 1]
                    DataRepository.create_worp(current_player_stats_id, waardeworp)
                else:
                    print(f"Error: current_player index {self.current_player} is out of bounds for self.usergamestats : {len(self.usergamestats)}")
                    break

                # Update score for current player
                current_player_index = self.current_player - 1
                current_player = self.players[current_player_index]
                if current_player["score"] - waardeworp == 0:
                    self.gamefinished == True
                else:
                    if current_player["score"] - waardeworp < 0:
                        print("score onder 0")
                    else:
                        current_player["score"] -= waardeworp
                        print(f"{current_player['username']}: {current_player['score']}")
                    self.last3throws.append(waardeworp)
                    self.amountofthrows += 1
                    if self.amountofthrows == 3:
                        print("3 keer gesmeten")
                        data = {
                            "player": self.current_player,
                            "username": current_player['username'],
                            "remaininscore": current_player["score"],
                            "throw1": self.last3throws[0],
                            "throw2": self.last3throws[1],
                            "throw3": self.last3throws[2]
                        }
                        self.socketio.emit("B2F_last3throws", {"beurt": data})
                        self.amountofthrows = 0
                        self.last3throws.clear()
                        # Switch to the next player in a circular manner
                        self.current_player = (self.current_player + 1) % self.amountofplayers
                        if self.current_player == 0:
                            self.current_player = self.amountofplayers
                        print(f"Switching to player {self.current_player}")

                                

            else:
                if (self.gamefinished == True):
                    self.socketio.emit("B2F_GameFinished",{
                        "player": self.current_player,
                        "username": current_player['username']
                    })                    



    def getdistance(self):
        smallest_distance = self.serial_comm.distanceTOF()
        # functionto get the distance
        if smallest_distance is not None:
            print(f"Smallest distance: {smallest_distance} mm")
            return smallest_distance
        else:
            print("No valid readings received.")

    def stopgame(self):
        # self.stop_event.set()

        self.gamestopped = True
        print("stopping game")
        for user_game_stats_id in self.usergamestats:
            DataRepository.update_usergamestats_stopped(user_game_stats_id)

        while self.position != 10:
            direction = "tegenkloksgewijs" if self.position > 10 else "kloksgewijs"
            self.move_motor(direction, 1)
            self.position = DataRepository.gethistoriek("stapmotor")["waarde"]

        self.reset_variables()

        print("Game stopped and reset to initial position.")

    def reset_variables(self):
        self.dart_detected1 = False
        self.gamepointuser1 = 310
        self.gamepointuser2 = 310
        self.amountofplayers = 1
        self.usergamestatsidplayer1 = 1
        self.usergamestatsidplayer2 = 2
        self.importantinfogame = {"gameid": 0, "user1_game_stats_id": 0, "user2_game_stats_id": 0}
        self.current_player = 1
        self.amountofthrows = 0

    def changepositionintonumber(self, position):
        listpositionsBAK = [3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6, 10, 15, 2, 17]
        listpositions = [6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13]
        waardeworp = listpositions[(position - 1) % 20]
        self.move_motor(self.laatsterichting, 200)
        distance = self.getdistance()
        if self.laatsterichting == "kloksgewijs":
            self.move_motor("tegenklokgewijs", 200)
        else:
            self.move_motor("kloksgewijs", 200)


        if int(distance) is not None:
            if distance < 20:
                print("triple")
                waardeworp = waardeworp * 3
            elif distance < 80:
                print('single')
            elif distance < 100:
                print('double')
                waardeworp = waardeworp * 2
            elif distance < 160:
                print('single')
            elif distance < 180:
                print('boule')
                waardeworp = 35
            elif distance > 180:
                print("andere kant")

        return waardeworp

    def algorithm(self):
        data_solo = {
            "usergamemode": "single",
            "user1name": "johndoe",
            "gamemode": 301,
            "finishmode": "singleout"
        }
        self.startgame(data_solo)

if __name__ == "__main__":
    try:
        controller = DartboardController(laser=12, sensor1=21, sensor2=20, steps=520, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22)
        controller.algorithm()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        GPIO.cleanup()
        controller.serial_comm.serial_connection.close()
        print("Program stopped.")
