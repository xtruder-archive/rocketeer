import threading
import copy
import random

from threading import Thread
from SimpleXMLRPCServer import MultiPathXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

from synch import synchronous

from process import StatusUpdateProcess

class StreamersHandler(object):
    def __init__(self, server):
        self.server= server

        self.streamers= {}
        self.instances= {}

        self.StreamerRegisterLock= threading.RLock()
        self.StreamerInstanceLock= threading.RLock()

    @synchronous("StreamerRegisterLock")
    def RegisterStreamer(self, streamer, name=""):
        if not streamer:
            raise Exception("Cannot register streamer!")

        if not name:
            name=streamer.__name__

        self.streamers[name]= streamer

    @synchronous("StreamerRegisterLock")
    def GetStreamers(self):
        print "here"
        return self.streamers.keys()

    @synchronous("StreamerRegisterLock")
    @synchronous("StreamerInstanceLock")
    def CreateStreamer(self, name):
        if name not in self.streamers:
            return 0

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
    def DestroyInstance(self, id):
        if not self.instances.has_key(id):
            return False
        del(self.server.dispatchers["/"+str(id)])
        self.instances[id][0].__del__()
        del(self.instances[id])

        return True

    def UpdateStatus(self):
        for key in self.instances:
            instance= self.instances[key][0]
            if isinstance(instance.UpdateStatus(),
                    StatusUpdateProcess):
                instance.UpdateStatus()

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
