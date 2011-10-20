import xmlrpclib

from time import sleep

import pylirc

client = xmlrpclib.ServerProxy("http://localhost:8400/")
h264_client= None

blocking= 1
if(pylirc.init("pylirc", "./conf", blocking)):
    code= {"config": ""}
    while(code["config"] != "quit"):
        #Read next code
        s= pylirc.nextcode(1)

        for (code) in s:
            if(code["config"] == "start_stream"):
                if (h264_client and \
                        h264_client.GetStreamerStatus()!=StreamerStatus.RUNNING) or \
                        not h264_client:
                    print("Creating new streamer")
                    h264= client.CreateStreamer("h264Stream")
                    h264_client= xmlrpclib.ServerProxy("http://localhost:8400/"+str(h264))
                    h264_cleint.SetStreamerValue("auto_restart", 1)
                    h264_client.StartStreamer()
                else:
                    print("Stoping stream")
                    client.DestroyInstance(h264)
                    h264_client= None

    client.DestroyInstances()
    pylirc.exit()
