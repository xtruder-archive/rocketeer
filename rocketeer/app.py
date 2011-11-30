import threading
import copy

from synch import synchronous

class AppStatus:
    STOPPED= 0
    RUNNING= 1
    ERROR= 2
    ENDED= 3
    UNKNOWN= 4

class App(object):
    def __init__(self):
        self.AppRunStatus= AppStatus.UNKNOWN
        self.AppStatus= None

        self.AppLock= threading.RLock()
        self.values= {}

        self.watchdogs= {}
	self.watchdog_instances= {}

    def __del__(self):
        self.StopApp()

    def _RegisterAppWatchdog(self, watchdog):
        self.watchdogs.append(watchdog)

    @synchronous("AppLock")
    def GetAppRunStatus(self):
        if self.AppRunStatus==None:
            return 0

        return self.AppRunStatus

    @synchronous("AppLock")
    def _SetAppRunStatus(self, status):
        self.AppRunStatus= status

    @synchronous("AppLock")
    def GetAppStatus(self):
        if self.AppStatus==None:
            return 0
        return self.AppStatus

    @synchronous("AppLock")
    def _SetAppStatus(self, status):
        self.AppStatus= status

    @synchronous("AppLock")
    def SetAppValue(self, key, value):
        self.values[key]= value

        return 0

    @synchronous("AppLock")
    def GetAppValue(self, key):
        if self.values.has_key(key):
            return self.values[key]

        return 0

    @synchronous("AppLock")
    def GetAppValues(self):
        return copy.copy(self.values)

    @synchronous("AppLock")
    def StartApp(self):
        for watchdog in self.watchdogs:
            self.watchdog_instances.append(watchdog(self))

    @synchronous("AppLock")
    def StopApp(self):
        for watchdog in self.watchdog_instances:
	    watchdog.__del__()

	self.watchdog_instances= {}

    def _GetWatchdogStatus(self):
        for watchdog in self.watchdog_instances:
            if watchdog.GetRunningStatus()==AppStatus.ERROR:
                return False

        return True

    def _UpdateAppStatus(self):
        pass

class AppProcess(App): #, Process):
    def __init__(self):
        App.__init__(self)

    @synchronous("AppLock")
    def StartApp(self):
        App.StartApp(self)

        self._SetAppRunStatus(AppStatus.UNKNOWN)
        self.Start() # We can do that in python :)
        return 1

    @synchronous("AppLock")
    def StopApp(self):
	App.StopApp(self)

        print("Stopping process")
        self.Terminate() # We can do that in python :)
        return 1

    @synchronous("AppLock")
    def _UpdateAppStatus(self):
	self.UpdateStatus()

        if self._GetWatchdogStatus()==False:
             self._SetAppRunStatus(AppStatus.ENDED)
