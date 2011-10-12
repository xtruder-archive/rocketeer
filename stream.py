from time import sleep

from ffmpegprocess import FFMpegProcess
from server import Server, StreamersHandler

from stream_h264 import h264Tpl
from stream_webm import webmTpl
from stream_prosojnice import prosojniceTpl
from stream_test import testTpl

class h264Stream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=h264Tpl)
        self.filename= "stream_h264.tpl"

class webmStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=webmTpl)
        self.filename= "stream_webm.tpl"

class prosojniceStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=prosojniceTpl)
        self.filename= "stream_prosojnice.tpl"

class testStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,template=testTpl)
        self.filename= "stream_test.tpl"

srv= Server(StreamersHandler)
streamersHandler= srv.GetRequestHandler()
streamersHandler.RegisterStreamer(h264Stream)
streamersHandler.RegisterStreamer(webmStream)
streamersHandler.RegisterStreamer(prosojniceStream)
streamersHandler.RegisterStreamer(testStream)
srv.start()

while(1):
    streamersHandler.UpdateStatus()
    sleep(.01)
