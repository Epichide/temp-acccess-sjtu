

import os
import sys
import os.path as osp



executable_path = sys.executable
executable_w_path = executable_path[:-4] + 'w.exe'#pythonw not arouse console
executable_path = executable_w_path
# get the path of install.py to get the path of health_report.py

path = os.path.split(os.path.realpath(__file__))[0]
# create the task
path = osp.join(path, 'access_request.py')
# sc 时间间隔
# st 启动时间
command = f'schtasks /create /sc daily /st 08:00 /tn "ACCESS SHJT Report" /tr "{executable_path} {path}"'
print("command",command)
os.system(command)