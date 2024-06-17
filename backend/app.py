import threading
import time
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from RPi import GPIO
from repositories.DataRepository import DataRepository
# from klasses.knop import knopke
# from klasses.displayaansturenPCF import displayi2c
# from klasses.MCP import Mcp
# from klasses.MPU650class import MPU6050
# from klasses.rotaryencoder import GPIOHandler
from subprocess import check_output
from Dartboardcontroller import DartboardController
from sensorcontroller import SensorController
from klasses.knop import knopke
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HELLOTHISISSECRET'

# ping interval forces rapid B2F communication
socketio = SocketIO(app, cors_allowed_origins="*",
                    async_mode='gevent', ping_interval=0.5)
CORS(app)

# *************************************SETUP**************************************************
# RSpin = 23
# enablepin = 24
laserlights = 12
laserin2 = 20
laserin3 = 21

stepsonegear = 510
stepmotorA = 4
stepmotorB = 17
stepmotorC = 27
stepmotorD = 22

buttonlcdrotary = 13
rotaryleft = 19
rotaryright = 26
buttonpower = 6
busmcp = 0
devicemcp = 0
mpuadress = 0x68

dc = None

def setup():
    # GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttonlcdrotary, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(buttonpower, GPIO.IN, pull_up_down=GPIO.PUD_UP)








# *************************************FUNCTIES************************************

def cleanup():
    GPIO.cleanup()




# ********************************************THREADING***************************************************

def start_all_threads():
    # threading.Thread(target=dartboard_thread, daemon=True).start()
    global dc
    dc = DartboardController(socketio, laserlights, laserin2, laserin3, stepsonegear, stepmotorA, stepmotorB, stepmotorC, stepmotorD)
    # dc.algorithm()
    print("thread dartboard started")
    threading.Thread(target=sensor_thread, daemon=True).start()
    print("thread sensors started")


def sensor_thread():
    time.sleep(5)
    print("starting thread sensors")
    sc = SensorController(socketio,busmcp, devicemcp, buttonlcdrotary, rotaryleft, rotaryright, 1, mpuadress)
    sc.run()

# *****************************************************API ROUTES*************************************************

endpoint = "/api/v1"

@app.route('/')
def home():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route(endpoint + '/users/', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        users = DataRepository.read_all_users()
        print("getting users from database")
        return jsonify(users), 200
    elif request.method == 'POST':
        print("creating user")
        data = DataRepository.json_or_formdata(request)
        print(data)
        result = DataRepository.create_user(**data)
        return jsonify(result), 201
    
@app.route(endpoint + '/users/<id>/', methods=['PATCH'])
def manage_users_by_id(id):
    if request.method == 'PATCH':
        data = DataRepository.json_or_formdata(request)
        result = DataRepository.update_user_by_id(id,**data)
        print("updating user")
        return jsonify(result), 200



@app.route(endpoint + '/users/<username>/', methods=['GET',"DELETE"])
def get_user(username):
    if request.method == "GET":
        user = DataRepository.read_everything_user_by_username(username)
        return jsonify(user), 200
    elif request.method == "DELETE":
        result = DataRepository.delete_user_by_username(username)
        print("deleting user" + str(result))
        return jsonify(result),200




@app.route(endpoint + '/games/', methods=['POST'])
def create_game():
    print("in the create game route")
    global dc
    data = DataRepository.json_or_formdata(request)
    # print("data: " + request)
    result = dc.startgame(data)
    return jsonify(result), 2

@app.route(endpoint + '/stop/', methods=['POST'])
def stop_game():
    print("in the stop game route")

    result = dc.stopgame()
    return jsonify(result), 20

@app.route(endpoint + '/throws/', methods=['GET'])
def read_throws_worldwide():
    if request.method == 'GET':
        print("readthrowsworldwide")
        throws_daily = DataRepository.read_daily_highest_score()
        throws_weekly = DataRepository.read_weekly_highest_score()
        return jsonify(daily = throws_daily, weekly = throws_weekly), 200

@app.route(endpoint + '/throws/<username>/', methods=['GET'])
def read_throws_user(username):
    if request.method == 'GET':
        print("readthrowsuser")
        # userid = DataRepository.read_user_by_username(username)
        throws_daily = DataRepository.read_daily_highest_score(username)
        print(throws_daily)
        throws_weekly = DataRepository.read_weekly_highest_score(username)
        return jsonify(daily = throws_daily, weekly = throws_weekly), 200

@app.route(endpoint + '/throws/<int:id>/', methods=['GET'])
def get_throws_by_game_id(id):
    throws = DataRepository.read_worpen_by_usergameID(id)
    return jsonify(throws), 200

@app.route(endpoint + '/usergamestats/', methods=['GET', 'POST'])
def manage_usergamestats():
    if request.method == 'GET':
        stats = DataRepository.read_all_usergamestats()
        return jsonify(stats), 200
    # elif request.method == 'POST': ook geen route voor website
    #     data = request.json_or_formdata(request)
    #     result = DataRepository.create_usergamestats(data['iduser'], data['idgame'])
    #     return jsonify(result), 201

@app.route(endpoint + '/historiek/', methods=['POST'])
def create_historiek():
    data = request.json_or_formdata(request)
    result = DataRepository.create_historiek(**data)
    return jsonify(result), 201

# @app.route(endpoint + '/temperatuur/', methods=['GET'])
# def get_temperatuur():
#     temps = DataRepository.getalltemperatures()
#     return jsonify(temps), 200
@app.route(endpoint + '/distance/', methods=['GET'])
def read_distance_stepmotor():
    result = DataRepository.get_distance_covered()
    return jsonify(result), 201

@app.route(endpoint + "/gamesboules/<id>/",methods=["GET"])
def read_gamesboules(id):
    result = DataRepository.read_games_boules_by_userid(id)
    print("dit is het result readgamesboules" + str(result))
    return jsonify(result),201

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connected')
    users = DataRepository.read_all_users()
    emit('B2F_namen_users', {'users': users}, broadcast=False)

# @socketio.on('F2B_read_all_worpen')
# def read_all_worpen():
#     print('alle worpen')
#     res = DataRepository.read_all_worpen()
#     print(res)
#     emit('B2F_alle_worpen',  {'worpen': res}, broadcast=False)
#buttonspoweroff
def button_pressedpoweroff():
    # GPIO.setmode(GPIO.BCM)
    print("Button pressed! poweroff")
    cleanup()
    # subprocess.run(["sudo", "poweroff"], check=True)
def button_releasedpoweroff():
    print("shutting off")
    cleanup()
    subprocess.run(["sudo", "poweroff"], check=True)

def start_buttons():
    print("buttonscheck started")
    button = knopke(6)
    # button.on_press(button_pressedpoweroff())
    button.on_release(button_releasedpoweroff())

# Main loop
if __name__ == "__main__":
    try:
        setup()
        start_all_threads()
        print("**** Starting APP ****")
        # start_buttons()

        socketio.run(app, debug=False, host='0.0.0.0')
       
        while True:
            # if received data from website :
            #     data_solo = {
            #         "usergamemode": "single",
            #         "user1name": "johndoe",
            #         "gamemode": 301,
            #         "finishmode": "singleout"
            #     }

            #     DartboardController.startgame(data_solo)
            
            pass
    except Exception as e:
        print("an error occured during startup:" , e) 

    finally:
        cleanup()
