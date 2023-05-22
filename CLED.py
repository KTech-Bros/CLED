import dbWorker, zipWorker, consoleWorker, fileModifier, classes
import json, sys, re, os, webbrowser, datetime, ast
        
def main():
    settings = read_settings()
    
    ping_data_base(settings)    

    deploy_zip(settings)

    create_data_base(settings)

    restore_bd(settings)
        
    change_files_parameters(settings)

    print_with_time("Done!")

    if settings.env_settings.startAfterDeployment:
        webbrowser.get('windows-default').open('http://localhost:'+str(settings.env_settings.port), new=2)

        start_creatio(settings)

        

# read settings envSettings.json and appsetting.json
def read_settings():
    print_with_time("Reading settings")
    env_settings_json = open("envSettings.json", "r")
    env_settings = json.loads(env_settings_json.read())

    app_setting_Json = open("appsetting.json", "r")
    app_settings = json.loads(app_setting_Json.read())
    
    return classes.appSettings(app_settings, env_settings)



def ping_data_base(settings: classes.appSettings):
    print_with_time("Testing data bases")

    data_base = dbWorker.DBWorker(settings)

    if data_base.ping_redis() == False:
        print_with_time("Ping Redis Failed")
        sys.exit(0)
    
    if data_base.ping_postgre() == False:
        print_with_time("Ping Postgres Failed")
        sys.exit(0)



def create_data_base(settings: classes.appSettings):

    print_with_time("Creating data bases")

    if settings.env_settings.dbName != "":
        name = settings.env_settings.dbName

    elif settings.env_settings.name != "":
        name = settings.env_settings.name
    
    else:
        name = "Creatio"

    data_base = dbWorker.DBWorker(settings)

    is_db_creation_sucsesful, newname =  data_base.create_database(name)

    if is_db_creation_sucsesful == False:
        print_with_time("Create database failed!")
        sys.exit(0)
    else:
        settings.app_settings.postgres_database = newname

def start_creatio(settings: classes.appSettings):

    folder_name = ""

    if settings.env_settings.name != "":
        folder_name = settings.env_settings.name

    else:
        folder_name = re.findall("([0-9a-zA-Z_.]+).zip",settings.env_settings.binaryPath)[0]

    path = settings.app_settings.creatio_locaton+"\\"+folder_name

    consoleWorker.сonsoleworker.console_out_folder(path, "dotnet Terrasoft.Webhost.dll")


def deploy_zip(settings: classes.appSettings):
    try:
        print_with_time("Copying zip archive")
        zip_file = zipWorker.ZipWorker(settings.env_settings.binaryPath)

        if not zip_file.check_zip_cache():
            zip_file.copy_zip()

        if settings.env_settings.createNewInstance:

            app_folder_name = zip_file.get_new_instance_name(settings)

        else:
            path_to_instance = os.path.join(settings.app_settings.creatio_locaton, app_folder_name)
            
            if os.path.isfile(path_to_instance):

                os.remove(path_to_instance)

        print_with_time("Unpacing zip archive")
        zip_file.unpack_zip(settings.app_settings.creatio_locaton, app_folder_name)
    except Exception as e:
        print_with_time("An error was encountered while working with binary archive, program stoped!")
        sys.exit(0)

def restore_bd(settings: classes.appSettings):
    try:
        print_with_time("Starting restoring DB")

        folder_name = ""

        if settings.env_settings.name != "":
             folder_name = settings.env_settings.name
        else:
             folder_name = re.findall("([0-9a-zA-Z_.]+).zip",settings.env_settings.binaryPath)[0]

        path = settings.app_settings.creatio_locaton+"\\"+ folder_name+"\\db"

        file_name = os.listdir(path)[0]
        
        db = dbWorker.DBWorker(settings)

        if settings.app_settings.postgress_location != "":

            gp_restore_path = find_file(settings.app_settings.postgress_location,"pg_restore.exe")

        else: 

            gp_restore_path = find_file(" C:\\Program Files\\PostgreSQL","pg_restore.exe")

            if gp_restore_path == "":
                        print_with_time("An error was encountered while search pg restore, program stoped!")
                        sys.exit(0)


        restore_command = db.get_restore_command(gp_restore_path, path+"\\"+file_name, settings.app_settings.postgres_database)

        consoleWorker.сonsoleworker.console_out_task(restore_command)

    except Exception as e:
        print_with_time("An error was encountered while restoring Data Bases, program stoped!")
        sys.exit(0)

def find_file(path, name):
    for r,d,f in os.walk(path):
        for files in f:
            if files == name:
                return os.path.join(r,files)


def change_files_parameters(settings: classes.appSettings):

    print_with_time("Starting updating files")

    try:

        if settings.env_settings.name != "":
            name = settings.env_settings.name
        else:
            name = re.findall("([0-9a-zA-Z_.]+).zip",settings.env_settings.binaryPath)[0]

        connection_string_db = settings.app_settings.dbConnectionString

        connection_string_db = connection_string_db + ';Database=' + settings.app_settings.postgres_database

        path = settings.app_settings.creatio_locaton+"\\"+name

        xml_params = []

        xml_params.append(classes.xmlParamiters(file_path="ConnectionStrings.config",
                                            element="name",
                                            element_value="db",
                                            target_element="connectionString",
                                            target_element_value=connection_string_db,
                                            tag_name="add"))
        
        xml_params.append(classes.xmlParamiters(file_path="ConnectionStrings.config",
                                            element="name",
                                            element_value="redis",
                                            target_element="connectionString",
                                            target_element_value=settings.app_settings.redis_connection_string,
                                            tag_name="add"))

        xml_params.append(classes.xmlParamiters(file_path="Terrasoft.WebHost.dll.config",
                                            element="key",
                                            element_value="CookiesSameSiteMode",
                                            target_element="value",
                                            target_element_value="Lax",
                                            tag_name="add"))

        fileModifier.change_xml_files(path, xml_params)

        fileModifier.change_json_param(path+"\\"+"appsettings.json", "Kestrel.Endpoints.Http.Url", "http://::"+str(settings.env_settings.port))

        fileModifier.del_json_param(path+"\\"+"appsettings.json", "Kestrel.Endpoints.Https")

    except Exception as e:
        print_with_time("An error was encountered while updating data in fiels, program stoped!")
        sys.exit(0)

def print_with_time(string):
    now = datetime.datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print(current_time, string)

if __name__ == "__main__":
    main()