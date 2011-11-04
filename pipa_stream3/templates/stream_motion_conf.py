import pystache
class motionConfTpl(pystache.View):
    def __init__(self, values):
        pystache.View.__init__(self)

        self.values= values

#    def config(self):
#        if self.values.has_key("config"):
#            return self.values["config"]
#        else:
#            return "/etc/motion/motion.conf"
