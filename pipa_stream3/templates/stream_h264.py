import pystache
from time import strftime, gmtime
class h264Tpl(pystache.View):
    def __init__(self, values):
        pystache.View.__init__(self)

        self.values= values
    def dumpfile(self):
        date= strftime("%d-%m-%Y-%H-%M", gmtime())
        if self.values.has_key("dumpfile"):
            return date+"_"+self.values["dumpfile"]
        else:
            return date
    def dumpfolder(self):
        if self.values.has_key("dumpfolder"):
            return self.values["dumpfolder]
        else:
            return "dump"
    def resolution(self):
        if self.values.has_key("res"):
            return self.values["res"]
        else:
            #return "640x480"
            return "768x567"
