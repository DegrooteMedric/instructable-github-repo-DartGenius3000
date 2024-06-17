


# ***********************************************************V3********************************************************


# import time
# import threading
# from datetime import datetime
# import RPi.GPIO as GPIO
# from klasses.knop import knopke  # Assuming this class exists and is correctly implemented
# from repositories.DataRepository import DataRepository  # Assuming this module exists and is correctly implemented
# from klasses.MCP import Mcp  # Assuming this class exists and is correctly implemented

# class DartboardController:
#     def __init__(self, laser=12, sensor1=16, sensor2=21, steps=510, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22):
#         self.laser = laser
#         self.sensor1 = knopke(pin=sensor1)
#         self.mcp = Mcp(0, 0)

#         self.position = 10  # Start at the middle position
#         self.steps = steps  # Number of steps to rotate gear 1 time
#         self.step_sequence = [
#             [1, 0, 0, 0],
#             [1, 1, 0, 0],
#             [0, 1, 0, 0],
#             [0, 1, 1, 0],
#             [0, 0, 1, 0],
#             [0, 0, 1, 1],
#             [0, 0, 0, 1],
#             [1, 0, 0, 1]
#         ]
#         self.stepmotorA = stepmotorA
#         self.stepmotorB = stepmotorB
#         self.stepmotorC = stepmotorC
#         self.stepmotorD = stepmotorD
#         self.dart_detected1 = False
#         self.gamepointuser1 = 310
#         self.gamepointuser2 = 310

#         self.amountofplayers = 1
#         self.usergamestatsidplayer1 = 1
#         self.usergamestatsidplayer2 = 2
#         self.importantinfogame = {"gameid": 0, "user1_game_stats_id": 0, "user2_game_stats_id": 0}
#         self.current_player = 1
#         self.amountofthrows = 0
#         self.gamefinished = False

#         # Initialize GPIO
#         GPIO.cleanup()
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.laser, GPIO.OUT)
#         GPIO.setup(self.stepmotorA, GPIO.OUT)
#         GPIO.setup(self.stepmotorB, GPIO.OUT)
#         GPIO.setup(self.stepmotorC, GPIO.OUT)
#         GPIO.setup(self.stepmotorD, GPIO.OUT)
#         GPIO.setup(sensor1, GPIO.IN)
#         GPIO.output(self.laser, 1)

#     # Callback for laser detection
#     def laserin1_callback(self, channel):
#         self.dart_detected1 = True
#         DataRepository.create_historiek("lasersensor1", "log_data", 1, "dartgezienlasersensor1")
#         print("Laser 1 detected!")

#     def start(self):
#         GPIO.remove_event_detect(self.sensor1.pin)
#         GPIO.add_event_detect(self.sensor1.pin, GPIO.FALLING, callback=self.laserin1_callback, bouncetime=200)
#         print("Event detection started for sensor1.")

#     # Motor movement logic
#     def move_motor(self, direction, steps):
#         current_step = 0
#         step_sequence = self.step_sequence if direction == "kloksgewijs" else list(reversed(self.step_sequence))
        
#         for _ in range(steps):
#             if self.dart_detected1:
#                 print("Stopping stepper motor as dart is detected!")
#                 break

#             for step in step_sequence:
#                 GPIO.output(self.stepmotorA, step[3])
#                 GPIO.output(self.stepmotorB, step[2])
#                 GPIO.output(self.stepmotorC, step[1])
#                 GPIO.output(self.stepmotorD, step[0])
#                 current_step = (current_step + 1) % 8
#                 time.sleep(0.001)  # Delay in seconds
#                 dart_angle = current_step / len(self.step_sequence)
#                 self.position += dart_angle

#     def movearoundtheworld(self):
#         print('move function')
#         print(self.dart_detected1)
        
#         while not self.dart_detected1:
#             print(f"{self.dart_detected1} - Searching for dart")
#             waardestapmotor = DataRepository.gethistoriek("stapmotor")
#             while waardestapmotor["waarde"] > 1:
#                 if self.dart_detected1:
#                     break
#                 self.oneturn("tegenkloksgewijs")
#                 waardestapmotor = DataRepository.gethistoriek("stapmotor")
#             while waardestapmotor["waarde"] < 20:
#                 if self.dart_detected1:
#                     break
#                 self.oneturn("kloksgewijs")
#                 waardestapmotor = DataRepository.gethistoriek("stapmotor")
#         return "dartdetected"

