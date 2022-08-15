import zipfile,re,os,urllib.request
import redis, psycopg2

class zipworker:
    def __init__(self, link):
        listoffind = re.findall("([0-9a-zA-Z_.]+.zip)",link)
        self.fileName = listoffind[0]
        self.pathToFile = os.getcwd()
        urllib.request.urlretrieve(link, self.fileName)

    def unPackZip(self):
        with zipfile.ZipFile(self.fileName, 'r') as zipObj:
            zipObj.extractall("folder")






