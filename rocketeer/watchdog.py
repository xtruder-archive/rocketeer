from PyLogDecorate.log import LogCall, LogClass

@LogClass({"subdecorate": True})
class AppWatchdog(object):
	"""
	Watchdog for applications. Idea is that we can have multiple watchdogs
	per applications, which watches if everything is okay with it.
	"""

    def __init__(self, app):
        self.app= app
		self.watchdogStarted= False

    @LogCall({"subdecorate": True})
    def StartWatchdog(self):
        self.watchdogStarted= True

    @LogCall({"subdecorate": True})
    def StopWatchdog(self):
        self.watchdogStarted= False

    @LogCall({"subdecorate": True})
    def GetRunningStatus(self):
        return self.watchdogStarted

@LoadClass()
class AppChainloader(AppWatchdog):
	"""
	Chainloader for application, which allows us to load another application
	when our application starts or ends.
	"""

	def __init__(self, parentApp, chainloadAppClass):
		self.chainloadAppClass= chainloadAppClass
		self.parentAppClass= parentAppClass

	def StartWatchdog(self):
		self.chainloadAppInstance= self.chainloadAppClass()
		self.chainloadAppInstance.StartApp()

		# Anounce that we are running
		AppWatchdog.StartWatchdog()

	def StopWatchdog(self):
		# Stop and delete out app instance
		self.chainloadAppInstance.StopApp()
		self.chainloadAppInstance.__del__()

		# Anounce that we are not running
		AppWatchdog.StopWatchdog()