#     def oneturn(self, direction):
#         time.sleep(0.1)
#         laatstewaardestapmotor = DataRepository.gethistoriek("stapmotor")
#         print(str(laatstewaardestapmotor) + "dit is de oude waarde")
#         if laatstewaardestapmotor["waarde"] == 20:
#             direction = "tegenkloksgewijs"
#         elif laatstewaardestapmotor["waarde"] == 1:
#             direction = "kloksgewijs"   

#         self.move_motor(direction, 515)

#         if direction == "kloksgewijs":
#             waardestapmotor = laatstewaardestapmotor["waarde"] + 1
#         else:
#             waardestapmotor = laatstewaardestapmotor["waarde"] - 1
        
#         print('Inserting value' + str(waardestapmotor))
#         response = DataRepository.create_historiek("stapmotor", "stepmotorposition", waardestapmotor, f"stapmotor 1 naar {'rechts' if direction == 'kloksgewijs' else 'links'}")
#         print(str(response) + "stappenmotor positie gedraaid")
#         print(str(DataRepository.gethistoriek("stapmotor")["waarde"]) + "dit is de nieuwe waarde")
#         self.position = waardestapmotor

#     def setstepmotorstart(self):
#         while self.mcp.read_channel(1) > 300:
#             print(self.mcp.read_channel(1))
#             # Move the stepper motor one step at a time
#             self.move_motor("kloksgewijs", 20)

#             # Simulate the delay between steps
#             time.sleep(0.1)

#         if DataRepository.gethistoriek("stapmotor")["waarde"] == 10:
#             response = DataRepository.create_historiek("stapmotor", "calibrate", 10, "stapmotor gecalibreerd")
#             print(str(response) + "gecalibreerd op positie 10")
#             self.position == 10

#     # Game logic
#     def startgame(self, data):
#         print("startgame")
#         self.setstepmotorstart()
#         usergamemode = data["usergamemode"]
#         user1name = data["user1name"]
#         user2name = data.get("user2name")
#         gamemode = data["gamemode"]
#         finishmode = data["finishmode"]
    
#         if usergamemode == "single":
#             usermode = 1
#         elif usergamemode == "teams":
#             usermode = 2 
#         else:
#             usermode = 3  # bot

#         if gamemode == 301 and finishmode == "singleout":
#             game_mode = 0
#         elif gamemode == 301 and finishmode == "doubleout":
#             game_mode = 1
#         elif gamemode == 501 and finishmode == "singleout":
#             game_mode = 2
#         elif gamemode == 501 and finishmode == "doubleout":
#             game_mode = 3
#         else:
#             raise ValueError("Invalid game mode or finish mode")

#         gameid = DataRepository.create_game(usermode, game_mode)
#         print(f"{gameid} - Game ID created")

#         user1_id = DataRepository.read_user_by_username(user1name)
#         user1_game_stats_id = DataRepository.create_usergamestats(user1_id["IDuser"], gameid)
#         self.usergamestatsidplayer1 = user1_game_stats_id

#         if user2name:
#             user2_id = DataRepository.read_user_by_username(user2name)
#             user2_game_stats_id = DataRepository.create_usergamestats(user2_id["IDuser"], gameid)
#             self.usergamestatsidplayer2 = user2_game_stats_id
#             self.amountofplayers = 2
#         else:
#             user2_game_stats_id = None
#             self.amountofplayers = 1

#         result = {
#             "gameid": gameid,
#             "user1_game_stats_id": user1_game_stats_id,
#             "user2_game_stats_id": user2_game_stats_id
#         }
#         self.importantinfogame = result
#         print(str(result) + "dit is het resultaat")
#         print("going to livegame")
#         threading.Thread(target=self.livegame, args=("nodartdetected",), daemon=True).start()  # Start livegame in a separate thread
#         return result

#     def livegame(self, response):
#         print("in livegame atm")
#         while self.gamefinished == False:
#             self.dart_detected1 = False
#             response = "notdartdetected"
#             time.sleep(3)
#             print("in livegame zoeken naar dart1")
#             response = self.movearoundtheworld()
#             print("in livegame zoeken naar dart")
#             if response == "dartdetected":
#                 print("Dart detected! Converting position to score and updating database.")
#                 waardeworp = self.changepositionintonumber(int(self.position))
#                 print(f"Score: {waardeworp}")

