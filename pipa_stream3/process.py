import os
import subprocess
import fcntl
import time
import re
import pystache

from io import FileIO

class Process(object):
    def __init__(self,command="", template=False):
        self.command= command
        self.template= template

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

    def _GenCommand(self):
        if self.template:
            print "template",self.template
            print self._GetTemplateValues()

            instance= self.template(self._GetTemplateValues())
            return self._GenTemplate(self.filename, instance)
        else:
            return self.command

    def _GenTemplate(self, filename, instance):
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
        txt= pystache.Template(FileIO(path).read(), instance).render()
        return re.sub('[\\n\\t\\\\]+', '', txt).split()

    def Start(self):
        if self.isRunning():
            self.Terminate()
        if self.started:
            self.started= False

        command= self._GenCommand()
        if isinstance(command, basestring):
            command= re.sub('[\\n\\t\\\\]+', '', command).split()
        print "Process command is", command
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

        #Determines if process was terminated by us.
        self.correctly_terminated= True

    def Kill(self):
        try:
            self.process.kill()
            self.process.wait()
        except:
            pass

        #Determines if process was terminated by us.
        self.correctly_terminated= True

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
    def __init__(self, command="", template=False):
        Process.__init__(self, command, template)

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


