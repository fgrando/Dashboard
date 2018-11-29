# DASHBOARD SCRIPT - do not use print()
RESULT = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - 
# put your code below:

import subprocess
def get_win_hostname():
    ret = subprocess.run(['hostname'], stdout=subprocess.PIPE, shell=True)
    txt = ret.stdout.decode("utf-8").strip()
    #print(txt)
    return[txt, "my PC name is"]

RESULT= get_win_hostname()
