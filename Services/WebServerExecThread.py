import os
import signal
import subprocess

from PyQt5.QtCore import QThread

#https://stackabuse.com/pythons-os-and-subprocess-popen-commands/
#https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
class WebServerExecThread(QThread):

    def __init__(self):
        super().__init__()
        self.server = None

    def run(self):
        self.server = subprocess.Popen(["python3 serverMain.py"], shell=True, preexec_fn=os.setsid)

    def stop(self):
        if self.server != None:
            os.killpg(os.getpgid(self.server.pid), signal.SIGTERM)
            self.server.wait()
            print("Stop Server")