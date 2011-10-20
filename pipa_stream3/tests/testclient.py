import xmlrpclib

from time import sleep

proxy = xmlrpclib.ServerProxy("http://localhost:8400/")
print proxy.GetStreamers()
proxy.CreateStreamer("testStream")
instances=proxy.GetStreamerInstances()
print instances
proxy2 = xmlrpclib.ServerProxy("http://localhost:8400/"+str(instances[0][0]))
proxy2.StartStreamer()
proxy2.SetStreamerValue("auto_restart",1)
while(1):
    print proxy2.GetStreamerStatus()
    rstatus= proxy2.GetStreamerRunStatus()
    print rstatus
    if rstatus==3:
        sleep(1)
        print proxy.GetStreamerInstances()
        proxy.DestroyInstance(instances[0][0])
        break
    sleep(.5)
print proxy.GetStreamerInstances()
