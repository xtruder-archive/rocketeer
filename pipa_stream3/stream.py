from time import sleep

from process import TemplateCommand, ConfigTemplateTemplateCommand
from ffmpegprocess import FFMpegProcess
from staticprocess import StaticProcess
from notifycopyprocess import NotifyCopyProcess
from server import Server, StreamersHandler

from templates.stream_h264 import h264Tpl
from templates.stream_webm import webmTpl
from templates.stream_prosojnice import prosojniceTpl
from templates.stream_test import testTpl
from templates.stream_motion import motionTpl
from templates.stream_motion_conf import motionConfTpl

class h264Stream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(h264Tpl, "templates/stream_h264.tpl"))

class webmStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(webmTpl, "templates/stream_webm.tpl"))

class prosojniceStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(prosojniceTpl, "templates/stream_prosojnice.tpl"))

class testStream(FFMpegProcess):
    def __init__(self):
        FFMpegProcess.__init__(self,bootstrap=TemplateCommand(testTpl, "templates/stream_test.tpl"))

class motionDetect(StaticProcess):
    def __init__(self):
        StaticProcess.__init__(self,bootstrap=ConfigTemplateTemplateCommand(motionTpl, motionConfTpl, \
                                "templates/stream_motion.tpl", "templates/stream_motion_conf.tpl"))

def CreateServer(ip="127.0.0.1", port=8400):
    srv= Server(StreamersHandler, ip, port)
    streamersHandler= srv.GetRequestHandler()
    streamersHandler.RegisterStreamer(h264Stream)
    streamersHandler.RegisterStreamer(webmStream)
    streamersHandler.RegisterStreamer(prosojniceStream)
    streamersHandler.RegisterStreamer(motionDetect)
    streamersHandler.RegisterStreamer(testStream)
    streamersHandler.RegisterStreamer(NotifyCopyProcess)
    srv.start()

    return srv
