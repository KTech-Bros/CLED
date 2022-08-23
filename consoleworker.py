import sys
from subprocess import PIPE,Popen

class сonsoleworker:
    def console_out(self, string):
        Popen(string,shell=False,stdin=PIPE,stdout=PIPE,stderr=PIPE)

    def get_init_params(self):
        command_list = sys.argv[:]
        command_list.pop(0)

        return command_list