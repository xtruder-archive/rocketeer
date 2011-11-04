import time

from streamer import StreamerProcess, StreamerStatus
from process import StatusUpdateProcess

class StaticProcess(StatusUpdateProcess, StreamerProcess):
    def __init__(self, bootstrap):
        StatusUpdateProcess.__init__(self, bootstrap)
        StreamerProcess.__init__(self)

    def UpdateStatus(self):
        if not StatusUpdateProcess.UpdateStatus(self):
            return None

        print("running")
        self._SetStreamerRunStatus(StreamerStatus.RUNNING)

        return result
