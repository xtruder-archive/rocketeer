import pystache
class testTpl(pystache.View):
    def __init__(self, values):
        pystache.View.__init__(self)

        self.values= values
    def src(self):
        if self.values.has_key("src"):
            return self.values["src"]
        else:
            return "video"
    def dst(self):
        if self.values.has_key("dst"):
            return self.values["dst"]
        else:
            return "video"
