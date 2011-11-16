from app import AppProcess, AppStatus
from process import StatusUpdateProcess

class StaticProcess(StatusUpdateProcess, AppProcess):
    def __init__(self, bootstrap):
        StatusUpdateProcess.__init__(self, bootstrap)
        AppProcess.__init__(self)

    def UpdateStatus(self):
        if not StatusUpdateProcess.UpdateStatus(self):
            return None

        print("running")
        self._SetAppRunStatus(AppStatus.RUNNING)

        return ""
