from .Database import Database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    # **********************************************GAME******************************************************

    @staticmethod
    def create_game(usermode, gamemode):
        """
        Creates a new game with the specified user mode and game mode.
        """
        sql = "INSERT INTO game (usermode, gamemode) VALUES (%s, %s)"
        params = [usermode, gamemode]
        return Database.execute_sql(sql, params)

    # ****************************************************USERS*****************************************************

    @staticmethod
    def read_user_by_username(username):
        """
        Retrieves a user by their username.
        """
        sql = "SELECT IDuser from user WHERE username = %s"
        params = [username]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def read_everything_user_by_username(username):
        """
        Retrieves a user by their username.
        """
        sql = "SELECT * from user WHERE username = %s"
        params = [username]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_all_users():
        """
        Retrieves all users.
        """
        sql = "SELECT * from user"
        return Database.get_rows(sql)
    
    @staticmethod
    def create_user(name, surname, age, length, username, country): 
        """
        Creates a new user with the specified details.
        """
        # Convert age and length to integers if they are not None
        intage = 0
        intlength = 0
        if age != "":
            intage = int(age)
        if length != "":
            intlength = int(age)
        # if isinstance(age, str) and age:
        #     intage = int(age)
        # else:
        #     intage = None

        # if isinstance(length, str) and length:
        #     intlength = int(length)
        # else:
        #     intlength = None

        
        sql = "INSERT INTO user (name, surname, age, length, username, country) VALUES (%s, %s, %s, %s, %s, %s)"
        params = [name, surname, intage, intlength, username, country]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_user_by_id(id, name, surname, age, length, username, country):
        """
        Updates the user with the specified ID.
        """
        sql = "UPDATE user SET name = %s, surname = %s, age = %s, length = %s, username = %s, country = %s WHERE IDuser = %s"
        params = [name, surname, age, length, username, country, id]
        return Database.execute_sql(sql, params)

    
    @staticmethod
    def delete_user_by_username(id):
        """
        Deletes the user with the specified ID.
        """
        sql = "DELETE FROM user WHERE username = %s"
        params = [id]
        return Database.execute_sql(sql, params)
 

    # *****************************************************WORPEN****************************************************
    @staticmethod
    def create_worp(usergameID, waarde):
        """
        Creates a new worp (throw) with the specified user game ID, value, and date.
        """
        sql = "INSERT INTO worpen (usergameID, waarde, date) VALUES (%s, %s, now())"
        params = [usergameID, waarde]
        return Database.execute_sql(sql, params)

    # @staticmethod
    # def read_all_worpen():
    #     """
    #     Retrieves all worpen (throws).
    #     """
    #     sql = "SELECT worpID, waarde, year(date) from worpen"
    #     return Database.get_rows(sql)
    @staticmethod
    def read_daily_highest_score(username=""):
        print("in the dailyhighest score " + username)
        """
        Retrieves the daily highest score (last 7 days) for all users worldwide or for the specified user.
        """
        if username:
            sql = """
                SELECT MAX(waarde) AS daily_highest_score, DATE_FORMAT(date, '%d-%m-%y') as date
                FROM worpen
                JOIN usergamestats ON worpen.usergameID = usergamestats.IDusergamestats
                JOIN user ON usergamestats.IDuser = user.IDuser
                WHERE user.username = %s
                AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                GROUP BY DATE(date);
            """
            params = [username]
        else:
            sql = """
                SELECT MAX(waarde) AS daily_highest_score, DATE_FORMAT(date, '%d-%m-%y') as date
                FROM worpen
                WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                GROUP BY DATE(date);
            """
            params = None
        return Database.get_rows(sql, params)

    @staticmethod
    def read_weekly_highest_score(username=""):
        """
        Retrieves the weekly highest score (last 4 weeks) for all users worldwide or for the specified user.
        """
        if username:
            sql = """
                SELECT MAX(waarde) AS weekly_highest_score, YEARWEEK(date) AS week_of_year
                FROM worpen
                JOIN usergamestats ON worpen.usergameID = usergamestats.IDusergamestats
                JOIN user ON usergamestats.IDuser = user.IDuser
                WHERE user.username = %s
                AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 4 WEEK)
                GROUP BY WEEK(date);
            """
            params = [username]
        else:
            sql = """
                SELECT MAX(waarde) AS weekly_highest_score, YEARWEEK(date) AS week_of_year
                FROM worpen
                WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 4 WEEK)
                GROUP BY WEEK(date);
            """
            params = None
        return Database.get_rows(sql, params)



    @staticmethod
    def read_worpen_by_usergameID(id):
        """
        Retrieves worpen (throws) by the specified user game ID.
        """
        sql = "SELECT * from worpen WHERE usergameID = %s"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_worpen_by_date(date):
        """
        Retrieves worpen (throws) by the specified date.
        """
        sql = "SELECT * from worpen WHERE date = %s"
        params = [date]
        return Database.get_rows(sql, params)

    # *******************************************************USERGAMESTATS**************************************************
    @staticmethod
    def create_usergamestats(iduser, idgame):
        """
        Creates a new user game stats record with the specified user ID and game ID.
        """
        sql = "INSERT INTO usergamestats (iduser, idgame) VALUES (%s, %s)"
        params = [iduser, idgame]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_usergamestats_stopped(idusergamestats, triple20s = 0, twenties = 0, doubles = 0, boules = 0, ninedarters = 0):
        """
        Updates the user game stats with the specified values and sets the game as stopped.
        """
        sql = """
        UPDATE usergamestats
        SET Triple20s = %s, 20s = %s, doubles = %s, boules = %s, 9darters = %s, gamestopped = %s
        WHERE IDusergamestats = %s
        """
        params = [triple20s, twenties, doubles, boules, ninedarters, 1, idusergamestats]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_all_usergamestats():
        """
        Retrieves all user game stats.
        """
        sql = "SELECT * from usergamestats"
        return Database.get_rows(sql)

    @staticmethod
    def read_usergamestats_by_date(date):
        """
        Retrieves user game stats by the specified date, joining with worpen (throws).
        """
        sql = """
        SELECT ug.*, w.*
        FROM usergamestats ug
        JOIN worpen w ON ug.IDusergamestats = w.usergameID
        WHERE w.date = %s
        """
        params = [date]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_usergamestats_by_user(iduser):
        """
        Retrieves user game stats by the specified user ID.
        """
        sql = """
        SELECT ug.*
        FROM usergamestats ug
        JOIN user u ON ug.IDuser = u.IDuser
        WHERE u.id = %s
        """
        params = [iduser]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_games_boules_by_userid(id):
        sql = "select count(*) AS games, count(boules) as boules from usergamestats where IDuser = %s"
        params = [id]
        return Database.get_one_row(sql,params)

    @staticmethod
    def read_usergamestats_by_gamemode(gamemode):
        """
        Retrieves user game stats by the specified game mode.
        """
        sql = """
        SELECT ug.*
        FROM usergamestats ug
        JOIN game g ON ug.IDgame = g.IDgame
        WHERE g.gamemode = %s
        """
        params = [gamemode]
        return Database.get_rows(sql, params)


