import zipfile,re,os,shutil,classes

class ZipWorker:
    def __init__(self, link):
        self.link = link
    
        self.file_name = re.findall("([0-9a-zA-Z_.]+.zip)",link)[0]
        
        self.path_to_exe = os.getcwd()

        self.path_to_folder  = os.path.join( self.path_to_exe ,"cache")

        self.is_folder_exist = os.path.isdir(self.path_to_folder)

        self.is_file_exist = False

        self.path_to_file = os.path.join(self.path_to_exe ,"cache", self.file_name)
        

    def check_zip_cache(self):

        if not self.is_folder_exist:
            return False

        if self.is_file_exist:
            return True
        
        if os.path.isfile(self.path_to_file):
            self.is_file_exist = True
            return True
        
    def get_new_instance_name(self, settings: classes.appSettings):

        location = settings.app_settings.creatio_locaton

        creatio_folder_file = os.listdir(location)

        name = settings.env_settings.name

        i = 0

        while name in creatio_folder_file:

            i += 1

            name = settings.env_settings.name + "_" + str(i)

        return name
    
    def get_new_instance_name(self, settings: classes.appSettings):

        location = settings.app_settings.creatio_locaton

        creatio_folder_file = os.listdir(location)

        name = settings.env_settings.name

        i = 0

        while name in creatio_folder_file:

            i += 1

            name = settings.env_settings.name + "_" + str(i)

        return name

        
    def copy_zip(self):

        if not self.is_folder_exist:
            os.mkdir(self.path_to_file)

        shutil.copyfile(self.link, self.path_to_file)

        self.is_file_exist = True


    def unpack_zip(self, path, name):

        original_path = os.path.dirname(os.path.abspath(__file__))

        if name == "":
            folder_name = self.file_name[0:-4]
        else:
            folder_name = name

        with zipfile.ZipFile(self.path_to_file, 'r') as zipObj:
                
            os.chdir(path)
            zipObj.extractall(path+"\\"+folder_name)

        os.chdir(original_path)