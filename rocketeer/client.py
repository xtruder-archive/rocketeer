import xmlrpclib

from time import sleep
from optparse import OptionParser

from daemon import createDaemon
from app import AppStatus

def main():
    usage = "usage: pstream3_client [options] command [arg1,arg2,...] [help]"
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

    if not args:
        print "No argument passed!"
        return 0

    print "Calling function", args[0]

    if options.ip and options.port:
        ip= options.ip
        port= options.port
    else:
        ip= "localhost"
        port= str(8400)

    client = xmlrpclib.ServerProxy("http://%s:%s/" % (ip, port))

    if options.instance:
        print "... on instance", options.instance

        instances= client.GetAppInstances()
        for (id,name) in instances:
            if  str(id)==str(options.instance):
                instance_client= xmlrpclib.ServerProxy("http://%s:%s/%s" % (ip, port, str(options.instance)))

                if args[0]=="help":
                    print "Methods:", instance_client.system.listMethods()
                else:
                    if len(args)>1:
                        if args[1]=="help":
                            print "Help docs:\n", instance_client.system.methodHelp(args[0])
                        else:
                            print "Return:", getattr(instance_client,args[0])(*args[1:])
                    else:
                        print "Return:", getattr(instance_client,args[0])()
    else:
        if args[0]=="help":
            print "Methods:", client.system.listMethods()
        else:
            if len(args)>1:
                if args[1]=="help":
                    print "Help docs:\n", client.system.methodHelp(args[0])
                else:
                    print "Return:", getattr(client,args[0])(*args[1:])
            else:
                print "Return:", getattr(client,args[0])()


if __name__ == "__main__":
    main()
