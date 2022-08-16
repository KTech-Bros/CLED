import zipfile,re,os,urllib.request
import redis, psycopg2
import sys
from subprocess import PIPE,Popen 

# class to work with .zip file
class zipworker:
    def __init__(self, link):
        listoffind = re.findall("([0-9a-zA-Z_.]+.zip)",link)
        self.fileName = listoffind[0]
        self.pathToFile = os.getcwd()
        urllib.request.urlretrieve(link, self.fileName)

    def unPackZip(self):
        with zipfile.ZipFile(self.fileName, 'r') as zipObj:
            zipObj.extractall("folder")

# class to work with Redis and PostgerSQL
class dbworker:
    def __init__(self, pgHostAdres, pgHostPort, pgUserName, pgDataBaseName, pgDataBasePassword, pgBackUpFilePath, redisHostAdres, redisHostPort, redisDataBasepassword):
        self.pgHostAdres = pgHostAdres
        self.pgHostPort = pgHostPort
        self.pgUserName = pgUserName
        self.pgDataBaseName = pgDataBaseName
        self.pgDataBasePassword = pgDataBasePassword
        self.pgBackUpFilePath = pgBackUpFilePath
        self.redisHostAdres = redisHostAdres
        self.redisHostPort = redisHostPort
        self.redisDataBasepassword = redisDataBasepassword
    
    def pingRedis(self):

        r = redis.Redis(
            host= self.redisHostAdres,
            port= self.redisHostPort, 
            password=  self.redisDataBasepassword)

        return r.ping() 
    
    def pingPG(self):

        try:
            connection = psycopg2.connect(user=self.pgUserName,
                                    password=self.pgDataBasePassword,
                                    host=self.pgHostAdres,
                                    port=self.pgHostPort)
            cursor = connection.cursor()
            postgreSQL_select_Query = "select 1"

            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()

            one = mobile_records[0][0]
            print(one)

            if one == 1:
                return True
        
        except:
            return False

    def restoreDB(self):
        command = 'pg_restore -d postgresql://{0}:{1}@{2}:{3}/{4} -v '.format(self.pgUserName,self.pgDataBasePassword,self.pgHostAdres,self.pgHostPort,self.pgDataBaseName)
        command = command + self.pgBackUpFilePath
        сonsoleworker.cout(self, command)


# Class to mork with CMD
class сonsoleworker:
    def cout(self, string):
        Popen(string,shell=False,stdin=PIPE,stdout=PIPE,stderr=PIPE)

    def cin(self):
        command_list = sys.argv[:]
        command_list.pop(0)

        return command_list

