#!/bin/python
import re
import pystache
import sys
import time
from time import gmtime, strftime
from io import FileIO

from ffmpegprocess import FFMpegProcess

class h264Tpl(pystache.View):
    def __init__(self, dumpf, res):
        pystache.View.__init__(self)

        self.dumpf= dumpf
        self.res= res
    def dumpfile(self):
        return self.dumpf
    def resolution(self):
        return self.res

class prosojniceTpl(pystache.View):
    def __init__(self):
        pystache.View.__init__(self)

def gen_template(filename, instance):
    txt= pystache.Template(FileIO(filename).read(), instance).render()
    return re.sub('[\\n\\t\\\\]+', '', txt).split()

if __name__ == "__main__":
    dump_trailing= ".dv"

    dump= raw_input("Ime predavanja: ")
    kamera= raw_input("Katero kamero uporabljate(nova/stara)?")
    date= strftime("%d-%m-%Y-%H-%M", gmtime())
    if not dump:
        dump= date+dump_trailing
    else:
        dump= date+"_"+dump+dump_trailing
    if kamera=="stara":
        res= "768x567"
    else:
        res= "720x405"

    h264= h264Tpl(dump,res)
    streamCmd= gen_template("stream.h264.tpl", h264)
    print "Stream command:\n\t", " ".join(streamCmd)

    prosojnice= prosojniceTpl()
    prosojniceCmd= gen_template("prosojnice.tpl", prosojnice)
    print "Prosojnice command:\n\t", " ".join(prosojniceCmd)

    streamProcess= FFMpegProcess(" ".join(streamCmd))
    prosojniceProcess= FFMpegProcess(" ".join(prosojniceCmd))

    print "Starting stream - press ctrl+c to stop: "
    streamProcess.Start()
    prosojniceProcess.Start()

    while(1):
        res1= streamProcess.UpdateStatus()
        res2= prosojniceProcess.UpdateStatus()

        status1= streamProcess.GetStreamerStatus()
        status2= prosojniceProcess.GetStreamerStatus()

        sys.stdout.write("\rStream[ run_status: "+str(streamProcess.GetStreamerRunStatus()))
        if status1:
            sys.stdout.write(" f: "+status1[0][1])
        sys.stdout.write("]")
        sys.stdout.write(" prosojnice[ run_status: "+str(prosojniceProcess.GetStreamerRunStatus()))
        if status2:
            sys.stdout.write(" f: "+status2[0][1])
        sys.stdout.write("]")

        time.sleep(0.01)
