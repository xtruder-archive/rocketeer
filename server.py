import threading
import copy
import random

from threading import Thread
from SimpleXMLRPCServer import MultiPathXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

from synch import synchronous

class StreamersHandler(object):
    def __init__(self, server):
        self.server= server

        self.streamers= {}
        self.instances= {}

        self.StreamerRegisterLock= threading.RLock()
        self.StreamerInstanceLock= threading.RLock()

    @synchronous("StreamerRegisterLock")
    def RegisterStreamer(self, name, streamer):
        if not streamer:
            raise Exception("Streamer not defined.")

        self.streamers[name]= streamer

    @synchronous("StreamerRegisterLock")
    def GetStreamers(self):
        print "here"
        return self.streamers.keys()

    @synchronous("StreamerRegisterLock")
    @synchronous("StreamerInstanceLock")
    def CreateStreamer(self, name):
        if name not in self.streamers:
            return None

        id= random.getrandbits(16)
        self.instances[id]= (self.streamers[name](), name)

        dispatcher= SimpleXMLRPCDispatcher()
        dispatcher.register_introspection_functions()
        dispatcher.register_instance(self.instances[id][0])
        self.server.add_dispatcher( "/"+str(id), dispatcher)

        return id

    @synchronous("StreamerInstanceLock")
    def GetStreamerInstances(self):
        ret=()
        for id in self.instances.keys():
            ret+= ((id, self.instances[id][1]),)

        return ret

    @synchronous("StreamerInstanceLock")
    def DestroyStreamer(self, id):
        if self.instances.has_key(id):
            return None
        del(self.server.dispatchers["/"+str(id)])
        del(self.instances[id])

class RHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = None

class Server(Thread):
    def __init__(self, requestHandler, host="localhost", port=8400):
        Thread.__init__(self)

        self.server = MultiPathXMLRPCServer((host, port), requestHandler=RHandler)
        self.requestHandler= requestHandler(self.server)
        self.dispatcher= SimpleXMLRPCDispatcher()
        self.dispatcher.register_introspection_functions()
        self.dispatcher.register_instance(self.requestHandler)
        self.server.add_dispatcher("/", self.dispatcher)

    def run(self):
        self.server.serve_forever()

    def __del__(self):
        self.server.shutdown()

    def GetRequestHandler(self):
        return self.requestHandler
