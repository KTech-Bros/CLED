import redis, psycopg2, ast, re
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DBWorker:
    def __init__(self, redis_connection_string, pg_connection_string):

        # Redis connecting string parse
        if type(redis_connection_string) != type(None):
            redis_dict = "{'"+redis_connection_string+"'}"
            redis_dict = redis_dict.replace(" ","")
            redis_dict = redis_dict.replace("=","':'")
            redis_dict = redis_dict.replace(";","','")
            redis_dict = ast.literal_eval(redis_dict)

            # Redis data init 
        
            if redis_dict["host"] == "":
                self.redis_host="127.0.0.1"
            else:
                self.redis_host=redis_dict["host"]

            if redis_dict["db"] == "":
                self.redis_db="0"
            else:
                self.redis_db=redis_dict["db"]

            if redis_dict["port"] == "":
                self.redis_port="0"
            else:
                self.redis_port=redis_dict["port"]

            if redis_dict["password"] == "":
                self.redis_password=""
            else:
                self.redis_password=redis_dict["password"]

        else:
            self.redis_host="127.0.0.1"
            self.redis_db="0"
            self.redis_port="0"
            self.redis_password=""
        
        self.redis_connection_string = redis_connection_string

        # Postgres connecting string parse

        if type(pg_connection_string) != type(None):

            postgres_dict = "{'"+pg_connection_string+"'}"
            postgres_dict = postgres_dict.replace(" ","")
            postgres_dict = postgres_dict.replace("=","':'")
            postgres_dict = postgres_dict.replace(";","','")
            postgres_dict = ast.literal_eval(postgres_dict)

            # Postgres data init 
        
            if postgres_dict["Port"] == "":
                self.postgres_port=5432
            else:
                self.postgres_port=int(postgres_dict["Port"])

            if postgres_dict["Database"] == "":
                self.postgres_database=""
            else:
                self.postgres_database=postgres_dict["Database"]

            if postgres_dict["Password"] == "":
                self.postgres_password=""
            else:
                self.postgres_password=postgres_dict["Password"]

            if postgres_dict["UserID"] == "":
                self.postgres_user=""
            else:
                self.postgres_user=postgres_dict["UserID"]

            if postgres_dict["Host"] == "":
                self.postgres_host="127.0.0.1"
            else:
                self.postgres_host=postgres_dict["Host"]

        else:

            self.postgres_port=5432
            self.postgres_database=""
            self.postgres_password=""
            self.postgres_user=""
            self.postgres_host="127.0.0.1"

        self.pg_connection_string = pg_connection_string
    
    def ping_redis(self):
        try:
            r = redis.Redis(
                host=self.redis_host,
                port=self.redis_port, 
                password=self.redis_password,
                db=self.redis_db)

            return r.ping() 
        except Exception as e:
            return False
    
    def ping_postgre(self):
        try:
            connection = psycopg2.connect(user=self.postgres_user,
                                    password=self.postgres_password,
                                    host=self.postgres_host,
                                    port=self.postgres_port)
            cursor = connection.cursor()
            postgreSQL_select_Query = "select 1"

            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()

            ansver = mobile_records[0][0]

            if ansver == 1:
                return True

            connection.close()
        
        except Exception as e:
            return False

    def create_database(self, name):
        try:
            connection = psycopg2.connect(user=self.postgres_user,
                                    password=self.postgres_password,
                                    host=self.postgres_host,
                                    port=self.postgres_port)

            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 

            cursor = connection.cursor()
            postgreSQL_select_Query = "SELECT datname FROM pg_database"

            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()
            cursor.close()

            name = name.lower()

            regex = "(^"+name+"_\d+$)|(^"+name+"$)"

            bd_name_counter = 0 
            for i in mobile_records:

                

                if bool(re.search(regex, i[0].lower())):
                    bd_name_counter += 1

            if bd_name_counter == 0:
                db_name = name
            else:
                db_name = name+"_"+str(bd_name_counter)
            
            postgreSQL_select_Query = "CREATE DATABASE "+ db_name

            cursor2 = connection.cursor()
            cursor2.execute(postgreSQL_select_Query)
            cursor2.close()
            return True, db_name
        
        except Exception as e:
            return False

    def get_restore_command(self, file_path, name):
        command = 'pg_restore -d postgresql://{0}:{1}@{2}:{3}/{4} -v '.format(self.postgres_user,self.postgres_password,self.postgres_host,self.postgres_port,name)
        command = command + file_path
        return command