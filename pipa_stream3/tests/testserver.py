import xmlrpclib

from pipa_stream3.server import Server
from pipa_stream3.server import StreamersHandler

a=Server(StreamersHandler, port=8500)
a.start()

class test(object):
    def test(self, a):
        return a

a.GetRequestHandler().RegisterStreamer(test, "test")

proxy = xmlrpclib.ServerProxy("http://localhost:8500/")
print proxy.GetStreamers()
id= proxy.CreateStreamer("test")
print proxy.GetStreamerInstances()
proxy2 = xmlrpclib.ServerProxy("http://localhost:8500/"+str(id))
print proxy2.test("text")
proxy.DestroyInstance(id)
print proxy.GetStreamerInstances()

a.__del__()
del(a)
