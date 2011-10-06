import threading
import copy

from threading import Thread
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

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
        return self.streamers.keys()

    @synchronous("StreamerRegisterLock")
    def CallStreamer(self, name, function, *args, **kwargs):
        if self.streamers.has_key(name):
            f= getattr(self.streamers[name], function, None)
            if f:
                return f(*args)
        return None

class Server(Thread):
    def __init__(self, requestHandler, host="localhost", port=8000):
        Thread.__init__(self)

        self.server = SimpleXMLRPCServer((host, port))
        self.server.register_introspection_functions()
        self.server.register_instance(requestHandler, allow_dotted_names=True)

        self.requestHandler= requestHandler

    def run(self):
        self.server.serve_forever()

    def __del__(self):
        self.server.shutdown()

    def GetRequestHandler(self):
        return self.requestHandler

class StreamersRequestHandler(StreamersHandler):
    def __init__(self): StreamersHandler.__init__(self)

