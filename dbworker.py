import classes
import redis, psycopg2, re
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DBWorker:
    def __init__(self, settings: classes.appSettings):

        # Redis connecting string parse
        if settings.app_settings.redis_connection_string != None:
            
            self.redis_host=settings.app_settings.redis_host
            self.redis_db=settings.app_settings.redis_db
            self.redis_port=settings.app_settings.redis_port
            self.redis_password=settings.app_settings.redis_password

        else:
            self.redis_host="127.0.0.1"
            self.redis_db="0"
            self.redis_port="0"
            self.redis_password=""
        
        self.redis_connection_string = settings.app_settings.redis_connection_string

        # Postgres connecting string parse

        if settings.app_settings.dbConnectionString != None:

            self.postgres_port=settings.app_settings.postgres_port
            self.postgres_password=settings.app_settings.postgres_password
            self.postgres_user=settings.app_settings.postgres_user
            self.postgres_host=settings.app_settings.postgres_host
            
        else:

            self.postgres_port=5432
            self.postgres_password=""
            self.postgres_user=""
            self.postgres_host="127.0.0.1"

        
        self.postgres_database="postgres"
        self.pg_connection_string = settings.app_settings.dbConnectionString
    
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
                                    dbname=self.postgres_database,
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
                                    dbname=self.postgres_database,
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
            return False, ""

    def get_restore_command(self, restore_path, file_path, name):
        command = '"'+restore_path+'" -d postgresql://{0}:{1}@{2}:{3}/{4} -v '.format(self.postgres_user,self.postgres_password,self.postgres_host,self.postgres_port,name)
        command = command + '"' + file_path + '"'
        return command