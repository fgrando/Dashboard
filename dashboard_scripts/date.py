# DASHBOARD SCRIPT - do not use print()
RESULT = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - 
# put your code below:

import subprocess
def get_win_date():
    ret = subprocess.run(['date', '/T'], stdout=subprocess.PIPE, shell=True)
    txt = ret.stdout.decode("utf-8").strip()
    #print(txt)
    return[txt]

RESULT= get_win_date()
