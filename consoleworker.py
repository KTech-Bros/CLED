import sys, os
from subprocess import PIPE,Popen

class сonsoleworker:
    def console_out_task(string):
        p = Popen(string,shell=False,stdin=PIPE,stdout=PIPE,stderr=PIPE)

        (output, err) = p.communicate() 
        p_status = p.wait()

    def console_out_folder(path, command):
        original_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path)
        os.system(command)
        os.chdir(original_path)

    def get_init_params():
        command_list = sys.argv[:]
        command_list.pop(0)

        return command_list