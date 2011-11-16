import threading
import copy
import random

from threading import Thread
from SimpleXMLRPCServer import MultiPathXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

from synch import synchronous

from process import StatusUpdateNode
from app import AppStatus

class AppsHandler(object):
    def __init__(self, server, auto_close= False):
        self.server= server

        self.Apps= {}
        self.instances= {}

        self.auto_close= auto_close

        self.AppRegisterLock= threading.RLock()
        self.AppInstanceLock= threading.RLock()

    @synchronous("AppRegisterLock")
    def RegisterApp(self, App, name=""):
        if not App:
            raise Exception("Cannot register App!")

        if not name:
            name=App.__name__

        self.Apps[name]= App

    @synchronous("AppRegisterLock")
    def GetApps(self):
        print "here"
        return self.Apps.keys()

#    @synchronous("AppRegisterLock")
    @synchronous("AppInstanceLock")
    def CreateApp(self, name):
        if name not in self.Apps:
            return 0

        id= random.getrandbits(16)
        self.instances[id]= (self.Apps[name](), name)

        dispatcher= SimpleXMLRPCDispatcher()
        dispatcher.register_introspection_functions()
        dispatcher.register_instance(self.instances[id][0])
        self.server.add_dispatcher( "/"+str(id), dispatcher)

        return id

    @synchronous("AppInstanceLock")
    def GetAppInstances(self):
        ret=()
        for id in self.instances.keys():
            ret+= ((id, self.instances[id][1]),)

        return ret

    @synchronous("AppInstanceLock")
    def DestroyInstance(self, id):
        id= int(id)
        if not self.instances.has_key(id):
            return False
        del(self.server.dispatchers["/"+str(id)])
        self.instances[id][0].__del__()
        del(self.instances[id])

        return True

    @synchronous("AppInstanceLock")
    def DestroyInstances(self):
        for id in self.instances.keys():
            self.DestroyInstance(id)

    @synchronous("AppInstanceLock")
    def UpdateStatus(self):
        delete=[] # Auto close objects
        for key in self.instances:
            instance= self.instances[key][0]
            if isinstance(instance,
                    StatusUpdateNode):

                instance.UpdateStatus()
                #Auto close
                if( self.auto_close and
                    instance.GetAppRunStatus()==AppStatus.ENDED):
                    delete+=[instance]
                #Auto restart
                elif( (instance.GetAppRunStatus()==AppStatus.ENDED or \
                      instance.GetAppRunStatus()==AppStatus.ERROR) and \
                        instance.GetAppValue("auto_restart") and not instance.correctly_terminated ) :
                    instance.StartApp()

        for instance in delete:
            instance.__del__()
            del(instance)


class RHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = None

class Server(Thread):
    def __init__(self, requestHandler, host="localhost", port=8400):
        Thread.__init__(self)

        self.server = MultiPathXMLRPCServer((host, port), requestHandler=RHandler)
        self.requestHandler= requestHandler(self.server, False)
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