#                 if self.current_player == 1:
#                     DataRepository.create_worp(self.usergamestatsidplayer1, waardeworp)
#                     self.gamepointuser1 -= waardeworp
#                     print(str(self.gamepointuser1))
#                 else:
#                     DataRepository.create_worp(self.usergamestatsidplayer2, waardeworp)
#                     self.gamepointuser2 -= waardeworp
                
#                 self.amountofthrows += 1
#                 if self.amountofthrows == 3:
#                     self.amountofthrows = 0
#                     if self.amountofplayers == 2:
#                         self.current_player = 2 if self.current_player == 1 else 1
#                         print(f"Switching to player {self.current_player}")

#     def changepositionintonumber(self, position):
#         listpositions = [3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6, 10, 15, 2, 17]
#         waardeworp = listpositions[(position - 1) % 20]
#         return waardeworp

#     def algorithm(self):
#         data_solo = {
#             "usergamemode": "single",
#             "user1name": "johndoe",
#             "gamemode": 301,
#             "finishmode": "singleout"
#         }

#         self.startgame(data_solo)
        
# if __name__ == "__main__":
#     try:
#         controller = DartboardController(laser=12, sensor1=16, sensor2=21, steps=520, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22)
#         controller.start()
#         controller.algorithm()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         GPIO.cleanup()


























# ***********************************************************V2********************************************************

# import time
# from datetime import datetime
# import RPi.GPIO as GPIO
# from klasses.knop import knopke
# from repositories.DataRepository import DataRepository

# class DartboardController:
#     def __init__(self, laser, sensor1, sensor2, steps, stepmotorA, stepmotorB, stepmotorC, stepmotorD):
#         self.laser = laser
#         self.sensor1 = knopke(pin=sensor1)
#         self.position = 10  # Start at the middle position
#         self.steps = steps  # Number of steps to rotate gear 1 time
#         self.step_sequence = [
#             [1, 0, 0, 0],
#             [1, 1, 0, 0],
#             [0, 1, 0, 0],
#             [0, 1, 1, 0],
#             [0, 0, 1, 0],
#             [0, 0, 1, 1],
#             [0, 0, 0, 1],
#             [1, 0, 0, 1]
#         ]
#         self.stepmotorA = stepmotorA
#         self.stepmotorB = stepmotorB
#         self.stepmotorC = stepmotorC
#         self.stepmotorD = stepmotorD
#         self.dart_detected1 = False

#         self.amountofplayers = 1
#         self.usergamestatsidplayer1 = 1
#         self.usergamestatsidplayer2 = 2
#         self.importantinfogame = {"gameid": 0, "user1_game_stats_id": 0, "user2_game_stats_id": 0}
#         self.userlive = 1
#         self.amountofthrows = 0
#         self.gamefinished = False

#         # Initialize GPIO
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.laser, GPIO.OUT)
#         GPIO.setup(self.stepmotorA, GPIO.OUT)
#         GPIO.setup(self.stepmotorB, GPIO.OUT)
#         GPIO.setup(self.stepmotorC, GPIO.OUT)
#         GPIO.setup(self.stepmotorD, GPIO.OUT)
#         GPIO.setup(sensor1, GPIO.IN)
#         GPIO.output(self.laser, 1)

#     # Callback for laser detection
#     def laserin1_callback(self, channel):
#         self.dart_detected1 = True
#         DataRepository.create_historiek("lasersensor1", "log_data", 1, "dartgezienlasersensor1")
#         print("Laser 1 detected!")

#     def start(self):
#         GPIO.add_event_detect(self.sensor1.pin, GPIO.RISING, callback=self.laserin1_callback)

#     # Motor movement logic
#     def move_motor(self, direction, steps):
#         current_step = 0
#         step_sequence = self.step_sequence if direction == "kloksgewijs" else list(reversed(self.step_sequence))
        
#         for _ in range(steps):
#             if self.dart_detected1:
#                 print("Stopping stepper motor as dart is detected!")
#                 break

