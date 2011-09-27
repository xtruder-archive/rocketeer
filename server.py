import web
import threading
import copy

from synch import synchronous

class StreamRestServer(threading.Thread):
    def run(self):
        urls= ()

class StreamersHandler(object):
    def __init__(self):
        self.streamers= {}

        self.StreamerRegisterLock= threading.RLock()

    @synchronous("StreamerRegisterLock")
    def RegisterStreamer(self, name, streamer):
        self.streamers[name]= streamer

    @synchronous("StreamerRegisterLock")
    def GetStreamers(self):
        return self.streamers

    @synchronous("StreamerRegisterLock")
    def GetStreamer(self, name):
        if self.streamers.has_key(name):
            return self.streamers[name]
        return None

class StreamersRequestHandler(StreamerHandler):
    def __init__(self):
        pass
