import dbworker, zipworker, consoleworker, fileModifier
import json, sys, re, os, webbrowser, datetime

def main():
    app_setting , env_settings = read_settings()
    ping_data_base(app_setting)

    create_data_base(app_setting, env_settings)    

    deploy_zip(env_settings, app_setting["Environments"])

    restore_bd(env_settings, app_setting)
        
    change_files_parameters(env_settings, app_setting)

    print_with_time("Done!")

    if env_settings["StartAfterDeployment"]:
        start_creatio(env_settings, app_setting)

    webbrowser.get('windows-default').open('http://localhost:'+str(env_settings["Port"]), new=2)

# read settings envSettings.json and appsetting.json
def read_settings():
    print_with_time("Reading settings")
    env_settings_json = open("envSettings.json", "r")
    env_settings = json.loads(env_settings_json.read())

    app_setting_Json = open("appsetting.json", "r")
    app_setting = json.loads(app_setting_Json.read())
    return app_setting ,env_settings



def ping_data_base(app_setting):
    print_with_time("Testing data bases")
    data_base_setting = app_setting["DataBase"]
    redis_setting = app_setting["Redis"]

    data_base = dbworker.DBWorker(redis_setting["connectionString"],data_base_setting["connectionString"])

    if data_base.ping_redis() == False:
        print_with_time("Ping Redis Failed")
        sys.exit(0)
    
    if data_base.ping_postgre() == False:
        print_with_time("Ping Postgres Failed")
        sys.exit(0)



def create_data_base(app_setting, env_settings):

    print_with_time("Creating data bases")

    if env_settings["DbName"] != "":
        name = env_settings["DbName"]

    elif env_settings["Name"] != "":
        name = env_settings["Name"]
    
    else:
        name = "Creatio"

    data_base_setting = app_setting["DataBase"]

    data_base = dbworker.DBWorker(None,data_base_setting["connectionString"])

    is_db_sucsesful, newname =  data_base.create_database(name)

    

    if is_db_sucsesful == False:
        print_with_time("Create database failed!")
        sys.exit(0)
    else:
        env_settings["DbName"] = newname

def start_creatio(env_settings, app_setting):

    environments = app_setting["Environments"]

    folder_name = ""

    if env_settings["Name"] != "":
        folder_name = env_settings["Name"]

    else:
        folder_name = re.findall("([0-9a-zA-Z_.]+).zip",env_settings["BinaryPath"])[0]

    path = environments["rootDirectory"]+"\\"+folder_name

    consoleworker.сonsoleworker.console_out_folder(path, "dotnet Terrasoft.Webhost.dll")


def deploy_zip(env_settings,environments):
    try:
        print_with_time("Copying zip archive")
        zip_file = zipworker.ZipWorker(env_settings["BinaryPath"])


        print_with_time("Unpacing zip archive")
        zip_file.unpack_zip(environments["rootDirectory"], env_settings["Name"])
    except Exception as e:
        print_with_time("An error was encountered while working with binary archive, program stoped!")
        sys.exit(0)

def restore_bd(env_settings, app_setting):
    try:
        print_with_time("Starting restoring DB")

        environments = app_setting["Environments"]

        folder_name = ""

        if env_settings["Name"] != "":
             folder_name = env_settings["Name"]
            
        else:
             folder_name = re.findall("([0-9a-zA-Z_.]+).zip",env_settings["BinaryPath"])[0]

        path = environments["rootDirectory"]+"\\"+ folder_name+"\\db"

        file_name = os.listdir(path)[0]

        data_base_setting = app_setting["DataBase"]
        
        db = dbworker.DBWorker(None,data_base_setting["connectionString"])

        restore_command = db.get_restore_command(path+"\\"+file_name, env_settings["DbName"])

        consoleworker.сonsoleworker.console_out_task(restore_command)

    except Exception as e:
        print_with_time("An error was encountered while restoring Data Bases, program stoped!")
        sys.exit(0)

def change_files_parameters(env_settings, app_setting):

    print_with_time("Starting updating files")

    try:

        environments = app_setting["Environments"]

        if env_settings["Name"] == "":
            name = re.findall("([0-9a-zA-Z_.]+).zip",env_settings["BinaryPath"])[0]
        else:
            name = env_settings["Name"]

        connection_string_db = app_setting["DataBase"]

        connection_string_redis = app_setting["Redis"]

        path = environments["rootDirectory"]+"\\"+name

        raw_connection_string = connection_string_db["connectionString"]
        
        db_name = re.findall("Database=(.+);User",raw_connection_string)[0]

        corect_connection_string = raw_connection_string.replace(db_name, env_settings["DbName"])
    

        xml_params = [{"file_name": "ConnectionStrings.config" ,"element": "name", "element_value": "db", "target_element": "connectionString", "target_element_value": corect_connection_string, "tag_name":"add"},
        {"file_name": "ConnectionStrings.config","element": "name", "element_value": "redis", "target_element": "connectionString", "target_element_value": connection_string_redis["connectionString"], "tag_name":"add"},
        {"file_name": "Terrasoft.WebHost.dll.config", "element": "key", "element_value": "CookiesSameSiteMode", "target_element": "value", "target_element_value": "Lax", "tag_name":"add"}]

        fileModifier.change_xml_files(path, xml_params)

        fileModifier.change_json_param(path+"\\"+"appsettings.json", "Kestrel.Endpoints.Http.Url", "http://::"+str(env_settings["Port"]))

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