#             for step in step_sequence:
#                 GPIO.output(self.stepmotorA, step[3])
#                 GPIO.output(self.stepmotorB, step[2])
#                 GPIO.output(self.stepmotorC, step[1])
#                 GPIO.output(self.stepmotorD, step[0])
#                 current_step = (current_step + 1) % 8
#                 time.sleep(0.001)  # Delay in seconds
#                 dart_angle = current_step / len(self.step_sequence)
#                 self.position += dart_angle

#     def movearoundtheworld(self):
#         while not self.dart_detected1:
#             print(f"{self.dart_detected1} - Searching for dart")
#             waardestapmotor = DataRepository.gethistoriek("stapmotor")
#             while waardestapmotor["waarde"] > 1:
#                 if self.dart_detected1:
#                     break
#                 self.oneturn("tegenkloksgewijs")
#                 waardestapmotor = DataRepository.gethistoriek("stapmotor")
#             while waardestapmotor["waarde"] < 20:
#                 if self.dart_detected1:
#                     break
#                 self.oneturn("kloksgewijs")
#                 waardestapmotor = DataRepository.gethistoriek("stapmotor")
#         return "dartdetected"

#     def oneturn(self, direction):
#         self.move_motor(direction, 515)
#         time.sleep(0.1)
#         laatstewaardestapmotor = DataRepository.gethistoriek("stapmotor")

#         if laatstewaardestapmotor["waarde"] == 20:
#             direction = "tegenkloksgewijs"
#         elif laatstewaardestapmotor["waarde"] == 1:
#             direction = "kloksgewijs"

#         if direction == "kloksgewijs":
#             waardestapmotor = laatstewaardestapmotor["waarde"] + 1
#         else:
#             waardestapmotor = laatstewaardestapmotor["waarde"] - 1
        
#         DataRepository.create_historiek("stapmotor", "stepmotorposition", waardestapmotor, f"stapmotor 1 naar {'rechts' if direction == 'kloksgewijs' else 'links'}")
#         self.position = waardestapmotor

#     def setstepmotorstart(self):
#         print("Calibrating stepper motor...")
#         while DataRepository.gethistoriek("stapmotor")["waarde"] > 10:
#             self.oneturn("tegenkloksgewijs")
#         while DataRepository.gethistoriek("stapmotor")["waarde"] < 10:
#             self.oneturn("kloksgewijs")
#         if DataRepository.gethistoriek("stapmotor")["waarde"] == 10:
#             response = DataRepository.create_historiek("stapmotor", "calibrate", 10, "stapmotor gecalibreerd")
#             print(response)

#     # Game logic
#     def startgame(self, data):
#         self.setstepmotorstart()
#         usergamemode = data["usergamemode"]
#         user1name = data["user1name"]
#         user2name = data.get("user2name")
#         gamemode = data["gamemode"]
#         finishmode = data["finishmode"]
    
#         if usergamemode == "single":
#             usermode = 1
#         elif usergamemode == "teams":
#             usermode = 2 
#         else:
#             usermode = 3  # bot

#         if gamemode == 301 and finishmode == "singleout":
#             game_mode = 0
#         elif gamemode == 301 and finishmode == "doubleout":
#             game_mode = 1
#         elif gamemode == 501 and finishmode == "singleout":
#             game_mode = 2
#         elif gamemode == 501 and finishmode == "doubleout":
#             game_mode = 3
#         else:
#             raise ValueError("Invalid game mode or finish mode")

#         gameid = DataRepository.create_game(usermode, game_mode)
#         print(f"{gameid} - Game ID created")

#         user1_id = DataRepository.read_user_by_username(user1name)
#         user1_game_stats_id = DataRepository.create_usergamestats(user1_id["IDuser"], gameid)
#         self.usergamestatsidplayer1 = user1_game_stats_id

#         if user2name:
#             user2_id = DataRepository.read_user_by_username(user2name)
#             user2_game_stats_id = DataRepository.create_usergamestats(user2_id["IDuser"], gameid)
#             self.usergamestatsidplayer2 = user2_game_stats_id
#             self.amountofplayers = 2
#         else:
#             user2_game_stats_id = None
#             self.amountofplayers = 1

#         result = {
#             "gameid": gameid,
#             "user1_game_stats_id": user1_game_stats_id,
#             "user2_game_stats_id": user2_game_stats_id
#         }
#         self.importantinfogame = result
#         return result

