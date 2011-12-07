import os
import subprocess
import fcntl
import re
import pystache
import inspect

from io import FileIO
from tempfile import NamedTemporaryFile

from app import AppStatus

class Bootstrap(object):
    """
    Class that is responsible for generating commands and has
    prestart and poststart functions.
    """ 
    values=[]

    def SetValues(self, values):
        self.values= values

    def GetCommand(self):
        """
        Gets generated command.
        
        @return: C{str}
        @rtype: C{str}
        """ 
        pass

    def PreStart(self):
        """
        Is executed before process start.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        pass

    def PostStop(self):
        """
        Is executed after process has stopped.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        pass

class StaticCommand(Bootstrap):
    """
    Bootstrap for a process whose command is just a static string.
    """ 
    def __init__(self, command):
        """
        Initialization.
        
        @param command: Command to execute.
        @type command: C{str}
        
        @return: Nothing
        @rtype: C{StaticCommand}
        """ 
        self.command= command

    def GetCommand(self):
        return self.command

class TemplateCommand(Bootstrap):
    """
    Bootstrap for process whose command is generated using 
    pystache template system.
    """ 
    def __init__(self, template, filename=""):
        """
        Initialization.
        
        @param template: Class of template.
        @type template: L{a}
        @param filename: Name of file where template data is stored.
        @type filename: C{str}
        
        @return: L{TemplateCommand}
        @rtype: L{TemplateCommand}
        """ 
        self.template= template
        self.filename= filename

    def GetCommand(self):
        """
        Gets generated command.
        
        @return: C{str}
        @rtype: C{str}
        """
        print "template",self.template
        print self.values

        instance= self.template(self.values)
        return self._GenTemplate(self.filename, instance)

    def _GenTemplate(self, filename, instance):
        """
        Generates command using template.
        
        @param filename: Filename where template data is stored.
        @type filename: C{str}
        @param instance: Template instance used for variable insertion.
        @type instance: L{}
        
        @return: Generated command.
        @rtype: C{str}
        """
	print inspect.getfile(self.template)
        path=os.path.join(os.path.dirname(inspect.getfile(self.template)), filename)
        txt= pystache.Template(FileIO(path).read(), instance).render()
        return re.sub('[\\n\\t\\\\]+', '', txt).split()

class ConfigTemplateTemplateCommand(TemplateCommand):
    """
    Bootstrap for process whose config file and statup command is
    generated using pystache template system.
    """ 

    def __init__(self, template, config_template, filename="", config_filename=""):
        """
        Initialization.
        
        @param template: Template for command generation.
        @type template: C{}
        @param config_template: Template for config generation.
        @type config_template: C{}
        @param filename: Filename where template data for command is stored.
        @type filename: C{str}
        @param config_filename: Filename where template data for config is stored.
        @type config_filename: C{str}
        
        @return: L{ConfigTemplateTemplateCommand}
        @rtype: L{ConfigTemplateTemplateCommand}
        """ 
        TemplateCommand.__init__(self, template, filename)

        self.config_template= config_template
        self.config_filename= config_filename

    def PreStart(self):
        """
        Config file is genrated and storred somewhere.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        instance= self.config_template(self.values)

        f=NamedTemporaryFile(delete=False)
        conf_template= self._GenTemplate(self.config_filename, instance)
        #print conf_template
        f.write(conf_template)
        f.close()

        self.config= f.name

        #We need to set for command generation.
        self.values= dict(self.values.items()+{"config": self.config}.items())

    def PostStop(self):
        """
        Config file is deleted.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        #must be able to handle multi calls
        try: os.unlink(self.config)
        except: pass

    def _GenTemplate(self, filename, instance):
        """
        Generates command using template.
        
        @param filename: Filename where template data is stored.
        @type filename: C{str}
        @param instance: Template instance used for variable insertion.
        @type instance: L{}
        
        @return: Generated command.
        @rtype: C{str}
        """
        path=os.path.join(os.path.dirname(inspect.getfile(self.template)), filename)
        return pystache.Template(FileIO(path).read(), instance).render()

