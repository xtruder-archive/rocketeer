from time import sleep

from ffmpegprocess import FFMpegProcess
from server import Server, StreamersHandler

from templates.stream_h264 import h264Tpl
from templates.stream_webm import webmTpl
from templates.stream_prosojnice import prosojniceTpl
from templates.stream_test import testTpl

class h264Stream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=h264Tpl)
        self.filename= "templates/stream_h264.tpl"

class webmStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=webmTpl)
        self.filename= "templates/stream_webm.tpl"

class prosojniceStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=prosojniceTpl)
        self.filename= "templates/stream_prosojnice.tpl"

class testStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=testTpl)
        self.filename= "templates/stream_test.tpl"

def CreateServer(ip="127.0.0.1", port=8400):
    srv= Server(StreamersHandler, ip, port)
    streamersHandler= srv.GetRequestHandler()
    streamersHandler.RegisterStreamer(h264Stream)
    streamersHandler.RegisterStreamer(webmStream)
    streamersHandler.RegisterStreamer(prosojniceStream)
    streamersHandler.RegisterStreamer(testStream)
    srv.start()

    return srv
