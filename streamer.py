import threading

from synch import synchronous

class StreamerStatus:
    STOPPED= 0
    RUNNING= 1
    ERROR= 2
    UNKNOWN= 3

class Streamer(object):
    def __init__(self):
        self.StreamerLock= threading.RLock()

    @synchronous("StreamerLock")
    def GetStreamerRunStatus(self):
        pass

    @synchronous("StreamerLock")
    def _SetStreamerRunStatus(self, status):
        pass

    @synchronous("StreamerLock")
    def GetStreamerStatus(self):
        pass

    @synchronous("StreamerLock")
    def _SetStreamerStatus(self, status):
        pass

    @synchronous("StreamerLock")
    def StartStreamer(self):
        pass

    @synchronous("StreamerLock")
    def StopStreamer(self):
        pass

class StreamerProcess(Streamer): #, Process):
    def __init__(self, template=False):
        Streamer.__init__(self)
        self.template= template

        self.streamerRunStatus= StreamerStatus.UNKNOWN
        self.streamerStatus= None
        self.template= template

    @synchronous("StreamerLock")
    def GetStreamerRunStatus(self):
        return self.streamerRunStatus

    @synchronous("StreamerLock")
    def _SetStreamerRunStatus(self, status):
        self.streamerRunStatus= status

    @synchronous("StreamerLock")
    def GetStreamerStatus(self):
        return self.streamerStatus

    @synchronous("StreamerLock")
    def _SetStreamerStatus(self, status):
        self.streamerStatus= status

    @synchronous("StreamerLock")
    def StartStreamer(self):
        self.Start() # We can do that in python :)

    @synchronous("StreamerLock")
    def StopStreamer(self):
        self.Terminate() # We can do that in python :)
