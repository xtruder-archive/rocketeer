from time import sleep

from optparse import OptionParser

from stream import CreateServer
from daemon import createDaemon

def main():
    usage = "usage: pstream3d [options]"
    parser = OptionParser(usage)
    parser.add_option("--daemon",
                      help="Run me as daemon", action="store_true", dest="daemon")
    parser.add_option("--ip",
                      help="Ip where should i listen", dest="ip")
    parser.add_option("--port",
                      help="Port where should i bind", dest="port")
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
        srv= CreateServer(ip, port)
    else:
        srv= CreateServer()

    while(1):
        try:
            srv.GetRequestHandler().UpdateStatus()
            sleep(.01)
        except KeyboardInterrupt:
            srv.__del__()
            break

if __name__ == "__main__":
    main()
