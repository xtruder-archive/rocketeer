import threading
import copy

from synch import synchronous

class StreamerStatus:
    STOPPED= 0
    RUNNING= 1
    ERROR= 2
    ENDED= 3
    UNKNOWN= 4

class Streamer(object):
    def __init__(self):
        self.streamerRunStatus= StreamerStatus.UNKNOWN
        self.streamerStatus= None

        self.StreamerLock= threading.RLock()
        self.values= {}

    def __del__(self):
        self.StopStreamer()

    @synchronous("StreamerLock")
    def GetStreamerRunStatus(self):
        if self.streamerRunStatus==None:
            return -1
        return self.streamerRunStatus

    @synchronous("StreamerLock")
    def _SetStreamerRunStatus(self, status):
        self.streamerRunStatus= status

    @synchronous("StreamerLock")
    def GetStreamerStatus(self):
        if self.streamerStatus==None:
            return -1
        return self.streamerStatus

    @synchronous("StreamerLock")
    def _SetStreamerStatus(self, status):
        self.streamerStatus= status

    @synchronous("StreamerLock")
    def SetStreamerValue(self, key, value):
        self.values[key]= value

    @synchronous("StreamerLock")
    def GetStreamerValue(self, key):
        if self.values.has_key(key):
            return self.values[key]

        return None

    @synchronous("StreamerLock")
    def GetStreamerValues(self):
        return copy.copy(self.values)

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

    @synchronous("StreamerLock")
    def StartStreamer(self):
        self.Start() # We can do that in python :)
        return 1

    @synchronous("StreamerLock")
    def StopStreamer(self):
        self.Terminate() # We can do that in python :)
        return 1
