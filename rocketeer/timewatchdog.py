from time import time

from watchdog import AppWatchdog

class TimeWatchdog(AppWatchdog):
    def __init__(self, app, limit):
	AppWatchdog.__init__(app)

        self.limit= limit

    def StartWatchdog(self):
        self.start_time= time()

    def StopWatchdog(self):
        pass

    def GetRunningStatus(self):
        if (time()-self.start_time)>self.limit:
            return False

        return True
