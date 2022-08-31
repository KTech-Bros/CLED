import zipfile,re,os,shutil

class ZipWorker:
    def __init__(self, link):
        self.file_name = re.findall("([0-9a-zA-Z_.]+.zip)",link)[0]
        
        self.path_to_exe = os.getcwd()

        path_to_folder = os.path.join( self.path_to_exe ,"temp")

        is_folder_exist = (os.path.isdir(path_to_folder))

        if not is_folder_exist:
            os.mkdir(path_to_folder)

        self.path_to_file = os.path.join( self.path_to_exe ,"temp", self.file_name)

        shutil.copyfile(link, self.path_to_file)
        

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