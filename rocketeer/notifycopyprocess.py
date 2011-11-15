import os
import paramiko
import os.path 
import time

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

from streamer import Streamer, StreamerStatus
from process import StatusUpdateNode

class NotifyCopyProcess(StatusUpdateNode, Streamer, ProcessEvent):
    def __init__(self):
        StatusUpdateNode.__init__(self)
        Streamer.__init__(self)

	mask = EventsCodes.ALL_FLAGS["IN_CREATE"]  # watched events

	self.wm = WatchManager()
	self.notifier = Notifier(self.wm, self)

	if self.GetStreamerValue("src"):
	    self.src=self.GetStreamerValue("src")
	else:
	    self.src="/tmp/motion/"

	self.wdd = self.wm.add_watch(self.src, mask, rec=True)

	if self.GetStreamerValue("host"):
	    self.host=self.GetStreamerValue("host")
        else:
	    self.host="dogbert"

	if self.GetStreamerValue("username"):
	    self.username=self.GetStreamerValue("username")
        else:
	    self.username="arhivar"

	if self.GetStreamerValue("password"):
	    self.password=self.GetStreamerValue("password")
        else:
	    self.password="nomorebacklog"

	if self.GetStreamerValue("dst"):
	    self.dst=self.GetStreamerValue("dst")
        else:
	    self.dst="/home/arhivar/static_html/live/slides4"

	try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, username=self.username, password=self.password)

            self.ftp = self.ssh.open_sftp()
	except:
	    self.error= True
	    print "Cannot connect"

    def UpdateStatus(self):
        if not StatusUpdateNode.UpdateStatus(self):
            return None
	
        self._SetStreamerRunStatus(StreamerStatus.RUNNING)

	self.notifier.process_events()
	if self.notifier.check_events(timeout=.1):
            self.notifier.read_events()

        return ""

    def process_IN_CREATE(self, event):
	print "Event", os.path.join(event.path, event.name)
	self.copyover(os.path.join(event.path, event.name))
	
    def copyover(self, file):
        outfile = "%s/%s" % (self.dst, os.path.basename(file))
	self.ftp.put(file, outfile)