class Process(object):
    """
    System process.

    @todo: Add support for reading process output from anything else than only
           stderr.
    """ 
    def __init__(self, bootstrap):
        """
        Initilaization.
        
        @param bootstrap: Bootstrap class used for command generation.
        @type bootstrap: L{Bootstrap}
        
        @return: New L{Process}
        @rtype: L{Process}
        """ 
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

        #Determines if there was error druing
        #process creation
        self.error= False

    def Start(self):
        """
        Starts process.
        First it generates command using bootstrap and then it executes it.
        
        @return: a
        @rtype: a
        """ 
        if self.isRunning():
            self.Terminate()
        if self.started:
            self.started= False
            self.bootstrap.PostStop()


        self.error= False

        self.bootstrap.SetValues(self.GetAppValues())
        print "Calling PreStart"
        self.bootstrap.PreStart()
        command= self.bootstrap.GetCommand()
        if isinstance(command, basestring):
            command= re.sub('[\\n\\t\\\\]+', '', command).split()
        print "Process command is", command

        try:
            self.process = subprocess.Popen(command, stderr = subprocess.PIPE, stdout = subprocess.PIPE )
        except:
            print "Problem creating process"
            self.error= True
            self.Kill()
            return

        self._setNonBlocking()
        print "Process created"

        #Determines if process was determined by us.
        self.correctly_terminated= False

    def _setNonBlocking(self):
        """
        Makes reading processe's output non-blocking.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        fd = self.process.stderr.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def isRunning(self):
        """
        Determines if process is still/yet running.
        
        @return: True if it still running and false otherwise.
        @rtype: C{boolean}
        """ 
        if not hasattr(self,"process"):
            return False
        if not self.process:
            return False
        self.process.poll()
        if self.process.returncode==None:
            return True
        return False

    def Terminate(self):
        """
        Terminates process. In case of exception it kills it.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        try:
            self.process.terminate()
            self.process.wait()
        except:
            self.Kill()
            return

        #Determines that process was terminated by us.
        self.correctly_terminated= True
        self.bootstrap.PostStop()

    def Kill(self):
        """
        kills process.
        
        @return: Nothing
        @rtype: C{None}
        """ 
        try:
            self.process.kill()
            self.process.wait()
        except:
            self.bootstrap.PostStop()
            return

        #Determines that process was terminated by us.
        self.correctly_terminated= True
        self.bootstrap.PostStop()

    def ReadLine(self):
        """
        Reads line from processe's stdout/stderr.
        
        @return: String of a readed line.
        @rtype: C{str}
        """ 
        line = ""
        self.process.stderr.flush()
        while(1):
            try: ch= self.process.stderr.read(1)
            except: return line
            if ch=="\n":
                return line
            line+=ch

    def ReadLines(self):
        """
        Reads lines from processe's output, untill everything has been read.
        
        @return: List of lines.
        @rtype: C{list}
        """ 
        lines= []

        while(1):
            line= self.ReadLine()
            if not line:
                return lines
            lines+= [line]

class StatusUpdateNode(object):
    """
    This is base class for apps that require periodical status updates.
    """ 
    error= False
    def UpdateStatus(self):
        """
        Updates status.
        
        @return: Positive value in case of success, negative otherwise.
        @rtype: C{boolean}
        """ 
        if self.error:
            self._SetAppRunStatus(AppStatus.ERROR)
            return None
        return True

class StatusUpdateProcess(Process, StatusUpdateNode):
    """
    Base class for processes, that requiere periodical status updates/checks.
    Basicly for all processes, except ones that we don't care what is their
    running status.
    """ 
    def __init__(self, bootstrap):
        Process.__init__(self, bootstrap)

    def UpdateStatus(self):
        """
        Updates status.
        Basicly it checks if process is still running and based on that it
        select RunStatus.
        
        @return: Positive value in case of success, negative otherwise.
        @rtype: C{boolean}
        """ 
        if not self.isRunning():
            print "dgfsdfgssssssssssssssssssssssssssssssss!"
            if self.started:
                self._SetAppRunStatus(AppStatus.ENDED)
            elif self.error:
                self._SetAppRunStatus(AppStatus.ERROR)
            else:
                self._SetAppRunStatus(AppStatus.STOPPED)
            return None

        print "rub                                       qwfrwdgsdfg"
        #Needed for auto restart.
        self.started= True
        return True