# ********************************************************HISTORIEK*************************************************
 # Method to get the device ID by device name
    @staticmethod
    def get_device_id_by_name(device_name):
        sql = "SELECT IDdevice FROM device WHERE naam = %s"
        params = [device_name]
        return Database.get_one_row(sql, params)

    # Method to get the action ID by action description
    @staticmethod
    def get_action_id_by_description(action_description):
        sql = "SELECT IDactie FROM actie WHERE actiebeschrijving = %s"
        params = [action_description]
        return Database.get_one_row(sql, params)

    # Method to create a new record in the historiek table
    @staticmethod
    def create_historiek(device_name, action_description, waarde=None, commentaar="geen commentaar"):
        device_id = DataRepository.get_device_id_by_name(device_name)
        # print(str(device_id) + "device_id")
        action_id = DataRepository.get_action_id_by_description(action_description)
        # print(str(action_id) + "action_id")
        sql = "INSERT INTO historiek (IDdevice, IDactie, actiedatum, waarde, commentaar) VALUES (%s, %s,now(), %s, %s)"
        params = [device_id["IDdevice"], action_id["IDactie"], waarde, commentaar]
        # print(params)
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def gethistoriek(devicename):
        deviceid = DataRepository.get_device_id_by_name(devicename)
        # print(str(deviceid) + "deviceid")
        sql = "SELECT waarde FROM historiek WHERE IDdevice = %s order by actiedatum DESC limit 1;"
        params = [deviceid["IDdevice"]] 
        return Database.get_one_row(sql,params)
    

    @staticmethod
    def get_distance_covered():
        # Get the current date
        sql = """
            SELECT COUNT(*) AS record_count
            FROM historiek
            WHERE IDdevice = 4 ;
        """
        result = Database.get_one_row(sql)
        return result



    @staticmethod
    def getalltemperatures():
        sql = "SELECT DATE_FORMAT(actiedatum, '%d-%m-%Y') as date,  HOUR(actiedatum) as hour, AVG(waarde) as avg_temperature  FROM historiek  WHERE IDdevice = 4 AND actiedatum >= NOW() - INTERVAL 7 DAY GROUP BY DATE(actiedatum), HOUR(actiedatum)  ORDER BY DATE(actiedatum) ASC, HOUR(actiedatum) ASC;"
        return Database.get_rows(sql)