#     def livegame(self,response):
#         while self.gamefinished == False:
#             self.dart_detected1 = False
#             response = "nodartdetected"
#             time.sleep(3)
#             response = self.movearoundtheworld()
#             if response == "dartdetected":
#                 print("Dart detected! Converting position to score and updating database.")
#                 waardeworp = self.changepositionintonumber(self.position)
#                 print(waardeworp)

#                 if self.userlive == 1:
#                     DataRepository.create_worp(self.usergamestatsidplayer1,waardeworp)
#                     self.amountofthrows += 1
#                 else:
#                     DataRepository.create_worp(self.usergamestatsidplayer2,waardeworp)
#                     self.amountofthrows += 1
#                 if self.amountofthrows == 3:
#                     self.amountofthrows = 0
#                     if (self.amountofplayers == 2):
#                         self.userlive != self.userlive


#     def changepositionintonumber(self, position):
#         listpositions = [3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6, 10, 15, 2, 17]
#         waardeworp = listpositions[position - 1]
#         return waardeworp


#     def algorithm(self):
#         data_solo = {
#             "usergamemode": "single",
#             "user1name": "johndoe",
#             "gamemode": 301,
#             "finishmode": "singleout"
#         }

#         result_1v1 = self.startgame(data_solo)
#         print(result_1v1)
#         self.livegame("nodartdetected")
        
                



# if __name__ == "__main__":
#     # GPIO.cleanup()
#     # Example usage
#     try:
#         controller = DartboardController(laser=12, sensor1=20, sensor2=21, steps=520, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22)
#         controller.start()
#         controller.algorithm()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         GPIO.cleanup()














# *************************************************************V1**********************************************************

# import time
# import datetime
# from datetime import datetime
# import RPi.GPIO as GPIO
# from klasses.knop import knopke
# from repositories.DataRepository import DataRepository

# class DartboardController:
#     def __init__(self, laser, sensor1, sensor2, steps, stepmotorA, stepmotorB, stepmotorC, stepmotorD):
#         self.laser = laser
#         self.sensor1 = knopke(pin=sensor1)
#         # self.sensor2 = knopke(pin=sensor2)
#         self.position = 10  # Start at the middle position
#         self.place = ""
#         self.stepforward = False
#         self.stepbackward = False
#         self.dart_detected1 = False
#         # self.dart_detected2 = False
#         # self.dart_detected2_opposite = False
#         self.steps = steps  # Number of steps to rotate gear 1 time
#         self.step_sequence = [
#             [1, 0, 0, 0],
#             [1, 1, 0, 0],
#             [0, 1, 0, 0],
#             [0, 1, 1, 0],
#             [0, 0, 1, 0],
#             [0, 0, 1, 1],
#             [0, 0, 0, 1],
#             [1, 0, 0, 1]
#         ]
#         self.stepmotorA = stepmotorA
#         self.stepmotorB = stepmotorB
#         self.stepmotorC = stepmotorC
#         self.stepmotorD = stepmotorD

#         self.amountofplayers = 1
#         self.usergamestatsidplayer1 = 1
#         self.usergamestatsidplayer2 = 2
#         self.importantinfogame =  {"gameid": 0,"user1_game_stats_id": 0, "user2_game_stats_id": 0}
#         self.userlive = 1
#         self.amountofthrows = 0
#         # Initialize GPIO
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.laser, GPIO.OUT)
#         GPIO.setup(self.stepmotorA, GPIO.OUT)
#         GPIO.setup(self.stepmotorB, GPIO.OUT)
#         GPIO.setup(self.stepmotorC, GPIO.OUT)
#         GPIO.setup(self.stepmotorD, GPIO.OUT)
#         GPIO.setup(sensor1, GPIO.IN)
#         # GPIO.setup(sensor2, GPIO.IN)
#         # GPIO.setup(sensor3, GPIO.IN)
#         GPIO.output(self.laser, 1)




# # ****************************************************CALLBACKS*********************************************
#     def laserin1_callback(self, channel):
#         self.dart_detected1 = True
#         DataRepository.create_historiek("lasersensor1","log_data",1,"dartgezienlasersensor1")
#         print("Laser 1 detected!")

#     # def laserin2_callback(self, channel):
#     #     self.dart_detected2 = True
#     #     print("Laser 2 detected the dart!")

#     # def laserin3_callback(self, channel):
#     #     self.dart_detected3 = True
#     #     print("Laser 3 detected!")

