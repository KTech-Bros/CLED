import unittest, random, sys, re
import fileModifier, dbworker



class TestFileModifier(unittest.TestCase):

    def test_xml_modify(self):
        file_path = sys.path[0] + r"\unit_test\xml_file\file.xml"

        test_string = str(random.randint(0, 1000000))

        fileModifier.change_xml_attribute(file_path, "name", "Name number 1", "value", test_string, "add")

        f = open(file_path)

        string_from_file = f.read()

        file_string_value = re.findall(r'value="(.*)"',string_from_file)[0]

        self.assertEqual(file_string_value, test_string, "The data string is diferend from expected!")

    def test_json_modify(self):
        file_path = sys.path[0] + r"\unit_test\json_file\file.json"

        test_string = str(random.randint(0, 1000000))

        fileModifier.change_json_param(file_path, "Name", test_string)

        f = open(file_path)

        string_from_file = f.read()

        string_from_file = string_from_file.replace("\n","")

        file_string_value = re.findall(r'"Name": "(.*)"',string_from_file)[0]

        self.assertEqual(file_string_value, test_string, "The data string is diferend from expected!")
    
class TestDBWorker(unittest.TestCase):
    def test_redis_sucsesful_ping(self):
        data_base = dbworker.DBWorker("host=127.0.0.1;db=0;port=6379;password=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81",None)
        
        self.assertEqual(True, data_base.ping_redis(), "The ping on redis failed! (is connection string correct?)")

    def test_redis_unsucsesful_ping(self):
        data_base = dbworker.DBWorker("host=127.0.0.1;db=0;port=378;password=eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81",None)
        
        self.assertEqual(False, data_base.ping_redis(), "The ping on redis didn't failed! (is connection string uncorrect?)")

    def test_postgres_sucsesful_ping(self):
        data_base = dbworker.DBWorker(None,"Port=5432;Database=test;User=postgresuser;Password=postgrespassword;Host=127.0.0.1")
        
        self.assertEqual(True, data_base.ping_postgre(), "The ping on postgres failed! (is connection string correct?)")

    def test_postgres_unsucsesful_ping(self):
        data_base = dbworker.DBWorker(None,"Port=543112;Database=test;User=postgresuser;Password=postgrespassword;Host=127.0.0.1")
        
        self.assertEqual(False, data_base.ping_postgre(), "The ping on postgres failed! (is connection string correct?)")

if __name__ == '__main__':
    unittest.main()