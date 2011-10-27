import xmlrpclib
import pylirc

from time import sleep
from optparse import OptionParser

from daemon import createDaemon
from streamer import StreamerStatus

def main():
    usage = "usage: pstream3_client [options]"
    parser = OptionParser(usage)
    parser.add_option("--daemon",
                      help="Run me as daemon", action="store_true", dest="daemon")
    parser.add_option("--ip",
                      help="Ip where should i listen", dest="ip")
    parser.add_option("--port",
                      help="Port where should i bind", dest="port")
    parser.add_option("--dump",
                      help="Folder where should i dump", dest="dump")
    parser.add_option("--lirc-config",
                      help="Path to lirc config", dest="lirc_config")
    parser.add_option("--pid",
                      help="Process pid", dest="pid")
    (options, args) = parser.parse_args()

    if options.daemon:
        ret= createDaemon()

        if options.pid:
            pid= os.getpid()
            f= open(options.pid, "w")
            f.write(str(pid))
            f.close()

    if options.ip and options.port:
        ip= options.ip
        port= options.port
    else:
        ip= "localhost"
        port= str(8400)

    client = xmlrpclib.ServerProxy("http://%s:%s/" % (ip, port))
    h264_client= None

    blocking= 1
    if options.lirc_config:
        lirc_path= options.lirc_config
    else:
        lirc_path="/etc/pstream/conf"
    if(pylirc.init("pylirc", lirc_path, blocking)):
        code= {"config": ""}
        while(code["config"] != "quit"):
            #Read next code
            s= pylirc.nextcode(1)
            #Right now i don't care what you press on remote.
            code["config"]= "start_stream"

            status= None
            if(code["config"] == "start_stream"):
                try:
                    status=h264_client.GetStreamerRunStatus()
                except:
                    status=None

                if (status!=StreamerStatus.RUNNING) or not status:
                    print("Creating new streamer")
                    h264= client.CreateStreamer("h264Stream")
                    print h264, client.GetStreamerInstances()
                    h264_client= xmlrpclib.ServerProxy("http://%s:%s/" % (ip,port) + str(h264))
                    h264_client.SetStreamerValue("auto_restart", 1)
                    if options.dump:
                        h264_client.SetStreamerValue("dumpfolder", options.dump)
                    else:
                        h264_client.SetStreamerValue("dumpfolder", "/home/recode/dump")
                    h264_client.StartStreamer()
                else:
                    print("Stoping stream")
                    client.DestroyInstance(h264)
                    continue

                while h264_client.GetStreamerRunStatus()!=StreamerStatus.RUNNING:
                    sleep(.5)
                print("Next code")
 

        client.DestroyInstances()
        pylirc.exit()

if __name__ == "__main__":
    main()
