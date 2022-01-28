import os
import subprocess
import threading
import time
from datetime import datetime

#RASPIVIDCMD = ["raspivid -t 0 -w 1280 -h 720"]
RASPIVIDCMD = "raspivid "
VIDEOCODEC = "h264"
TIMETOWAITFORABORT = 0.5


# class for controlling the running and shutting down of raspivid
class RaspiVidController(threading.Thread):
    def __init__(self, filePath, timeout, width, height, preview, otherOptions=None):
        threading.Thread.__init__(self)

        self.date = datetime.today().strftime('%d%m%Y_%H%M%S')

        # setup the raspivid cmd
        self.raspividcmd = RASPIVIDCMD

        self.filePath = filePath + '_' + self.date + '.' + VIDEOCODEC

        #add options

        if timeout > 0:
            self.raspividcmd += "-o" + ' '
            self.raspividcmd += self.filePath + ' '
            self.raspividcmd += "-t" + ' '
            self.raspividcmd += str(timeout) + ' '
            self.raspividcmd += "-w" + ' '
            self.raspividcmd += str(width) + ' '
            self.raspividcmd += "-h" + ' '
            self.raspividcmd += str(height) + ' '
            self.raspividcmd += "-fps" + ' '
            self.raspividcmd += str(25) + ' '
        else:
            self.raspividcmd += "-t" + ' '
            self.raspividcmd += str(timeout) + ' '
            self.raspividcmd += "-w" + ' '
            self.raspividcmd += str(width) + ' '
            self.raspividcmd += "-h" + ' '
            self.raspividcmd += str(height) + ' '
            self.raspividcmd += "-fps" + ' '
            self.raspividcmd += str(25) + ' '
        if preview == False:
            self.raspividcmd += "-n"

        # # if there are other options, add them
        # if otherOptions != None:
        #     self.raspividcmd = self.raspividcmd + otherOptions

        print(self.raspividcmd)
        # set state to not running
        self.running = False

    def run(self):
        # run raspivid
        raspivid = subprocess.Popen(self.raspividcmd, shell=True)

        # loop until its set to stopped or it stops
        self.running = True
        while (self.running and raspivid.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False

        # kill raspivid if still running
        if raspivid.poll() == True: raspivid.kill()

    def stopController(self):
        self.running = False