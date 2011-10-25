import pystache
class webmTpl(pystache.View):
    def __init__(self, values):
        pystache.View.__init__(self)

        self.values= values
    def dumpfile(self):
        date= strftime("%d-%m-%Y-%H-%M", gmtime())
        if self.values.has_key("dumpf"):
            return date+"_"+self.values["dumpf"]
        else:
            return date
    def dumpfolder(self):
        if self.values.has_key("dump_folder"):
            return self.values["dump_folder]
        else:
            return "dump"
    def resolution(self):
        if self.values.has_key("res"):
            return self.values["res"]
        else:
            #return "640x480"
            return "768x567"
