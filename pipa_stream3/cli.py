from time import sleep

from optparse import OptionParser

from stream import CreateServer
from daemon import createDaemon

def main():
    usage = "usage: psyncho [options] args"
    parser = OptionParser(usage)
    parser.add_option("--daemon",
                      help="Run me as daemon?", action="store_true", dest="daemon")
    parser.add_option("--ip",
                      help="Ip where to listen", dest="ip")
    parser.add_option("--port",
                      help="Port where to listen", dest="port")
    
    (options, args) = parser.parse_args()

    if options.daemon:
        ret= createDaemon()

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
