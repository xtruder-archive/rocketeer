from PyLogDecorate.log import LogCall, LogClass

@LogClass({"subdecorate": True})
class AppWatchdog(object):
    def __init__(self, app):
        self.app= app

    @LogCall({"subdecorate": True})
    def StartWatchdog(self):
        pass

    @LogCall({"subdecorate": True})
    def StopWatchdog(self):
        pass

    @LogCall({"subdecorate": True})
    def GetRunningStatus(self):
        pass
