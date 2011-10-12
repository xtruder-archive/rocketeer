import unittest
from time import sleep

from pipa_stream3.streamer import StreamerStatus
from pipa_stream3.ffmpegprocess import FFMpegProcess

class TestFFMpegProcess(unittest.TestCase):
    def test_parse(self):
        p= FFMpegProcess("ffmpeg -y -i video.avi video.mp4")
        p.Start()
        while(1):
            lines= p.UpdateStatus()
            if p.GetStreamerRunStatus()==StreamerStatus.ENDED or p.GetStreamerRunStatus()==StreamerStatus.ERROR:
                break
            if not lines:
                continue
            print "Run status: ", p.GetStreamerRunStatus()
            print "Status: ", p.GetStreamerStatus()
            sleep(0.01)
if __name__ == '__main__':
        unittest.main()
