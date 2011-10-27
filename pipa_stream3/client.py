import xmlrpclib
import pylirc

from time import sleep
from optparse import OptionParser

from daemon import createDaemon
from streamer import StreamerStatus

def main():
    usage = "usage: pstream3_client [options] command [arg1,arg2,...]"
    parser = OptionParser(usage)
    parser.add_option("--daemon",
                      help="Run me as daemon", action="store_true", dest="daemon")
    parser.add_option("--ip",
                      help="Ip where should i listen", dest="ip")
    parser.add_option("--port",
                      help="Port where should i bind", dest="port")
    parser.add_option("--instance",
                      help="Instance for which to run command", dest="instance")
    (options, args) = parser.parse_args()

    if options.ip and options.port:
        ip= options.ip
        port= options.port
    else:
        ip= "localhost"
        port= str(8400)

    client = xmlrpclib.ServerProxy("http://%s:%s/" % (ip, port))

    if options.instance:
        for (id,name) in client.GetStreamerInstances():
            if  id==options.instance:
                instance_client= xmlrpclib.ServerProxy("http://%s:%s/%s/" % (ip, port, str(options.instance))) 

if __name__ == "__main__":
    main()
