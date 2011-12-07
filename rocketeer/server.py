import threading
import copy
import random

from logging import INFO
from threading import Thread
from SimpleXMLRPCServer import MultiPathXMLRPCServer, SimpleXMLRPCDispatcher, SimpleXMLRPCRequestHandler

from synch import synchronous

from process import StatusUpdateNode
from app import AppStatus

from PyLogDecorate.log import LogCall, LogClass

@LogClass({"subdecorate": True})
class AppsHandler(object):
    """
    Request handler for apps.
    """ 

    def __init__(self, server, auto_close= False):
        print "init"
        self.server= server

        self.Apps= {}
        self.instances= {}

        self.auto_close= auto_close

        self.AppRegisterLock= threading.RLock()
        self.AppInstanceLock= threading.RLock()

    @synchronous("AppRegisterLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def RegisterApp(self, App, name=""):
        if not App:
            raise Exception("Cannot register App!")

        if not name:
            name=App.__name__

        self.Apps[name]= App

    @synchronous("AppRegisterLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def GetApps(self):
        return self.Apps.keys()

#    @synchronous("AppRegisterLock")
    @synchronous("AppInstanceLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def CreateApp(self, name):
        if not self.Apps:
            return 0
        if name not in self.Apps:
            return 0

        id= int(random.getrandbits(16))
        print self.Apps[name]
        if not self.instances:
            self.instances= {}
        self.instances[id]= (self.Apps[name](), name,)

        dispatcher= SimpleXMLRPCDispatcher()
        dispatcher.register_introspection_functions()
        dispatcher.register_instance(self.instances[id][0])
        self.server.add_dispatcher( "/"+str(id), dispatcher)

        return id

    @synchronous("AppInstanceLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def GetAppInstances(self):
        ret=()
        for id in self.instances.keys():
            ret+= ((id, self.instances[id][1]),)

        return ret

    @synchronous("AppInstanceLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def DestroyInstance(self, id):
        id= int(id)
        if not self.instances.has_key(id):
            return False
        del(self.server.dispatchers["/"+str(id)])
        self.instances[id][0].__del__()
        del(self.instances[id])

        return True

    @synchronous("AppInstanceLock")
    @LogCall({"subdecorate": True, "level": INFO})
    def DestroyInstanes(self):
        for id in self.instances.keys():
            self.DestroyInstance(id)

    @synchronous("AppInstanceLock")
    @LogCall({"subdecorate": True})
    def UpdateStatus(self):
        delete=[] # Auto close objects
        for key in self.instances:
            instance= self.instances[key][0]
            if isinstance(instance,
                    StatusUpdateNode):

                instance._UpdateAppStatus()
                # Auto close
                if( self.auto_close and
                    instance.GetAppRunStatus()==AppStatus.ENDED):
                    delete+=[instance]
                # Auto restart
                elif( (instance.GetAppRunStatus()==AppStatus.ENDED or \
                      instance.GetAppRunStatus()==AppStatus.ERROR) and \
                        instance.GetAppValue("auto_restart") and not instance.correctly_terminated ) :
                    instance.StartApp()
                # In case of error we have to stop app if it is already running.
                elif( instance.GetAppRunStatus()==AppStatus.ERROR ):
                    print "Stopping app"
                    instance.StopApp()

        for instance in delete:
            instance.__del__()
            del(instance)


class RHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = None

@LogClass()
class Server(Thread):
    @LogCall()
    def __init__(self, requestHandler, host="localhost", port=8400):
        Thread.__init__(self)

        self.server = MultiPathXMLRPCServer((host, port), requestHandler=RHandler)
        self.requestHandler= requestHandler(self.server, False)
        self.dispatcher= SimpleXMLRPCDispatcher()
        self.dispatcher.register_introspection_functions()
        self.dispatcher.register_instance(self.requestHandler)
        self.server.add_dispatcher("/", self.dispatcher)

    @LogCall({"level": INFO})
    def run(self):
        self.server.serve_forever()

    @LogCall({"level": INFO})
    def __del__(self):
        self.server.shutdown()

    def GetRequestHandler(self):
        return self.requestHandler
