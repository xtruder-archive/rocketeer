import unittest
import time
import xmlrpclib

from threading import Thread

from rocketeer.server import AppsHandler, Server
from rocketeer.process import StaticCommand
from rocketeer.staticprocess import StaticProcess
from rocketeer.timewatchdog import TimeWatchdog

class DummyProcess(StaticProcess):
    def __init__(self):
        StaticProcess.__init__(self, StaticCommand("sleep 1000"))

class DummyTimeWatchdogProcess(DummyProcess):
    def __init__(self):
        DummyProcess.__init__(self)

        self.RegisterAppWatchdog(TimeWatchdog(self,10))

class AutoUpdateThread(Thread):
    def __init__(self, handler):
        Thread.__init__(self)
        self.handler= handler

    def run(self):
        while True:
            self.handler.UpdateStatus()
            time.sleep(1)

class TestProcessApp(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.server= Server( AppsHandler )
        self.server.requestHandler.RegisterApp(DummyProcess)
        self.server.requestHandler.RegisterApp(DummyTimeWatchdogProcess)
        print "Starting server thread"
        self.server.start()

        #Thread for auto status updates
        self.AutoUpdateThread= AutoUpdateThread(self.server.requestHandler)
        print "Starting update thread"
        self.AutoUpdateThread.start()

    def test_StartAndStop(self):
        proxy= xmlrpclib.ServerProxy("http://localhost:8400/")
        print "Creating app"
        id= proxy.CreateApp("DummyProcess")
        proxy2= xmlrpclib.ServerProxy("http://localhost:8400/"+str(id))
        print "Starting app with id "+ str(id)
        proxy2.StartApp()
        time.sleep(10)
        proxy2.StopApp()

    def test_StartAndStopWatchdog(self):
        proxy= xmlrpclib.ServerProxy("http://localhost:8400/")
        print "Creating app"
        id= proxy.CreateApp("DummyTimeWatchdogProcess")
        proxy2= xmlrpclib.ServerProxy("http://localhost:8400/"+str(id))
        print "Starting app with id "+ str(id)
        proxy2.StartApp()
        time.sleep(20)
        proxy2.StopApp()

if __name__ == '__main__':
        unittest.main()
