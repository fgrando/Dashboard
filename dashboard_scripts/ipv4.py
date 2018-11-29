# DASHBOARD SCRIPT - do not use print()
RESULT = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - 
# put your code below:

import subprocess
import re

def get_win_ipv4():
    ret = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, shell=True)
    txt = ret.stdout.decode("utf-8").strip()
    ip = re.findall("(?<=IPv4 Address. . . . . . . . . . . : )[\d]+.[\d]+.[\d]+.[\d]+", txt, re.DOTALL)

    if len(ip) > 0:
        txt = ip[0].strip()
    #print(txt)
    return[txt]

RESULT= get_win_ipv4()
