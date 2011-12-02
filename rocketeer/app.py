import threading
import copy

from synch import synchronous

class AppStatus:
    """
    Status of an app.
    """

    STOPPED= 0
    """
    Indicates that app has been stopped by us
    """
    RUNNING= 1
    """
    Indicates that app is running
    """ 
    ERROR= 2
    """
    Indicates that there has been an error
    """ 
    ENDED= 3
    """
    Indicates that app has been closed by itself
    """ 
    UNKNOWN= 4
    """
    Indicates that app is in not yet know state(on startup only)
    """ 

class App(object):
    """
    Virtual aplication, that can be new process or just thread with all
    needed interfaces.
    """ 

    def __init__(self):
        self.AppRunStatus= AppStatus.UNKNOWN
        self.AppStatus= None

        self.AppLock= threading.RLock()
        self.values= {}

        self.watchdogs= []

    def __del__(self):
        self.StopApp()

    def RegisterAppWatchdog(self, watchdog):
        """
        Registers watchdog instance with this app. 
        StartWatchdog is called when app is started and StopWatchdog when
        app is stopeed. You can get app's status using GetRunningStatus.
        
        @param watchdog: Instance of L{AppWatchdog}.
        @type watchdog: L{AppWatchdog}
        
        @return: Nothing
        @rtype: C{None}
        """ 
        self.watchdogs.append(watchdog)

    @synchronous("AppLock")
    def GetAppRunStatus(self):
        """
        Gets running status of an app.
        
        @return: Running status of an app.
        @rtype: L{AppStatus}
        """ 

        if self.AppRunStatus==None:
            return 0

        return self.AppRunStatus

    @synchronous("AppLock")
    def _SetAppRunStatus(self, status):
        """
        Sets app's running status.
        
        @param status: Running status.
        @type status: L{AppStatus}
        
        @return: Nothing
        @rtype: C{None}
        """ 
        self.AppRunStatus= status

    @synchronous("AppLock")
    def GetAppStatus(self):
        """
        Gets app's status as list of some data usefull for your client app.
        
        @return: List of C{str}
        @rtype: C{list}
        """

        if self.AppStatus==None:
            return 0
        return self.AppStatus

    @synchronous("AppLock")
    def _SetAppStatus(self, status):
        """
        Sets app status with some contextual data.
        
        @param status: List of L{str}
        @type status: C{list}
        
        @return: Nothing
        @rtype: C{None}
        """

        self.AppStatus= status

    @synchronous("AppLock")
    def SetAppValue(self, key, value):
        """
        Sets app value. Usefull for passing data to app.
        
        @param key: Where to store
        @type key: C{str}
        @param value: What to store
        @type value: C{str}
        
        @return: Nothing
        @rtype: C{None}
        """

        self.values[key]= value
        return 0

    @synchronous("AppLock")
    def GetAppValue(self, key):
        """
        Get app's value, that was set before.
        
        @param key: Which value to get.
        @type key: C{str}
        
        @return: 0 on fail, C{str} on success.
        @rtype: C{int} or C{str}
        """

        if self.values.has_key(key):
            return self.values[key]

        return 0

    @synchronous("AppLock")
    def GetAppValues(self):
        """
        Gets all values, that were set before.
        
        @return: List of C{str}
        @rtype: C{list}
        """

        return copy.copy(self.values)

    @synchronous("AppLock")
    def StartApp(self):
        """
        Starts app.
        Please note that it also start all watchdogs.
        
        @return: Nothing
        @rtype: C{None}
        """

        for watchdog in self.watchdogs:
            watchdog.StartWatchdog()

    @synchronous("AppLock")
    def StopApp(self):
        """
        Stops app.
        
        @return: Nothing
        @rtype: C{None}
        """

        for watchdog in self.watchdogs:
            watchdog.StopWatchdog()

    def _GetWatchdogStatus(self):
        """
        Gets status of all watchdogs.
        
        @return: If any of watchdogs is False returns False, otherwise True
        @rtype: C{boolean}
        """

        for watchdog in self.watchdogs:
            if watchdog.GetRunningStatus()==False:
                return False

        return True

    def _UpdateAppStatus(self):
        """
        Updates app's status.
        This function must be called periodicly to fetch new app status.
        
        @return: Nothing
        @rtype: C{None}
        """

        if self._GetWatchdogStatus()==False:
            self._SetAppRunStatus(AppStatus.ERROR)

class AppProcess(App): #, Process):
    """
    App class for processes.
    """ 
    def __init__(self):
        App.__init__(self)

    @synchronous("AppLock")
    def StartApp(self):
        """
        Starts app.
        Please note that it also start all watchdogs.
        
        @return: Nothing
        @rtype: C{None}
        """

        App.StartApp(self)

        self._SetAppRunStatus(AppStatus.UNKNOWN)
        self.Start() # We can do that in python :)
        return 1

    @synchronous("AppLock")
    def StopApp(self):
        """
        Stops app.
        
        @return: Nothing
        @rtype: C{None}
        """

        App.StopApp(self)

        print("Stopping process")
        self.Terminate() # We can do that in python :)
        if self.correctly_terminated:
            print "Correctly terminated"
            self._SetAppRunStatus(AppStatus.STOPPED)

        return 1

    @synchronous("AppLock")
    def _UpdateAppStatus(self):
        """
        Updates app's status.
        This function must be called periodicly to fetch new app status.
        
        @return: Nothing
        @rtype: C{None}
        """

        self.UpdateStatus()
        if( self.GetAppRunStatus()!=AppStatus.STOPPED and \
           self.GetAppRunStatus()!=AppStatus.ENDED and \
           self.GetAppRunStatus()!=AppStatus.ERROR):
            App._UpdateAppStatus(self)
