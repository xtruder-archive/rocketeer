import os
import subprocess
import fcntl
import time
import re
import pystache

from io import FileIO

from streamer import StreamerStatus

class Bootstrap(object):
    values=[]

    def SetValues(self, values):
        self.values= values

    def GetCommand(self):
        pass

    def PreStart(self):
        pass

    def PostStop(self):
        pass

class StaticCommand(Bootstrap):
    def __init__(self, command):
        self.command= command

    def GetCommand():
        return self.command

class TemplateCommand(Bootstrap):
    def __init__(self, template, filename=""):
        self.template= template
        self.filename= filename

    def GetCommand(self):
        print "template",self.template
        print self.values

        instance= self.template(self.values)
        return self._GenTemplate(self.filename, instance)

    def _GenTemplate(self, filename, instance):
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        txt= pystache.Template(FileIO(path).read(), instance).render()
        return re.sub('[\\n\\t\\\\]+', '', txt).split()

class ConfigTemplateTemplateCommand(TemplateCommand):
    def __init__(self, template, config_template, filename="", config_filename=""):
        StaticCommand.__init__(self, template, filename)

        self.config_template= config_template
        self.config_filename= config_filename

    def PreStart(self):
        instance= self.config_template(self.values)

        self.config= "/tmp/test.conf"
        f=open(self.config, "w")
        f.write(self._GenTemplate(self.config_filename, instance))
        f.close()

        self.values+= {"config": self.config}

    def PostStop(self):
        os.remove(self.config)

class Process(object):
    def __init__(self, bootstrap):
        self.bootstrap= bootstrap

        #Determines if process has been started.
        #It is used for determing if process was
        #stopped by itself or if it hasn't been
        #yet launched.
        self.started= False

        #Flag if process was correctly terminated.
        #Only set if we call terminate or kill,
        #and determines if process was terminated
        #by us or by itself.
        #It is used for auto restart.
        self.correctly_terminated= False

    def _GetTemplateValues(self):
        pass

    def Start(self):
        if self.isRunning():
            self.Terminate()
        if self.started:
            self.started= False
            self.bootstrap.PostStop()

        self.bootstrap.SetValues(self._GetTemplateValues())
        command= self.bootstrap.GetCommand()
        if isinstance(command, basestring):
            command= re.sub('[\\n\\t\\\\]+', '', command).split()
        print "Process command is", command
        print "Calling PreStart"
        self.bootstrap.PreStart()
        self.process = subprocess.Popen(command, stderr = subprocess.PIPE, stdout = subprocess.PIPE )
        self._setNonBlocking()
        print "Process created"

        #Determines if process was determined by us.
        self.correctly_terminated= False

    def _setNonBlocking(self):
        fd = self.process.stderr.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def isRunning(self):
        if not hasattr(self,"process"):
            return False
        if not self.process:
            return False
        self.process.poll()
        if self.process.returncode==None:
            return True
        return False

    def Terminate(self):
        try:
            self.process.terminate()
            self.process.wait()
        except:
            pass

        #Determines that process was terminated by us.
        self.correctly_terminated= True
        self.bootstrap.PostStop()

    def Kill(self):
        try:
            self.process.kill()
            self.process.wait()
        except:
            pass

        #Determines that process was terminated by us.
        self.correctly_terminated= True
        self.bootstrap.PostStop()

    def ReadLine(self):
        line = ""
        self.process.stderr.flush()
        while(1):
            try: ch= self.process.stderr.read(1)
            except: return line
            if ch=="\n":
                return line
            line+=ch

    def ReadLines(self):
        lines= []

        while(1):
            line= self.ReadLine()
            if not line:
                return lines
            lines+= [line]

class StatusUpdateProcess(Process):
    def __init__(self, bootstrap):
        Process.__init__(self, bootstrap)

    def UpdateStatus(self):
        if not self.isRunning():
            if self.started:
                self._SetStreamerRunStatus(StreamerStatus.ENDED)
            else:
                self._SetStreamerRunStatus(StreamerStatus.STOPPED)
            return None

        #Needed for auto restart.
        self.started= True
        return True


