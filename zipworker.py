import zipfile,re,os,urllib.request

class ZipWorker:
    def __init__(self, link):
        list_of_file_names = re.findall("([0-9a-zA-Z_.]+.zip)",link)
        self.fileName = list_of_file_names[0]
        self.pathToFile = os.getcwd()
        urllib.request.urlretrieve(link, self.fileName)

    def unpack_zip(self, path):
        with zipfile.ZipFile(self.fileName, 'r') as zipObj:
            zipObj.extractall(path)