#     def start(self):
#         GPIO.add_event_detect(self.sensor1.pin, GPIO.RISING, callback=self.laserin1_callback)
#         # GPIO.add_event_detect(self.sensor2.pin, GPIO.RISING, callback=self.laserin2_callback)
#         # GPIO.add_event_detect(self.sensor3.pin, GPIO.RISING, callback=self.laserin3_callback)









# # ******************************************************MOTORSTUFF**********************************************
#     def move_motor(self, direction, steps):
#         current_step = 0
#         for _ in range(steps):
#             # time.sleep(0.1)
            
#             if self.dart_detected1:
#                 print("Stopping stepper motor as dart is detected!")
#                 self.dart_detected1 = True
#                 break
            
#             if direction == "kloksgewijs":
#                 step_sequence = self.step_sequence 
#             else:
#                 step_sequence = reversed(self.step_sequence)
            
#             for step in step_sequence:
#                 GPIO.output(self.stepmotorA, step[3])
#                 GPIO.output(self.stepmotorB, step[2])
#                 GPIO.output(self.stepmotorC, step[1])
#                 GPIO.output(self.stepmotorD, step[0])
#                 # print(f"Step: {current_step}, Pins: {step}")
#                 current_step = (current_step + 1) % 8
#                 time.sleep(0.001)  # Delay in seconds
#                 dart_angle = current_step / len(self.step_sequence)
#                 self.position += dart_angle

#                 # if self.position >= 20:
#                 #     print("Stopping stepper motor as position is blocked")
#                 #     break


#     def movearoundtheworld(self):
#         while self.dart_detected1 == False:
#             print(str(self.dart_detected1) + "dit is de status van mijn dartdetected")
#             print("searching for dart")
#             waardestapmotor = DataRepository.gethistoriek("stapmotor")
#             while waardestapmotor["waarde"] > 1:
#                 print(str(self.dart_detected1) + "dit is de breakbinnenwhile")
#                 if self.dart_detected1 == True:
#                     break
#                 else:
#                     self.oneturn("tegenkloksgewijs")
#                     waardestapmotor = DataRepository.gethistoriek("stapmotor")
#                     # print(waardestapmotor["waarde"])
#             while waardestapmotor["waarde"] < 20:
#                 print(str(self.dart_detected1) + "dit is de breakbinnenwhile2000")
#                 if self.dart_detected1 == True:
#                     break
#                 else:
#                     self.oneturn("kloksgewijs")
#                     # print(waardestapmotor["waarde"])

#         return "dartdetected"


#     def oneturn(self,direction):
#         self.move_motor(direction,515)
#         time.sleep(0.1)
#         laatstewaardestapmotor = DataRepository.gethistoriek("stapmotor")

#         print(laatstewaardestapmotor)

#         if laatstewaardestapmotor["waarde"] == 20:
#             direction = "tegenkloksgewijs"
#         if laatstewaardestapmotor["waarde"] == 1:
#             direction = "kloksgewijs"

#         if direction == "kloksgewijs":
#             # print("kloksgewijs")
#             # send data to database forward:
#             waardestapmotor = laatstewaardestapmotor["waarde"] + 1
#             # print(waardestapmotor)
#             # print(str(waardestapmotor) + "nieuwe waarde stapmotor")
#             response = DataRepository.create_historiek("stapmotor","stepmotorposition",waardestapmotor,"stappenmotor 1 naar rechts")
#             print(response)
#         else:
#             # send data to database backward:
#             waardestapmotor = laatstewaardestapmotor["waarde"] - 1
#             DataRepository.create_historiek("stapmotor","stepmotorposition",waardestapmotor,"stappenmotor 1 naar links")
#         self.position = waardestapmotor

#     def setstepmotorstart(self):
#         print("stappenmotor goedzetten")
#         while (DataRepository.gethistoriek("stapmotor")["waarde"]) > 10:
#             self.oneturn("tegenkloksgewijs")
#         while (DataRepository.gethistoriek("stapmotor")["waarde"]) < 10:
#             self.oneturn("kloksgewijs")
#         if(DataRepository.gethistoriek("stapmotor")["waarde"] == 10):
#             print(DataRepository.gethistoriek("stapmotor")["waarde"])
#             response = DataRepository.create_historiek("stapmotor","calibrate",10,"stapmotor gecalibreerd")



