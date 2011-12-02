from time import time

from watchdog import AppWatchdog

class TimeWatchdog(AppWatchdog):
    def __init__(self, app, limit):
	AppWatchdog.__init__(self, app)

        self.limit= limit
        self.start_time= time()

    def StartWatchdog(self):
        self.start_time= time()

    def StopWatchdog(self):
        pass

    def GetRunningStatus(self):
        if (time()-self.start_time)>self.limit:
            print "Time watchdog limit exceeded"
            return False

        return True
