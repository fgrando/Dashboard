# DASHBOARD SCRIPT - do not use print()
RESULT = []
# - - - - - - - - - - - - - - - - - - - - - - - - - - 
# put your code below:

import subprocess
def get_win_hostname():
    ret = subprocess.run(['forfiles', '/M', 'C:\\Users\\user\\Desktop\\dashboard.py,' '/C', '"cmd /c echo @fdate @ftime"'], stdout=subprocess.PIPE, shell=True)
    txt = ret.stdout.decode("utf-8").strip()
    print(txt)
    return[txt, "LAST CHANGE"]

RESULT= get_win_hostname()