# # *********************************************************GAME******************************************************

#     def startgame(self, data):
#         self.setstepmotorstart()
#         # Extract values from the data dictionary
#         usergamemode = data["usergamemode"]
#         user1name = data["user1name"]
#         user2name = data.get("user2name")  # Use .get() to handle the possibility of solo mode
#         gamemode = data["gamemode"]
#         finishmode = data["finishmode"]
    
           

#         # Determine the values for usermode and gamemode to be passed to create_game
#         if usergamemode == "single":
#             usermode = 1
#         elif usergamemode == "teams":
#             usermode = 2 
#         else:
#             usermode = 3 # bot

#         if gamemode == 301 and finishmode == "singleout":
#             game_mode = 0
#         elif gamemode == 301 and finishmode == "doubleout":
#             game_mode = 1
#         elif gamemode == 501 and finishmode == "singleout":
#             game_mode = 2  # Add appropriate game mode mapping
#         elif gamemode == 501 and finishmode == "doubleout":
#             game_mode = 3  # Add appropriate game mode mapping
#         else:
#             raise ValueError("Invalid game mode or finish mode")

#         # Create the game
#         gameid = DataRepository.create_game(usermode, game_mode)
#         print(str(gameid), "dit is het gameid")

#         # Get user ID by username for the first user and create usergamestats
#         user1_id = DataRepository.read_user_by_username(user1name)
#         print(str(user1_id), "tis is het id van user 1")
#         user1_game_stats_id = DataRepository.create_usergamestats(user1_id["IDuser"], gameid)
#         self.usergamestatsidplayer1 = user1_game_stats_id
   

#         # If a second user is provided, get their ID and create their game stats
#         if user2name:
#             user2_id = DataRepository.read_user_by_username(user2name)
#             user2_game_stats_id = DataRepository.create_usergamestats(user2_id["IDuser"], gameid)
#             self.usergameidplayer2 = user2_game_stats_id
#             self.amountofplayers = 2
#         else:
#             user2_game_stats_id = None
#             self.usergameidplayer2 = None
#             self.amountofplayers = 1

#         # Return result, which includes the game ID and the IDs of the user game stats
#         result = {
#             "gameid": gameid,
#             "user1_game_stats_id": user1_game_stats_id,
#             "user2_game_stats_id": user2_game_stats_id
#         }
#         self.importantinfogame = result
#         return result


#     def changepositionintonumber(self,position): #might have to add ring aswell which will just do *2 or *3
#         listpositions = [3,19,7,16,8,11,14,9,12,5,20,1,18,4,13,6,10,15,2,17] 
#         waardeworp = listpositions[position - 1] #hier -1 omdat mijn stappenmotor 1-20 doet en de list hier 0-19 is
#         return waardeworp


#     def algorithm(self): #voorlopig de start voor alles aan te sturen(speelt de website)
#         data_solo = {
#             "usergamemode": "single",
#             "user1name": "johndoe",
#             "gamemode": 301,
#             "finishmode": "singleout"
#         }

#         result_1v1 = controller.startgame(data_solo)
#         print(result_1v1)
#         response = self.movearoundtheworld()
#         if response == "dartdetected":
#             print("er is een dart gedecteerd ik zal nu de waarde omvormen en in de db steken")
#             waardeworp = self.changepositionintonumber(self.position)
#             print(str(waardeworp) + "  waardeworp")
#             if self.userlive == 1:
#                 DataRepository.create_worp(result_1v1["user1_game_stats_id"],waardeworp)
#                 self.amountofthrows += 1
#                 if self.amountofthrows == 3:
#                     self.userlive = 2
#                     self.amountofthrows = 0
#             if self.userlive == 2:
#                 DataRepository.create_worp(result_1v1["user2_game_stats_id"],waardeworp)
#                 if self.amountofthrows == 3:
#                     self.userlive = 2
#                     self.amountofthrows = 0  



# if __name__ == "__main__":
#     # GPIO.cleanup()
#     # Example usage
#     try:
#         controller = DartboardController(laser=12, sensor1=20, sensor2=21, steps=520, stepmotorA=4, stepmotorB=17, stepmotorC=27, stepmotorD=22)
#         controller.start()
#         controller.algorithm()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         GPIO.cleanup()