import ast

class app_settings:
    def __init__(self, app_setting):

        dataBase = app_setting["DataBase"] 
        self.dbConnectionString = dataBase["connectionString"]

        postgres_dict = "{'"+self.dbConnectionString+"'}"
        postgres_dict = postgres_dict.replace(" ","")
        postgres_dict = postgres_dict.replace("=","':'")
        postgres_dict = postgres_dict.replace(";","','")
        postgres_dict = ast.literal_eval(postgres_dict)


        if "Port" in postgres_dict:
            self.postgres_port=int(postgres_dict["Port"])
        else:
            self.postgres_port=5432

        if "Database" in postgres_dict:
            self.postgres_database=postgres_dict["Database"]
        else:
            self.postgres_database=""

        if "Password" in postgres_dict:
            self.postgres_password=postgres_dict["Password"]
        else:
            self.postgres_password=""

        if "UserID" in postgres_dict:
            self.postgres_user=postgres_dict["UserID"]
        else:
            self.postgres_user=""

        if "Host" in postgres_dict:
            self.postgres_host=postgres_dict["Host"]
        else:
            self.postgres_host="127.0.0.1"



        redis = app_setting["Redis"]
        self.redis_connection_string = redis["connectionString"]

        redis_dict = "{'"+self.redis_connection_string+"'}"
        redis_dict = redis_dict.replace(" ","")
        redis_dict = redis_dict.replace("=","':'")
        redis_dict = redis_dict.replace(";","','")
        redis_dict = ast.literal_eval(redis_dict)

        if "host" in redis_dict:
            self.redis_host=redis_dict["host"]
        else:
            self.redis_host="127.0.0.1"

        if "db" in redis_dict:
            self.redis_db=redis_dict["db"]
        else:
            self.redis_db="0"

        if "port" in redis_dict:
            self.redis_port=redis_dict["port"]
        else:
            self.redis_port=6379

        if "password" in redis_dict:
            self.redis_password=redis_dict["password"]
        else:
            self.redis_password=""
            

        environments = app_setting["Environments"]
        self.creatio_locaton = environments["rootDirectory"]


        postgres = app_setting["Postgres"]
        self.postgress_location = postgres["rootDirectory"]




class env_settings:
    def __init__(self, env_settings):

        if "Name" in env_settings:
            self.name = env_settings["Name"]
        else:
            self.name = "Creatio"

        if "Port" in env_settings:
            self.port = env_settings["Port"]
        else:
            self.port = 5000

        if "DbName" in env_settings:
            self.dbName = env_settings["DbName"]
        else:
            self.dbName = ""

        if "BinaryPath" in env_settings:
            self.binaryPath = env_settings["BinaryPath"]
        else:
            self.binaryPath = ""

        if "RedisDbNumber" in env_settings:
            self.redisDBNumber = env_settings["RedisDbNumber"]
        else:
            self.redisDBNumber = 0

        if "StartAfterDeployment" in env_settings:
            self.startAfterDeployment = env_settings["StartAfterDeployment"]
        else:
            self.startAfterDeployment = False

        if "CreateNewInstance" in env_settings:
            self.createNewInstance = env_settings["CreateNewInstance"]
        else:
            self.createNewInstance = True




class appSettings:
    def __init__(self,app_setting, env_setting):
        self.app_settings  = app_settings(app_setting)
        self.env_settings = env_settings(env_setting)



class xmlParamiters:
    def __init__(self, file_path ,element, element_value, target_element, target_element_value, tag_name):
        self.file_path = file_path
        self.element = element
        self.element_value = element_value
        self.target_element = target_element
        self.target_element_value = target_element_value
        self.tag_name = tag_name