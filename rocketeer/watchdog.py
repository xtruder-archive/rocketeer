class AppWatchdog(object):
    def __init__(self, app):
        self.app= app

    def __del__(self):
        pass

    def GetRunningStatus(self):
        pass
