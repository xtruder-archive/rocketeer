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
        self.started= False

        #Flag if process was correctly terminated
        #Only set if we call terminate or kill
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
        txt= pystache.Template(FileIO(filename).read(), instance).render()
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
        except:
            pass

        self.correctly_terminated= True

    def Kill(self):
        try:
            self.process.kill()
        except:
            pass

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

    def UpdateStatus(Process):
        pass


