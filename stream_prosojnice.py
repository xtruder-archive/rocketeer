import pystache
class prosojniceTpl(pystache.View):
    def __init__(self, values):
        pystache.View.__init__(self)

        self.values= values
    def prefix(self):
        date= strftime("%d-%m-%Y", gmtime())
        if self.values.has_key("prefix"):
            return date+"_"+self.values["prefix"]
        else:
            return date
