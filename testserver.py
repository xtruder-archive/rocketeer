import xmlrpclib

from server import Server
from server import StreamersRequestHandler

a=Server(StreamersRequestHandler(), port=8200)
a.start()

class test(object):
    def test(self, a):
        return a

a.GetRequestHandler().RegisterStreamer("test", test())

proxy = xmlrpclib.ServerProxy("http://localhost:8200/")
print proxy.CallStreamer("test", "test", "kekec")
