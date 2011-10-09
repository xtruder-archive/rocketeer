import xmlrpclib

from server import Server
from server import StreamersHandler

a=Server(StreamersHandler, port=8500, host="192.168.3.1")
a.start()

class test(object):
    def test(self, a):
        return a

a.GetRequestHandler().RegisterStreamer("test", test)

proxy = xmlrpclib.ServerProxy("http://192.168.3.1:8500/")
print proxy.GetStreamers()
id= proxy.CreateStreamer("test")
print proxy.GetStreamerInstances()
proxy2 = xmlrpclib.ServerProxy("http://192.168.3.1:8500/"+str(id))
print proxy2.test("text")
